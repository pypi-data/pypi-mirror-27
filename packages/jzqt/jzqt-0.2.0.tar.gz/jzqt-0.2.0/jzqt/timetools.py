# coding: utf-8
"""Date and time tools"""

from calendar import isleap
from datetime import date, datetime, timedelta

DAY = timedelta(1)
HOUR = timedelta(hours=1)
WEEK = timedelta(weeks=1)
SECOND = timedelta(seconds=1)
MINUTE = timedelta(minutes=1)
MICROSECOND = timedelta(microseconds=1)
MILLISECOND = timedelta(milliseconds=1)
ZERO_TIMEDELTA = timedelta()


class timerange(object):
    """Time range object, like ``range``

    timerange(start, stop[, step]) -> timerange object

    >>> from datetime import date, datetime
    >>> list(timerange(datetime(1970, 1, 1), datetime(1970, 1, 3)))
    [datetime.datetime(1970, 1, 1, 0, 0), datetime.datetime(1970, 1, 2, 0, 0)]
    >>> list(timerange(date(2017, 12, 31), date(2018, 1, 2)))
    [datetime.date(2017, 12, 31), datetime.date(2018, 1, 1)]
    >>> len(timerange(datetime(1970, 1, 1, 1), datetime(1970, 1, 1, 3), HOUR))
    2
    """

    def __init__(self, start, stop, step=None):
        for idx, arg in ((1, start), (2, stop)):
            if not isinstance(arg, (date, datetime)):
                raise TypeError('timerange() arg {} must be date '
                                'or datetime object'.format(idx))
        if step is None:
            step = timedelta(1)
        if not isinstance(step, timedelta):
            raise TypeError('timerange() arg 3 must be timedelta object')
        if step == ZERO_TIMEDELTA:
            raise ValueError('timerange() arg 3 must not be timedelta(0)')
        self._start = start
        self._stop = stop
        self._step = step
        # compute length
        if step > ZERO_TIMEDELTA and start > stop:
            self._length = 0
        elif step < ZERO_TIMEDELTA and start < stop:
            self._length = 0
        else:
            delta_length = int((self._stop - self._start).total_seconds() * 1000000)
            step_length = int(self._step.total_seconds() * 1000000)
            self._length = int(delta_length / step_length)
            if delta_length % step_length != 0:
                self._length += 1

    def __str__(self):
        return "timerange(start={}, stop={}, step={})".format(
            repr(self._start), repr(self._stop), repr(self._step)
        )

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return bool(self._length)

    def __len__(self):
        return self._length

    def __iter__(self):
        curr = self._start
        step = self._step
        stop = self._stop

        def should_iterate():
            if step > timedelta():
                return curr < stop
            return curr > stop

        while should_iterate():
            yield curr
            try:
                curr += step
            except OverflowError:
                break

    def __eq__(self, other):
        if not isinstance(other, timerange):
            return False
        if self._start != other.start:
            return False
        if self._stop != other.stop:
            return False
        if self._step != other.step:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return (self._start, self._stop, self._step).__hash__()

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    @property
    def step(self):
        return self._step


def prev_month_first_day(dt=None):
    """Return last month first day.

    >>> from datetime import datetime, date
    >>> print(prev_month_first_day(datetime(1970, 1, 1, 11, 11)))
    1969-12-01 11:11:00
    >>> print(prev_month_first_day(date(1970, 8, 9)))
    1970-07-01
    """
    dt = dt or datetime.now()
    if dt.month == 1:
        return dt.replace(year=dt.year - 1, month=12, day=1)
    return dt.replace(month=dt.month - 1, day=1)


def prev_month_last_day(dt=None):
    """Return last month last day.

    >>> from datetime import datetime, date
    >>> print(prev_month_last_day(datetime(2017, 1, 31, 1, 1)))
    2016-12-31 01:01:00
    >>> print(prev_month_last_day(date(1900, 3, 23)))
    1900-02-28
    """
    dt = dt or datetime.now()
    if dt.month == 1:
        return this_month_last_day(dt.replace(year=dt.year - 1, month=12))
    return this_month_last_day(dt.replace(month=dt.month - 1, day=1))


def this_month_first_day(dt=None):
    """Return this month first day.

    >>> from datetime import datetime, date
    >>> print(this_month_first_day(datetime(2222, 12, 31, 11, 22, 33)))
    2222-12-01 11:22:33
    >>> print(this_month_first_day(date(1970, 1, 1)))
    1970-01-01
    """
    dt = dt or datetime.now()
    return dt.replace(day=1)


def this_month_last_day(dt=None):
    """Return this month last day.

    >>> from datetime import datetime, date
    >>> print(this_month_last_day(datetime(2000, 2, 9, 3)))
    2000-02-29 03:00:00
    >>> print(this_month_last_day(date(1999, 8, 3)))
    1999-08-31
    """
    dt = dt or datetime.now()
    if dt.month in {1, 3, 5, 7, 8, 10, 12}:
        return dt.replace(day=31)
    if dt.month != 2:
        return dt.replace(day=30)
    if isleap(dt.year):
        return dt.replace(day=29)
    return dt.replace(day=28)


def next_month_first_day(dt=None):
    """Return next month first day.

    >>> from datetime import datetime, date
    >>> print(next_month_first_day(datetime(1999, 12, 9, 3)))
    2000-01-01 03:00:00
    >>> print(next_month_first_day(date(1999, 7, 3)))
    1999-08-01
    """
    dt = dt or datetime.now()
    if dt.month == 12:
        return dt.replace(year=dt.year + 1, month=1, day=1)
    return dt.replace(month=dt.month + 1, day=1)


def next_month_last_day(dt=None):
    """Return next month last day.

    >>> from datetime import datetime, date
    >>> print(next_month_last_day(datetime(1999, 12, 9, 3)))
    2000-01-31 03:00:00
    >>> print(next_month_last_day(date(1999, 1, 3)))
    1999-02-28
    """
    dt = dt or datetime.now()
    if dt.month == 12:
        return this_month_last_day(dt.replace(year=dt.year + 1, month=1))
    return this_month_last_day(dt.replace(month=dt.month + 1, day=1))
