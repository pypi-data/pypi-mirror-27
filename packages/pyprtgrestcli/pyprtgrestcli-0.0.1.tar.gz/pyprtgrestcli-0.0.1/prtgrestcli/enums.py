from enum import Enum

class PrtgErrorCodes(Enum):
    OK = 0
    WARNING = 1
    SYSTEM_ERROR = 2
    PROTOCOL_ERROR = 3
    CONTENT_ERROR = 4

    def __str__(self):
        return str(self.value)

class PrtgUnits(Enum):
    BytesBandwidth = "BytesBandwidth"
    BytesMemory = "BytesMemory"
    BytesDisk = "BytesDisk"
    Temperature = "Temperature"
    Percent = "Percent"
    TimeResponse = "TimeResponse"
    TimeSeconds = "TimeSeconds"
    Custom = "Custom"
    Count = "Count"
    CPU = "CPU (*)"
    BytesFile = "BytesFile"
    SpeedDisk = "SpeedDisk"
    SpeedNet = "SpeedNet"
    TimeHours = "TimeHours"

    def __str__(self):
        return str(self.value)

class PrtgSizes(Enum):
    One = "One"
    Kilo = "Kilo"
    Mega = "Mega"
    Giga = "Giga"
    Tera = "Tera"
    Byte = "Byte"
    KiloByte = "KiloByte"
    MegaByte = "MegaByte"
    GigaByte = "GigaByte"
    TeraByte = "TeraByte"
    Bit = "Bit"
    KiloBit = "KiloBit"
    MegaBit = "MegaBit"
    GigaBit = "GigaBit"
    TeraBit = "TeraBit"

    def __str__(self):
        return str(self.value)

class PrtgSpeedTimes(Enum):
    Second = "Second"
    Minute = "Minute"
    Hour = "Hour"
    Day = "Day"

    def __str__(self):
        return str(self.value)

class PrtgModes(Enum):
    Absolute = "Absolute"
    Difference = "Difference"

    def __str__(self):
        return str(self.value)

class PrtgDecimalModes(Enum):
    Auto = "Auto"
    All = "All"

    def __str__(self):
        return str(self.value)
