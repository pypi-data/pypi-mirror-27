from abc import ABCMeta, abstractmethod
from copy import copy
from difflib import get_close_matches
import inspect
from imgtec.codescape import da_exception, tiny
from imgtec.codescape.acquirer import *
from imgtec.codescape.probe_identifier import Identifier
from threading import RLock
import subprocess
import logging
import platform
import paramiko
import socket
from scp import SCPClient
from paramiko.ssh_exception import NoValidConnectionsError, SSHException

logger = logging.getLogger("Acquirer")

SERVER_HOST = socket.gethostname()
SERVER_PORT = "8000"
SERVER_NAME = "acquirer@" + SERVER_HOST

ALLOWED_STATUSES = ["Available", "No target", ""]
FAILED_STATUSES = ["Offline", "DA Error", "Runtime Error", "No target"]
MAX_WAITING_TIME_FOR_BOARD_BOOT = 20

CONMUX_SERVERS = ["le-fw-console"]


def is_linux():
    return not platform.system().lower().startswith("win")


class ProbeAlreadyAcquired(ProbeBeingUsed):
    pass


class TargetAlreadyUsed(Exception):
    def __init__(self, message, actual_user, *args):
        self.actual_user = actual_user
        super(TargetAlreadyUsed, self).__init__(' '.join([message, actual_user]), *args)


class TargetFactory(object):
    def __init__(self, tiny_to_use, conmux=False):
        self.tiny = tiny_to_use
        self.conmux = conmux

    def new_targets(self, targets_data):
        result = []
        for id, name, data in targets_data:
            try:
                result.append(self.new_target(id, name, data))
            except ValueError as e:
                logger.info("{0}: Wrong target config data: {1}".format(id, str(e)))
        return result

    def new_target(self, identifier, name, boardparams):
        if not boardparams:
            return Target(identifier, name, tiny_to_use=self.tiny)

        elif name.lower().startswith("boston"):
            if len(boardparams) != 3:
                raise ValueError("Wrong number of board parameters")
            hostname, user, password = boardparams
            return BostonTarget(identifier, name, hostname, user, password, tiny_to_use=self.tiny)

        elif any(conmux_srv in boardparams[0] for conmux_srv in CONMUX_SERVERS):
            if len(boardparams) != 1:
                raise ValueError("Wrong number of board parameters")
            return ConmuxTarget(identifier, name, address=boardparams[0], tiny_to_use=self.tiny, conmux=self.conmux)

        else:
            if len(boardparams) != 1:
                raise ValueError("Wrong number of board parameters")
            return UsbTarget(identifier, name, dev_path=boardparams[0], tiny_to_use=self.tiny)


class Target(object):
    def __init__(self, identifier, name, properties=None, status="Available", tiny_to_use=tiny):
        self.identifier = Identifier(identifier)
        self.name = name
        self.properties = properties or {}
        self.connection = None
        self.status = status
        self.tiny = tiny_to_use
        self.owner = "Server"
        self.lock = RLock()

    def __enter__(self):
        logger.debug("Taking lock for {0} ({1})".format(self.name, self.identifier))
        self.lock.acquire()

    def __exit__(self, *args):
        logger.debug("Releasing lock for {0} ({1})".format(self.name, self.identifier))
        self.lock.release()

    @property
    def short_id(self):
        return self.identifier.short_id()

    def connect(self, owner, force=False, _boring_logs=True):
        if _boring_logs:
            logger.debug("{0}: {1} connecting to target, force = {2}".format(self.short_id, owner, force))
        self._connect(owner, force)
        if _boring_logs:
            logger.debug("{0}: {1} connected successfully".format(self.short_id, owner))

    def _connect(self, owner, force):
        try:
            options = {'fake-ownership': owner}
            if force:
                options['force-disconnect'] = 1
                logger.debug("{0}: force disconnecting".format(self.short_id))
            self.connection = self.tiny.ConnectProbe(self.identifier, options=options)
        except da_exception.CommsDeviceNotFoundError as e:
            self._set_error_status("Offline")
            raise DeviceNotFoundError(e.message + " " + self.identifier)
        except da_exception.Error as e:
            if "The device is already in use" in e.message:
                actual_owner = _get_owner_from_error_message(e.message)
                logger.debug("{0}: is already in use by {1}".format(self.short_id, actual_owner))
                raise TargetAlreadyUsed("Target already in use by", actual_owner)
            else:
                self._set_error_status("DA Error", e.message)
                raise e
        except RuntimeError as e:
            self._set_error_status("Runtime Error", e.message)
            raise e

        self.owner = owner if owner != SERVER_NAME else "Server"
        self.status = owner if owner != SERVER_NAME else "Available"

    def _set_error_status(self, status, msg=""):
        if self.status != status:
            logger.debug("{0}: {1}: {2}".format(self.short_id, status, msg))
        self.status = status
        self.owner = "Server"

    def disconnect(self, boring_logs=True):
        if self.connection:
            user = "{0} ({1})".format(self.status, self.owner)
            self.connection.Disconnect()
            if boring_logs:
                logger.debug("{0}: {1} disconnected".format(self.short_id, user))

    def release(self, force=False, boring_logs=True, user=SERVER_NAME):
        if force:
            logger.debug("{0}: Release called by: {1}".format(self.short_id, _get_callers()))
        self.disconnect(boring_logs)
        self.connect(user, force, boring_logs)

    def init_target(self, boring_logs=True):
        user = self.owner if self.owner != "Server" else SERVER_NAME
        self.release(False, boring_logs, user)

    def collect_cpu_info(self, _boring_logs=False):
        try:
            self._collect_cpu_info(_boring_logs)
        except NoTargetException:
            if self.is_available():
                self.status = "No target"

    def _collect_cpu_info(self, logs):
        if self.is_available() or self.connection.GetDAMode() not in ["scanonly", "uncommitted"]:
            try:
                # logger.debug("{0}: Trying to get cpu info".format(self.short_id)) if logs else None
                self.properties.clear()
                self.connection.AutoDetect()
                self.properties = dict(self.connection.CpuInfo(True))
                self.properties = check_if_properties_are_correct(self.properties, self.identifier)
            except RuntimeError as e:
                if str(e).startswith("The probe was not able to detect any socs/cores"):
                    logger.debug("{0}: has no target connected".format(self.short_id)) if logs else None
                    raise NoTargetException("There is no target connected or it is offline.")
                else:
                    logger.info("Was not able to initialize {0}, error msg: {1}".format(self.short_id, str(e))) if logs else None

    def refresh(self, _boring_logs=False):
        previous_status = self.status
        try:
            self.release(boring_logs=_boring_logs)
            self.collect_cpu_info(_boring_logs)
        except DeviceNotFoundError:
            if previous_status != self.status:
                logger.info("Was not able to find device {0}".format(self.identifier))
        except RuntimeError as e:
            if previous_status != self.status:
                logger.info("Was not able to initialize {0}, error msg: {1}".format(self.identifier, e.message))

    def is_owned_by(self, owner):
        return self.owner == owner

    def is_used_by_user(self):
        return self.owner != "Server"

    def is_available(self):
        return self.status in ALLOWED_STATUSES

    def is_broken(self):
        return self.status in FAILED_STATUSES

    def is_reflashing(self):
        return self.status == "Reflashing"

    def can_be_refreshed(self):
        return not self.is_used_by_user() and not self.is_reflashing()

    @property
    def can_reflash(self):
        return False

    def details(self, weights, verbose=False):
        status = _remove_prefix_from_domain(self.status)
        properties_to_show = get_properties_to_show(self.properties, verbose, weights)
        return [str(self.identifier), self.name, status, properties_to_show]

    def check_if_is_allowed_to_acquire(self, owner):
        if self.is_available():
            return
        cases = {
            owner: ProbeAlreadyAcquired("Target is already assigned to you."),
            "Offline": ProbeOffline("Probe is offline."),
            "DA Error": ProbeError("Probe is broken."),
            "Reflashing": ProbeBeingUsed("Probe is already being flashed by server with one of the recently uploaded "
                                         "bitstreams to get its cpuinfo.")
        }
        raise cases.get(self.status, ProbeBeingUsed("Target is already in use by " + self.status))

    def get_value(self, weights):
        sum = 0
        for feature, weight in weights.iteritems():
            try:
                feature_name, feature_val = feature
                target_val = self.properties.get(feature_name)
                if isinstance(target_val, type(feature_val)):
                    if isinstance(target_val, str):
                        target_val, feature_val = target_val.lower(), feature_val.lower()
                    if target_val == feature_val:
                        sum += weight
            except KeyError:
                pass
        return sum

    def change_properties(self):
        raise ValueError("{0} does not have any board properties.".format(self.identifier))

    def get_board_properties(self):
        raise ValueError("{0} does not have any board properties.".format(self.identifier))

    def matches_properties(self, properties):
        props = copy(self.properties)
        props["name"] = self.name
        props["probe_type"] = self.identifier.type
        result = check_if_matches_properties(props, properties)
        return result

    def change_owner(self, owner):
        self.check_if_is_allowed_to_acquire(owner)
        self.disconnect()
        self.connect(owner, force=True)


class FlashableTarget(Target):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        Target.__init__(self, *args, **kwargs)

    def _reconnect(self):
        self.status = "Available"
        if self.is_used_by_user():
            self.change_owner(self.owner)
        else:
            self.release()
        self._collect_cpu_info(True)

    @property
    def can_reflash(self):
        return True

    def _collect_cpu_info(self, logs):
        if self.connection:
            time_elapsed = 0
            while time_elapsed < MAX_WAITING_TIME_FOR_BOARD_BOOT:
                display_logs = (time_elapsed + 2 >= MAX_WAITING_TIME_FOR_BOARD_BOOT)
                try:
                    super(FlashableTarget, self)._collect_cpu_info(logs=display_logs)
                    if self.properties:
                        break
                except NoTargetException:
                    if self.tiny == tiny:
                        time.sleep(2)
                    time_elapsed += 2
                    if time_elapsed >= MAX_WAITING_TIME_FOR_BOARD_BOOT:
                        raise

    def reflash(self, bitstream):
        self.status = "Reflashing"
        self.properties.clear()

        try:
            logger.info("{0}: Flashing with {1}".format(self.identifier, bitstream.filename))
            self._reflash(bitstream.filename)
            logger.info("{0}: Flashed properly with {1}".format(self.identifier, bitstream.name))
        except Exception as e:
            try:
                self._reconnect()
            except Exception as exc:
                logger.error("Error connecting to target after reflash: {0}".format(exc))
            raise e

        self._reconnect()

    @abstractmethod
    def _reflash(self, bitstream_file_path):
        pass


class UsbTarget(FlashableTarget):
    def __init__(self, identifier, name, dev_path=None, copy=None, **kwargs):
        FlashableTarget.__init__(self, identifier, name, **kwargs)
        self.dev_path = dev_path
        self.copy = copy or self._copy

    def _reflash(self, bitstream_file_path):
        self.copy(bitstream_file_path, self.dev_path)

    def _copy(self, src, dst):
        try:
            if is_linux():
                command = "cat {0} > {1}".format(src, dst)
            else:
                raise FlashingError("USB flashing is not supported on Windows.")
                # command = "copy /y {0} /b > {1} /b".format(src, dst)
            res = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

            if res:
                raise FlashingError("Error while trying to flash, subprocess returned {0} error code".format(res))
        except subprocess.CalledProcessError as e:
            raise FlashingError("error {0}: {1}".format(e.returncode, e.output))

    def change_properties(self, *args):
        if len(args) != 1:
            raise ValueError("Wrong number of properties. Needs only dev path.")
        self.dev_path = args[0]

    def get_board_properties(self):
        return self.dev_path


class ConmuxTarget(FlashableTarget):
    def __init__(self, identifier, name, address, conmux=True, **kwargs):
        FlashableTarget.__init__(self, identifier, name, **kwargs)
        self.address = address  # e.g. le-fw-console/sw-malta-1
        self.conmux_connection = None
        self.conmux = conmux

    def init_target(self, boring_logs=True):
        try:
            logger.debug("{0}: Initializing malta board".format(self.short_id))
            if self.conmux and not self.conmux_connection:
                self._conmux_connect()
            super(ConmuxTarget, self).init_target(boring_logs)
        except ConmuxError as e:
            logger.info("{0}: Error while initializing: {1}".format(self.address, e.message))
            self.status = "Conmux Error"

    def _conmux_connect(self):
        from pexpect.exceptions import TIMEOUT
        import pexpect

        output_line = ""
        try:
            while True:
                self.conmux_connection = pexpect.spawn('conmux', [self.address])
                self.conmux_connection.expect("\n", timeout=30)
                output_line = self.conmux_connection.before.lower()
                print output_line
                if "connected to" in output_line:
                    logger.debug("{0}: Conmux connection with {1} established correctly".format(self.short_id, self.name))
                    break
                elif "entry not found" in output_line:
                    self._conmux_disconnect()
                    raise ConmuxError("Board was not found by conmux.")
                elif "is being used by" in output_line:
                    self._conmux_disconnect()
                    raise ConmuxError("Board is used by {0}".format(output_line.split()[-1]))
        except TIMEOUT:
            self._conmux_disconnect()
            logger.debug("{0}: Timeout while flashing, last conmux output: {1}".format(self.short_id, output_line))
            raise ConmuxError("Time out while connecting to board with conmux.")
        except pexpect.ExceptionPexpect as e:
            self._conmux_disconnect()
            raise ConmuxError(e.message)

    def _conmux_disconnect(self):
        try:
            if self.conmux_connection is not None:
                self.conmux_connection.sendline("~$ quit")
                self.conmux_connection.close()
        except Exception as e:
            logger.debug("{0}: Error while disconnecting conmux connection: {1}".format(self.short_id, e))
            self.conmux_connection = None

    def _restart_conmux(self):
        self._conmux_disconnect()
        self._conmux_connect()

    def _reflash(self, bitstream_name):
        if self.conmux_connection is None:
            self._conmux_connect()
        self.conmux_connection.sendline("~$ flash {0}".format(bitstream_name))

        output_line = ""
        from pexpect.exceptions import TIMEOUT
        try:
            while True:
                self.conmux_connection.expect("\n", timeout=500)
                output_line = self.conmux_connection.before.lower()
                print output_line
                if "failed" in output_line or "error" in output_line:
                    logger.info("{0}: Error while flashing: {1}".format(self.short_id, output_line))
                    self._restart_conmux()
                    raise FlashingError(output_line)
                elif "device or resource busy" in output_line:
                    self._restart_conmux()
                    raise ConmuxError("Conmux returned message that device is busy, try again.")
                elif "flashing in progress" in output_line:
                    logger.info("{0}: Flashing in progress".format(self.short_id))
                elif "success" in output_line:
                    break
        except TIMEOUT:
            logger.debug("{0}: Timeout while flashing, last conmux output: {1}".format(self.short_id, output_line))
            self._restart_conmux()
            raise FlashingError("Timeout while flashing")

    def change_properties(self, *args):
        if len(args) != 1:
            raise ValueError("Wrong number of properties. Needs only address.")
        self.address = args[0]

    def get_board_properties(self):
        return self.address


class BostonTarget(FlashableTarget):
    def __init__(self, identifier, name, hostname, user, password, reflash_func=None, **kwargs):
        FlashableTarget.__init__(self, identifier, name, **kwargs)
        self.hostname = hostname
        self.user = user
        self.password = password
        self.reflash_func = reflash_func or self._ssh_reflash

    def change_properties(self, *args):
        if len(args) != 3:
            raise ValueError("Wrong number of properties. Needs only hostname, username and password.")
        self.hostname, self.user, self.password = args

    def get_board_properties(self):
        return self.hostname, self.user, self.password

    def __repr__(self):
        return "{0}@{1} (password:'{2}')".format(self.user, self.hostname, self.password)

    def _reflash(self, bitstream_file_path):
        self.reflash_func(bitstream_file_path)

    def _ssh_reflash(self, bitstream_file_path):
        ssh = paramiko.SSHClient()
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            logger.info('Trying to connect to {0}'.format(self))
            ssh.connect(self.hostname, 
                        username=self.user, 
                        password=self.password, 
                        # This means it won't use Pageant on Windows. Doing that gives an error 'lost ssh-agent'
                        allow_agent=False
                        )
        except Exception as e:
            msg = "Could not connect to boston board {0} connected to '{1}': {2}".format(self, self.identifier, e)
            logger.error(msg)
            raise FlashingError(msg)

        logger.info('Successfully connected to {0}, copying bitfile...'.format(self))
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(bitstream_file_path, os.path.join("/home/user/Boston/Acquirer", basename(bitstream_file_path)))
        logger.info('Copied bitfile for {0}, reflashing...'.format(self))

        try:
            bitfile_path = os.path.join("/home/user/Boston/Acquirer", basename(bitstream_file_path))
            self._exec_command(ssh, "flashing", "boston flash \"{0}\"".format(bitfile_path))
            self._exec_command(ssh, "fpga_prog", "fpga_prog")
        except SSHException as e:
            FlashingError("SSH error when flashing {0}: {1}".format(self.identifier, str(e)))

    def _exec_command(self, ssh, cmd_name, cmd):
        path = ''.join([
                "PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
                ":/home/user/.local/bin:/home/user/bin:"
                "/opt/Xilinx/14.4/LabTools/LabTools/bin/lin:"
                "/opt/Xilinx/Vivado/2014.4/bin/:"
                "/home/user/Boston"
        ])
        logger.info("{}: {}".format(self.short_id, ' '.join([path, cmd])))
        stdin, stdout, stderr = ssh.exec_command(' '.join([path, cmd]))

        out, err = stdout.readlines(), stderr.readlines()
        if out:
            logger.debug("Stdout while {} {}: \n{}".format(cmd_name, self.short_id, "".join(out)))
        if err:
            logger.debug("Stderr: {}".format("".join(err)))
            raise FlashingError("{}: Error while {}: {}".format(self.identifier, cmd_name, "".join(err)))


def filter_targets(properties, targets, internal_code_names):
    result = [t for t in targets if t.matches_properties(properties)]

    if result:
        return result
    else:
        all_properties = _get_all_properties(targets, internal_code_names)
        wrong_props = [p for p, v in [split_property_and_val(p) for p in properties] if p not in all_properties]

        if len(wrong_props) == 0:
            property_or_ies = "property" if len(properties) == 1 else "properties"
            raise TargetNotFound("There is no target with {0}: {1}".format(property_or_ies, ', '.join(properties)))
        elif len(wrong_props) == 1:
            msg = "None of the targets have the property " + wrong_props[0]
        else:
            msg = "None of the targets have the properties " + ', '.join(wrong_props)

        matches = [m for p in wrong_props for m in get_close_matches(p, all_properties + CLIENT_FUNCTIONS)]
        matches = sorted(set(matches))
        if matches:
            msg += ". Did you mean {0}?".format(natural_join(matches, "or"))

        raise TargetNotFound(msg)


def _get_all_properties(targets, internal_code_names):
    '''get a list of unique properties of the targets, target names and cpu_names'''
    all_props = ["name", "probe_type"]
    for t in targets:
        all_props.extend(t.properties.keys())
        all_props.extend(internal_code_names)
        all_props.append(t.name)
        all_props.append(t.identifier.type)
        for p in ["cpu_name", "display_name"]:
            try:
                all_props.append(t.properties[p])
            except KeyError:
                pass
    return sorted(set(all_props))


def _get_owner_from_error_message(message):
    """
        >>> _get_owner_from_error_message("The device is already in use : Connection Refused.  In use by Acquirer@lesoft-tester")
        'acquirer@lesoft-tester'
        >>> _get_owner_from_error_message("The device is already in use : Connection Refused.  In use by")
        Traceback (most recent call last):
         ...
        AttributeError: Was not able to get probe owner name from error message.
    """
    try:
        return re.search(r"In use by (\S+)", message).group(1).lower()
    except AttributeError:
        raise AttributeError("Was not able to get probe owner name from error message.")


def _remove_prefix_from_domain(owner):
    """
        >>> _remove_prefix_from_domain("Mateusz.Stankiewicz@dt-M-Stankiewicz.le.imgtec.org")
        'Mateusz.Stankiewicz@dt-M-Stankiewicz'
        >>> _remove_prefix_from_domain("Mateusz.Stankiewicz@dt-M-Stankiewicz")
        'Mateusz.Stankiewicz@dt-M-Stankiewicz'
    """
    try:
        return re.search(".+@[^.]*", owner).group(0)
    except (IndexError, AttributeError):
        return owner


def check_if_properties_are_correct(properties, identifier):
    for p, v in properties.iteritems():
        if p is None or v is None:
            logger.warning("{0} has an empty property: {1} = {2}".format(identifier, p, v))
    return dict((p, v) for p, v in properties.iteritems() if p is not None and v is not None)


def get_properties_to_show(properties, verbose, weights):
    if verbose:
        props = sorted(properties.iteritems())
    else:
        props = _get_main_properties(properties, weights)
    return ', '.join([_format_property_to_show(p) for p in props])


def _get_main_properties(properties, weights):
    def by_weight(property):
        return -weights.get(property, 0)

    sorted_props = sorted(properties.iteritems(), key=by_weight)
    return sorted_props[:3]


def _format_property_to_show(p):
    if p[0] in ["cpu_name", "display_name"]:
        return str(p[1])
    if isinstance(p[1], bool) and p[1]:
        return p[0]
    return '{0}={1}'.format(p[0], p[1])


def _get_callers():
    c = inspect.currentframe()
    callers = inspect.getouterframes(c, 2)
    return ", ".join(c[3] for c in callers[2:-1])


def check_if_matches_properties(props, desired_props):
    for key_to_lower in ["cpu_name", "display_name", "name", "probe_type"]:
        desired_props = [e.lower() if e.startswith(key_to_lower) else e for e in desired_props]
        try:
            props[key_to_lower] = props[key_to_lower].lower()
        except KeyError:
            pass

    for expr in desired_props:
        if not _expr_matches(expr, props):
            return False
    return True


def evaluate_expression(expr, values):
    globals = {'__builtins__': {'True': True, 'False': False}}
    return eval(expr, globals, values)


def _expr_matches(expr, props):
    """
    >>> p = {"has_cpu": True, "name": "WPJ344"}
    >>> _expr_matches("123", p), _expr_matches("has_cpu", p), _expr_matches("name=='WPJ344'", p)
    (False, True, True)
    """
    try:
        res = evaluate_expression(expr, props)
        return res and str(res) != expr
    except (NameError, SyntaxError):
        return False


def split_property_and_val(prop):
    """
    >>> split_property_and_val("has_cpu==True")
    ('has_cpu', True)
    >>> split_property_and_val("has_cpu")
    ('has_cpu', True)
    >>> split_property_and_val("num_tc!=123")
    ('num_tc', 123)
    >>> split_property_and_val("name<=sp123")
    ('name', 'sp123')
    """
    m = re.match(r"([^=<!>]*)[=<!>\'\"]+([^=<!>\'\"]*)", prop)
    if m:
        prop, val = m.groups()
        return prop, fix_type(val)
    return prop, True


def fix_type(v, fix_ints=True):
    """
    >>> fix_type("11"), fix_type("abc"), fix_type("False"),
    (11, 'abc', False)
    >>> fix_type("11", False)
    '11'
    """
    if v == "True" or v == "False":
        return eval(v)
    elif fix_ints:
        try:
            return int(v)
        except ValueError:
            pass
    return v


def fix_types(properties, fix_ints=True):
    return dict((p, fix_type(v, fix_ints)) for p, v in properties.iteritems())


def natural_join(items, conjuction='and', oxford_comma=True):
    '''Return list of items joined in a natural language style.

    >>> natural_join(['Jack', 'John'])
    'Jack and John'
    >>> natural_join(['Jack', 'John', 'Jill'], 'and')
    'Jack, John, and Jill'
    >>> natural_join(['Jack', 'John', 'Jill'], 'or')
    'Jack, John, or Jill'
    >>> natural_join(['Jack', 'John', 'Jill'], 'or', False)
    'Jack, John or Jill'
    >>> natural_join(['Jack'], 'or')
    'Jack'
    >>> natural_join([], 'or')
    ''
    '''
    if len(items) == 0:
        return ""
    elif len(items) == 1:
        return items[0]
    else:
        res = ", ".join(items[:-1])
        res += ", " if oxford_comma and len(items) > 2 else " "
        return res + conjuction + " " + items[-1]
