# Usage

[![Pypi-v](https://img.shields.io/pypi/v/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![Pypi-pyversions](https://img.shields.io/pypi/pyversions/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![Pypi-l](https://img.shields.io/pypi/l/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![Pypi-wheel](https://img.shields.io/pypi/wheel/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![CircleCI](https://img.shields.io/circleci/project/github/ToucanToco/toucan-client.svg)](https://circleci.com/gh/ToucanToco/toucan-client)
[![codecov](https://codecov.io/gh/ToucanToco/laputa/branch/master/graph/badge.svg?token=Ae7jTcHofN)](https://codecov.io/gh/ToucanToco/laputa)

```python
client = ToucanClient('https://api.some.project.com')
small_app = client['my-small-app']
etl_config = small_app.config.etl.get()  # -> GET 'https://api.some.project.com/config/etl'

# Example: send a post request with some json data
response = small_app.config.etl.put(json={'DATA_SOURCE': ['example']})
# response.status_code equals 200 if everything went well

# Example: add staging option
small_app.stage = 'staging'  # -> GET 'https://api.some.project.com/config/etl?stage=staging'
```

# Development

## PEP8

New code must be PEP8-valid (with a maximum of 100 chars): tests wont pass if code is not.
To see PEP8 errors, run `pycodestyle <path_to_file_name>` or recursively: `pycodestyle -r .`
