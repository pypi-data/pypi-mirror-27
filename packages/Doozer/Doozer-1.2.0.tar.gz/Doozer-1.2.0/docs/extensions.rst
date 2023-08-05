==========
Extensions
==========

Extensions provide additional functionality to applications. Configuration
management is shared between applications and extensions in a central location.

Using Extensions
================

.. code::

    from doozer import Application
    from doozer_sqlite import SQLite

    app = Application(__name__)
    db = SQLite(app)

    db.connection.execute('SELECT 1;')

Developing Extensions
=====================

Doozer provides an :class:`~doozer.extensions.Extension` base class to make
extension development easier.

.. code::

    from doozer import Extension

    class SQLite(Extension):
        DEFAULT_SETTINGS = {'SQLITE_CONNECTION_STRING': ':memory:'}

        def __init__(self, app=None):
            self._connection = None
            super().__init__(app)

        @property
        def connection(self):
            if not self._connection:
                conn_string = self.app.settings['SQLITE_CONNECTION_STRING']
                self._connection = sqlite3.connect(conn_string)
            return self._connection

The :class:`~doozer.extensions.Extension` class provides two special attributes
that are meant to be overridden:

* :attr:`~doozer.extensions.Extension.DEFAULT_SETTINGS` provides default values
  for an extension's settings during the
  :meth:`~doozer.extensions.Extension.init_app` step. When a value is used by
  an extension and has a sensible default, it should be stored here (e.g., a
  database hostname).
* :attr:`~doozer.extensions.Extension.REQUIRED_SETTINGS` provides a list of
  keys that are checked for existence during the
  :meth:`~doozer.extensions.Extension.init_app` step. If one or more required
  settings are not set on the application instance assigned to the extension, a
  ``KeyError`` is raised. Extensions should set this when a value is required
  but has no default (e.g., a database password).

.. _extending-the-cli:

Extending the Command Line
==========================

Doozer offers an extensible command line interface. To register your own
commands, use :func:`~doozer.cli.register_commands`. Any function passed to it
will have its usage created directly from its signature. During the course of
initializing the application for use with the extension (i.e.,
:meth:`~doozer.extensions.Extension.init_app`), Doozer will check for a method
on the extension's instance named ``register_cli`` and call it. If you place
any calls to :func:`~doozer.cli.register_commands` inside it, the command line
interface will be extended automatically.

In order to access the new commands, the ``doozer`` command line utility must
be given a reference to an :class:`~doozer.base.Application`. This is done
through the ``--app`` argument:

.. code::

    $ doozer --app APP_PATH

.. note::

    For details about the syntax to use when passing a reference to an
    :class:`~doozer.base.Application`, see :ref:`running-applications`.

A positional argument in the Python function will result in a required
positional argument in the command::

    def trash(heap):
        pass

.. code:: sh

    $ doozer --app APP_PATH NAMESPACE trash HEAP

A keyword argument in the Python function will result in a positional argument
in the command with a default value to be used when the argument is omitted::

    def trash(heap='marjory'):
        pass

.. code:: sh

    $ doozer --app APP_PATH NAMESPACE trash [HEAP]

A keyword-only argument in the Python function will result in an optional
argument in the command::

    def trash(*, heap='marjory'):
        pass

.. code:: sh

    $ doozer --app APP_PATH NAMESPACE trash [--heap HEAP]

By default, all optional arguments will have a flag that matches the function
argument's name. When no other optional arguments start with the same
character, a single-character abbreviated flag can also be used.

.. code:: sh

    $ doozer --app APP_PATH NAMESPACE trash [-g HEAP]

The ``trash`` function can then be registered with the CLI::

    register_commands('fraggle', [trash])

.. code:: sh

    $ doozer --app APP_PATH fraggle trash --help

Additionally, if a command includes a ``quiet`` or ``verbose`` argument, it
will automatically receive the count of the number of times it was specified
(e.g., ``-v`` will have the value ``1``, ``-vv`` will have the value ``2``).
When both arguments are included, they will be added as a mutually exclusive
group.

.. note::

    Due to how :meth:`argparse <python:argparse.ArgumentParser.add_argument>`
    handles argument counts, ``quiet`` and ``verbose`` will be set to ``None``
    rather than ``0`` when the flag isn't specified when the command is
    invoked.

.. code:: sh

    $ doozer --app APP_PATH fraggle trash -vvvv
    $ doozer --app APP_PATH fraggle trash --quiet

Available Extensions
====================

Several extensions are available for use:

* `Henson-AMQP <https://henson-amqp.readthedocs.io>`_
* `Henson-Database <https://henson-database.readthedocs.io>`_
* `Henson-Logging <https://henson-logging.readthedocs.io>`_
