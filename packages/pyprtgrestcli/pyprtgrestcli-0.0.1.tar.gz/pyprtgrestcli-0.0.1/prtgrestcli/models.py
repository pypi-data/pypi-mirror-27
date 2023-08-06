# -*- coding: utf-8 -*-
from prtgrestcli.exceptions import PrtgTooManyChannelsInSensorData
from prtgrestcli.exceptions import PrtgUnsupportedHTTPMethod
from prtgrestcli.enums import PrtgUnits
from prtgrestcli.enums import PrtgErrorCodes
from prtgrestcli.enums import PrtgSizes
from prtgrestcli.enums import PrtgSpeedTimes
from prtgrestcli.enums import PrtgModes
from prtgrestcli.enums import PrtgDecimalModes
from xml.dom.minidom import getDOMImplementation
import requests
import json

MAX_RESULTS = 50

class PrtgResult(object):

    def __init__(   self, channel, value = 0):

        if not isinstance(channel, str) or channel == "" : raise ValueError('%%channel%% must be a non null string')
        self._channel = channel

        if not (isinstance(value, int) or isinstance(value, float)): raise ValueError('%%value%% must be an integer or a float')
        self._value = value

        self._unit = None
        self._custom_unit = None
        self._speed_size = None
        self._volume_size = None
        self._speed_time = None
        self._mode = None
        self._float = None
        self._decimal_mode = None
        self._warning = None
        self._show_chart = 1
        self._show_table = 1
        self._limit_max_error = None
        self._limit_max_warning = None
        self._limit_min_error = None
        self._limit_min_warning = None
        self._limit_error_msg = None
        self._limit_warning_msg = None
        self._limit_mode = None
        self._value_lookup = None

    def __str__(self):
        return "{channel}:{value}".format(channel=self._channel, value=self._value)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if not isinstance(value, str): raise ValueError('%%channel%% must be a string')
        self._channel = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not (isinstance(value, int) or isinstance(value, float)): raise ValueError('%%value%% must be an integer or a float')
        self._value = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        if not isinstance(value, PrtgUnits): raise ValueError('%%unit%% must be a Unit valid value')
        self._unit = value

    @property
    def custom_unit(self):
        return self._custom_unit

    @custom_unit.setter
    def custom_unit(self, value):
        if not isinstance(value, str): raise ValueError('%%custom_unit%% must be a string')
        self._custom_unit = value

    @property
    def speed_size(self):
        return self._speed_size

    @speed_size.setter
    def speed_size(self, value):
        if not isinstance(value, PrtgSizes): raise ValueError('%%speed_size%% must be a string')
        self._speed_size = value

    @property
    def volume_size(self):
        return self._volume_size

    @volume_size.setter
    def volume_size(self, value):
        if not isinstance(value, PrtgSizes): raise ValueError('%%volume_size%% must be a string')
        self._volume_size = value

    @property
    def speed_time(self):
        return self._speed_time

    @speed_time.setter
    def speed_time(self, value):
        if not isinstance(value, PrtgSpeedTimes): raise ValueError('%%speed_time%% must be a string')
        self._speed_time = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, PrtgModes): raise ValueError('%%mode%% must be a valid Mode')
        self._mode = value

    @property
    def float(self):
        return self._float

    @float.setter
    def float(self, value):
        if not (value == 0 or value == 1): raise ValueError('%%float%% must be 1 or 0')
        self._float = value

    @property
    def decimal_mode(self):
        return self._decimal_mode

    @decimal_mode.setter
    def decimal_mode(self, value):
        if not isinstance(value, PrtgDecimalModes): raise ValueError('%%decimal_mode%% must be 1 or 0')
        self._decimal_mode = value

    @property
    def warning(self):
        return self._warning

    @warning.setter
    def warning(self, value):
        if not (value == 0 or value == 1): raise ValueError('%%warning%% must be 1 or 0')
        self._warning = value

    @property
    def show_chart(self):
        return self._show_chart

    @show_chart.setter
    def show_chart(self, value):
        if not (value == 0 or value == 1): raise ValueError('%%show_chart%% must be 1 or 0')
        self._show_chart = value

    @property
    def show_table(self):
        return self._show_table

    @show_table.setter
    def show_table(self, value):
        if not (value == 0 or value == 1): raise ValueError('%%show_table%% must be 1 or 0')
        self._show_table = value

    @property
    def limit_max_error(self):
        return self._limit_max_error

    @limit_max_error.setter
    def limit_max_error(self, value):
        if not isinstance(value, int): raise ValueError('%%limit_max_error%% must be 1 or 0')
        self._limit_max_error = value

    @property
    def limit_max_warning(self):
        return self._limit_max_warning

    @limit_max_warning.setter
    def limit_max_warning(self, value):
        if not isinstance(value, int): raise ValueError('%%limit_max_warning%% must be 1 or 0')
        self._limit_max_warning = value

    @property
    def limit_min_error(self):
        return self._limit_min_error

    @limit_min_error.setter
    def limit_min_error(self, value):
        if not isinstance(value, int): raise ValueError('%%limit_min_error%% must be 1 or 0')
        self._limit_min_error = value

    @property
    def limit_min_warning(self):
        return self._limit_min_warning

    @limit_min_warning.setter
    def limit_min_warning(self, value):
        if not isinstance(value, int): raise ValueError('%%limit_min_warning%% must be 1 or 0')
        self._limit_min_warning = value

    @property
    def limit_error_msg(self):
        return self._limit_error_msg

    @limit_error_msg.setter
    def limit_error_msg(self, value):
        if not isinstance(value, str): raise ValueError('%%limit_error_msg%% must be a string')
        self._limit_error_msg = value

    @property
    def limit_warning_msg(self):
        return self._limit_warning_msg

    @limit_warning_msg.setter
    def limit_warning_msg(self, value):
        if not isinstance(value, str): raise ValueError('%%limit_warning_msg%% must be a string')
        self._limit_warning_msg = value

    @property
    def limit_mode(self):
        return self._limit_mode

    @limit_mode.setter
    def limit_mode(self, value):
        if not (value == 0 or value == 1): raise ValueError('%%limit_mode%% must be 1 or 0')
        self._limit_mode = value


    @property
    def value_lookup(self):
        return self._value_lookup

    @value_lookup.setter
    def value_lookup(self, value):
        if not isinstance(value, str): raise ValueError('%%value_lookup%% must be a string')
        self._value_lookup = value

class PrtgHTTPPushDataAdvancedSensor(object):

        def __init__(self, name):
            self.name = name

        def send(self, to_probe, data, method="POST", data_format = "JSON"):

            if not isinstance(method, str) or method.upper() not in ["GET", "POST"]:
                raise ValueError('%%method%% must be \"GET\" or \"POST\"')

            if not isinstance(data_format, str) or data_format.upper() not in ["JSON", "XML"]:
                raise ValueError('%%data_format%% must be \"JSON\" or \"XML\"')

            if not isinstance(data, PrtgSensorData):
                raise ValueError('data is not valid SensorData')

            if not isinstance(to_probe, PrtgProbe):
                raise ValueError('probe is not valid Probe')

            method = method.upper()
            data_format = data_format.upper()
            endpoint = to_probe.endpoint

            if data_format == 'JSON' : data = data.to_JSON()
            if data_format == 'XML' : data = data.to_XML()

            if method == "POST":
                r = requests.post('{}/{}'.format(endpoint, self.name), data = data)
            else:
                r = requests.get('{}/{}'.format(endpoint, self.name), data = data)

            return r

class PrtgSensorData(object):

    def __init__(self):
        self._results = []
        self._error = None
        self._text = None

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if not (value == 0 or value == 1): raise ValueError('%%error%% must be 1 or 0')
        self._error = value

    @property
    def text(self):
        return self._text

    @error.setter
    def text(self, value):
        if not isinstance(value, str): raise ValueError('%%text%% must be a string')
        self._test = value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        raise RuntimeError('Use add_channel method to update channels')

    def add_result(self, result):

        if len(self._results) > MAX_RESULTS:
            raise TooManyChannelsInSensorData()
        else:
            if not isinstance(result, PrtgResult): raise ValueError('Not a valid result')
            self._results.append(result)

    def to_JSON(self):
        prtgdict = {}
        results = []
        for result in self._results:
            resdict = {}
            data = result.__dict__
            data = {key: value for key, value in data.items() if value is not None}
            for key, value in data.items():
                if not value is None:
                    modified_key = key.replace('_',' ').title().replace(' ', '')
                    if isinstance(value, int) or isinstance(value, float):
                        resdict[modified_key] = value
                    else:
                        resdict[modified_key] = str(value)
            results.append(resdict)

        prtgdict["result"] = results
        prtgdict["text"] = self._text
        prtgdict["error"] = self._error
        return json.dumps({"prtg":prtgdict})

    def to_XML(self):
        dom = getDOMImplementation()
        xml = dom.createDocument(None, 'prtg', None)
        top_element = xml.documentElement

        if self._error is not None:
            xmltag = xml.createElement('error')
            xmldata = xml.createTextNode(str(self._error))
            xmltag.appendChild(xmldata)
            top_element.appendChild(xmltag)

        if self._text is not None:
            xmltag = xml.createElement('text')
            xmldata = xml.createTextNode(self._text)
            xmltag.appendChild(xmldata)
            top_element.appendChild(xmltag)

        for result in self._results:
            resdict = {}
            data = result.__dict__
            data = {key: value for key, value in data.items() if value is not None}
            node = xml.createElement('result')
            for key, value in data.items():
                modified_key = key.replace('_',' ').title().replace(' ', '')
                xmltag = xml.createElement(modified_key)
                xmldata = xml.createTextNode(str(value))
                xmltag.appendChild(xmldata)
                node.appendChild(xmltag)

            top_element.appendChild(node)

        return xml.toprettyxml()


class PrtgProbe(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint
