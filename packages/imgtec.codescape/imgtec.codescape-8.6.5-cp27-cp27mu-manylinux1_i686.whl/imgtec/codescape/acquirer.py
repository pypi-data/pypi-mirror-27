"""
To acquire a probe specify either a probe identifier, or target properties e.g::

    acquirer acquire sp22

When there are many properties the target that satisfies the largest number of
them will be assigned::

    acquirer acquire has_fpu has_vze==False
    acquirer acquire name=='WPJ344' probe_type=='sp'
    acquirer acquire endian=='big'

When you are done with the target you should release it (without passing a probe identifier
will release all targets assigned to you.) ::

    acquirer release sp22

To force disconnect someone::

    acquirer release -f sp22

To see all targets managed by a server::

    acquirer list

To get list with all cpuinfos (not only three most desired properties)::

    acquirer list --verbose

To get list of the bitstreams and flash the target::

    acquirer list --bitstreams
    acquirer flash sp192 SN1234567

"""
import re
import os
import socket
import sys
import xmlrpclib
import time
import types
from argparse import RawDescriptionHelpFormatter, ArgumentParser
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from imgtec.codescape.probe_identifier import Identifier
from imgtec.console.results import get_console_width
from imgtec.lib.cacert import get_cacert_file
from imgtec.lib.rst import simple_table
from inspect import getargspec
from os.path import basename
from textwrap import fill
from urllib2 import urlopen, HTTPError, URLError
from imgtec.console.results import test_console_width

CLIENT_CONF_FILE = "acquirer_server_details.ini"

VERSION = "1.28"

SERVER_HOST = "LE-ACQUIRER"
SERVER_PORT = "8000"
SERVER_NAME = "acquirer@" + SERVER_HOST
SERVER_CFG_SECTION = "Server"
MAX_FLASHING_TIME = 1200  # 20 min
MAX_BITSTREAM_DOWNLOAD_TIME = 600


class NoReservationsFound(Exception):
    pass


class WrongVersionError(Exception):
    pass


class ServerConnectionError(Exception):
    pass


class ServerException(Exception):
    pass


class AcquiringError(Exception):
    pass


class ProbeBooked(Exception):
    pass


class ProbeBeingUsed(Exception):
    pass


class TargetNotFound(Exception):
    pass


class ProbeOffline(Exception):
    pass


class ProbeError(Exception):
    pass


class NoTargetException(Exception):
    pass


class TargetExistsError(Exception):
    pass


class DeviceNotFoundError(Exception):
    pass


class ConfigFileError(Exception):
    pass


class FlashingError(Exception):
    pass


class FirmwareNotFound(Exception):
    pass


class FirmwareNotMatching(Exception):
    pass


class TargetAlreadyFree(Exception):
    pass


class NoTargetFlashed(Exception):
    pass


class FlashableBoardNotFound(Exception):
    pass


class ConmuxError(Exception):
    pass


class NoRFCServerFound(Exception):
    pass


def _get_owner():
    for name in ('USER', 'LOGNAME', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return '{0}@{1}'.format(user.lower(), socket.getfqdn().lower())
    raise EnvironmentError("Failed to detect user name.")


def get_user_files_dir(*tail):
    root = os.environ.get('IMGTEC_USER_HOME', os.path.join('~', 'imgtec'))
    return os.path.expanduser(os.path.join(root, *tail))


def _split_id_and_kwargs(args):
    '''
        >>> _split_id_and_kwargs(["has_fpu==1", "num_cores>3"])
        (None, ['has_fpu==1', 'num_cores>3'])
        >>> _split_id_and_kwargs(["sp22"])
        ('SysProbe 22', None)
        >>> _split_id_and_kwargs(["SysProbe 22"])
        ('SysProbe 22', None)
    '''
    if not args:
        raise AttributeError("You haven't specified any parameters of the probe")
    try:
        id = get_id(args[0])
        if len(args) == 1:
            return id, None
        else:
            raise AttributeError("You cannot pass id with other parameters.")
    except ValueError:
        return None, args


def api_function(func):
    ''' Decorator for api functions that sets server if not specified and takes care of xmlrpclib faults.'''
    def wrapped(*args, **kwargs):
        try:
            for i, a in enumerate(args):
                kwargs[getargspec(func).args[i]] = a

            srv = kwargs.get("server", None)
            if not isinstance(srv, types.NoneType):
                check_server_version(srv)
                return func(**kwargs)
            else:
                kwargs["server"] = get_server()
                check_server_version(kwargs["server"])
            return func(**kwargs)

            #all_args = getcallargs(func, *args, **kwargs)  # python 2.7
            #if isinstance(all_args["server"], types.NoneType):
            #    all_args["server"] = get_server()
            #check_server_version(all_args["server"])
            #return func(**all_args)

        except xmlrpclib.Fault as e:
            exc, msg = _get_type_and_msg_from_xmlrpclib_exc(e)
            raise exc(msg)
        except xmlrpclib.ProtocolError as e:
            raise ServerConnectionError(e.errmsg)
    return wrapped


@api_function
def _acquire(owner, parameters, bitstream, start_time, end_time, printing, need_time, new_target, force, daily, server):
    owner = owner or _get_owner()
    id, kwargs = _split_id_and_kwargs(parameters) if not bitstream or parameters else (None, None)

    queue_id = server.server_acquire(owner, id, kwargs, bitstream, start_time, end_time, need_time, new_target, force, daily)
    elapsed = 0
    while elapsed < MAX_FLASHING_TIME:
        val = server.server_get_queue_value(queue_id)
        if val is None:
            time.sleep(0.01)
            elapsed += 0.01
        elif isinstance(val, basestring):
            if printing:
                print val
        else:
            return val
    raise Exception("Server get some problem and your query get timed out")


def acquire(properties_or_id, owner=None, time_from=None, time_to=None, need_time=None, new_target=False, force=False, daily=False, server=None):
    ''' Assigns a probe to a user.

    `properties_or_id` can be an id of a probe or list or properties e.g.
        ["endian==big"]
        ["has_fpu", "has_vze==False", "num_cores<3"]
        ["probe_type==sp", "name!='WPJ344'"]
        ["74Kc"]

    `owner` is user id that tries to acquire.

    `time_from` and `time_to` are start and end time if target is going to be booked in certain period of time ie:
        "12:32" or "14"
    If `time_to` is not passed, target will be booked for 8 hours.
    `need_time` is booking time in minutes and can be passed instead of `time_to` to specify reservation end time
    in minutes. If `time_from` is specified then will acquire a target from this time for this amount of time.

    If server will find matching target which is already assigned to the user then will extend its reservation
    time for next 8 hours and return its identifier. To acquire any new target instead of this,
    argument `new_target` has to be True.

    The probe cannot be used by others until it has been released. It can be done by the same user
    or someone else using `release` with "-f" flag.
    '''
    if not isinstance(properties_or_id, list):
        properties_or_id = [properties_or_id]
    target_id, msg, res_id = _acquire(owner, properties_or_id, None, time_from, time_to, False, need_time, new_target, force, daily, server)
    return target_id, res_id, msg


def acquire_bitstream(bitstream, owner=None, id=None, time_from=None, time_to=None, need_time=None, new_target=False, force=False, daily=False, server=None):
    ''' Acquires a probe and flashes with specified bitstream.

    `id` specifies which board will be flashed. If it is no specified then server will try to find free board to flash by itself.
    Raises exception when there is no free board or when there is no requested bitstream file.

    `owner` is user id that tries to acquire.
    `time_from` and `time_to` are start and end time if target is going to be booked in certain period of time ie:
        "12:32" or "14"
    If `time_to` is not passed, target will be booked for 8 hours.
    `need_time` is booking time in minutes and can be passed instead of `time_to` to specify reservation end time
    in minutes. If `time_from` is specified then will acquire a target from this time for this amount of time.

     If server will find matching target which is already assigned to the user then will extend its reservation
    time for next 8 hours and return its identifier. To acquire any new target instead of this,
    argument `new_target` has to be True.

    The probe cannot be used by others until it has been released. It can be done by the same user
    or someone else using `release` with "-f" flag.
    '''
    return _acquire(owner, [id] if id else None, bitstream, time_from, time_to, False, need_time, new_target, force, daily, server)


@api_function
def release(owner=None, id=None, server=None):
    '''
    Releases a probe owned by the current user, returning it to the pool.

    If the id is not specified then will release all the targets assigned to user.
    '''
    server.server_release(owner or _get_owner(), get_id(id) if id else None)


@api_function
def force_disconnect(id, server=None):
    '''
    Releases a probe specified by `id` from user.
    '''
    if not id:
        raise AttributeError("You need to specify which probe you want to force disconnect.")
    server.server_force_disconnect(get_id(id))


class WrappedTable(list):
    def __init__(self, titles, targets, column_to_wrap):
        super(WrappedTable, self).__init__(targets)
        self.titles = titles
        self.col_to_wrap = column_to_wrap

    def __repr__(self):
        max_line_length, max_line_len_without_wrapped_col = self._get_max_lengths()

        if max_line_length > get_console_width():
            new_len_of_wrapped_col = get_console_width() - max_line_len_without_wrapped_col

            if new_len_of_wrapped_col > 8:
                for line in self:
                    line[self.col_to_wrap] = fill(line[self.col_to_wrap], new_len_of_wrapped_col)
        return simple_table(self.titles, self)

    def _get_max_lengths(self):
        max_lengths = [max(len(str(x)) for x in line) for line in zip(*self + [self.titles])]

        max_line_length = sum(max_lengths) + len(max_lengths)

        max_line_len_without_wrapped_col = max_line_length - max_lengths[self.col_to_wrap]

        return max_line_length, max_line_len_without_wrapped_col


class VerboseTable(list):
    """
    >>> input = ("SysProbe 22", "Available", "WPJ3444", "cpuinfo here")
    >>> with test_console_width(35):
    ...     VerboseTable([input, input])
    SysProbe 22	 Available  WPJ3444
    <BLANKLINE>
    cpuinfo here
    <BLANKLINE>
    ===================================
    SysProbe 22	 Available  WPJ3444
    <BLANKLINE>
    cpuinfo here
    <BLANKLINE>
    ===================================
    """
    def __repr__(self):
        res = []
        for target in self:
            res.append("  ".join(target[:-1]))
            if target[-1]:
                res.append("")
                res.append(target[-1])
            res.append("")
            res.append("=" * get_console_width())
        return "\n".join(res)


TARGET_INFO_TITLES = ['Identifier', 'Name', 'Status', 'Cpuinfo']
BITSTREAM_INFO_TITLES = ["Board type", "Bitstream", "Cpuinfo config"]
@api_function
def list_of_targets(verbose=False, bitstreams=False, properties=None, server=None):
    '''
    List all targets with information about status and its most valuable properties.
    When `verbose` is true then will show full cpuinfo, not only three main properties.
    When `bitstreams` is true will show list of available bitstreams to flash (sorted by board type).
    `Properties` is a list of cpu_info properties that user would like filter the targets.
    List shows each target status, that tells if it is used by someone, free, offline or broken.
    '''
    if bitstreams:
        if verbose:
            return VerboseTable(server.server_bitstreams(True, properties))
        return WrappedTable(BITSTREAM_INFO_TITLES, server.server_bitstreams(False, properties), 1)
    else:
        if verbose:
            return VerboseTable(server.server_list(True, properties))
        return WrappedTable(TARGET_INFO_TITLES, server.server_list(False, properties), -1)


class ReservationsList(list):
    def __init__(self, titles, reservations):
        super(ReservationsList, self).__init__(reservations)
        self.titles = titles

    def del_col(self, n):
        self.titles.pop(n)
        [row.pop(n) for row in self]

    def __repr__(self):
        return simple_table(self.titles, self)


@api_function
def reservations(user=None, old=False, identifier=None, server=None):
    '''
    Returns ReservationsList object that contains all actual reservations.
    If `user` is specified then will show all reservations belonging to that user.
    If `identifier` is specified then will show all reservations of a target with this id.
    If `old` is true then will show also reservations that have already expired.
    Each element in list contains target identifier, reservation id, start and end time of reservation.
    Raises NoReservationsFound if nothing found.
    '''
    if old:
        reservations = server.server_old_reservations(identifier, user)
    else:
        reservations = server.server_reservations(identifier, user)

    header = ["Target", "User", "Id", "From", "To"]
    result = ReservationsList(header, reservations)
    if user:
        result.del_col(1)
    if identifier:
        result.del_col(0)
    return result


@api_function
def add_target(id, name, boardparams=None, server=None):
    '''
    Adds new target to the list of targets.

    Requires `Id` and `name` of the target like e.g. "sp22" and "WPJ344".
    Target must be online to be added.
    '''
    server.server_add_target(get_id(id), name, boardparams)


@api_function
def remove_target(id, server=None):
    '''
    Removes target from server list of targets but do not disconnect if someone is already using it.
    May return a message if target was not found or that it is in use and will be deleted after releasing.
    '''
    return server.server_remove_target(get_id(id))


@api_function
def remove_bitstream(name, server=None):
    '''
    Removes a bitstream file from the server. Cannot be removed if someone is already flashing a board with it.
    '''
    if name:
        server.server_remove_bitstream(name)


@api_function
def cancel_reservation(id, user=None, server=None):
    '''
    Cancels target booking. `Id` is an id of reservation to cancel.
    Does not throw any exception if the reservation with specified `id` does not exist.
    Does not delete reservations that have already gone.
    `User` is a reservation owner. It is not allowed to cancel a reservation that belongs to someone else.
    '''
    server.server_cancel_reservation(id, user or _get_owner())


@api_function
def change_name(id, new_name, server=None):
    '''
    Change name of the target when something else is connected to the probe.
    All the bookings and connections remain unchanged.
    '''
    server.server_change_name(get_id(id), new_name)


@api_function
def change_properties(id, new_props, server=None):
    '''
    Change target properties like username and password for boston board or dev path for malta/sead.
    '''
    return server.server_change_properties(get_id(id), new_props)


@api_function
def change_actual_reservation_end_time(id, time_to=None, server=None):
    '''
    Change end time of actual reservation. Time cannot be bigger that 8 hours ahead.
    Target `id` needs to be specified if there is more that one assigned to the user.
    `time_to` is a new end time e.g. 13, 13:20. If an end time is not specified then 8 hours will be passed by default.
    '''
    return server.server_change_actual_res_end_time(_get_owner(), get_id(id) if id else None, time_to)


@api_function
def change_logger_level(level, server=None):
    """ Change logging level to error, warning, info or debug."""
    return server.server_change_logger_level(level)


@api_function
def get_target_status(id, server=None):
    return server.server_target_status(id)


@api_function
def upload(filename, board_type, conmux=False, overwrite=False, server=None):
    '''
    Uploads a sead or boston bitstream file to the server.
    For conmux bitstreams tells server that there is new bitstream to add it to the servers pool of bitstreams.
    '''
    if conmux:
        server.save_new_bitstream(filename, board_type)
    else:
        file_size = os.stat(filename).st_size
        user = _get_owner()
        hostname, port = server.server_upload(basename(filename), file_size, board_type, user, overwrite)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Connected to {0} on port {1}.".format(hostname, port)
        s.connect((hostname, port))
        try:
            with open(filename, 'rb') as f:
                print 'Uploading...'
                l = f.read(2048)
                while l:
                    s.send(l)
                    l = f.read(2048)
            print "Bitstream uploaded."
        finally:
            s.close()


@api_function
def add_bitstream_from_url(url, board_type, custom_filename=None, overwrite=False, printing=False, server=None):
    queue_id = server.server_add_bitstream_from_url(url, board_type, custom_filename, overwrite)
    return _get_value_from_queue(server, queue_id, MAX_BITSTREAM_DOWNLOAD_TIME, printing)


def _get_value_from_queue(server, queue_id, max_time, printing):
    elapsed = 0
    while elapsed < max_time:
        val = server.server_get_queue_value(queue_id)
        if val is None:
            time.sleep(0.01)
            elapsed += 0.01
        elif isinstance(val, basestring):
            if printing:
                print val
        elif isinstance(val, Exception):
            raise val
        else:
            return "Done!"
    raise Exception("Server had some problem and your query timed out.")


@api_function
def refresh(server=None):
    '''
    Checks if targets which were offline are now available.
    '''
    server.server_refresh()


@api_function
def flash_board(identifier, bitstream, owner=None, printing=False, server=None):
    '''
    Flash a board with selected bitstream.
    `Bitstream` can be a name ie. "sead3_XC5VLX110_sisi_SN1234567",
    name with extension ie. "sead3_XC5VLX110_sisi_SN1234567.fl"
    or just serial number ie. "SN1234567"
    '''
    owner = owner or _get_owner()
    queue_id = server.server_flash_board(get_id(identifier), bitstream, owner)
    return _get_value_from_queue(server, queue_id, MAX_FLASHING_TIME, printing)


def client_acquire(args):
    target_id, msg, res_id = _acquire(args.owner, args.parameters, args.bitstream, args.start_time,
                                      args.end_time, True, args.need_time, args.new, args.force, args.daily, args.server)
    if msg:
        print msg
    if res_id:
        print "Your reservation id is {0}.".format(res_id)
    return target_id


def client_release(args):
    if args.force is True:
        force_disconnect(args.identifier, args.server)
    else:
        release(None, args.identifier, args.server)


def client_refresh(args):
    refresh(args.server)


def client_target_status(args):
    return get_target_status(args.identifier, args.server)


def client_flash(args):
    return flash_board(args.identifier, args.bitstream, None, True, args.server)


def client_add_target(args):
    add_target(args.identifier, args.name, args.boardparams, args.server)


def client_remove(args):
    try:
        id = get_id(args.identifier)
        return remove_target(id, args.server)
    except ValueError:
        remove_bitstream(args.identifier, args.server)


def client_cancel(args):
    cancel_reservation(args.identifier, None, args.server)


def client_upload(args):
    if is_url(args.filename):
        add_bitstream_from_url(args.filename, args.board_type, None, args.overwrite, True, args.server)
    else:
        upload(args.filename, args.board_type, args.conmux, args.overwrite, args.server)


def client_list(args):
    return list_of_targets(args.verbose, args.bitstreams, args.properties, args.server)


def client_change_name(args):
    change_name(args.identifier, args.new_name, args.server)


def client_change_properties(args):
    return change_properties(args.identifier, args.new_properties, args.server)


def change_end_time(args):
    return change_actual_reservation_end_time(args.identifier, args.end_time, args.server)


def client_reservations(args):
    try:
        id = None
        user = None if args.all or args.old else _get_owner()
        if args.target:
            try:
                id = get_id(args.target)
            except ValueError:
                user = args.target

        return reservations(user, args.old, id, args.server)
    except NoReservationsFound as e:
        return e.message


def client_logger(args):
    return change_logger_level(args.level)


def get_id(custom_id):
    return str(Identifier(custom_id))


def is_url(url):
    try:
        urlopen(url, cafile=get_cacert_file())
        return True
    except HTTPError:
        return True
    except (ValueError, URLError):
        return False


class ArgumentParserWithFormattedHelp(ArgumentParser):
    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, formatter_class=RawDescriptionHelpFormatter, **kwargs)


CLIENT_FUNCTIONS = "release acquire list reservations add remove cancel server upload flash refresh change_end_time change_name change_properties".split()


def _create_argparser():
    argparser = ArgumentParser(description="Target sharing management utility", epilog=__doc__,
                               formatter_class=RawDescriptionHelpFormatter)
    subparsers = argparser.add_subparsers(parser_class=ArgumentParserWithFormattedHelp)

    acq_pars = subparsers.add_parser("acquire", help="assigns a probe to a user. The probe cannot be used by others "
                                                     "until it has been released. The target can be specified by "
                                                     "probe identifier, target name or requirement expressions "
                                                     "like 'has_fpu', 'prid==1'. The target can be booked for a time "
                                                     "in the future by specifying a concrete start time",
                                     epilog=acquire_epilog)
    acq_pars.set_defaults(func=client_acquire)
    acq_pars.add_argument('parameters', nargs='*', help="Probe identifier, target name or other requirement expressions (see examples).")
    acq_pars.add_argument('--start-time', '-s', help="Reserve target from specified time e.g. 12, 12:20. A day other than today can be "
                               "specified using YYYY-MM-DD format e.g. 2016-08-11 12:30")
    acq_pars.add_argument('--end-time', '-e', help="Reserve target until specified time e.g. 12, 12:20. A day other than today can be "
                               "specified using YYYY-MM-DD format e.g. 2016-08-11 12:30. If an end time is not specified "
                               "then 8 hours will be passed by default.")
    acq_pars.add_argument('--need-time', '-t', type=str, default=None, help="Reservation time as 2m(2 minutes), 2h(2 hours), 2d or 2w. Can be used instead of start/end time.")
    acq_pars.add_argument('--bitstream', '-b', type=str, default=None, help="Acquire concrete bitstream e.g. mediatek_FPGA1_SN651C18_rebuild.fl")
    acq_pars.add_argument('--owner', '-o', type=str, default=None, help="Acquire for someone else. Needs to be specified username with a domain ie. sam.partington@dt-s-partington.mips.com")
    acq_pars.add_argument('--new',   '-n', action="store_true",    help="Acquire any new target instead of extending the actually assigned target reservation.")
    acq_pars.add_argument('--force', '-f', action="store_true",    help="Force disconnect a probe from its current user.")
    acq_pars.add_argument('--daily', '-d', action="store_true",    help="Book for every day at the specified time.")

    rel_pars = subparsers.add_parser("release", help="Release a probe owned by the current user, returning it to the pool.", epilog=release_epilog)
    rel_pars.set_defaults(func=client_release)
    rel_pars.add_argument('identifier', nargs='?', help="Probe identifier to be released.")
    rel_pars.add_argument("--force", "-f", action="store_true",
                          help="Force disconnect a probe from its current user")

    list_pars = subparsers.add_parser("list", epilog=list_epilog, help="List all targets with information about status and properties.")
    list_pars.add_argument('properties', nargs='*', help="Properties that targets will be filtered with.")
    list_pars.add_argument("--verbose", "-v", action="store_true", help="Show full cpuinfo.")
    list_pars.add_argument("--bitstreams", "-b", action="store_true", help="Show list of available bitstreams.")
    list_pars.set_defaults(func=client_list)

    res_pars = subparsers.add_parser("reservations", epilog=reservations_epilog,
                                     help="List user reservations or concrete target reservations if identifier is specified.",)
    res_pars.add_argument('target', nargs='?', default=None, help="Probe identifier or user name for which reservations will be shown.")
    res_pars.add_argument('--old', action="store_true", help="Show expired reservations.")
    res_pars.add_argument('--all', action="store_true", help="Show everybody's reservations.")
    res_pars.set_defaults(func=client_reservations)

    add_pars = subparsers.add_parser("add", help="Add new target to the list of targets. Identifier and name must "
                                                 "be specified.", epilog=add_epilog)
    add_pars.set_defaults(func=client_add_target)
    add_pars.add_argument('identifier', help='Identifier of the new target.')
    add_pars.add_argument('name', help='Name of the new target.')
    add_pars.add_argument('boardparams', nargs="*", help=r'''For sead boards device path eg. /dev/usb/lp0 or \\.\COM1.
                               For boston boards hostname, username and password.
                               For malta boards connected by conmux address e.g. le-fw-console/sw-malta-1 or device path
                               e.g. /dev/usb/lp1 if connected directly to the server.''')

    rem_pars = subparsers.add_parser("remove", epilog=remove_epilog, help="Remove a target from list of targets or bitstream from the server.")
    rem_pars.set_defaults(func=client_remove)
    rem_pars.add_argument('identifier', help='Identifier of the target to remove or name/SN of a bitstream.')

    can_pars = subparsers.add_parser("cancel", help="Cancels reservation.")
    can_pars.set_defaults(func=client_cancel)
    can_pars.add_argument('identifier', help='Identifier of the reservation to cancel.')

    srv_pars = subparsers.add_parser("server", help="Set server details.", epilog=server_epilog)
    srv_pars.add_argument('server_address', nargs='?',
                          help="Server address in a form host:port, eg. lesoft-tester:8000")
    srv_pars.add_argument("--restart", action="store_true", help="Restart the server.")
    srv_pars.add_argument("--close", action="store_true", help="Turn off the server.")
    srv_pars.set_defaults(func=set_server)

    upl_pars = subparsers.add_parser("upload", help="Upload a sead or boston bitstream file. Malta bitstreams have to "
                                                    "be copied manually and acquire needs to be told that a new one "
                                                    "has been uploaded.", epilog=upload_epilog)
    upl_pars.add_argument('filename', help="Filename of a bitstream file or url")
    upl_pars.add_argument('board_type', help="Board that a bitstream file is for. e.g. sead3-LX110")
    upl_pars.add_argument('--conmux', action="store_true", help="Mark this as a conmux bitstream, which is already uploaded, but needs to be added to the pool of bitstreams.")
    upl_pars.add_argument('--overwrite', '-o', action="store_true", help="Overwrite file if already exists on the server.")
    upl_pars.set_defaults(func=client_upload)

    ref_pars = subparsers.add_parser("refresh", help="Checks if targets which were offline are now available. Normally this is done automatically every minute.")
    ref_pars.set_defaults(func=client_refresh)

    fls_pars = subparsers.add_parser("flash", help="Flashes a board with a selected bitstream.")
    fls_pars.set_defaults(func=client_flash)
    fls_pars.add_argument('identifier', help="Probe identifier that will be flashed.")
    fls_pars.add_argument('bitstream', help="Name of the bitstream e.g. mediatek_FPGA1_SN651C18_rebuild.fl or serial "
                                            "number for conmux bitstreams e.g. SN01234AB")

    end_pars = subparsers.add_parser("change-end-time", help="Change actual reservation end time.")
    end_pars.set_defaults(func=change_end_time)
    end_pars.add_argument('identifier', default=None, help="Probe identifier that its reservation will be changed. It needs to be specified if there is more that one target assigned.")
    end_pars.add_argument('end_time', default=None, help="New end time e.g. 13, 13:20. If an end time is not specified then 8 hours will be passed by default.")

    chn_pars = subparsers.add_parser("change-name", help="Change name of the target when something else is connected to the probe.")
    chn_pars.set_defaults(func=client_change_name)
    chn_pars.add_argument('identifier', help="Probe identifier that will be renamed.")
    chn_pars.add_argument('new_name', help="New name of the target e.g. WPJ344.")

    chn_pars = subparsers.add_parser("change_properties", help="Change name of the target when something else is connected to the probe.")
    chn_pars.set_defaults(func=client_change_properties)
    chn_pars.add_argument('identifier', help="Probe identifier that will be renamed.")
    chn_pars.add_argument('new_properties', nargs='?', help=r"""New board properties ie. '/dev/usb/lp0', '\\.\COM1' or 'hostname username password'.""")

    log_pars = subparsers.add_parser("logger", help="Change logging level.")
    log_pars.set_defaults(func=client_logger)
    log_pars.add_argument('level', nargs='?', help="Level to be set: error, warning, info, debug. If not passed then will just print current level")

    stat_pars = subparsers.add_parser("status", help="Get target status.")
    stat_pars.set_defaults(func=client_target_status)
    stat_pars.add_argument('identifier', default=None, help="Probe identifier.")

    argparser.add_argument('--version', action='version', version=str(VERSION))

    return argparser, subparsers


def _check_server_details(server_address):
    srv = get_server(server_address)
    try:
        srv.ping()
    except socket.error:
        raise ServerConnectionError("Server cannot be found at: {0}. You can use `change_details`"
                                    "to change server configuration".format(server_address))


def get_server(server_address=None, use_default=True):
    '''
    Returns xmlrpc server instance that can be passed to api functions.
    If `server_address` is not passed then will try to get server details from config file from user profile directory.
    If `use_default` is True then will use server details hardcoded in the script,
    otherwise will ask a user to provide them.
    '''
    server_address = server_address or _get_server_address(use_default)
    return xmlrpclib.ServerProxy(server_address, allow_none=True)


def _get_server_address(use_default):
    config_filename = get_user_files_dir(CLIENT_CONF_FILE)
    try:
        return _read_server_address_from_config(config_filename)
    except (NoSectionError, NoOptionError):
        if use_default:
            return "http://" + SERVER_HOST + ":" + SERVER_PORT
        else:
            print "Server details have not been found."
            return _create_new_server_config(config_filename)


def _create_new_server_config(config_filename):
    server_address = _ask_for_server_address()
    _check_server_details(server_address)
    save_server_details_to_file(config_filename, server_address)
    return server_address


def save_server_details_to_file(config_filename, srv_addr):
    folder = os.path.dirname(config_filename)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    addr_parts = [srv_addr]
    #If there's no port use the default
    if not re.match('.*:[0-9]+[\/]*', srv_addr):
        addr_parts.extend([':', SERVER_PORT])

    if not srv_addr.startswith("http://"):
        addr_parts.insert(0, "http://")
        
    srv_addr = ''.join(addr_parts)
    #Make sure it exists without overwriting
    with open(config_filename, 'r') as f:
        config_parser = ConfigParser()
        config_parser.read(config_filename)

        if not config_parser.has_section(SERVER_CFG_SECTION):
            config_parser.add_section(SERVER_CFG_SECTION)

        config_parser.set(SERVER_CFG_SECTION, "server_address", srv_addr)
        
    with open(config_filename, 'w') as f:
        config_parser.write(f)

    return srv_addr


def _read_server_address_from_config(config_filename):
    config_parser = ConfigParser()
    config_parser.read(config_filename)
    return config_parser.get(SERVER_CFG_SECTION, "server_address")


def _ask_for_server_address():
    host = raw_input("Please give server host (or press enter for '{0}'): ".format(SERVER_HOST)) or SERVER_HOST
    port = raw_input("Please give server port (or press enter for '{0}'): ".format(SERVER_PORT)) or SERVER_PORT
    return "http://" + host + ":" + port


def check_server_version(server):
    server_ver = server.get_version()
    if str(server_ver) != str(VERSION):
        raise WrongVersionError("Server has version {0} and you have {1}".format(server_ver, VERSION))


def set_server(args):
    if args.server_address:
        config_filename = get_user_files_dir(CLIENT_CONF_FILE)
        server = save_server_details_to_file(config_filename, args.server_address)
        return "Server set to: {0}".format(server)
    elif args.restart:
        return restart_server()
    elif args.close:
        return close_server()
    else:
        return _get_server_address(None)


@api_function
def close_server(server=None):
    '''
    Turns off the server releasing not used probes that were managed by the server and exits with code 3.
    If server_address is not specified then will use address from config file.
    '''
    server.close_server(3)
    return "Server closed."


@api_function
def restart_server(server=None):
    '''
    Restarts the server releasing not used probes that were managed by the server and exits with code 2.
    If server_address is not specified then will use address from config file.
    '''
    server.close_server(2)
    time_elapsed = 0
    while time_elapsed < 10:
        time.sleep(0.5)
        time_elapsed += 0.5
        try:
            if server.ping():
                return "Server restarted properly."
        except socket.error:
            pass
    raise ServerException("Timed out waiting for server to restart, it may have encountered an issue.")


def _is_debug():
    try:
        config_parser = ConfigParser()
        config_parser.read(get_user_files_dir(CLIENT_CONF_FILE))
        return config_parser.get("Debug", "debug").lower() == "true"
    except (NoSectionError, NoOptionError):
        return False


def _get_type_and_msg_from_xmlrpclib_exc(e):
    if e.faultCode == 1:
        m = re.match("<type 'exceptions.(.*)'>:(.*)", e.faultString)
        if m:
            exc_name, exc_msg = m.groups()
            if hasattr(__builtins__, exc_name):
                return getattr(__builtins__, exc_name), exc_msg
        else:
            m = re.match(r"<class '__main__\.(.*)'>:(.*)", e.faultString)
            if m:
                exc_name, exc_msg = m.groups()
                return getattr(sys.modules[__name__], exc_name), exc_msg
    return ServerException, re.sub("<.*>:", "", e.faultString)


def parse_args(args):
    argparser, subparsers = _create_argparser()
    possible_options = subparsers._name_parser_map.keys() + ['-h', '--help', '--version']

    if len(args) and args[0] not in possible_options:
        args.insert(0, "acquire")

    return argparser.parse_args(args)


def _update_if_standalone():
    # check if running standalone script not the acquirer in codescape
    if os.path.realpath(__file__).split(os.sep)[-4:-1] == "imgtec imgtec codescape".split():
        return False
    else:
        import urllib2
        new_version = urllib2.urlopen("http://lesoft-tester:8080/job/Acquirer_setup/lastSuccessfulBuild/artifact/codescape/sw/imgtec/dist/acquirer.py")
        with open(os.path.normpath(sys.argv[0]), "w") as output:
            output.write(new_version.read())
        return True


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ["update", "--update"]:
        if _update_if_standalone():
            print "Updated to the newest version."
            return

    args = parse_args(sys.argv[1:])
    if not _is_debug():
        sys.tracebacklimit = 0

    if args.func == set_server:
        print set_server(args)
    else:
        try:
            args.server = get_server(use_default=False)
            res = args.func(args)
            if res:
                print res
        except xmlrpclib.Fault as e:
            if not _is_debug():
                _, msg = _get_type_and_msg_from_xmlrpclib_exc(e)
                print msg
            else:
                raise
        except socket.error as e:
            raise ServerConnectionError("Couldn't connect to {0} - {1}".format(_get_server_address(False), e))

acquire_epilog = '''
To acquire a probe specify either a probe identifier, or target properties e.g::

    acquirer acquire sp22

Script is acquiring by default so there is no need to add 'acquire' part::

    acquirer sp22

When there are many properties the target that satisfies the largest number of
them will be assigned::

    acquirer acquire has_fpu has_vze==False
    acquirer acquire 74Kc
    acquirer acquire Samurai
    acquirer acquire name=='WPJ344' probe_type=='sp'
    acquirer acquire endian=='big'
    acquirer acquire num_tc>num_vpe
    acquirer acquire display_name==74Kc
    acquirer acquire display_name==cpu_name

Note that there must not be any space between around comparison operator.

Acquirer will look for target with desired properties in pool of real targets and when will not find anything then
will try to find bitstream with these properties and flash it on any available board.

Target can be also acquired with concrete bitstream (by passing whole name or just serial number)::

    acquirer acquire sp71 --bitstream bb_concord_musket_samurai-1Core_1VC_32K-4003500
    acquirer acquire sp71 --bitstream SN1234567

To acquire a target in advance for a period a time there need to be specified start time and/or end time to.
If the end time will not be greater than start time, the server will treat it as tomorrow's time::

    acquirer acquire sp22 -s 12:30 -e 13
    acquirer acquire sp22 -s 13:30 -e 8:10

Other users will not be able to reserve the target if it already reserved by someone else during this time.
If someone is using a target and somebody else booking time is coming then he will get an email
asking to release the target.
Target can be acquired also from concrete time and without specifying how long it will be used::

    acquirer acquire sp22 -s 12

Or can be acquired from now with specifying how long will be used (in minutes)::

    acquirer acquire sp22 --need-time 45
    acquirer acquire sp22 -t 45

Or until what time will be used::

    acquirer acquire sp22 -e 16:00

For example this command will acquire a target from 12:30 to 13:15::

    acquirer acquire sp22 -s 12:30 -t 45

If a target is already booked by someone eg. from 14 to 15 and you want to acquire it now without telling how
long you will by using it, then you will get a message half an hour before end time that you have to release it before 14
and will get disconnected at 14. If target is not booked after you, then you can extend your reservation time::

    acquirer change-end-time 18:00 sp22

Or acquire target again what will add 8h to the reservation end time (or less if target is booked by
someone else within these 8 hours).
To acquire a target with concrete parameters for future:

    acquire mips_32 prid==11 has_vze==False -s 18 -e 23

In that case if server found boston or sead board with these properties and someone else will flash the target
before 18:00 with bitstream that does not match them, then server will try to find other matching target or
find matching bitstream that can be flashed on this probe. If is changed then user gets and email with
identifier of the new assigned target.

To force acquire::

    acquirer acquire sp123 -f -s 22 -e 5
    acquirer acquire mips_32 WPJ344 -f

Target will be force disconnected if anyone is connected and assigned to you.
If the end time is not specified, the reservation time will be 8 hours or will be cut if someone else booked it afterwards.
When end time is specified then all reservations during this time will be canceled.

'''

reservations_epilog = '''
To print out your reservations::

    acquirer reservations

To print out all users actual reservations::

    acquirer reservations --all

If you pass a target id there will be printed all its reservations::

    acquirer reservations sp22 --all

To print out all users reservations that have already expired::

    acquirer reservations --old --all

To print another user's reservations (will accept a partial name)::

    acquirer reservations Mateusz

Every reservation that has not passed yet can be canceled::

    acquirer cancel 11

You need to pass reservation id that you get when acquired.
If you do not remember this number, you can search for this it in a list of reservations.

'''

release_epilog = '''
When you are done with the target you should release it ::

    acquirer release

This will release all targets assigned to you.  To release just one pass the
probe identifier::

    acquirer release sp22

In that event that a target has been unintentionally left in an acquired state
by another user, the force disconnect feature can be used to drop their
acquirement::

    acquirer release -f sp22

Please exercise consideration for the other user.

'''

add_epilog = '''
If there is no preferred target it can be added::

    acquirer add sp22 "WPJ344"

For sead and boston targets there needs to be specified boards connection parameters:
device path for sead and hostname, username and password for boston::

    acquirer add sp71 sead3-LX110 dev/usb/lp0
    acquirer add sp72 boston boston.foo.bar.org user password123
    acquirer add sp73 corefpga6 le-fw-console/sw-malta-1

Target name can be changed later::

    acquirer change-name sp22 Danube

'''

list_epilog = '''
To see all the targets managed by a server::

    acquirer list

To get a list with all cpuinfos (only three most desired properties::

    acquirer list --verbose

To get a list of targets and that match certain properties you can pass names of properties as arguments::

    acquirer list has_cpu has_fpu

Properties will be assumbed to be boolean unless an expression is used. For example::

    acquirer list "name=='wpj344'"

Note the quotes around the expression and the property 'name', which is itself a string.

'''

server_epilog = '''
Host and port of the server can be changed be passing them as host:port::

    acquirer server lesoft-tester:8000

To restart the server::

    acquirer server --restart

To shutdown the server::

    acquirer server --close

'''

remove_epilog = '''
To remove a target from the server::

    acquirer remove sp22

To remove a bitstream::

    acquirer remove SN1234567

'''

upload_epilog = r'''
Bitstream files can be uploaded to the server::

    acquirer upload "C:\Bitstreams\bb_concord_musket_samurai-1Core_1VC_32K-4003500.mcs" boston
    acquirer upload "C:\Bitstreams\mediatek_FPGA1_SN651C18_rebuild.fl" sead-LX155

Conmux bitstreams has to be copied manually and acquirer need to be told that there is new bitstream to get cpuinfo,
otherwise it will not be possible to flash board with this bitstream and it will not be found when
target is acquired by properties::

    acquirer upload "corefpga6-somename-SN1234567" corefpga6 --conmux

'''


if __name__ == '__main__':
    main()
