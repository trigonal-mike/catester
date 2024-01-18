

## Timeout:

stopit:
https://pypi.org/project/stopit/

- License MIT

func_timeout:
https://pypi.org/project/func-timeout/

- License LGPLv2


https://pypi.org/project/stopit/#signaling-based-resources

https://pypi.org/project/stopit/#comparing-thread-based-and-signal-based-timeout-control


Can’t interrupt a long Python atomic instruction. e.g. if time.sleep(20.0) is actually executing, the timeout will take effect at the end of the execution of this line.

**func_timeout** seems to has solved it for windows as well, but its license is LGPLv2, do we want/need that?


## Pytest-JSON-Report
https://pypi.org/project/pytest-json-report/
- not longer maintained
- incompatible with metadata (environment is not set)
- do we need it actually?

## Pytest-Metadata
https://pypi.org/project/pytest-metadata/
- this plugin provides environment data


