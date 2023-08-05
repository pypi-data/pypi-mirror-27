"""
Tests for hours of operation utilities
"""
import datetime

import pytz
from pytz import utc

from mock import patch

from pytest import raises

from hoursofoperation import lib


def test_hoursFromConfig():
    """
    Do I transform my input into an object with open/close
    times for every day of the week?
    """
    original = {
        'timezone': 'US/Eastern',
        'default': {
            'open': '8:00 AM',
            'close': '6:00 PM'
        },
        'sat': {
            'open': '10:00 AM',
            'close': '4:00 PM'
        },
        'sun': {
            'close': '12:00 AM'
        }
    }
    expected = {
        'open': [
            'fri 8:00 AM',
            'mon 8:00 AM',
            'sat 10:00 AM',
            'thu 8:00 AM',
            'tue 8:00 AM',
            'wed 8:00 AM'
        ],
        'close': [
            'fri 6:00 PM',
            'mon 6:00 PM',
            'sat 4:00 PM',
            'sun 12:00 AM',
            'thu 6:00 PM',
            'tue 6:00 PM',
            'wed 6:00 PM'
        ],
        'default': {
            'close': '6:00 PM', 
            'open': '8:00 AM'
        },
    }

    assert lib.hoursFromConfig(original) == expected


def test_hoursFromConfigOpenAfterClose():
    """
    Do I raise an exception if an open time is after a close time?
    """
    hours = {
        'timezone': 'US/Eastern',
        'default': {
            'open': '8:00 PM',
            'close': '6:00 PM'
        }
    }
    raises(lib.HoursError, lib.hoursFromConfig, hours)


def test_hoursFromConfigMissingDay():
    """
    Do I raise an exception if any days were not specified?
    """
    hours = {
        'timezone': 'US/Eastern',
        'mon': {
            'open': '8:00 AM',
            'close': '6:00 PM'
        }
    }
    raises(lib.HoursError, lib.hoursFromConfig, hours)


def test_hoursDatetime():
    """
    Do I return the open and close time for today?
    """
    # the medical group is in US/Eastern
    hours = {
        'default': {
            'open': '9:00','close': '5:00'
        },
        'open': ['mon 9:00 AM', 'tue 9:00 AM', 'wed 9:00 AM', 'thu 9:00 AM', 'fri 9:00 AM', 'sat 9:00 AM', 'sun 9:00 AM'],
        'close':['mon 5:00 PM', 'tue 5:00 PM', 'wed 5:00 PM', 'thu 5:00 PM', 'fri 5:00 PM', 'sat 5:00 PM', 'sun 5:00 PM']
    }

    # patching datetime.datetime.now() because parseDate uses it
    class mockDateTime(datetime.datetime):
        @classmethod
        def now(self):
            return datetime.datetime(year=2016, month=9, day=1, hour=16, tzinfo=None)

    # Currently, it is 4:00 PM UTC (during clinic opening hours)
    # In UTC, opening hours are 9/1 from 1:00 PM to 9:00 PM
    fakeDate = datetime.datetime(year=2016, month=9, day=1, hour=16, tzinfo=utc).astimezone(pytz.timezone('US/Eastern'))
    putcnowTZ = patch.object(lib, 'utcnowTZ', return_value=fakeDate, autospec=True)
    pNow = patch.object(datetime, 'datetime', mockDateTime)
    with pNow, putcnowTZ:
        expectedResult = {'open': datetime.datetime(year=2016, month=9, day=1, hour=13, minute=0, tzinfo=utc),
                          'close': datetime.datetime(year=2016, month=9, day=1, hour=21, minute=0, tzinfo=utc)
                         }
        result = lib.hoursDatetime(hours, 'US/Eastern')
        assert result == expectedResult

    # Currently, it is 11:00 AM UTC (before clinic opening hours)
    # In UTC, opening hours are 9/1 from 1:00 PM to 9:00 PM
    fakeDate = datetime.datetime(year=2016, month=9, day=1, hour=11, tzinfo=utc)
    putcnowTZ = patch.object(lib, 'utcnowTZ', return_value=fakeDate, autospec=True)
    pNow = patch.object(datetime, 'datetime', mockDateTime)
    with pNow, putcnowTZ:
        expectedResult = {'open': datetime.datetime(year=2016, month=9, day=1, hour=13, minute=0, tzinfo=utc),
                          'close': datetime.datetime(year=2016, month=9, day=1, hour=21, minute=0, tzinfo=utc)
                         }
        result = lib.hoursDatetime(hours, 'US/Eastern')
        assert result == expectedResult

    # Currently, it is 10:00 PM UTC, or 12:00 P.M US/Eastern (after clinic opening hours)
    # In UTC, opening hours are 9/1 from 1:00 PM to 9:00 PM
    fakeDate = datetime.datetime(year=2016, month=9, day=1, hour=22, tzinfo=utc)
    putcnowTZ = patch.object(lib, 'utcnowTZ', return_value=fakeDate, autospec=True)
    pNow = patch.object(datetime, 'datetime', mockDateTime)
    with pNow, putcnowTZ:
        expectedResult = {'open': datetime.datetime(year=2016, month=9, day=1, hour=13, minute=0, tzinfo=utc),
                          'close': datetime.datetime(year=2016, month=9, day=1, hour=21, minute=0, tzinfo=utc)
                         }
        result = lib.hoursDatetime(hours, 'US/Eastern')
        assert result == expectedResult


def test_hoursOfOperation():
    """
    Do I return the expected hours of operation?
    """
    # pretend we are currently located in China(CST) = China Standard Time
    # China does not observe daylight saving time, so this test theoretically won't break for that reason
    central = pytz.timezone('Asia/Shanghai')
    pLocalTZ = patch.object(lib, 'tzlocal', return_value=central, autospec=True)

    tz = 'US/Samoa'
    hours = {
        'default': {
            'open': '9:00',
            'close': '15:00'
        },
        'close': ['sat 15:30', 'mon 15:00', 'tue 15:00', 'wed 15:00', 'thu 15:00', 'fri 15:00', 'sun 15:00'],
        'open': ['sat 9:00', 'mon 9:00', 'tue 9:00', 'wed 9:00', 'thu 9:00', 'fri 9:00', 'sun 9:00']
    }

    # patching datetime.datetime.now() because parseDate uses it
    class mockDateTime(datetime.datetime):
        @classmethod
        def now(self):
            return datetime.datetime(year=2016, month=9, day=1, hour=16, tzinfo=None)

    fakeToday = datetime.datetime(year=2016, month=9, day=1, hour=16, tzinfo=utc)
    putcnowTZ = patch.object(lib, 'utcnowTZ', return_value=fakeToday, autospec=True)
    pNow = patch.object(datetime, 'datetime', mockDateTime)
    with putcnowTZ, pLocalTZ, pNow:
        # Thu, Samoa hours are 9/1 from 9:00 AM - 3:00 PM --> Shanghai hours are 9/2 from 4:00 AM - 10:00 AM
        # Currently, it is 9/2/2016 at 12:00 AM in Shanghai
        # In Shanghai we expect these hours of operation
        expected = {'close': 'Friday 10:00 AM CST',
                    'open': 'Friday 04:00 AM CST',
                    'nextOpen': None,
                    'openLater': True,
                    'currentlyClosed': True}
        assert lib.hoursOfOperation(hours, tz) == expected

    fakeToday = datetime.datetime(year=2016, month=9, day=2, hour=4, tzinfo=utc)
    putcnowTZ = patch.object(lib, 'utcnowTZ', return_value=fakeToday, autospec=True)
    pNow = patch.object(datetime, 'datetime', mockDateTime)
    with putcnowTZ, pLocalTZ, pNow:
        # Thu, Samoa hours are 9/1 from 9:00 AM - 3:00 PM --> Shanghai hours are 9/2 from 4:00 AM - 10:00 AM
        # Currently, it is 9/2/2016 at 12:00 PM in Shanghai
        # In Shanghai we expect these hours of operation
        expected = {'close': 'Friday 10:00 AM CST',
                    'open': 'Friday 04:00 AM CST',
                    'nextOpen': 'Saturday 04:00 AM CST',
                    'openLater': False,
                    'currentlyClosed': True}
        assert lib.hoursOfOperation(hours, tz) == expected

    fakeToday = datetime.datetime(year=2016, month=9, day=2, hour=1, tzinfo=utc)
    putcnowTZ = patch.object(lib, 'utcnowTZ', return_value=fakeToday, autospec=True)
    pNow = patch.object(datetime, 'datetime', mockDateTime)
    with pNow, pLocalTZ, putcnowTZ:
        # Thu, Samoa hours are 9/1 from 9:00 AM - 3:00 PM --> Shanghai hours are 9/2 from 4:00 AM - 10:00 AM
        # Currently, it is 9/2/2016 at 9:00 AM in Shanghai
        # In Shanghai we expect these hours of operation
        expected = {'close': 'Friday 10:00 AM CST',
                    'open': 'Friday 04:00 AM CST',
                    'nextOpen': None,
                    'openLater': False,
                    'currentlyClosed': False}
        assert lib.hoursOfOperation(hours, tz) == expected


def test_hoursOfOperationNoHours():
    """
    If no hours are given, do I return the expected hours of operation?
    """
    # pretend that it is currently Thursday 9/1/2016 at 4:00 p.m. UTC
    fakeDate = datetime.datetime(year=2016, month=9, day=1, hour=16, tzinfo=utc)
    timezone = 'US/Samoa'
    hours = {
        'close': [],
        'open': [],
        'default': {}
    }
    with patch.object(lib, 'utcnowTZ', return_value=fakeDate, autospec=True):
        expected = {'close': None,
                    'open': None,
                    'nextOpen': None,
                    'openLater': None,
                    'currentlyClosed': None}
        assert lib.hoursOfOperation(hours, timezone) == expected