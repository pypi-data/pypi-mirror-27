Release History
---------------

0.6.0
+++++

This release cleans up a lot of older code and makes some small modifications to the `Tardis` API to make it more
Pythonic. 0.6.0 includes support for humanizing a `Tardis` object, as well as outputing a localized string
representing the `Tardis` object.

This change introduces the following breaking changes:
    - `Tardis.epoch` is a property, not a function.
    - `Tardis.midnight` is a property, not a function.
    - `Tardis.naive` is a property, not a function.
    - `Tardis.timezone` is a property, not a function.

- tardis/dates.py
    - `is_datetime_naive()` no longer returns True when dt is None
    - `localize()` works with pytz tzinfo objects
    - `normalize()` works with pytz tzinfo objects
    - `Tardis.__init__()` accepts tzinfo objects as input to timezone
    - `Tardis.timezone()` is now a property
    - Added suport for humanizing a `Tardis` object
    - Added support for localizing a `Tardis` object for string output
- tardis/interface.py
    - `parse()` understands `dateutil.tz.tzoffset`, `datetutil.tz.tzlocal` and `dateutil.tz.tzutc` and converts those tzinfo
      objects into pytz based tzinfo objects.  This allows `parse()` to return a `Tardis` object with a `pytz.FixedOffset`
      timezone attached to it instead of returning a `Tardis` object converted to UTC
