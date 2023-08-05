================================================================================
gease - gITHUB RELease
================================================================================

.. image:: https://api.travis-ci.org/moremoban/gease.svg?branch=master
   :target: http://travis-ci.org/moremoban/gease

.. image:: https://codecov.io/gh/moremoban/gease/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/moremoban/gease


::

    A long long time ago, ancient developers do not have the command to do a github
    release. They relied on mouse clicks and web user interface to do their releases.
    Until 2017, they got a specialized command, **gs** and realized release management
    is no long a manual job.

**gease** simply makes a git release using github api v3.

.. image:: https://github.com/moremoban/gease/raw/master/images/cli.png
   :width: 600px


Installation
================================================================================


You can install gease via pip:

.. code-block:: bash

    $ pip install gease


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/moremoban/gease.git
    $ cd gease
    $ python setup.py install

Setup and Configuration
================================================================================

First, please create `personal access token` for yourself
`on github <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`_.

.. image:: https://github.com/moremoban/gease/raw/master/images/generate_token.png

Next, please create a gease file(`.gease`) in your home directory and place the
token inside it. Gease file is a simple json file. Here is an example::

   {"user":"chfw","personal_access_token":"AAFDAFASDFADFADFADFADFADF"}

Command Line
================================================================================

::

   gease simply makes a git release using github api v3. version 0.0.1

   Usage: gs repo tag [release message]

   where:

      release message is optional. It could be a quoted string or space separate
	  string

   Examples:

      gs gease v0.0.1 first great release
      gs gease v0.0.2 "second great release"


License
================================================================================

MIT

