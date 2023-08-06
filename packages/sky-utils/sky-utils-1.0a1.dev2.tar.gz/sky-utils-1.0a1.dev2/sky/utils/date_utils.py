import datetime

import pytz

__author__ = 'muhammet@macit.org'


class DateService():
    pass


class TzAwareDateService():
    UTC = 'UTC'
    TIMEZONE_TURKIYE = 'Europe/Istanbul'
    OLDEST_TIME = datetime.datetime.fromtimestamp(0, tz=pytz.utc)
    FORMAT_ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

    @staticmethod
    def current_time():
        """
        :return: python datetime object for current time in utc timezone, this method adds tzinfo standart dt.dt.now()
        """
        return datetime.datetime.now(tz=pytz.utc)

    @staticmethod
    def oldest_time():
        """
        :return: python datetime object for the earliest computer time as known as timestamp=0 in utc timezone
        """
        return TzAwareDateService.OLDEST_TIME

    @staticmethod
    def tz_utc():
        """
        :return: tzinfo in UTC
        """
        return pytz.utc

    @staticmethod
    def tz_tr():
        """
        :return: tzinfo for Turkiye within DST if available
        """
        return pytz.timezone(TzAwareDateService.TIMEZONE_TURKIYE)

    @staticmethod
    def tz(zone_info):
        """
        :param zone_info: any zone representation
        :return: tzinfo for given zone info
        """
        return pytz.timezone(zone_info)

    @staticmethod
    def parse(date_str, date_format, zone_info=pytz.utc, wanted_zone=None):
        """
        This method overrides timezone info with given zone_info
        :param date_str: string representation of date
        :param date_format: string expression of date format
        :param zone_info: used to replace existing zone info (default utc)
        :return: python datetime object assumed in given zone
        """
        date = datetime.datetime.strptime(date_str, date_format)
        dt = zone_info.localize(date)
        if wanted_zone:
            return dt.astimezone(wanted_zone)
        return dt

    @staticmethod
    def serialize(date_object):
        """
        :param date_object: python datetime object
        :return:
        """
        return date_object.isoformat()

    @staticmethod
    def localize(date, zone_info=UTC):
        if date.tzinfo:
            return date.astimezone(TzAwareDateService.tz(zone_info))
        return TzAwareDateService.tz(zone_info).localize(date)
