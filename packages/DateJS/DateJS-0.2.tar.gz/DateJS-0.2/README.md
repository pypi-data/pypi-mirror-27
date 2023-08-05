# DateJS    ![Build Status](https://travis-ci.org/rithik/DateJS.svg?branch=master)

## Convert Date from a JavaScript Date object to a Python DateTime object

## Usage

To use this library, you must first install the library (pip install DateJS)

In your code, you must import DateJS package by including `from DateJS import DateJS`.

To convert JavaScript Date, initialize a DateJS object by doing `DateJS(JAVASCRIPT_DATE_STRING)`, where the `JAVASCRIPT_DATE_STRING` can be determined by running `new Date().toString()` in JavaScript.

## Get Values

You can access a wide array of values by calling one of the following methods:

#### Year -> `getYear()`
#### Month -> `getMonth()`
#### Date -> `getDate()`
#### Hours -> `getHours()`
#### Minutes -> `getMinutes()`
#### Seconds -> `getSeconds()`
#### Milliseconds -> `getMilliseconds()`
#### Common Timezone (From pytz.common_timezones) -> `getTimezone()`
#### Simple Timezone (From pre-determined list of all common timezones) -> `getSimpleTimezone()`

## Common Errors

If you get a JavaScript Runtime Error, you can fix this by running `sudo apt-get install nodejs`. This will configure the JavaScript Runtime Environment.

## Examples

```python
from DateJS import DateJS

dJS = DateJS("Thu Oct 19 2017 21:50:06 GMT-0400 (Eastern Daylight Time)")

dJS.getTime() # Get datetime object of time with timezone data

dJS.getTimezone() # Returns a timezone object from pytz

dJS.getSimpleTime() # Returns most common timezone object from pytz

```

If you use the example above, JavaScript will automatically convert the Date into the timezone of the python server. In order to maintain the existing timezone, you can pass in each argument separately.

Format: `DateJS(JAVASCRIPT_STRING, YEAR, MONTH, DATE, HOUR, MINUTE, SECOND, MILLISECOND, OFFSET)`.

The month should be in the range 0-11 (so October would correspond with 9).

The last argument is the timezone offset. This can be determined by doing `new Date().getTimezoneOffset()`.

```python

dJS = DateJS("Thu Oct 19 2017 21:50:06 GMT-0400 (Eastern Daylight Time)", 2017, 9, 19, 21, 50, 6, 0, 240)

dJS.getTime() # Get datetime object of time with timezone data

dJS.getTimezone() # Returns a timezone object from pytz

dJS.getSimpleTime() # Returns most common timezone object from pytz

```

## Unnoticed Errors

If you would like to report any errors, please open an issue. If you know how to fix the issue, please submit appropiate changes.

