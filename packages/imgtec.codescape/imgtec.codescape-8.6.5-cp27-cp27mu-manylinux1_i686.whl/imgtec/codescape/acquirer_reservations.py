from abc import ABCMeta
import datetime
import pickle
import logging
from imgtec.codescape.acquirer import *
from threading import RLock

logger = logging.getLogger("Acquirer")

DEFAULT_RES_TIME = 8  # in hours
MINUTES_BEFORE_END_TO_SEND_EMAIL = 30


def get_actual_time():
    return datetime.datetime.now().replace(second=0, microsecond=0)


class ReservationFactory(object):
    def __init__(self, get_actual_time, id_generator):
        self.get_actual_time = get_actual_time
        self.id_generator = id_generator

    def new(self, daily, *args, **kwargs):
        res_id = self.id_generator.get_next_id()
        cls = DailyReservation if daily else DisposableReservation
        return cls(res_id, self.get_actual_time(), *args, **kwargs)


class Reservation(object):
    __metaclass__ = ABCMeta

    def __init__(self, id, user=None, target_id=None, bitstream_to_flash=None, desired_properties=None, acquire_new=False, force=False):
        self.id = id
        self.target_id = target_id
        self.user = user
        self.bitstream_to_flash = bitstream_to_flash
        self.desired_properties = desired_properties
        self.acquire_new = acquire_new
        self.force = force
        self.time_to_specified = True

    def _check_need_time(self, need_time_in_minutes):
        if self.bitstream_to_flash and need_time_in_minutes < MAX_FLASHING_TIME / 60:
            raise ValueError("Reservation time must be at least {0} minutes long if you want to flash the target.".format(MAX_FLASHING_TIME / 60))
        elif need_time_in_minutes < 2:
            raise ValueError("Reservation time must be at least 2 minutes long.")

    @property
    def short_time_from(self):
        return format_time(self.time_from)

    @property
    def short_time_to(self):
        return format_time(self.time_to)

    def details(self):
        return [str(self.target_id), _remove_prefix_from_domain(self.user), self.id, self.long_time_from,
                self.long_time_to]

    def matches_user(self, user):
        return self.user.lower().startswith(user.lower())

    def is_broken(self):
        return not (self.id and self._time_from and self._time_to and self.id and self.user)

    def all_details(self):
        return "ID {0}, target_id {1}, time {2} - {3}, user {4}, bitstream to flash: {5}, desired_properties: {6}, expired: {7}" \
            .format(self.id, str(self.target_id), self.short_time_from, self.short_time_to, self.user,
                    self.bitstream_to_flash,  self.desired_properties, self.expired)


class DailyReservation(Reservation):
    def __init__(self, id, actual_time, user=None, time_from=None, time_to=None, need_time=None, *args, **kwargs):
        if not time_from:
            raise ValueError("You need to specify booking start time.")
        if not time_to and not need_time:
            raise ValueError("You need to specify booking end time or how much time you need.")
        Reservation.__init__(self, id, user, *args, **kwargs)
        need_time = _parse_need_time(need_time)
        self._canceled = False
        self._time_from = parse_time(time_from)
        if time_to:
            self._time_to = parse_time(time_to)
        else:
            self._time_to = self._time_from + datetime.timedelta(minutes=need_time)

        need_time = times_diff(self._time_from, self._time_to)
        self._check_need_time(need_time)
        self._end_time_if_changed = None

    def __str__(self):
        return "from {0} to {1}".format(format_time(self.time_from), format_time(self.time_to))

    def change_end_time(self, time_to):
        if isinstance(time_to, datetime.datetime):
            time_to = time_to.time()
        if isinstance(time_to, datetime.time):
            time_to = str(time_to)[:-3]

        new_end_time = parse_time(time_to)
        need_time = times_diff(self._time_from, new_end_time)
        self._check_need_time(need_time)
        self._end_time_if_changed = new_end_time

    @property
    def long_time_from(self):
        return "Everyday " + format_time(self._time_from)

    @property
    def long_time_to(self):
        return "Everyday " + format_time(self._time_to)

    def cancel(self, _):
        self._canceled = True

    def expire(self, _):
        self._end_time_if_changed = None  # cant be expired, only canceled

    def is_expired(self):
        return self._canceled

    def is_going_to_end(self, actual_time):
        return (actual_time + datetime.timedelta(minutes=MINUTES_BEFORE_END_TO_SEND_EMAIL)).time() == self.time_to

    def is_going_to_start_soon(self, actual_time):
        return (actual_time + datetime.timedelta(minutes=MINUTES_BEFORE_END_TO_SEND_EMAIL * 2)).time() >= self.time_from

    def is_its_time(self, actual_time):
        if self.time_from < self.time_to:
            return self.time_from <= actual_time.time() <= self.time_to
        else:
            return self.time_from <= actual_time.time() or actual_time.time() <= self.time_to

    def is_gone(self, _):
        return False

    @property
    def time_from(self):
        return self._time_from

    @property
    def time_to(self):
        return self._end_time_if_changed or self._time_to

    def should_end_now(self, actual_time):
        return self.time_to == actual_time.time()

    def should_start_now(self, actual_time):
        return self.time_from == actual_time.time()

    def get_datetime_from(self, actual_time):
        time_from = actual_time.replace(hour=self._time_from.hour, minute=self._time_from.minute)
        if time_from < actual_time:
            time_from += datetime.timedelta(days=1)
        return time_from

    def ends_before(self, bound):
        bound_as_time = bound if isinstance(bound, datetime.time) else bound.time()
        if self.time_from < self.time_to:
            return self.time_to < bound_as_time or bound_as_time < self.time_from
        else:
            return self.time_to < bound_as_time < self.time_from


class DisposableReservation(Reservation):
    def __init__(self, id, actual_time, user=None, time_from=None, time_to=None, need_time=None, *args, **kwargs):
        Reservation.__init__(self, id, user, *args, **kwargs)
        need_time = _parse_need_time(need_time)
        self._expired = False

        if time_from:
            self._time_from = _parse_datetime_from(time_from, actual_time)
        else:
            self._time_from = actual_time

        if time_to:
            self._time_to = _parse_datetime_to(self._time_from, time_to)
        else:
            self._time_to = self._time_from + datetime.timedelta(minutes=(need_time or DEFAULT_RES_TIME * 60))
            if not need_time:
                self.time_to_specified = False

        need_time = self._time_to - self._time_from
        need_time = need_time.total_seconds() / 60
        self._check_need_time(need_time)

    def __str__(self):
        return "from {0} to {1}".format(self.short_time_from, self.short_time_to)

    def change_end_time(self, time_to):
        if time_to is None:
            self._time_to = self._time_from + datetime.timedelta(hours=DEFAULT_RES_TIME)
        else:
            time_to = _time_or_datetime_to_str(time_to)
            time_to = _parse_datetime_to(self._time_from, time_to)
            self._time_to = time_to
        self.time_to_specified = False

    @property
    def long_time_from(self):
        return format_date_and_time(self._time_from)

    @property
    def long_time_to(self):
        return format_date_and_time(self._time_to)

    def cancel(self, end_time):
        self.expire(end_time)

    def expire(self, end_time):
        self._time_to = end_time
        self._expired = True

    @property
    def time_from(self):
        return self._time_from.time()

    @property
    def time_to(self):
        return self._time_to.time()

    def is_expired(self):
        return self._expired

    def is_going_to_end(self, actual_time):
        return actual_time + datetime.timedelta(minutes=MINUTES_BEFORE_END_TO_SEND_EMAIL) == self._time_to

    def is_going_to_start_soon(self, actual_time):
        return actual_time + datetime.timedelta(minutes=MINUTES_BEFORE_END_TO_SEND_EMAIL * 2) >= self._time_from

    def is_its_time(self, actual_time):
        return self._time_from <= actual_time <= self._time_to

    def is_gone(self, actual_time):
        return self._time_to < actual_time

    def should_end_now(self, actual_time):
        return self._time_to == actual_time

    def should_start_now(self, actual_time):
        return self._time_from == actual_time

    def get_datetime_from(self, _):
        return self._time_from

    def ends_before(self, bound):
        bound = _time_or_datetime_to_str(bound)
        bound = _parse_datetime_to(self._time_from, bound)
        return self._time_to < bound


def _parse_need_time(input):
    """
    >>> _parse_need_time("1w"), _parse_need_time("2D"), _parse_need_time("3h")
    (10080, 2880, 180)
    >>> _parse_need_time("2m"), _parse_need_time("2"), _parse_need_time(2)
    (2, 2, 2)
    """
    try:
        return int(input) if input else input
    except ValueError:
        m = re.match("(\d+)\s?(\w?)", input)
        if m:
            value, unit = m.groups()
            value, unit = int(value), unit.lower()
            if unit == "w":
                return value * 7 * 24 * 60
            elif unit == "d":
                return value * 24 * 60
            elif unit == "h":
                return value * 60
            elif unit == "m" or unit == "":
                return value
            raise ValueError("Wrong time unit: {0}. Allowed ones are w(weeks), d(days), h(hours), m(minutes).".format(unit))
    raise ValueError("Wrong time format. You need to pass value and unit ie. 2h (two hours).")


def _time_or_datetime_to_str(t):
    if isinstance(t, datetime.time) or isinstance(t, datetime.datetime):
        return str(t)[:-3]
    return t


def _parse_datetime_from(time_from, actual_time):
    time_from = _string_to_datetime(time_from)
    if time_from.year == 1900:
        time_from = actual_time.replace(hour=time_from.hour, minute=time_from.minute)
    if time_from < actual_time:
        raise ValueError("You cannot reserve a date in the past.")
    return time_from


def time_to_today_datetime(time_to, actual_time):
    if time_to:
        return _parse_datetime_to(actual_time, time_to)
    return actual_time + datetime.timedelta(hours=DEFAULT_RES_TIME)


def _parse_datetime_to(time_from, time_to):
    time_to = _string_to_datetime(time_to)
    if time_to.year == 1900:
        time_to = time_from.replace(hour=time_to.hour, minute=time_to.minute)
        if time_to <= time_from:  # treat as next day
            time_to += datetime.timedelta(days=1)
    if time_to < time_from:
        raise ValueError("End time cannot be before start time.")
    return time_to


def parse_time(str_to_parse):
    res = _string_to_datetime(str_to_parse, with_date=False)
    return datetime.time(res.hour, res.minute)


def check_if_reservation_overlap(reservations, new):
    for res in reservations:
        if are_reservations_overlaping(res, new):
            owner = res.user if new.user != res.user else "you"
            raise ProbeBooked("Probe is reserved during this time period by {0} (from {1} to {2})".format(owner, res.long_time_from, res.long_time_to))


def are_reservations_overlaping(res1, res2):
    if isinstance(res1, DisposableReservation) and isinstance(res2, DisposableReservation):
        return _are_times_or_dates_overlaping(res1._time_from, res1._time_to, res2._time_from, res2._time_to)
    else:
        return _are_times_or_dates_overlaping(res1.time_from, res1.time_to, res2.time_from, res2.time_to)


def _are_times_or_dates_overlaping(from1, to1, from2, to2):
    latest_start = max(from1, from2)
    earliest_end = min(to1, to2)
    return latest_start < earliest_end


def find_reservation_during(reservations, time):
    for res in reservations:
        if res.time_from <= time < res.time_to:
            return res
    raise NoReservationsFound


def cut_reservation_if_need(res, reservations, messages=None):
    if not res.time_to_specified:
        timedelta_to_next_res = datetime.timedelta.max
        for r in reservations:
            if isinstance(r, DailyReservation) or r._time_from > res._time_from:
                timedelta_to_next_res = min(time_between(res, r), timedelta_to_next_res)
        if (timedelta_to_next_res.total_seconds() / 60) < DEFAULT_RES_TIME * 60:
            res._time_to = res._time_from + timedelta_to_next_res
            if messages is not None:
                messages.append("Reservation end time was set to {0}".format(res.short_time_to))


def time_between(res, next):
    if isinstance(next, DailyReservation):
        return datetime.timedelta(minutes=times_diff(res.time_from, next.time_from))
    else:
        return next._time_from - res._time_from


def format_time(time):
    return time.strftime("%H:%M") if time else "None"


def format_date_and_time(date):
    return date.strftime("%d.%m.%y %H:%M")


def is_reservation_need_to_be_cut(desired, next_time_from):
    return desired.time_from <= next_time_from < desired.time_to


def _string_to_datetime(time, with_date=True):
    formats = ["%H:%M", "%H"]
    if with_date:
        formats.append("%Y-%m-%d %H:%M")
    for fmt in formats:
        try:
            return datetime.datetime.strptime(time, fmt).replace(second=0, microsecond=0)
        except ValueError:
            pass
    raise ValueError("Time and/or date must be in format HH or HH:MM or YYYY-MM-DD HH:MM.")


reservations_lock = RLock()


class ReservationPickler(object):
    def __init__(self, filename):
        self.filename = filename

    def add_reservation(self, res):
        try:
            with reservations_lock:
                with open(self.filename, "ab") as f:
                    pickle.dump(res, f)
        except (IOError, OSError) as e:
            logger.info("Was trying to add {0} ({1}) reservation but {2}".format(res.id, res.target_id, str(e)))

    def update_reservation(self, res):
        logger.debug("Marking {0} reservation as expired".format(res.id))
        with reservations_lock:
            reservations = self.read_reservations()
            reservations = [res if r.id == res.id else r for r in reservations]
            with open(self.filename, "wb") as f:
                for r in reservations:
                    pickle.dump(r, f)

    def read_reservations(self):
        results = []
        errors_found = False
        try:
            with reservations_lock:
                with open(self.filename, 'rb') as fp:
                    try:
                        while True:
                            data = pickle.load(fp)
                            try:
                                if data and not data.is_broken():
                                    results.append(data)
                                else:
                                    errors_found = True
                                    logger.error("Found an error in reservations file: {0}" .format(data.all_details()))
                            except AttributeError:
                                errors_found = True
                                logger.error("Found an error in reservations file: {0}".format(data))
                    except EOFError:
                        pass
                if errors_found:
                    with open(self.filename, "wb") as f:
                        [pickle.dump(r, f) for r in results]
        except (IOError, OSError) as e:
            logger.info("Was trying to read reservations but {0}".format(e))
        return results


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


def sort_reservations(reservations, actual_time):
    def sorting_key(res):
        return res.get_datetime_from(actual_time)

    return sorted(reservations, key=sorting_key)


def times_diff(earlier, later):
    """
    >>> a = datetime.time(hour=23, minute=44)
    >>> b = datetime.time(hour=01, minute=10)
    >>> times_diff(a, b)
    86
    >>> times_diff(b, a)
    1354
    """
    delta = 60 * (later.hour - earlier.hour) + (later.minute - earlier.minute)
    if earlier > later:
        delta += 24*60
    return delta

