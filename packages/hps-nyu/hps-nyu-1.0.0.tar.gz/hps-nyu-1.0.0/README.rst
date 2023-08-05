++++++++++++++++++++
HPS platform library
++++++++++++++++++++

This library contains modules for developing the platform for the games
played in CSCI-GA 2965, Heuristic Problem Solving with Prof. Dennis Shasha at NYU.

The following modules are available:

1. **servers**
       The ``servers`` package contains a Python 3 server classes that can use
       either sockets or `ZeroMQ <http://zeromq.org/>`_ for trasportation of
       messages. Both servers support sending and recieving of large messages
       and sending to one or all clients.

2. **clients**
       The ``clients`` package contains clients for the server in a few languages.
       They all implement the similar interface. Currently, Python 3, C++ and Java
       clients are implemented. See the `clients/README.rst <./hps/clients/README.rst>`_
       for details on the clients.

See the `docs <./docs>`_ directory for the API documentation for all the modules
and classes.

Installing
----------

To install the server module, run ::

    pip install --user hps-nyu

This will install the package in the current user's home directory, and does not
require root access. It can now be imported directly into your Python script.

To import a particular server class, use ``from hps.servers import <ServerClass>``.

For installing clients, see the README.rst file in the individual client directories.

Contributing
------------

We hope that this can be ever growing library for the course. Please feel free to
send in pull requests with bug fixes, new features or even entirely new modules
that may be relevant for the course.
