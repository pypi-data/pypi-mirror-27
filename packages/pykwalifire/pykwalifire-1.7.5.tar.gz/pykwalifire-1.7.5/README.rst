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

--------------

Change Log
==========

`1.7.3 <https://github.com/sdruskat/pykwalifire/tree/1.7.3>`__ (2017-12-18)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.7.2...1.7.3>`__

.. section-1:

`1.7.2 <https://github.com/sdruskat/pykwalifire/tree/1.7.2>`__ (2017-12-18)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.7.1...1.7.2>`__

.. section-2:

`1.7.1 <https://github.com/sdruskat/pykwalifire/tree/1.7.1>`__ (2017-12-18)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.7.0...1.7.1>`__

.. section-3:

`1.7.0 <https://github.com/sdruskat/pykwalifire/tree/1.7.0>`__ (2017-12-13)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.6.0...1.7.0>`__

.. section-4:

`1.6.0 <https://github.com/sdruskat/pykwalifire/tree/1.6.0>`__ (2017-01-22)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.5.2...1.6.0>`__

.. section-5:

`1.5.2 <https://github.com/sdruskat/pykwalifire/tree/1.5.2>`__ (2016-11-12)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.5.1...1.5.2>`__

.. section-6:

`1.5.1 <https://github.com/sdruskat/pykwalifire/tree/1.5.1>`__ (2016-03-06)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.5.0...1.5.1>`__

.. section-7:

`1.5.0 <https://github.com/sdruskat/pykwalifire/tree/1.5.0>`__ (2015-09-30)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.4.1...1.5.0>`__

.. section-8:

`1.4.1 <https://github.com/sdruskat/pykwalifire/tree/1.4.1>`__ (2015-08-27)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.4.0...1.4.1>`__

.. section-9:

`1.4.0 <https://github.com/sdruskat/pykwalifire/tree/1.4.0>`__ (2015-08-04)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.3.0...1.4.0>`__

.. section-10:

`1.3.0 <https://github.com/sdruskat/pykwalifire/tree/1.3.0>`__ (2015-07-13)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.2.0...1.3.0>`__

.. section-11:

`1.2.0 <https://github.com/sdruskat/pykwalifire/tree/1.2.0>`__ (2015-05-19)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.1.0...1.2.0>`__

.. section-12:

`1.1.0 <https://github.com/sdruskat/pykwalifire/tree/1.1.0>`__ (2015-04-04)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.0.1...1.1.0>`__

.. section-13:

`1.0.1 <https://github.com/sdruskat/pykwalifire/tree/1.0.1>`__ (2015-03-08)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/1.0.0...1.0.1>`__

.. section-14:

`1.0.0 <https://github.com/sdruskat/pykwalifire/tree/1.0.0>`__ (2015-03-08)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/15.01...1.0.0>`__

.. section-15:

`15.01 <https://github.com/sdruskat/pykwalifire/tree/15.01>`__ (2015-01-17)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/14.12...15.01>`__

.. section-16:

`14.12 <https://github.com/sdruskat/pykwalifire/tree/14.12>`__ (2014-12-24)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/14.08...14.12>`__

.. section-17:

`14.08 <https://github.com/sdruskat/pykwalifire/tree/14.08>`__ (2014-08-24)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/14.06.1...14.08>`__

.. section-18:

`14.06.1 <https://github.com/sdruskat/pykwalifire/tree/14.06.1>`__ (2014-06-23)
-------------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/14.06...14.06.1>`__

.. section-19:

`14.06 <https://github.com/sdruskat/pykwalifire/tree/14.06>`__ (2014-06-07)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/0.1.2...14.06>`__

.. section-20:

`0.1.2 <https://github.com/sdruskat/pykwalifire/tree/0.1.2>`__ (2013-01-26)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/v0.1.1...0.1.2>`__

`v0.1.1 <https://github.com/sdruskat/pykwalifire/tree/v0.1.1>`__ (2013-01-21)
-----------------------------------------------------------------------------

`Full
Changelog <https://github.com/sdruskat/pykwalifire/compare/v0.1.0...v0.1.1>`__

`v0.1.0 <https://github.com/sdruskat/pykwalifire/tree/v0.1.0>`__ (2013-01-20)
-----------------------------------------------------------------------------

\* *This Change Log was automatically generated by
`github_changelog_generator <https://github.com/skywinder/Github-Changelog-Generator>`__*

.. |Build Status| image:: https://travis-ci.org/sdruskat/pykwalifire.svg?branch=master
   :target: https://travis-ci.org/sdruskat/pykwalifire
.. |Coverage Status| image:: https://coveralls.io/repos/github/sdruskat/pykwalifire/badge.svg?branch=master
   :target: https://coveralls.io/github/sdruskat/pykwalifire?branch=master
