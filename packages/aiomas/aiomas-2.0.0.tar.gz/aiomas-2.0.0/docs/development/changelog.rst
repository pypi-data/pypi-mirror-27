Change log
==========

2.0.0 – 2017-12-28
------------------

- [BREAKING] Converted to f-Strings and ``async``/``await`` syntax.  The
  minimum required Python versions are now Python 3.6 and PyPy3 5.10.0.

- [BREAKING] Removed ``aiomas.util.async()`` and ``aiomas.util.create_task()``.

- [CHANGE] Move from Bitbucket and Mercurial to GitLab and Git.

- [FIX] Adjust to asyncio changes and explicitly pass references to the current
  event loop where necessary.


1.0.3 – 2016-05-09
------------------

- [FIX] The function :func:`asyncio.ensure_future()` called in
  ``aiomas.util.create_task()`` was introduced in Python 3.4.4 and is not
  available in Python 3.4.0–3.4.3 (which is, e.g., used on Ubuntu 14.04).
  There is now a fallback to :func:`asyncio.async()` if
  :func:`asyncio.ensure_future()` is not available.


1.0.2 – 2016-05-04
------------------

- [CHANGE] ``aiomas.util.create_task()`` replaces ``aiomas.util.async()``.
  ``aiomas.util.async()`` is now deprecated and will be removed in aiomas 2 and
  when a new Python release no longer allows to use *async* as name.

- [NEW] Added developer documentation.


1.0.1 – 2016-04-22
------------------

.. currentmodule:: aiomas.agent

- [BREAKING CHANGE] Renamed the *async* argument for :meth:`Container.create()`
  and :meth:`Container.shutdown()` to *as_coro*.  Realized to late that it will
  come to name clashes with the ``async`` keyword added to Python 3.5.
  I assume that no one really uses this project yet, thus I mark it as bug-fix
  relaese rather then bumping aiomas to v2.


1.0.0 – 2016-04-18
------------------

.. currentmodule:: aiomas

- [BREAKING CHANGE] :meth:`channel.Channel.close()` and
  :meth:`rpc.RpcClient.close()` are now coroutines.

- [BREAKING CHANGE] :func:`rpc.start_server()` and
  :func:`rpc.open_connection()` now take RPC services instead of routers.
  Services are the objects that contain the routers.  To fix your code, replace
  things like ``router=MyService().router`` with ``rpc_service=MyService()``.

- [CHANGE] :meth:`channel.Channel.send()` now raises a :exc:`ValueError` if
  a message is too long to be send.  A message is too long if its length does
  not fit into a 32bit unsigned integer.

- [NEW] The various *connect* functions now accept a *timeout* parameter.  If
  it is set to a number > 0 (or to ``None``) it tries to connect for the
  specified amount of time (or indefinitely) before raise
  a :exc:`ConnectionRefusedError`.  This way, you can start clients before (or
  at the "same" time) you start the server.

- [NEW] You can register a callback to :class:`rpc.RpcClient` that gets called
  when the network connection is reset.  This helps reacting to connection
  losses if the :class:`rpc.RpcClient` only has an RPC service running but is
  not actively performing any task.

- [NEW] Added a :exc:`~exceptions.SerializationError` that gets raised if
  a message cannot be serialized.

- [NEW] Added a :mod:`~aiomas.subproc` module that helps you to spawn
  subprocesses for agents.  Each subprocess will have a container and
  a managing agent that can be remote-controlled to start more agents within
  its container.

- [NEW] Added a :class:`~local_queue.LocalQueue` transport that sends messages
  of multiple connections (e.g., from different agent containers) within
  a process in a deterministic order.  This should make debugging, tuning and
  testing easier.

- [NEW] A lot of documentation.


0.6.1 – 2015-10-21
------------------

- [CHANGE] Agent now also accepts subclasses of Container (`issue #17`_).

- [FIX] `issue #16`_: Container API docs no correctly refer to the "create()"
  method.

.. _`issue #16`: https://bitbucket.org/sscherfke/aiomas/issues/16/
.. _`issue #17`: https://bitbucket.org/sscherfke/aiomas/issues/17/


0.6.0 – 2015-09-18
------------------

- [CHANGE] Asserted Python 3.5 compatibility and converted all examples to use
  the new ``async`` and ``await`` keywords.

- [CHANGE] ``Container.__init__()`` no longer contains an asynchronous task.
  Instead, you now need to call the factory function ``Container.create()``.

- [CHANGE] Removed ``Container.spawn()``.  You can now directly instantiate
  agent instances but you still need to pass a reference to the agent's
  container to ``Agent.__init__()``.

- [NEW] ``AiomasError`` is the new base class for all errors in aiomas (`issue
  #15`_).

- [NEW] Documentation tests now have their own *tox* environment (``tox -e
  docs``).

- [NEW] Added support and docs_ for TLS encryption.

- [NEW] Added some documentation about the channel layer.

.. _docs: https://aiomas.readthedocs.io/en/latest/guides/tls.html
.. _`issue #15`: https://bitbucket.org/sscherfke/aiomas/issues/15/


0.5.0 – 2015-06-27
------------------

- [CHANGE] Agent addresses now start with *tcp://* or *ipc://* (for Unix domain
  sockets) instead of just *agent://*.

- [CHANGE] Using dictionaries as routers is now easier (`issue #13`_).

- [CHANGE] Renamed the ``rpc`` attribute for routers to ``router``.

- [CHANGE] Renamed ``Agent.name`` to ``Agent.addr`` and improved agent's *str*
  representation.

- [CHANGE] Updated and improved *str* and *repr* for agents, proxies and agent
  proxies.

- [CHANGE] ``Codec.add_serializer()`` now raises an exception if there is
  already a serializer for a given type (`issue #9`_).

- [NEW] Added ``aiomas.util.run()`` (and an ``aiomas.run()`` alias) which are
  shortcuts for ``loop = asyncio.get_event_loop();
  loop_run_{until_complete|forever}()``.

- [NEW] Added a ``@serializable`` decorator to ``aiomas.codecs`` which
  simplifies making a type serializable.

- [NEW] Documentation: Overview, Agents, Codecs, Clocks (draft), Testing (draft).

- [NEW] ``Container.connect()`` checks if an agent exists in the remote
  container.

- [NEW] Proxies are now cached with weakrefs.

- [FIX] `issue #12`_: ``Router.path`` reversed the order of path components.

- [FIX] Fixed a bug where concurrent calls to ``Container.connect()`` would
  lead to multiple connections to the same address.

.. _`issue #9`: https://bitbucket.org/sscherfke/aiomas/issues/9/
.. _`issue #12`: https://bitbucket.org/sscherfke/aiomas/issues/12/
.. _`issue #13`: https://bitbucket.org/sscherfke/aiomas/issues/13/


0.4.0 – 2015-04-15
------------------

- [CHANGE] ``Channel`` and ``Container`` no longer take codec instances but
  classes.  They also accept a list of factories for extra serializers.

- [CHANGE] The ``rpc.open_connection()`` and ``rpc.start_server()`` methods
  no longer accept the ``add_to`` parameter.  ``rpc.start_server()`` accept
  a *client_connected_cb* instead, which should be a function with one
  argument, the ``RpcClient`` for each new connection.
  ``rpc.open_connection()`` already returns the ``RpcClient()``.

- [CHANGE] Renamed the package extras from *MsgPack* to *mp* and from
  *MsgPackBlosc* to *mpb* to work around a bug in pip/setuptools.  They are
  also shorter now. ;-)

- [NEW] ``RpcClient`` no has a ``channel`` and a ``service`` attribute.

- [NEW] Improved error message for ``LookupError``.

- [FIX] `issue #8`_:  Every channel instance created by
  ``channel.start_server()`` now has a separate codec instance to avoid
  problems with some serializers.

.. _`issue #8`: https://bitbucket.org/sscherfke/aiomas/issues/8/


0.3.0 – 2015-03-11
------------------

- [CHANGE] Removed LocalProxies and everything related to it because they
  caused several problems.  That means that agents within a single container
  now also communicate via TCP sockets.  Maybe something similar but more
  robust will be reintroduced in a later release.

- [CHANGE] ``Channel.send()`` is no longer a coroutine.  It returns a Future
  instead.

- [CHANGE] Removed ``Container.get_url_for()`` which didn’t (and couldn’t) work
  as I originally assumed.

- [CHANGE] ``JSON`` is now the default codec.  msgpack and blosc don’t get
  installed by default.  This way, we only have pure Python dependencies for
  the default installation which is very handy if you are on Windows.  You can
  enable the other codecs via ``pip install -U aiomas[MsgPack]`` or ``pip
  install -U aiomas[MsgPackBlosc]``.

- [NEW] Support for Python 3.4.0 and 3.4.1 (yes, Python 3.3 with asyncio works,
  too, but I’ll drop support for it as soon as it becomes a burden) (Resolves
  `issue #6`_).

- [NEW] ``ExternalClock`` accepts a date string or an Arrow object to set the
  inital date and time.

- [NEW] ``aiomas.util.async()`` which is like ``asyncio.async()`` but registers
  a callback that instantly captures and raises exceptions, instead of delaying
  them until the task gets garbage collected.

- [NEW] The agent container adds a serializer for Arrow dates.

- [NEW] ``Proxy`` implements ``__eq__()`` and ``__hash__()``.  Two different
  proxy objects sharing the same channel and pointing to the same remote
  function will no appear to be equal.  This makes it less error prone to use
  Proxy instances as keys in dictionaries.

- [NEW] Updated and improved flow-control for ``Channel`` and its protocol.

- [NEW] Improved error handling if the future returned by ``Channel.send()``
  is triggered or cancelled by an external party (e.g., by going out of scope).
  If asyncio’s DEBUG mode is enabled, you will even get more detailed error
  messages.

- [NEW] ``MessagePackBlosc`` codec.  It uses msgpack to serialize messages and
  blosc to compress them.  It can massively reduce the message size and
  consumes very little CPU time.

- [NEW] A Contract Net example
  (https://gitlab.com/sscherfke/aiomas/blob/master/examples/agent_contractnet.py)

- [NEW] ``__str__()`` representations for agents, containers and codecs (fixes
  `issue #5`_).

- [FIX] `issue #7`_: Improved error handling and messages if the
  (de)serialization raises an exception.

- [FIX] Containers now work with unix domain sockets.

- [FIX] Various minor bug-fixes

.. _`issue #5`: https://bitbucket.org/sscherfke/aiomas/issues/5/
.. _`issue #6`: https://bitbucket.org/sscherfke/aiomas/issues/6/
.. _`issue #7`: https://bitbucket.org/sscherfke/aiomas/issues/7/


0.2.0 - 2015-01-23
------------------

- [CHANGE] The *MsgPack* codec is now the default.  Thus, *msgpack-python* is
  now a mandatory dependency.

- [CHANGE] Renamed ``RpcClient.call`` to ``RpcClient.remote``.

- [NEW] ``aiomas.agent`` module with an ``Agent`` base class and
  a ``Container`` for agents.  Agents within a container communicate via direct
  method calls.  Agents in different containers use RPC.

- [NEW] ``aiomas.clock`` module which offers various clocks for a MAS:

  - ``AsyncioClock`` is a real-time clock and wraps asyncio's ``time()``,
    ``sleep()``, ``call_later()`` and ``call_at()`` functions.

  - ``ExternalClock`` can be synchronized with external simulation
    environments.  This allows you to *stop* the time or let it pass
    faster/slower than the wall-clock time.

- [NEW] Support for unix domain sockets in ``aiomas.channel`` and
  ``aiomas.rpc``.

- [NEW] "rpc_service()" tasks created by an RPC server can now be collected
  so that you can wait for their completion before you shutdown your program.

- [NEW] Added contents to the README and created a Sphinx project.  Only the
  API reference is done yet.  A tutorial and topical guides will follow.

- [FIX] aiomas with the JSON codec is now compatible to simpy.io



0.1.0 – 2014-12-18
------------------

Initial release with the following features:

- A *request-reply channel* via TCP that allows to send multiple messages and
  to asynconously wait for results (or an exception).

- Messages can be serialized with *JSON* or *msgpack*.

- The underlying communication protocol should be compatible with `simpy.io
  <https://bitbucket.org/simpy/simpy.io/>`_ (if you use JSON and no custom
  serializers).

- Remote procedure calls (RPCs) supporting nested handlers and bidirectional
  calls (callees can make calls to the caller before returning the actual
  result).
