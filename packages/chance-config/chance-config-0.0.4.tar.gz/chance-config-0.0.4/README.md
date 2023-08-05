# Config ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Config is a Python-based project for reading configurations from YAML files.

## Installation

### Requirements
- Python 2.7 and up
- pkg_resources
- pyYAML

```
$ pip install chance-config 
```

## Usage

```python
import chanconfig

# With package given
chanconfig.Config('test.yaml', 'foo.conf')

# With relative/absolute path
chanconfig.Config('foo/conf/test.yaml')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
