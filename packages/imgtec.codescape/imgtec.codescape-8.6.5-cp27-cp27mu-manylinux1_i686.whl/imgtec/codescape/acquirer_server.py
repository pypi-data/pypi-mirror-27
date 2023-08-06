import logging
import os
import Queue
import re
import serial
import serial.rfc2217
import socket
import sys
import threading
from collections import defaultdict
from ConfigParser import ConfigParser, NoSectionError, NoOptionError, DuplicateSectionError
from contextlib import contextmanager
from imgtec.codescape import version as imgtec_version
from imgtec.codescape.acquirer import *
from imgtec.codescape.acquirer import _check_server_details
from imgtec.codescape.acquirer_targets import *
from imgtec.codescape.acquirer_reservations import *
from imgtec.codescape.probe_identifier import _da_name_map
from imgtec.lib import get_user_files_dir
from imgtec.lib.rst import simple_table, html_table
from imgtec.lib.img_sendmail import img_sendmail_internal
from itertools import chain
from os.path import basename, dirname, isfile, splitext, exists
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from threading import Thread, Timer, Lock
from urllib2 import urlopen
from textwrap import dedent

logging_format = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=logging_format)
logger = logging.getLogger("Acquirer")
LOG_FILE = "logfile.log"

SERVER_CONF_FILE = "acquirer.ini"
BOOKINGS_FILE = "reservations.p"

VERSION = "1.28"

DEFAULT_EXIT_CODE = 2
DEFAULT_UPLOAD_PORT_IF_NOT_SPECIFIED_IN_FILE = 9000
REFRESH_INTERVAL = 60 # seconds


def _join_if_list_or_tuple(x):
    return " ".join(x) if isinstance(x, list) or isinstance(x, tuple) else x


def message_proposing_similar_matches(word, possibilities):
    if word and possibilities:
        matches = get_close_matches(word, possibilities)
        return make_propositions_message(matches)
    return ""


def make_propositions_message(matches):
    if len(matches) == 1:
        return " Did you mean {0}?".format(matches[0])
    elif matches:
        return " Did you mean one of {0}?".format(', '.join(matches))
    return ""


def get_only_file_name(full_file_name):
    return splitext(basename(full_file_name))[0]


def _fix_probe_type_expression(expr):
    """
    >>> _fix_probe_type_expression("probe_type!=sp")
    "probe_type!='SysProbe'"
    >>> _fix_probe_type_expression("probe_type=='other'")
    "probe_type=='other'"
    >>> _fix_probe_type_expression("sp")
    "probe_type=='SysProbe'"
    """
    m = re.search(r"(probe_type[!=]=)[\"']?([^\"']+)[\"']?", expr)
    if m:
        property, type = m.groups()
        type = _da_name_map.get(type.lower(), type)
        return "{0}'{1}'".format(property, type)
    else:
        try:
            return "probe_type=='{0}'".format(_da_name_map[expr.lower()])
        except KeyError:
            return expr


def check_is_bitstream_matching_target(target, bitstream):
    if not is_bitstream_matching_target(bitstream, target):
        raise FirmwareNotMatching("Board type({0}) and bitstream board type({1}) do not match.".format(target.name, bitstream.board_type))


def is_bitstream_matching_target(bitstream, target):
    return bitstream.board_type.lower() == target.name.lower()


def _put_free_targets_first(targets):
    free_targets = [t for t in targets if t.is_available()]
    return free_targets + [t for t in targets if t not in free_targets]


class Configuration(ConfigParser):
    def __init__(self, filename):
        self.filename = filename

        if not exists(filename):
            logger.debug("There was no {0} file so creating new one".format(filename))
            dir = dirname(filename)
            if not exists(dir):
                os.makedirs(dir)
                open(filename, "w+").close()

        ConfigParser.__init__(self, allow_no_value=True)
        self.optionxform = str
        self.read(self.filename)

    def _add_new_option(self, section, option, value):
        self._add_new_config_section(section)
        self.set(section, option, value)
        self._write()

    def _add_new_config_section(self, section):
        try:
            self.add_section(section)
        except DuplicateSectionError:
            pass

    def _write(self):
        with open(self.filename, 'w') as f:
            self.write(f)

    def _add_options_from_dictionary(self, section, dictionary):
        self._add_new_config_section(section)
        for k, v in dictionary.iteritems():
            if isinstance(k, tuple):
                k = "{0} % {1}".format(*k)
            self.set(section, k, str(v))
        self._write()

    def _read_dict(self, section):
        def _fix_tuples(item):
            if " % " in item[0]:
                p, v = item[0].split(" % ")
                return (p, fix_type(v)), item[1]
            return item
        try:
            return dict(_fix_tuples(i) for i in self.items(section))
        except NoSectionError:
            return {}


class IdGenerator(object):
    def __init__(self, configuration):
        self.configuration = configuration

    def get_next_id(self):
        try:
            actual = int(self.configuration.get_res_id())
            result = str(actual + 1)
        except (NoOptionError, NoSectionError):
            result = "1"
        self.configuration.write_res_id(result)
        return result


class ProbeAllocatorConfiguration(Configuration):
    def __init__(self, filename):
        if not exists(filename):
            logger.info("There is no config file with targets and weights. You can add targets using the "
                        "`add target_id target_name` command or fill a template file:\n" + str(filename))
        Configuration.__init__(self, filename)
        self._add_template_section("Targets", '# Target_id = Target_name\n# SysProbe 22 = WPJ344')
        self._add_template_section("Weights", '# Property = weight\n# has_vze % True = 1')
        self._add_template_section("Ports", 'upload_port = 9000\n')
        Configuration.__init__(self, filename)

    def get_res_id(self):
        return self.get("Reservations", "actual_id")

    def write_res_id(self, new_id):
        self._add_new_option("Reservations", "actual_id", new_id)

    def _add_template_section(self, section, template):
        if not self.has_section(section):
            self._add_new_option(section, template, None)

    def add_target_to_config_file(self, identifier, name, boardparams):
        data = " ".join([name] + boardparams) if boardparams else name
        self._add_new_option("Targets", identifier, data)

    def change_target_properties(self, id, old_props, new_props):
        old = self.get("Targets", id)
        old_props, new_props = _join_if_list_or_tuple(old_props), _join_if_list_or_tuple(new_props)
        name_and_params = old.replace(old_props, new_props)
        self.set("Targets", id, name_and_params)
        self._write()

    def update_weights_in_config_file(self, properties):
        self._add_options_from_dictionary("Weights", properties)

    def read_targets(self):
        read = self.items("Targets")
        result = []
        for id, data in read:
            if data is None:
                logger.info("Wrong target config: {0}".format(id))
            else:
                logger.info("Read target from config: {0}".format(data))
                data = data.split()
                name = data.pop(0)
                result.append((id, name, data))

        return result

    def read_weights(self):
        result = dict()
        for k, v in self._read_dict("Weights").iteritems():
            if len(k) != 2 or not v:
                logger.warning("Wrong property in config file: {0} = {1}".format(k, v))
            else:
                try:
                    result[k] = int(v)
                except ValueError:
                    logger.warning("Wrong weight value in config file: {0} = {1}".format(k, v))
        return result

    def read_upload_port(self):
        try:
            return int(self.get("Ports", "upload_port"))
        except (NoOptionError, NoSectionError):
            return DEFAULT_UPLOAD_PORT_IF_NOT_SPECIFIED_IN_FILE

    def write_internal_code_name(self, internal, name):
        self._add_new_option("Internal names", internal, name)

    def read_internal_code_names(self):
        read = self._read_dict("Internal names")
        return dict((i.lower(), n) for i, n in read.iteritems())

    def remove_target(self, id):
        existed = self.remove_option("Targets", id)
        self._write()
        return existed


class BitstreamConfiguration(Configuration):
    def __init__(self, filename):
        Configuration.__init__(self, filename)

    def write_details(self, board_type, serial_number, conmux, url_source=None):
        self._add_new_option("Details", "board_type", board_type)
        self._add_new_option("Details", "serial_number", serial_number)
        self._add_new_option("Details", "conmux", conmux)
        if url_source:
            self._add_new_option("Details", "source", url_source)

    def write_properties(self, properties):
        self._add_options_from_dictionary("Cpu_info", properties)

    def get_details(self):
        try:
            read = dict(self.items("Details"))
            return fix_types(read, False)
        except NoSectionError:
            raise ConfigFileError("Config file {0} is empty".format(self.filename))

    def get_properties(self):
        try:
            read = dict(self.items("Cpu_info"))
            return fix_types(read)
        except NoSectionError:
            return dict()


class BitstreamFile(object):
    ''' Stores full bitstream name (with directory path and extension) and board type e.g. boston or corefpga5
    Conmux bitstreams store just specified name ie malta-12334-SN00001'''
    def __init__(self, filename="", board_type=None, serial_number=None, config_file=None, conmux=False):
        if (not filename or not board_type) and config_file:
            self.config_file = config_file

            config_parser = BitstreamConfiguration(config_file)
            details = config_parser.get_details()
            self.board_type = details["board_type"]
            self.conmux = details["conmux"]
            if self.conmux:
                self.filename = basename(config_file.replace(".ini", ""))
            elif self.board_type == "boston":
                self.filename = config_file.replace(".ini", ".mcs")
            else:
                self.filename = config_file.replace(".ini", ".fl")

            self.serial_number = details["serial_number"]
            self.properties = config_parser.get_properties()
        else:
            self.filename = filename
            self.conmux = conmux
            self.config_file = config_file or splitext(self.filename)[0] + ".ini"
            self.board_type = board_type
            self.serial_number = serial_number or self._match_serial_number()
            self.properties = dict()

    @property
    def files(self):
        return (self.config_file, self.filename if not self.conmux else None)

    @property
    def name(self):
        return get_only_file_name(self.config_file)

    def create_config_file(self, url_source=None):
        cpu_info_parser = BitstreamConfiguration(self.config_file)
        cpu_info_parser.write_details(self.board_type, self.serial_number, self.conmux, url_source)

    def store_cpuinfo(self, properties, logs=True):
        if not self.properties:
            cpu_info_parser = BitstreamConfiguration(self.config_file)
            logger.debug("Storing cpu info after flashing {0}".format(self.name)) if logs else None
            cpu_info_parser.write_properties(properties)

    def _match_serial_number(self):
        m = re.search(r"[^a-zA-Z0-9](REF\d{5}|SN[A-Za-z0-9]{6}|\d{7})([^a-zA-Z0-9]|$)", self.name)
        return m.group(1) if m else ""

    def matches_acquire(self, wanted_bitstream):
        case_matches = [self.serial_number, self.name, self.filename, basename(self.filename)]
        return wanted_bitstream.lower() in [s.lower() for s in case_matches]

    def matches_properties(self, desired_properties):
        return check_if_matches_properties(self.properties, desired_properties)

    def details(self, weights, verbose):
        cpu_info = self.get_properties_to_show(weights, verbose)
        name = "(conmux) " if self.conmux else ""
        name += self.name
        return self.board_type, name, cpu_info

    def get_properties_to_show(self, weights, verbose=False):
        if not self.properties:
            return "Not fetched yet"
        return get_properties_to_show(self.properties, verbose, weights)


def targets_owned_by(user, targets):
    return [t.identifier for t in targets if t.is_owned_by(user)]


def find_target_by_id(targets, identifier, owner=None):
    for t in targets:
        if t.identifier == identifier:
            return t
    msg = "There is no target with identifier {0}.".format(identifier)
    if owner:
        msg += make_propositions_message(targets_owned_by(owner, targets))
    else:
        all_ids = [t.identifier for t in targets]
        msg += message_proposing_similar_matches(identifier, all_ids)
    raise TargetNotFound(msg)


class QueueThreadingServer(object):
    def __init__(self):
        self.server_query_threads = []
        self.server_queues = []

    def server_get_queue_value(self, id):
        try:
            val = self.server_queues[id].get_nowait()
            if not isinstance(val, basestring):
                self.server_queues[id].task_done()
                if isinstance(val, ProbeAlreadyAcquired):
                    return val.message
                if isinstance(val, Exception):
                    raise val
            return val
        except Queue.Empty:
            return None

    def _make_queue_to_notify_when_finished(self):
        queue = Queue.Queue()
        self.server_queues.append(queue)
        queue_id = self.server_queues.index(queue)
        return queue, queue_id


def _run_in_thread_with_queue(func):
    def wrapped(self, *args):
        queue, queue_id = self._make_queue_to_notify_when_finished()
        args, kwargs = (self,) + args, {"queue": queue}
        t = ThreadWithQueue(func.__name__, queue, func, args, kwargs)
        self.server_query_threads.append(t)
        t.start()
        return queue_id
    return wrapped

def log_threads():
    logger.debug("There are {0} thread(s) running.".format(threading.activeCount()))
    for thread in threading.enumerate():
        logger.debug("Name: {0} Daemon: {1} Function: {2}".format(
            thread.name, 
            thread.daemon, 
            thread.function.__name__ if hasattr(thread, 'function') else 'N/A'))

class AcquirerServer(QueueThreadingServer):
    def __init__(self, tiny=tiny, config_file=None, flasher=None, email_sender=None, 
            bookings_file=get_user_files_dir(BOOKINGS_FILE),
            get_actual_time=get_actual_time, conmux=True, logging_to_file=True):
        QueueThreadingServer.__init__(self)
        if logging_to_file:
            hdlr = logging.FileHandler(get_user_files_dir(LOG_FILE))
            logger.addHandler(hdlr)

        self.config_filename = config_file or get_user_files_dir(SERVER_CONF_FILE)
        logger.debug("Reading server config from {0}".format(self.config_filename))
        self.configuration = ProbeAllocatorConfiguration(self.config_filename)

        self.target_factory = TargetFactory(tiny, conmux)
        self.targets = self.target_factory.new_targets(self.configuration.read_targets())

        self.weights_handler = WeightsHandler(self.configuration)
        self.flasher = flasher or TargetFlasher(self.configuration.read_upload_port())
        self.allocator = ProbeAllocator(self.configuration, self.targets, self.flasher, self.weights_handler,
                                        email_sender, bookings_file, get_actual_time)
        self.rfc_servers_manager = RFCMultilpexor()
        self._init_rfc_servers()

        self.targets_to_delete = []
        logger.debug("Server started.")

    def _init_rfc_servers(self):
        targets_with_serial = [t for t in self.targets if isinstance(t, UsbTarget) and t.dev_path]
        for t in targets_with_serial:
            self.rfc_servers_manager.add_new_server(t)
        logger.debug("Created {0} rfc2217 servers.".format(len(targets_with_serial)))

    def close_server(self, _=None):
        threads_running = len(self.server_query_threads)
        if threads_running:
            logger.info("{0} server query threads still running...".format(threads_running))
            [t.join() for t in self.server_query_threads]

        self.flasher.join_threads()
        [t.disconnect() for t in self.targets if t.is_available()]

    def server_status(self, identifier):
        return find_target_by_id(self.targets, identifier).status

    @_run_in_thread_with_queue
    def server_flash_board(self, identifier, bitstream_name, owner, queue):
        target = find_target_by_id(self.targets, identifier)

        if not target.is_owned_by(owner):
            if target.is_used_by_user():
                raise ValueError("You cannot flash a target that you have not acquired. Target is in use by {0}".format(target.owner))
            else:
                raise ValueError("You need to acquire a target before you flash it.")

        bitstream = self.flasher.get_bitstream(bitstream_name)
        return self.flasher.reflash(target, bitstream, owner, queue)

    def server_reservations(self, identifier=None, user=None):
        return self.allocator.get_reservations_details(identifier, user, False)

    def server_old_reservations(self, identifier=None, user=None):
        return self.allocator.get_reservations_details(identifier, user, True)

    def server_change_name(self, identifier, new_name):
        t = find_target_by_id(self.targets, identifier)
        logger.debug("Changing name for {0}, from {1} to {2}".format(t.identifier, t.name, new_name))
        self.configuration.change_target_properties(t.identifier, t.name, new_name)
        t.name = new_name

    def server_change_properties(self, identifier, new_props):
        t = find_target_by_id(self.targets, identifier)
        old_props = t.get_board_properties()

        if new_props is None:
            return old_props
        else:
            t.change_properties(*new_props)
            logger.debug("{0}: Changed target properties from {1} to {2}".format(t.identifier, old_props, new_props))
            self.configuration.change_target_properties(t.identifier, old_props, new_props)
            return t.get_board_properties()

    def server_target_status(self, identifier):
        t = find_target_by_id(self.targets, identifier)
        return t.status

    def server_list(self, verbose=False, properties=None):
        targets = [t for t in self.targets if not properties or t.matches_properties(properties)]
        targets = sorted(targets, key=lambda t: (t.identifier.type, t.identifier.name))
        result = [self._get_target_details(t, verbose) for t in targets]
        return result

    def _get_target_details(self, target, verbose):
        id, name, status, props = target.details(self.weights_handler.weights, verbose)
        status += self._get_until_when_available(target)
        return [id, name, status, props]

    def _get_until_when_available(self, target):
        if target.is_available():
            when = self.allocator.get_until_when_available(target)
            return "\nuntil {0}".format(when) if when else ""
        return ""

    @_run_in_thread_with_queue
    def server_add_bitstream_from_url(self, url, board_type, custom_filename, overwrite, queue=None):
        return self.flasher.download_bitstream_from_url(url, board_type, custom_filename, overwrite, queue)

    def server_force_disconnect(self, identifier):
        target = find_target_by_id(self.targets, identifier)
        self.allocator.force_disconnect(target)

    def _has_got_target(self, identifier):
        return identifier in [t.identifier for t in self.targets]

    def server_add_target(self, identifier, name, boardparams=None):
        if self._has_got_target(identifier):
            raise TargetExistsError("There is already one target with this identifier.")

        target = self.target_factory.new_target(identifier, name, boardparams)

        target.init_target()
        target.collect_cpu_info()

        self.targets.append(target)
        self.configuration.add_target_to_config_file(str(identifier), name, boardparams)
        self.weights_handler.add_weights(target.properties)

    def _delete_target(self, t):
        logger.info("Deleted {0}".format(t.identifier))
        t.disconnect()
        if isinstance(t, ConmuxTarget):
            t._conmux_disconnect()
        self.targets.remove(t)

    def server_remove_target(self, identifier):
        message = None
        try:
            target = find_target_by_id(self.targets, identifier)
            if not target.is_used_by_user():
                logger.debug("Deleted {0}".format(identifier))
                self._delete_target(target)
            else:
                message = "Target {0} is in use and will be deleted when released".format(identifier)
                logger.debug(message)
                self.targets_to_delete.append(target)
        except TargetNotFound:
            pass
        existed = self.configuration.remove_target(identifier)
        if not existed:
            raise TargetNotFound("There is no target with id:{0} in config file.".format(identifier))
        return message

    def server_refresh(self):
        self.allocator.refresh_all_and_sort_out(one_shot=True)

    def server_change_actual_res_end_time(self, user, identifier=None, time_to=None):
        target = find_target_by_id(self.targets, identifier) if identifier else self._find_target_by_owner(user)

        if not target.is_owned_by(user):
            raise ValueError("Target {0} is not assigned to you.".format(target.identifier))

        return self.allocator.change_actual_res_end_time(target, time_to)

    def _find_target_by_owner(self, owner):
        targets = [t for t in self.targets if t.is_owned_by(owner)]
        if len(targets) > 1:
            raise TargetNotFound("You must be more specific. There is more than one target assigned to you: {0}."
                                 .format(natural_join([t.identifier for t in targets])))
        try:
            return targets[0]
        except IndexError:
            raise TargetNotFound("There are no targets assigned to you.")

    def server_remove_bitstream(self, name):
        self.flasher.remove_bitstream(name)

    def server_bitstreams(self, verbose=False, properties=None):
        return self.flasher.get_bitstreams_details(verbose, properties, self.weights_handler.weights)

    def server_upload(self, filename, file_size, board_type, user, overwrite=False):
        return self.flasher.upload_bitstream(filename, file_size, board_type, user, overwrite)

    def save_new_bitstream(self, filename, board_type, _=True):
        self.flasher.save_new_bitstream(filename, board_type, True)

    def server_cancel_reservation(self, id_to_cancel, owner):
        self.allocator.cancel_reservation(id_to_cancel, owner)

    def server_acquire(self, owner, identifier=None, properties=None, bitstream=None,
                       time_from=None, time_to=None, need_time=None, new_target=False, force=False, daily=False):

        logger.debug("{0} is acquiring {1} with {2} bitstream from {3} to {4}".format(owner, identifier or properties, bitstream or "no", time_from or "now", time_to))

        bitstream_to_flash = self.flasher.get_bitstream(bitstream) if bitstream else None

        return self._acquire(owner, identifier, properties, bitstream_to_flash, time_from, time_to, need_time, new_target, force, daily)

    @_run_in_thread_with_queue
    def _acquire(self, *args, **kwargs):
        target_id, msgs, res_id = self.allocator.acquire(*args, **kwargs)
        self._append_message_about_rfc_server(msgs, target_id)
        msg = " ".join(msgs)
        return target_id, msg, res_id

    def _append_message_about_rfc_server(self, msgs, target_id):
        target = find_target_by_id(self.targets, target_id)
        if isinstance(target, UsbTarget):
            try:
                host, port = self.rfc_servers_manager.get_server_details(target)
                msgs.append("Rfc server address is {0}:{1}.".format(host, port))
            except NoRFCServerFound:
                pass

    def server_release(self, user, identifier=None):
        if identifier:
            targets = [find_target_by_id(self.targets, identifier, user)]
        else:
            targets = [t for t in self.targets if t.is_owned_by(user)]

        if targets:
            self.allocator.release(targets, user)
            self._delete_removed_which_were_in_use(targets)

    def _delete_removed_which_were_in_use(self, released):
        [self._delete_target(t) for t in released if t in self.targets_to_delete]


class ProbeAllocator(object):
    def __init__(self, configuration, targets, target_flasher, weights_handler, email_sender=None,
                 bookings_file=None, get_actual_time=get_actual_time):
        self.configuration = configuration
        self.get_actual_time = get_actual_time
        self.targets = targets
        self.weights_handler = weights_handler

        self.props_fixer = PropertyNamesFixer(self.configuration.read_internal_code_names(), self.targets)

        id_generator = IdGenerator(self.configuration)
        self.reservation_factory = ReservationFactory(self.get_actual_time, id_generator)
        self.email_sender = email_sender or EmailSender()
        self.flasher = target_flasher

        logger.info("Reservations file is {0}".format(bookings_file))
        self.reservation_pickler = ReservationPickler(bookings_file)
        self.reservations = self._read_reservations()
        self.actual_reservations = dict()
        self._set_targets_owners()

        self._init_targets()

        self.refreshing_threads = []

        logger.debug("First refresh will be executed in {0} seconds.".format(REFRESH_INTERVAL))
        self._run_refreshing_daemon()

    def _set_targets_owners(self):
        for t in self.targets:
            for r in self.reservations[t.identifier]:
                if r.is_its_time(self.get_actual_time()):
                    t.owner = r.user

    def _read_reservations(self):
        reservations = self.reservation_pickler.read_reservations()
        all_read_res = len(reservations)
        reservations = [r for r in reservations if not r.is_expired() and not r.is_gone(self.get_actual_time())]
        logger.debug("Read {0} reservations and {1} of them have not expired.".format(all_read_res, len(reservations)))

        result = defaultdict(list)
        for r in reservations:
            result[r.target_id].append(r)

        return result

    def _run_refreshing_daemon(self):
        self.refreshing_daemon = Timer(REFRESH_INTERVAL, self.refresh_all_and_sort_out)
        self.refreshing_daemon.name = "Refreshing_timer"
        self.refreshing_daemon.setDaemon(True)
        self.refreshing_daemon.start()

    def refresh_all_and_sort_out(self, one_shot=False):
        self.refreshing_threads = [t for t in self.refreshing_threads if t.is_alive()]
        current_refreshes = [t.name for t in self.refreshing_threads]
        for t in self.targets:
            thread_name = "refreshing_{0}".format(t.short_id)
            if not thread_name in current_refreshes:
                thread = Thread(target=self._refresh_and_sort_out, args=(t,), name=thread_name)
                thread.start()
                self.refreshing_threads.append(thread)
            else:
                logger.debug("Refresh for {0} already running".format(t.identifier))

        if not one_shot:
            self._run_refreshing_daemon()

    def _refresh_and_sort_out(self, target):
        if target.can_be_refreshed():
            logger.debug("Refreshing {0} ({1})".format(target.name, target.identifier))
            target.refresh()
        self._sort_out_reservations(target)

    def _init_targets(self):
        threads = [(Thread(None, self._init_target, "init_{0}".format(t.short_id), (t, True)), t) for t in self.targets]
        [thread.start() for thread, target in threads]
        for thread, target in threads:
            thread.join(20)
            if thread.isAlive():
                logger.warning("Timed out waiting on init of {0} ({1})".format(target.name, target.identifier))

    def _init_target(self, target, boring_logs=True):
        try:
            target.init_target(boring_logs)
            target.collect_cpu_info(boring_logs)
        except TargetAlreadyUsed as e:
            self._remove_reservation(target)
            self._start_already_connected_user_reservation(target, e.actual_user)
        except DeviceNotFoundError:
            logger.info("Was not able to find device {0}".format(target.identifier))
            self._remove_reservation(target)
        except RuntimeError as e:
            logger.info("Was not able to initialize {0}, error msg: {1}".format(target.identifier, e.message))
            self._remove_reservation(target)

    def _start_already_connected_user_reservation(self, target, user):
        res = self.reservation_factory.new(False, user, None, None, None, target.identifier)
        logger.debug("{0}: was already in use by '{1}' so connecting as them, reservation id is {2}".format(target.short_id, user, res.id))
        self.reserve_target(res)

    def _reserve_again(self, target, desired, queue):
        msgs = []
        actual_res = self._get_actual_reservation(target)

        if not isinstance(desired, DisposableReservation):
            raise ProbeBeingUsed("Please release the probe before adding daily reservation.")

        if actual_res.ends_before(desired.time_to):
            msgs.append(self._change_res_end_time(actual_res, target, desired._time_to))
        elif not desired.bitstream_to_flash:
            msgs.append("Target is already assigned to you.")

        if desired.bitstream_to_flash:
            self.flasher.reflash(target, desired.bitstream_to_flash, desired.user, queue)
            msgs.append("Target was flashed with {0}.".format(desired.bitstream_to_flash.name))
        return msgs, actual_res.id

    def reserve_target(self, desired, queue=None):
        messages = []
        target = find_target_by_id(self.targets, desired.target_id)
        with target:
            all_reservations = self.get_reservations(target)

            if not desired.acquire_new and target.is_owned_by(desired.user) and desired.should_start_now(self.get_actual_time()):
                return self._reserve_again(target, desired, queue)

            if desired.force:
                if desired.should_start_now(self.get_actual_time()):
                    if not target.is_owned_by(desired.user):
                        self._release_target(target)
                else:
                    self._shorten_reservation_before(target, desired.time_from)

                cut_reservation_if_need(desired, all_reservations, messages)
                self._cancel_overlaping_reservations(target, desired)
            else:
                cut_reservation_if_need(desired, all_reservations, messages)
                check_if_reservation_overlap(all_reservations, desired)

            if desired.should_start_now(self.get_actual_time()):
                target.change_owner(desired.user)

                if desired.bitstream_to_flash:
                    try:
                        self.flasher.reflash(target, desired.bitstream_to_flash, desired.user, queue)
                        messages.append("Target was flashed with {0}.".format(desired.bitstream_to_flash.name))
                    except Exception:
                        target.release()
                        raise
                self.actual_reservations[target.identifier] = desired

            self._add_reservation(target, desired)
            return messages, desired.id

    def _add_reservation(self, target, reservation):
        all = self.get_reservations(target)
        all.append(reservation)
        all[:] = sort_reservations(all, self.get_actual_time())
        self.reservation_pickler.add_reservation(reservation)

    def _shorten_reservation_before(self, target, new_time_to):
        try:
            res = find_reservation_during(self.get_reservations(target), new_time_to)
            self._change_res_end_time(res, target, new_time_to)
            logger.info("{0}: {1} reservation end time was changed {2}.".format(target.identifier, res.user, str(res)))
        except NoReservationsFound:
            pass

    def _reserve_other_matching_target(self, res, target):
        new_res = copy(res)
        targets = self._find_targets_to_acquire_by_properties(new_res)
        new_target, reservation_msgs, res_id = self._reserve_any_target(targets, new_res)
        self._remove_reservation(target, res)
        self.email_sender.message_that_assigned_other_matching(new_res, new_target, reservation_msgs)
        logger.debug("Target in reserved in {0} reservation has changed parameters so assigned {1} that matches them".format(res_id, new_target.short_id))

    def _assign_target_to_user(self, res, target):
        target.change_owner(res.user)
        if res.bitstream_to_flash:
            try:
                self.flasher.reflash(target, res.bitstream_to_flash, res.user)
                self.email_sender.message_that_target_is_flashed_properly(target, res.bitstream_to_flash, res.user)
            except Exception as e:
                self.email_sender.message_that_flashing_failed(target, res.bitstream_to_flash, res.user, e)
        else:
            self.email_sender.message_that_assigned(res, target)
        self.actual_reservations[target.identifier] = res

    def _kick_off_user(self, res, target):
        self.email_sender.message_that_kicking_off(res, target)
        self._release_target(target)

    def _sort_out_reservations(self, target):
        all_res = self.get_reservations(target)
        for res, next_res in map(None, all_res, all_res[1:]):
            try:
                if res.should_end_now(self.get_actual_time()):
                    self._end_reservation(res, next_res, target)

                if res.is_going_to_end(self.get_actual_time()) and (not next_res or next_res.user != res.user):
                    self.email_sender.message_user_that_res_is_ending(res, target)

                if res.should_start_now(self.get_actual_time()) and not target.is_owned_by(res.user):
                    self._start_reservation(res, target)
            except (DeviceNotFoundError, RuntimeError, da_exception.Error) as e:
                logger.debug("{0}: {1}".format(target.identifier, str(e)))

    def _end_reservation(self, res, next_res, target):
        if next_res and next_res.user == res.user and next_res.should_start_now(self.get_actual_time()):
            self._move_user_reservation_from_actual_to_next(next_res, target)
        elif target.is_owned_by(res.user):
            self._kick_off_user(res, target)

    def _start_reservation(self, res, target):
        # check if properties are still okay, if not find matching target with these properties or find bitstream and flash
        if res.desired_properties and not target.matches_properties(res.desired_properties):
            try:
                self._reserve_other_matching_target(res, target)
                return
            except (AcquiringError, TargetNotFound):
                # if failed searching for a new bitstream and flashing then try to find bitstream matching this board
                try:
                    res.bitstream_to_flash = self.flasher.get_any_matching_bitstream(res.desired_properties, target)
                except FirmwareNotFound:
                    self.email_sender.message_that_changed_params_and_cannot_find_any_new_one(res, target)
                    self._remove_reservation(target, res)
                    return
        try:
            with target:
                if not target.is_available():
                    self._release_target(target)
                    self.email_sender.message_that_disconnecting(res, target)
                self._assign_target_to_user(res, target)
        except Exception as e:
            self.email_sender.message_that_error_occurred_while_trying_to_assign(res, target, e)

    def _remove_reservation(self, target, res=None):
        try:
            if not res:
                res = self._pop_actual_reservation(target)
            logger.info("{0}: Removing {1}'s reservation after releasing booking ({2})".format(target.short_id, res.user, res.id))
            if isinstance(res, DisposableReservation):
                self.get_reservations(target).remove(res)
            self._expire_reservation(res)
        except NoReservationsFound:
            logger.debug("{0}: Was trying to remove a reservation but target has not got any.".format(target.short_id))

    def _get_actual_reservation(self, target):
        try:
            return self.actual_reservations[target.identifier]
        except KeyError:
            raise NoReservationsFound

    def _pop_actual_reservation(self, target):
        try:
            return self.actual_reservations.pop(target.identifier)
        except KeyError:
            raise NoReservationsFound

    def _expire_reservation(self, res):
        res.expire(self.get_actual_time())
        self.reservation_pickler.update_reservation(res)

    def _move_user_reservation_from_actual_to_next(self, next_res, target):
        logger.debug("It is time for reservation {0} but target is already in use by {1} so removing old reservation and setting this one as actual".format(next_res.id, next_res.user))
        self._remove_reservation(target)
        target.actual_reservation = next_res

    def _acquire_by_id(self, res, queue):
        messages, res_id = self.reserve_target(res, queue)
        return str(res.target_id), messages, res_id

    def change_actual_res_end_time(self, target, time_to):
        actual = self._get_actual_reservation(target)
        return self._change_res_end_time(actual, target, time_to)

    def _change_res_end_time(self, res, target, time_to):
        res.change_end_time(time_to)
        cut_reservation_if_need(res, self.get_reservations(target))
        self.reservation_pickler.update_reservation(res)
        return "Your {0} reservation time was changed to {1}.".format(target.identifier, res.short_time_to)

    def get_reservations(self, target):
        return self.reservations[target.identifier]

    def _acquire_by_bitstream(self, res, queue):
        targets = self.find_boards_to_flash(res.bitstream_to_flash)
        target, messages, res_id = self._reserve_any_target(targets, res, queue)
        return str(target.identifier), messages, res_id

    def _acquire_by_properties(self, res, queue):
        """ Try to acquire target by properties, if not found or all are in use then try to
        find bitstream with desired properties and flash it
        """
        self.props_fixer.fix_internal_codes_and_properties(res.desired_properties)
        logger.debug("Acquired properties: {0}".format(", ".join(res.desired_properties)))
        try:
            targets = self._find_targets_to_acquire_by_properties(res)
            try:
                target, messages, res_id = self._reserve_any_target(targets, res, queue)
                return str(target.identifier), messages, res_id
            except AcquiringError:
                error_message = _make_error_msg_when_no_target_found(targets)
                raise TargetNotFound(error_message)
        except (ProbeBeingUsed, ProbeBooked, TargetNotFound) as e:
            try:
                return self._flash_any_board_to_have_properties(res, queue)
            except NoTargetFlashed:
                pass
            raise e

    def _flash_any_board_to_have_properties(self, res, queue):
        for bitstream, targets in self.find_boards_with_bitstream(res.desired_properties):
            try:
                res.bitstream_to_flash = bitstream
                target, messages, res_id = self._reserve_any_target(targets, res, queue)
                return str(target.identifier), messages, res_id
            except (FirmwareNotFound, AcquiringError, FlashableBoardNotFound):
                pass
        raise NoTargetFlashed("Could not flash any target to get matching properties.")

    def find_boards_with_bitstream(self, properties):
        try:
            for bitstream in self.flasher.get_bitstreams_with_properties(properties):
                try:
                    targets = self.find_boards_to_flash(bitstream)
                    yield (bitstream, targets)
                except FlashableBoardNotFound:
                    pass
        except FirmwareNotFound:
            pass

    def acquire(self, owner, identifier, properties, bitstream_to_flash, time_from, time_to,
                need_time, new_target, force, daily, queue):
        res = self.reservation_factory.new(daily, owner, time_from, time_to, need_time, identifier,
                                           bitstream_to_flash, properties, new_target, force)

        if res.target_id:
            return self._acquire_by_id(res, queue)
        elif res.desired_properties:
            return self._acquire_by_properties(res, queue)
        elif res.bitstream_to_flash:
            return self._acquire_by_bitstream(res, queue)
        else:
            raise ValueError("Neither identifier, properties, or bitstream have been specified.")

    def _reserve_any_target(self, targets, reservation, queue=None):
        targets = _put_free_targets_first(targets)
        for target in targets:
            reservation.target_id = target.identifier
            try:
                if reservation.bitstream_to_flash or target.status != "No target":
                    messages, res_id = self.reserve_target(reservation, queue)
                    return target, messages, res_id
            except Exception:
                pass
        raise AcquiringError("Unable to find any board to flash.")

    def release(self, targets, user):
        for target in targets:
            with target:
                if target.is_owned_by(user):
                    self._release_target(target)
                elif target.is_available():
                    msg = "Target is already free." + make_propositions_message(targets_owned_by(user, self.targets))
                    raise TargetAlreadyFree(msg)
                else:
                    raise AttributeError("Cannot disconnect someone else. Target is in use by {0}. "
                                         "Try with -f flag to force disconnect.".format(target.owner))

    def _release_target(self, target):
        self._remove_reservation(target)
        target.release(force=True)

    def force_disconnect(self, target):
        self._release_target(target)

    def _find_targets_to_acquire_by_properties(self, res):
        targets = self._find_targets_matching_to_properties(res.desired_properties)
        if not res.acquire_new and res.should_start_now(self.get_actual_time()):
            owned_by_user = [t for t in targets if t.is_owned_by(res.user)]
            targets = owned_by_user or targets
        return targets

    def _find_targets_matching_to_properties(self, properties):
        matching_targets = filter_targets(properties, self.targets, self.props_fixer.get_internal_code_names())
        matching_targets.sort(key=lambda t: t.get_value(self.weights_handler.get_weights()))
        self.weights_handler.increase_weights(properties)
        return matching_targets

    def find_boards_to_flash(self, bitstream):
        res = [t for t in self.targets if isinstance(t, FlashableTarget) and is_bitstream_matching_target(bitstream, t)]
        if not res:
            raise FlashableBoardNotFound("Has not found a board to flash a firmware.")
        return res

    def cancel_reservation(self, id_to_cancel, owner):
        for t in self.targets:
            for res in self.get_reservations(t):
                if res.id == id_to_cancel:
                    if res.user != owner:
                        raise ValueError("You cannot cancel another user's reservations.")
                    self._cancel_reservation(t, res)
                    return
        raise NoReservationsFound("There is no reservation with id {0}".format(id_to_cancel))

    def _cancel_reservation(self, target, res):
        try:
            if res == self._get_actual_reservation(target):
                target.release(force=True)
        except NoReservationsFound:
            pass
        self.get_reservations(target).remove(res)
        res.cancel(self.get_actual_time())
        self.reservation_pickler.update_reservation(res)

    def _cancel_overlaping_reservations(self, target, reservation):
        res = [r for r in self.get_reservations(target) if are_reservations_overlaping(r, reservation)]
        if res:
            logger.debug("Cancelling {0} reservations: {1}".format(len(res), ", ".join(str(r.id) for r in res)))
            for r in res:
                self._remove_reservation(target, r)
                # if r.user != reservation.user:
                #   self.email_sender.message_that_reservation_is_canceled(target, r, reservation.user)

    def get_reservations_details(self, identifier, user, old=False):
        if old:
            res = self.reservation_pickler.read_reservations()
            res = [r for r in res if (not identifier or r.target_id == identifier)]
        else:
            targets = [find_target_by_id(self.targets, identifier)] if identifier else self.targets
            res = [r for t in targets for r in self.get_reservations(t)]

        result = [r.details() for r in res if not user or r.matches_user(user)]

        if not result:
            message = "No reservations"
            message += " of {0}".format(identifier) if identifier else ""
            message += " made by {0}.".format(user) if user else "."
            raise NoReservationsFound(message)
        return sorted(result, key=lambda x: (x[0], x[2]))

    def get_until_when_available(self, target):
        if self.get_reservations(target):
            return self.get_reservations(target)[0].short_time_from
        return None


class PropertyNamesFixer(object):
    def __init__(self, internal_code_names, targets):
        self.internal_code_names = internal_code_names
        self.targets = targets

    def get_internal_code_names(self):
        return self.internal_code_names.keys()

    def fix_internal_codes_and_properties(self, properties):
        if self.internal_code_names:
            properties[:] = [self.internal_code_names.get(p.lower(), p) for p in properties]
        properties[:] = [_fix_one_equal_sign(p) for p in properties]
        properties[:] = [_fix_missing_quotes(p) for p in properties]
        properties[:] = [self._fix_name_property(p) for p in properties]

    def _fix_name_property(self, p):
        """ Changes sp into probe_type=='SysProbe', knight into display_name=='P6600' """
        p = _fix_probe_type_expression(p)
        if not re.search("[=!<>]", p):
            for t in self.targets:
                if p.lower() == t.name.lower():
                    return "name=='{0}'".format(t.name)
                if p.lower() == t.properties.get("cpu_name", "").lower():
                    return "cpu_name=='{0}'".format(t.properties["cpu_name"])
                if p.lower() == t.properties.get("display_name", "").lower():
                    return "display_name=='{0}'".format(t.properties["display_name"])
                if p.lower() == t.identifier.type.lower():
                    return "probe_type=='{0}'".format(t.identifier.type)
        return p


def _fix_one_equal_sign(p):
    r"""
    >>> str(_fix_one_equal_sign("property='abc'"))
    "property=='abc'"
    >>> str(_fix_one_equal_sign("property!=abc"))
    'property!=abc'
    """
    return re.sub("([^<>!=])=([^<>!=])", r"\1==\2", p)


def _fix_missing_quotes(p):
    """
    >>> _fix_missing_quotes("probe_type==SysProbe")
    "probe_type=='SysProbe'"
    >>> _fix_missing_quotes("probe_type=True")
    'probe_type=True'
    >>> _fix_missing_quotes("probe_type==123")
    'probe_type==123'
    """
    m = re.match("^([^<>!=]*)([=<>!]{1,2})([^'\"=]*)$", p)
    if m:
        name, signs, value = m.groups()
        if value.lower() in ["true", "false"]:
            return "{0}{1}{2}".format(name, signs, value.capitalize())
        elif not value.isdigit():
            return "{0}{1}'{2}'".format(name, signs, value)
    return p


def make_forwarder(name):
    def forwarder(self, *args, **kwargs):
        return self._run_on_slaves(name, *args, **kwargs)
    forwarder.__name__ = name
    return forwarder


class MasterServer(QueueThreadingServer):
    def __init__(self, server=None, *args, **kwargs):
        QueueThreadingServer.__init__(self)
        self.local_server = AcquirerServer(*args, **kwargs)
        self.slave_servers = [self.local_server]  # acquirer_servers
        self.version = VERSION
        self.server = server

    server_release =                    make_forwarder('server_release')
    server_force_disconnect =           make_forwarder('server_force_disconnect')
    server_remove_target =              make_forwarder('server_remove_target')
    server_refresh =                    make_forwarder('server_refresh')
    server_remove_bitstream =           make_forwarder('server_remove_bitstream')
    server_cancel_reservation =         make_forwarder('server_cancel_reservation')
    server_status =                     make_forwarder('server_status')
    server_reservations =               make_forwarder('server_reservations')
    server_old_reservations =           make_forwarder('server_old_reservations')
    server_change_name =                make_forwarder('server_change_name')
    server_target_status =              make_forwarder('server_target_status')
    server_change_properties =          make_forwarder('server_change_properties')
    save_new_bitstream =                make_forwarder('save_new_bitstream')
    server_change_actual_res_end_time = make_forwarder('server_change_actual_res_end_time')

    def close_server(self, exit_code=None):
        logger.info("Server is closing")
        [s.close_server(exit_code) for s in self.slave_servers]
        logger.info("Server shutting down with {0} code".format(exit_code or "No"))
        self.exit_status = exit_code or DEFAULT_EXIT_CODE
        self.server.server_close()

    def ping(self):
        return True

    def get_version(self):
        return self.version

    def server_change_logger_level(self, level=None):
        if level:
            level = level.upper() if isinstance(level, str) else level
            logger.setLevel(level)
            logger.debug("Logging level changed to {0}".format(logging.getLevelName(logger.level)))
        return logging.getLevelName(logger.level)

    def server_add_server(self, address):
        try:
            _check_server_details(address)
        except ServerConnectionError:
            raise ServerConnectionError("Acqurier server was not found at: {0}".format(address))

        slave = get_server(address)
        self.add_slave_server(slave)

    def add_slave_server(self, slave):
        self.slave_servers.append(slave)

    def server_bitstreams(self, verbose=False, properties=None):
        lists_of_bitstreams = [slave.server_bitstreams(verbose, properties) for slave in self.slave_servers]
        return list(chain(*lists_of_bitstreams))

    def server_list(self, verbose=False, properties=None):
        lists_of_targets_details = [slave.server_list(verbose, properties) for slave in self.slave_servers]
        return list(chain(*lists_of_targets_details))

    def server_upload(self, filename, file_size, board_type, user, overwrite=False):  # TODO slaves ?
        return self.local_server.server_upload(filename, file_size, board_type, user, overwrite)

    def server_add_target(self, identifier, name, boardparams=None):
        return self.local_server.server_add_target(identifier, name, boardparams)

    def _run_on_slaves(self, func, *args, **kwargs):
        done = False
        e = None
        for slave in self.slave_servers:
            try:
                result = getattr(slave, func)(*args, **kwargs)
                if result:
                    return result
                done = True
            except TargetNotFound as e:
                pass

        if not done and e:
            raise e

    @_run_in_thread_with_queue
    def server_add_bitstream_from_url(self, url, board_type, custom_filename, overwrite, queue=None):
        args = (url, board_type, custom_filename, overwrite)
        return self.run_threaded_function_on_slaves("server_add_bitstream_from_url", args, queue)

    @_run_in_thread_with_queue
    def server_flash_board(self, identifier, bitstream_name, owner, _=None, queue=None):
        return self.run_threaded_function_on_slaves("server_flash_board", (identifier, bitstream_name, owner), queue)

    @_run_in_thread_with_queue
    def server_acquire(self, owner, identifier, properties, bitstream_to_flash,
                       time_from, time_to, need_time, new_target, force, daily=False, queue=None):
        args = (owner, identifier, properties, bitstream_to_flash, time_from, time_to, need_time, new_target, force, daily)
        return self.run_threaded_function_on_slaves("server_acquire", args, queue)

    def run_threaded_function_on_slaves(self, func, args, queue):
        for slave in self.slave_servers:
            try:
                queue_id = getattr(slave, func)(*args)
                elapsed = 0
                while elapsed < MAX_FLASHING_TIME:
                    val = slave.server_get_queue_value(queue_id)
                    if val is None:
                        time.sleep(0.01)
                        elapsed += 0.01
                    elif isinstance(val, basestring):
                        queue.put(val)
                    else:
                        return val
            except (TargetNotFound, ServerException, ServerConnectionError):
                pass
        raise


class WeightsHandler(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.weights = self.configuration.read_weights()

    def get_weights(self):
        return self.weights

    def add_weights(self, properties):
        new_properties = dict((p, 5) for p in properties.iteritems() if p not in self.weights)
        self.weights.update(new_properties)
        logger.debug("New target added new properties: {0}".format(", ".join("{0} = {1}".format(p[0], p[1]) for p in new_properties)))
        self.configuration.update_weights_in_config_file(new_properties)

    def increase_weights(self, properties):
        for p in properties:
            name, value = split_property_and_val(p)
            if name not in ["name", "probe_type"]:
                try:
                    self.weights[(name, value)] += 1
                    logger.debug("Property {0} increased from {1} to {2}".format(name, self.weights[(name, value)] - 1, self.weights[(name, value)]))
                except KeyError:
                    self.weights[(name, value)] = 6
                    logger.debug("Property {0} is new and its value is {1}".format(name, self.weights[(name, value)]))
        self.configuration.update_weights_in_config_file(self.weights)


class TargetFlasher(object):
    def __init__(self, upload_port, bitstreams_dir=None):
        self.upload_port = upload_port
        self.bitstreams_dir = bitstreams_dir or os.path.join(get_user_files_dir(), "bitstreams")
        self.actually_used_bitstreams = []
        self.uploading_threads = []
        self.open_to_save = open

    def _get_bitstream_dir_files(self):
        try:
            for file in os.listdir(self.bitstreams_dir):
                yield os.path.join(self.bitstreams_dir, file)
        except (IOError, OSError) as e:
            logger.info("Creating bitstreams dir because {0}".format(e))
            os.makedirs(self.bitstreams_dir)

    def reflash(self, target, bs, owner=None, queue=None):
        check_is_bitstream_matching_target(target, bs)
        with self._locking_bitstream(bs, owner):
            if target.can_reflash:
                if queue:
                    queue.put("Starting reflashing {0} with {1}...".format(target.identifier, bs.name))
                try:
                    target.reflash(bs)
                except Exception as e:
                    if isinstance(e, NoTargetException):
                        logger.info(" Target was probably not flashed properly with {0}.".format(bs.name))
                    logger.error(e)
                    if queue:
                        queue.put(e)
                self._store_cpu_info(bs, target)
            else:
                err = RuntimeError('Cannot reflash target {0}'.format(target.identifier))
                logger.error(err)
                if queue:
                    queue.put(err)

    def _store_cpu_info(self, bs, target):
        bs.store_cpuinfo(target.properties if not target.is_broken() else {})

    @contextmanager
    def _locking_bitstream(self, bs, owner):
        try:
            self.actually_used_bitstreams.append((bs.filename, owner))
            yield
        finally:
            self.actually_used_bitstreams.remove((bs.filename, owner))

    def get_any_matching_bitstream(self, desired_properties, target):
        try:
            matching_bitstreams = self.get_bitstreams_with_properties(desired_properties)
            return next(bs for bs in matching_bitstreams if is_bitstream_matching_target(bs, target))
        except (StopIteration, FirmwareNotFound):
            raise FirmwareNotFound

    def get_bitstreams_with_properties(self, desired_properties):
        return find_matching_bitstreams(desired_properties, self.get_bitstreams())

    def _actual_bitstream_users(self, bitstream):
        return [tuple[1] for tuple in self.actually_used_bitstreams if tuple[0] == bitstream.filename]

    def download_bitstream_from_url(self, url, board_type, custom_filename="", overwrite=False, queue=None):
        filename = custom_filename or basename(url)
        localname = self._check_localname(filename, overwrite)

        if queue:
            queue.put("Downloading {0} ...".format(filename))
        self._download_from_url(url, localname)
        self.save_new_bitstream(localname, board_type, False, url)

    def _download_from_url(self, url, filename):
        data = urlopen(url).read()
        with open(filename, "wb") as f:
            f.write(data)

    def _check_localname(self, filename, overwrite):
        localname = os.path.join(self.bitstreams_dir, filename)
        if not overwrite and isfile(localname):
            raise ValueError("Bitstream already exists.")
        return localname

    def upload_bitstream(self, filename, file_size, board_type, user, overwrite=False):
        localname = self._check_localname(filename, overwrite)
        logger.debug("Received request from {0} to upload {1}".format(user, filename))
        return self._download_bitstream_in_thread((localname, file_size, board_type), user)

    def _download_bitstream_in_thread(self, args, name):
        queue = Queue.Queue()
        t = Thread(None, self._download_bitstream, name=name, args=args+(queue,))
        self.uploading_threads.append(t)
        t.start()
        try:
            return queue.get(timeout=2)
        except Queue.Empty:
            raise ServerException("Server was not able to get any port for you")

    def _download_bitstream(self, localname, file_size, board_type, queue):
        with socket_to_receive(self.upload_port) as (sock, hostaddr, port):
            queue.put((hostaddr, port))
            logger.debug("Opened socket for {0} file on {1}:{2}".format(basename(localname), hostaddr, port))
            sock.listen(5)

            conn, addr = sock.accept()
            logger.debug("Receiving bitstream {0} from {1}".format(basename(localname), addr))
            bytes_recd = 0
            with self.open_to_save(localname, 'wb') as f:
                while bytes_recd < file_size:
                    chunk = conn.recv(min(file_size - bytes_recd, 2048))
                    if chunk == '':
                        raise RuntimeError("socket connection broken")
                    f.write(chunk)
                    bytes_recd += len(chunk)
            conn.close()
            logger.debug("Successfully downloaded bitstream to {0} ".format(localname))

            self.save_new_bitstream(localname, board_type)

    def save_new_bitstream(self, filename, board_type, conmux=False, url_source=None):
        config_file = os.path.join(self.bitstreams_dir, filename + ".ini") if conmux else None
        bitstream = BitstreamFile(filename, board_type, config_file=config_file, conmux=conmux)
        bitstream.create_config_file(url_source)
        logger.debug("Received {0} bitstream and created its config file".format(filename))

    def get_bitstreams_details(self, verbose, properties, weights):
        bitstreams = self.get_bitstreams()
        if properties:
            bitstreams = [bs for bs in bitstreams if bs.matches_properties(properties)]
            if not bitstreams:
                raise FirmwareNotFound("There are no bitstreams matching these properties.")
        res = [bs.details(weights, verbose) for bs in bitstreams]
        return sorted(res)

    def get_bitstreams(self):
        result = []
        for file in self._get_bitstream_dir_files():
            if file.endswith(".ini"):
                try:
                    result.append(BitstreamFile(config_file=file))
                except ConfigFileError:
                    pass
        if not result:
            raise FirmwareNotFound("There are no bitstream files on the server.")
        return result

    def get_bitstream(self, name):
        matching_bitstreams = [bs for bs in self.get_bitstreams() if bs.matches_acquire(name)]

        if len(matching_bitstreams) > 1:
            raise FirmwareNotFound("There is more than one bitstream that matches {0}. Please be more specific. "
                                   "Ones that matches are:\n{1}".format(name, "\n".join(b.name for b in matching_bitstreams)))
        elif not matching_bitstreams:
            msg = "There is no bitstream called {0}.".format(name)
            all_bitstreams_names = [bs.name for bs in self.get_bitstreams()]
            msg += message_proposing_similar_matches(name, all_bitstreams_names)
            raise FirmwareNotFound(msg)

        return matching_bitstreams[0]

    def join_threads(self):
        if self.uploading_threads:
            users_uploading = ", ".join([t.name for t in self.uploading_threads])
            logger.info("Someone is still uploading a bitstream: {0}".format(users_uploading))
            [t.join() for t in self.uploading_threads]

    def remove_bitstream(self, name):
        bitstream_to_del = self.get_bitstream(name)
        users = self._actual_bitstream_users(bitstream_to_del)
        if users:
            raise RuntimeError("Cannot delete bitstream because it is in use by {0}.".format(natural_join(users)))
        [self._del_file(file) for file in bitstream_to_del.files if file]

    def _del_file(self, file):
        try:
            logger.info("Removing {0}".format(file))
            os.remove(file)
        except Exception as e:
            logger.info("Exception while removing: {0}".format(e))


class EmailSender(object):
    def _send_email(self, addressee, msg, subject):
        addressee = addressee.split("@")[0]
        addressee_email = addressee + "@mips.com"
        recipient = [(addressee, addressee_email)]
        img_sendmail_internal(("Acquirer", "acquirer-noreply@mips.com"), recipient, subject, msg, [])
        logger.debug("Sent email to {0} with message about {1}".format(addressee_email, subject))

    def message_that_reservation_is_canceled(self, target, res, canceler):
        message = "Your {0} reservation from {1} to {2} has been cancelled because {3} has force acquired the target."\
            .format(target.identifier, res.long_time_from, res.long_time_tom, canceler)
        self._send_email(res.user, message, target.identifier)

    def message_that_flashing_failed(self, target, bs, owner, e):
        message = "An error occurred while flashing {0} with {1}:\n{2}\nTarget is assigned to you".format(target.identifier, bs.name, str(e))
        self._send_email(owner, message, target.identifier)

    def message_that_target_is_flashed_properly(self, target, bs, owner):
        message = "{0} is flashed with {1} and assigned to you".format(target.identifier, bs.name)
        self._send_email(owner, message, target.identifier)

    def message_that_assigned_other_matching(self, res, target, msgs):
        msg = "Target that was assigned to you during reservation has changed parameters so found {0} " \
              "that satisfies these properties and it is assigned to you.".format(target.identifier)
        msgs.insert(0, msg)
        self._send_email(res.user, " ".join(msgs), "Reservation {0}".format(res.id))

    def message_that_assigned(self, res, target):
        message = "{0} is available now and it is assigned to you.\nYou have it booked {1}".format(target.identifier, res)
        self._send_email(res.user, message, target.identifier)

    def message_user_that_res_is_ending(self, res, target):
        message = "Your reservation ends at {0}. Could you release it before this time, please?".format(res.short_time_to)
        self._send_email(res.user, message, target.identifier)

    def message_that_kicking_off(self, res, target):
        message = "Your {0} reservation ended at {1}. You did not release it so you were disconnected.".format(target.identifier, res.short_time_to)
        self._send_email(res.user, message, target.identifier)

    def message_that_disconnecting(self, res, target):
        message = "{0} has reserved this target from {1} so you have been disconnected now.".format(res.user, res.short_time_from)
        self._send_email(target.owner, message, target.identifier)

    def message_that_error_occurred_while_trying_to_assign(self, res, target, e):
        message = "Error occurred while trying to assign {0}:\n{1}".format(target.short_id, str(e))
        self._send_email(res.user, message, target.identifier)
        logger.debug("Error occurred while sorting out {0} {1} reservation: {2}".format(target.short_id, res.user, str(e)))

    def message_that_changed_params_and_cannot_find_any_new_one(self, res, target):
        msg = "{0} that was assigned to you during reservation has changed parameters and the server " \
              "was not able to find any target or bitstream file with these parameters. " \
              "This means that someone has deleted this bitstream file.".format(target.identifier)
        self._send_email(res.user, msg, "Reservation {0}".format(res.id))


def _make_error_msg_when_no_target_found(targets):
    if len(targets) == 1:
        message = "{0} matched the criteria but ".format(targets[0].identifier)
        message += "it is in use by " if targets[0].is_used_by_user() else "its status is "
        message += targets[0].status + "."
    else:
        message = "{0} targets matched the criteria, but none of them are available: {1}.".format(len(targets), natural_join([t.identifier for t in targets]))
    return message


class RFCMultilpexor(object):
    def __init__(self):
        self.serial_servers = dict()
        self.hostaddr = socket.gethostname()
        self.actual_port = 9100

    def add_new_server(self, target):
        com = target.dev_path
        server = RFCServer(com, self.actual_port, target.identifier)
        self.actual_port += 1
        self.serial_servers[target.identifier] = server

    def get_server_details(self, target):
        try:
            srv = self.serial_servers[target.identifier]
            return self.hostaddr, srv.port
        except KeyError:
            raise NoRFCServerFound("There is no RFC Server for {0}.".format(target.identifier))


class RFCServer(object):
    def __init__(self, serial_com, port, identifier):
        self.port = port
        self.serial_com = serial_com
        self.running = True
        self.identifier = identifier

    def stop(self):
        self.running = False

    def run(self):
        with serial.Serial(self.serial_com, timeout=3) as ser:
            ser.dtr, ser.rts = False, False
            with socket_to_receive(self.port) as (srv, hostaddr, port):
                srv.listen(1)
                while self.running:
                    client_socket, addr = srv.accept()
                    logging.info('Connected by {0}:{1}'.format(addr[0], addr[1]))
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    ser.dtr, ser.rts = True, True
                    # enter network <-> serial loop
                    r = Redirector(ser, client_socket, self.identifier)
                    try:
                        r.shortcircuit()
                    finally:
                        # logging.info('Disconnected')
                        r.stop()
                        client_socket.close()
                        ser.dtr, ser.rts = False, False
                    #except socket.error as msg:
                    #    logging.error(str(msg))


class Redirector(object):
    def __init__(self, serial_instance, socket, identifier):
        self.identifier = identifier
        self.serial = serial_instance
        self.socket = socket
        self._write_lock = Lock()
        self.rfc2217 = serial.rfc2217.PortManager(self.serial, self, logger=None)

    def statusline_poller(self):
        while self.alive:
            time.sleep(1)
            self.rfc2217.check_modem_lines()

    def shortcircuit(self):
        """connect the serial port to the TCP port by copying everything
           from one side to the other"""
        self.alive = True
        self.thread_read = Thread(target=self.reader)
        self.thread_read.daemon = True
        self.thread_read.name = 'serial->socket'
        self.thread_read.start()
        self.thread_poll = Thread(target=self.statusline_poller)
        self.thread_poll.daemon = True
        self.thread_poll.name = 'status line poll'
        self.thread_poll.start()
        self.writer()

    def reader(self):
        """loop forever and copy serial->socket"""
        while self.alive:
            try:
                data = self.serial.read(self.serial.in_waiting or 1)
                if data:
                    # escape outgoing data when needed (Telnet IAC (0xff) character)
                    self.write(b''.join(self.rfc2217.escape(data)))
            except socket.error as msg:
                self.log.error('{}'.format(msg))
                # probably got disconnected
                break
        self.alive = False
        self.log.debug('reader thread terminated')

    def write(self, data):
        """thread safe socket write with no data escaping. used to send telnet stuff"""
        with self._write_lock:
            self.socket.sendall(data)

    def writer(self):
        """loop forever and copy socket->serial"""
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.serial.write(b''.join(self.rfc2217.filter(data)))
            except socket.error as msg:
                logger.info('{0} rfc serv exception: {1}'.format(self.identifier, msg))
                # probably got disconnected
                break
        self.stop()

    def stop(self):
        """Stop copying"""
        self.log.debug('stopping')
        if self.alive:
            self.alive = False
            self.thread_read.join()
            self.thread_poll.join()


class ThreadWithQueue(Thread):
    '''
    Thread that runs function and puts its output from the functions or exceptions to the queue
    that can be then read by client.
    '''
    def __init__(self, name, queue, function, args, kwargs):
        Thread.__init__(self, name=name)
        self.queue = queue
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
            if result is None:
                self.queue.put(True)
            else:
                self.queue.put(result)
        except Exception as e:
            self.queue.put(e)


@contextmanager
def socket_to_receive(upload_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", upload_port))
    port = sock.getsockname()[1]

    hostaddr = socket.gethostname()
    try:
        yield sock, hostaddr, port
    finally:
        sock.close()


def find_matching_bitstreams(desired_properties, bitstreams):
    '''
    Returns a list of matching bitstreams with different board_types
    `desired_properties` is a list of properties to match
    `bitstreams` is list of bitstreams

    Returns a list of tuples with bitstream files and types of board they need to be flashed on.
    If none of the bitstream files matches properties then will raise FirmwareNotFound exception.
    For eg. it returns one matching bitstream that needs sead3-Lx110, one for boston and one for sead3-LX155,
    then in the case any of these boards are not available can use other with different type.
    '''
    res = []
    for bitstream in bitstreams:
        try:
            if bitstream.matches_properties(desired_properties) and bitstream.board_type not in [r.board_type for r in res]:
                res.append(bitstream)
        except ConfigFileError as e:
            logger.info(e.message)
    if not res:
        raise FirmwareNotFound("Has not found a firmware with such properties. " + ', '.join(desired_properties))
    return res

class RequestHandler(SimpleXMLRPCRequestHandler):
    _master_server = None

    def do_GET(self):
        path = self.path[1:]
        if not path:
            self.respond(200, [("Content-type", "text/html")])
            
            t_list = RequestHandler._master_server.server_list()
            if not t_list:
                t_list = [['']*len(TARGET_INFO_TITLES)]

            try:
                b_list = RequestHandler._master_server.server_bitstreams()
            except FirmwareNotFound:
                b_list = [['']*len(BITSTREAM_INFO_TITLES)]

            # Note the escaped '{}'
            html = dedent('''\
            <html>
                <head>
                    <title>Acquirer Status</title>
                    <style>
                        table {{
                            border-collapse: collapse;
                        }}
                        table, th, td {{
                            border: 1px solid black;
                            padding: 8px;
                        }}
                    </style>
                </head>
                <body>
                    <p>Imgtec version: {IMGTEC_VERSION}<br>
                    Server version: {SERVER_VERSION}</p>
                    <p>To use to this server <a href="python_client">download the client script</a> and run:
                        <blockquote>acquirer.py server {HOSTNAME}</blockquote>
                    Or use your installed imgtec library:
                        <blockquote>python -m imgtec.codescape.acquirer server {HOSTNAME}</blockquote>
                    <p>
                    <p></p>
                    <form action="refresh_targets">
                        <input type="submit" value="Refresh target status" />
                    </form>
                    <p>{TARGET_TABLE}</p>
                    <p>{BITSTREAM_TABLE}</p>
                </body>
            </html>
                ''').format(
                    IMGTEC_VERSION=imgtec_version,
                    SERVER_VERSION=VERSION, 
                    TARGET_TABLE=html_table(TARGET_INFO_TITLES, t_list),
                    BITSTREAM_TABLE=html_table(BITSTREAM_INFO_TITLES, b_list),
                    HOSTNAME=self.headers.get('Host')
                    )

            self.wfile.write(html)

        elif path == 'python_client':
            self.respond(200, 
                [("Content-type", "text/plain"), 
                ('Content-disposition', 'attachment; filename="acquirer.py"')])

            with open(os.path.join(os.path.split(__file__)[0], 'acquirer.py'), 'r') as client:
                self.wfile.write(client.read())

        else:
            if path == 'refresh_targets':
                RequestHandler._master_server.server_refresh()
            self.redirect()

    def redirect(self):
        self.respond(307, [("Location", '/')])

    def respond(self, code, headers):
        self.send_response(code)
        for h in headers:
            self.send_header(*h)
        self.end_headers()

def run_server():
    server = SimpleXMLRPCServer(("", 8000), requestHandler=RequestHandler, logRequests=False, allow_none=True)
    logger.debug("Server started at {0}".format(server.server_address))
    local = MasterServer(server=server)
    RequestHandler._master_server = local
    server.register_instance(local)
    try:
        server.serve_forever()
    except socket.error:
        pass
    sys.exit(local.exit_status)


if __name__ == '__main__':
    run_server()
