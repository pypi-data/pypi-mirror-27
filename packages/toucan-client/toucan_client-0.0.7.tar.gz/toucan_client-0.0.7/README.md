[![Pypi-v](https://img.shields.io/pypi/v/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![Pypi-pyversions](https://img.shields.io/pypi/pyversions/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![Pypi-l](https://img.shields.io/pypi/l/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![Pypi-wheel](https://img.shields.io/pypi/wheel/toucan-client.svg)](https://pypi.python.org/pypi/toucan-client)
[![CircleCI](https://img.shields.io/circleci/project/github/ToucanToco/toucan-client.svg)](https://circleci.com/gh/ToucanToco/toucan-client)
[![codecov](https://codecov.io/gh/ToucanToco/toucan-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ToucanToco/toucan-client)

# Installation

`pip install toucan_client`

# Usage

```python
client = ToucanClient('https://api.some.project.com/my_small_app')
etl_config = client.config.etl.get()  # -> GET 'https://api.some.project.com/config/etl'

# Example: add staging option
client.stage = 'staging'  # -> GET 'https://api.some.project.com/config/etl?stage=staging'

# Example: send a post request with some json data
client.json = {'DATA_SOURCE': ['example']}
response = client.config.etl.put()
# response.status_code equals 200 if everything went well
```

# Development

## PEP8

New code must be PEP8-valid (with a maximum of 100 chars): tests wont pass if code is not.
To see PEP8 errors, run `pycodestyle <path_to_file_name>` or recursively: `pycodestyle -r .`
