aiomas – A library for multi-agent systems and RPC based on asyncio
===================================================================

.. image:: https://gitlab.com/sscherfke/aiomas/badges/master/pipeline.svg
   :height: 20px
   :alt: pipeline status
   :target: https://gitlab.com/sscherfke/aiomas/commits/master

.. image:: https://gitlab.com/sscherfke/aiomas/badges/master/coverage.svg
   :height: 20px
   :alt: coverage report
   :target: https://gitlab.com/sscherfke/aiomas/commits/master

*aiomas* is an easy-to-use library for *request-reply channels*, *remote
procedure calls (RPC)* and *multi-agent systems (MAS)*.  It’s written in pure
Python on top of asyncio__.

Here are three simple examples that show the different layers of aiomas and
what they add on top of each other:

The *request-reply channel* has the lowest level of abstraction (but already
offers more then vanilla asyncio):

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> async def handle_client(channel):
   ...     """Handle a client connection."""
   ...     req = await channel.recv()
   ...     print(req.content)
   ...     await req.reply('cya')
   ...     await channel.close()
   >>>
   >>>
   >>> async def client():
   ...     """Client coroutine: Send a greeting to the server and wait for a
   ...     reply."""
   ...     channel = await aiomas.channel.open_connection(('localhost', 5555))
   ...     rep = await channel.send('ohai')
   ...     print(rep)
   ...     await channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(('localhost', 5555), handle_client))
   >>> aiomas.run(client())
   ohai
   cya
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

The *RPC layer* adds remote procedure calls on top of it:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>>
   >>> class MathServer:
   ...     router = aiomas.rpc.Service()
   ...
   ...     @router.expose
   ...     def add(self, a, b):
   ...         return a + b
   ...
   >>>
   >>> async def client():
   ...     """Client coroutine: Call the server's "add()" method."""
   ...     rpc_con = await aiomas.rpc.open_connection(('localhost', 5555))
   ...     rep = await rpc_con.remote.add(3, 4)
   ...     print('What’s 3 + 4?', rep)
   ...     await rpc_con.close()
   >>>
   >>> server = aiomas.run(aiomas.rpc.start_server(('localhost', 5555), MathServer()))
   >>> aiomas.run(client())
   What’s 3 + 4? 7
   >>> server.close()
   >>> aiomas.run(server.wait_closed())

Finally, the *agent layer* hides some of the boilerplate code required to setup
the sockets and allows agent instances to easily talk with each other:

.. code-block:: python3

   >>> import aiomas
   >>>
   >>> class TestAgent(aiomas.Agent):
   ...     def __init__(self, container):
   ...         super().__init__(container)
   ...         print('Ohai, I am %s' % self)
   ...
   ...     async def run(self, addr):
   ...         remote_agent = await self.container.connect(addr)
   ...         ret = await remote_agent.service(42)
   ...         print('%s got %s from %s' % (self, ret, remote_agent))
   ...
   ...     @aiomas.expose
   ...     def service(self, value):
   ...         return value
   >>>
   >>> c = aiomas.Container.create(('localhost', 5555))
   >>> agents = [TestAgent(c) for i in range(2)]
   Ohai, I am TestAgent('tcp://localhost:5555/0')
   Ohai, I am TestAgent('tcp://localhost:5555/1')
   >>> aiomas.run(until=agents[0].run(agents[1].addr))
   TestAgent('tcp://localhost:5555/0') got 42 from TestAgentProxy('tcp://localhost:5555/1')
   >>> c.shutdown()

*aiomas* is released under the MIT license. It requires Python 3.4 and above
and runs on Linux, OS X, and Windows.

__ https://docs.python.org/3/library/asyncio.html


Installation
------------

*aiomas* requires Python >= 3.6 (or PyPy3 >= 5.10.0).  It uses the *JSON* codec
by default and only has pure Python dependencies.

Install *aiomas* via pip__ by running:

.. code-block:: bash

   $ pip install aiomas

You can enable the optional MsgPack__ codec or its Blosc__ compressed version
by installing the corresponding features (note, that you need a C compiler to
install them):

.. code-block:: bash

   $ pip install aiomas[mp]   # Enables the MsgPack codec
   $ pip install aiomas[mpb]  # Enables the MsgPack and MsgPackBlosc codecs

__ https://pip.pypa.io/
__ https://pypi.python.org/pypi/msgpack-python/
__ https://pypi.python.org/pypi/blosc/


Features
--------

*aiomas* just puts three layers of abstraction around raw TCP / unix domain
sockets provided by *asyncio*:

Agents and agent containers:
  The top-layer provides a simple base class for your own agents. All agents
  live in a container.

  Containers take care of creating agent instances and performing the
  communication between them.

  The container provides a *clock* for the agents. This clock can either be
  synchronized with the real (wall-clock) time or be set by an external process
  (e.g., other simulators).

RPC:
  The *rpc* layer implements remote procedure calls which let you call methods
  on remote objects nearly as if they were normal objects:

  Instead of ``ret = obj.meth(arg)`` you write ``ret = await obj.meth(arg)``.

Request-reply channel:
  The *channel* layer is the basis for the *rpc* layer. It sends JSON__ or
  MsgPack__ encoded byte strings over TCP or unix domain sockets. It also maps
  replies (of success or failure) to their corresponding request.

Other features:

- TLS support for authorization and encrypted communication.

- Interchangeable and extensible codecs: JSON and MsgPack (the latter
  optionally compressed with Blosc) are built-in.  You can add custom codecs or
  write (de)serializers for your own objects to extend a codec.

- Deterministic, emulated sockets: A *LocalQueue* transport lets you send and
  receive message in a deterministic and reproducible order within a single
  process.  This helps testing and debugging distributed algorithms.

__ http://www.json.org/
__ http://msgpack.org/


Planned features
^^^^^^^^^^^^^^^^

Some ideas for future releases:

- Optional automatic re-connect after connection loss


Contribute
----------

- Issue Tracker: https://gitlab.com/sscherfke/aiomas/issues
- Source Code: https://gitlab.com/sscherfke/aiomas

Set-up a development environment with:

.. code-block:: bash

   $ virtualenv -p `which python3` aiomas
   $ pip install -r requirements-setup.txt

Run the tests with:

.. code-block:: bash

   $ pytest
   $ # or
   $ tox


Support
-------

- Documentation: https://aiomas.readthedocs.io/en/latest/

- Mailing list: https://groups.google.com/forum/#!forum/python-tulip

- Stack Overflow: http://stackoverflow.com/questions/tagged/aiomas

- IRC: #asyncio


License
-------

The project is licensed under the MIT license.


Changelog
=========

2.0.1 – 2017-12-29
------------------

- [CHANGE] Restore support for Python 3.5 so that the docs on Read the Docs
  build again.


2.0.0 – 2017-12-28
------------------

- [BREAKING] Converted to f-Strings and ``async``/``await`` syntax.  The
  minimum required Python versions are now Python 3.6 and PyPy3 5.10.0.

- [BREAKING] Removed ``aiomas.util.async()`` and ``aiomas.util.create_task()``.

- [CHANGE] Move from Bitbucket and Mercurial to GitLab and Git.

- [FIX] Adjust to asyncio changes and explicitly pass references to the current
  event loop where necessary.

You can find information about older versions in the `documentation
<https://aiomas.readthedocs.io/en/latest/development/changelog.html>`_.


Authors
=======

The original author of aiomas is Stefan Scherfke.

The initial development has kindly been supported by `OFFIS
<www.offis.de/en/>`_.


