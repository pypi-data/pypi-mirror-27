import unittest
import datetime
import pytz

from sky.utils.date import TzAwareDateService as tzdutil

__author__ = 'muhammet@macit.org'


class TestTzAwareDateService(unittest.TestCase):
    def test__current_time(self):
        dt = tzdutil.current_time()
        self.assertEqual(dt.tzinfo, pytz.utc, "datetime zone missmatch")

    def test__oldest_time(self):
        dt = tzdutil.oldest_time()
        dt2 = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        self.assertEqual(dt.tzinfo, pytz.utc, "datetime zone missmatch")
        self.assertEqual(dt, dt2, "datetime value missmatch")

    def test__utc(self):
        utc = tzdutil.tz_utc()
        self.assertEqual(utc._tzname, tzdutil.UTC)
        self.assertEqual(utc._utcoffset, datetime.timedelta(seconds=0))

    def test__tr(self):
        tz_tr = tzdutil.tz_tr()
        self.assertEqual(tz_tr, pytz.timezone(tzdutil.TIMEZONE_TURKIYE), "timezone missmatch")
        # non dst date
        # non_dst = datetime.datetime(2015, 1, 1, tzinfo=tz_tr)
        # dst = datetime.datetime(2015, 6, 1, tzinfo=tz_tr)
        # self.assertEqual(non_dst, pytz.timezone("+02:00"), "datetime zone missmatch")
        # self.assertEqual(dst.tzinfo, pytz.timezone("+03:00"), "datetime zone missmatch")

    def test__tz(self):
        self.assertEqual(tzdutil.tz_tr(), tzdutil.tz(tzdutil.TIMEZONE_TURKIYE))
        self.assertEqual(tzdutil.tz_utc(), tzdutil.tz(tzdutil.UTC))

    def test__parse(self):
        date_str = "2015-09-30T21:13:34.116Z"
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        date_in_iso_format = "2015-09-30T21:13:34.116000+00:00"
        dt = tzdutil.parse(date_str, date_format)
        self.assertIsNotNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), date_in_iso_format)

    def test__serialize(self):
        self.test__parse()
