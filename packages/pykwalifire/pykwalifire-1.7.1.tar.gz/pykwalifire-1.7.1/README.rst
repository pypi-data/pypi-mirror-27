|Build Status| |Coverage Status|

pykwalifire
===========

**pykwalifire** is a fork of the YAML/JSON validation library
`pykwalify <https://github.com/Grokzen/pykwalify>`__. It adds the
following features.

New features
------------

Specify custom file extensions for YAML and JSON data files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to be able to validate JSON or YAML files with non-default file
extensions, the following two options have been introduced:

-  ``-y EXT, --yaml-extension EXT`` to specify a custom extension
   ``EXT``, allowing to validate YAML files such as *my-yaml-file.yext*.
-  ``-j EXT, --json-extension EXT`` to specify a custom extension
   ``EXT``, allowing to validate JSON files such as *my-json-file.jext*.

History
-------

Cf. `pykwalify <https://github.com/Grokzen/pykwalify>`__.

Installation
============

*pykwalifire* is available from PyPI:
https://pypi.python.org/pypi/pykwalifire.

Install it with

.. code:: bash

    pip install pykwalifire

Basic usage
===========

Create a data file. JSON and YAML formats are both supported.

.. code:: yaml

    - foo
    - bar

Create a schema file with validation rules.

.. code:: yaml

    type: seq
    sequence:
      - type: str

Validate the file from the command line:

.. code:: bash

    pykwalifire -d data.yaml -s schema.yaml

If the YAML data file would be called *data.customextension*, you would
validate it with

.. code:: bash

    pykwalifire -d data.customextension -s schema.yaml -y customextension

Documentation
-------------

For further documentation, please see the `pykwalify
documentation <http://pykwalify.readthedocs.io/en/master/>`__.

License
=======

*pykwalifire* is licensed under the MIT license, cf. `license
file <LICENSE.md>`__.

``pykwalify`` branch
====================

The `pykwalify
branch <https://github.com/sdruskat/pykwalifire/tree/pykwalify>`__ is
used to create pull requests against the `upstream
repository <https://github.com/Grokzen/pykwalify>`__. Hopefully this way
all work that’s been done in *pykwalifire* can be contributed back to
the original project.

**Thanks @Grokzen for creating a great piece of open source software!**

.. |Build Status| image:: https://travis-ci.org/sdruskat/pykwalifire.svg?branch=master
   :target: https://travis-ci.org/sdruskat/pykwalifire
.. |Coverage Status| image:: https://coveralls.io/repos/github/sdruskat/pykwalifire/badge.svg?branch=master
   :target: https://coveralls.io/github/sdruskat/pykwalifire?branch=master
