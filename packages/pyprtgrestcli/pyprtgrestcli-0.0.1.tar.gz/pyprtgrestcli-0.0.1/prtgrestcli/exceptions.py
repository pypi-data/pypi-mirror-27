# -*- coding: utf-8 -*-

"""
PRTG Exceptions
"""


class PrtgException(Exception):
    """
    Base PRTG Exception
    """
    pass


class PrtgBadRequest(PrtgException):
    """
    Bad request
    """
    pass


class PrtgBadTarget(PrtgException):
    """
    Invalid target
    """
    pass


class PrtgUnknownResponse(PrtgException):
    """
    Unknown response
    """
    pass

class PrtgTooManyChannelsInSensorData(PrtgException):
    """
    Too many channels in sensor data
    """
    pass

class PrtgUnsupportedHTTPMethod(PrtgException):
    """
    UnsupportedHTTPMethod
    """
    pass
