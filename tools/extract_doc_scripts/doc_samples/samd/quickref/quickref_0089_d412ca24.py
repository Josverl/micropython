# Source: samd\quickref.rst:89
# Type: code_block
# Platform: unix

from machine import RTC

rtc = RTC()
date_time = rtc.datetime()  # return the actual date & time.
rtc.datetime(date_time_tuple)  # Set date & time, ignoring weekday
date_time = rtc.now()  # Return date & time in Unix order.
rtc.calibration(value)  # Set a calibration factor
