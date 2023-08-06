[![Build Status](https://travis-ci.org/sdruskat/pykwalifire.svg?branch=master)](https://travis-ci.org/sdruskat/pykwalifire) [![Coverage Status](https://coveralls.io/repos/github/sdruskat/pykwalifire/badge.svg?branch=master)](https://coveralls.io/github/sdruskat/pykwalifire?branch=master)

# pykwalifire

**pykwalifire** is a fork of the YAML/JSON validation library [pykwalify](https://github.com/Grokzen/pykwalify).
It adds the following features.

## New features

### Specify custom file extensions for YAML and JSON data files [1.7.0]

In order to be able to validate JSON or YAML files with non-default file extensions, 
the following two options have been introduced:

- `-y EXT, --yaml-extension EXT` to specify a custom extension `EXT`, allowing to
validate YAML files such as *my-yaml-file.yext*.
- `-j EXT, --json-extension EXT` to specify a custom extension `EXT`, allowing to
validate JSON files such as *my-json-file.jext*.

### Support Python 3.x exclusively [2.0.1]

*pykwalifire* drops support for Python 2.7. Python 2.x will not be maintained
past 2020, and its default `ascii` encoding makes it a nightmare for unicode
support. To be able to use *pykwalifire* you must use it with Python 3.

### Default `ruamel` YAML parser [2.0.1]

As *PyYAML*, the most widely used YAML parser in the Python world, does not
support YAML 1.2, *ruamel.yaml* is the default parser for *pykwalifire*.

## History

Cf. [pykwalify](https://github.com/Grokzen/pykwalify).

# Installation

*pykwalifire* is available from PyPI: https://pypi.python.org/pypi/pykwalifire.

Install it with 

```bash
pip install pykwalifire
```

# Basic usage

Create a data file. JSON and YAML formats are both supported.

```yaml
- foo
- bar
```

Create a schema file with validation rules.

```yaml
type: seq
sequence:
  - type: str
```

Validate the file from the command line:

```bash
pykwalifire -d data.yaml -s schema.yaml
```

If the YAML data file would be called *data.customextension*, you would validate it
with

```bash
pykwalifire -d data.customextension -s schema.yaml -y customextension
```


## Documentation

For further documentation, please see the [pykwalify documentation](http://pykwalify.readthedocs.io/en/master/).

# License

*pykwalifire* is licensed under the MIT license, cf. [license file](LICENSE.md).

# `pykwalify` branch

The [pykwalify branch](https://github.com/sdruskat/pykwalifire/tree/pykwalify)
is used to create pull requests against the [upstream repository](https://github.com/Grokzen/pykwalify).
Hopefully this way all work that's been done in *pykwalifire* can be contributed
back to the original project.

**Thanks @Grokzen for creating a great piece of open source software!**

---

