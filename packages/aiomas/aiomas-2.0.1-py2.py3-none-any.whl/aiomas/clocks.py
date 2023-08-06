"""
Clocks to be used with :class:`aiomas.agent.Container`.

All clocks should subclass :class:`BaseClock`.  Currently available clock types
are:

- :class:`AsyncioClock`: a real-time clock synchronized with the :mod:`asyncio`
  event loop.

- :class:`ExternalClock`: a clock that can be set by external tasks / processes
  in order to synchronize it with external systems or simulators.

"""
import asyncio
import heapq
import itertools

import arrow


__all__ = ['BaseClock', 'AsyncioClock', 'ExternalClock', 'TimerHandle']


class BaseClock:
    """Interface for clocks.

    Clocks must at least implement :meth:`time()` and :meth:`utcnow`.

    """

    def time(self):
        """Return the value (in seconds) of a monotonic clock.

        The return value of consecutive calls is guaranteed to be greater or
        equal then the results of previous calls.

        The initial value may not be defined. Don't depend on it.

        """
        raise NotImplementedError()

    def utcnow(self):
        """Return an :class:`arrow.arrow.Arrow` date with the current time in
        UTC."""
        raise NotImplementedError()

    def sleep(self, dt, result=None):
        """Sleep for a period *dt* in seconds.  Return an
        :class:`asyncio.Future`.

        If *result* is provided, it will be passed back to the caller when
        the coroutine has finished.

        """
        raise NotImplementedError()

    def sleep_until(self, t, result=None):
        """Sleep until the time *t*.  Return an :class:`asyncio.Future`.

        *t* may either be a number in seconds or an :class:`arrow.arrow.Arrow`
        date.

        If *result* is provided, it will be passed back to the caller when
        the coroutine has finished.

        """
        raise NotImplementedError()

    def call_in(self, dt, func, *args):
        """Schedule the execution of ``func(*args)`` in *dt* seconds and return
        immediately.

        Return an opaque handle which lets you cancel the scheduled call via
        its ``cancel()`` method.

        """
        raise NotImplementedError()

    def call_at(self, t, func, *args):
        """Schedule the execution of ``func(*args)`` at *t* and return
        immediately.

        *t* may either be a number in seconds or an :class:`arrow.arrow.Arrow`
        date.

        Return an opaque handle which lets you cancel the scheduled call via
        its ``cancel()`` method.

        """
        raise NotImplementedError()

    def _check_date(self, date):
        """Assert that *date* is not in the past and convert it into float if
        it is an :class:`arrow.arrow.Arrow`."""
        if isinstance(date, arrow.arrow.Arrow):
            t = (date - self.utcnow()).total_seconds() + self.time()
        else:
            t = date
        if t <= self.time():
            raise ValueError('Date "{}" is in the past'.format(date))
        return t


class AsyncioClock(BaseClock):
    """:mod:`asyncio` based real-time clock."""
    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

    def time(self):
        return self._loop.time()

    def utcnow(self):
        return arrow.utcnow()

    def sleep(self, dt, result=None):
        return asyncio.sleep(dt, result, loop=self._loop)

    def sleep_until(self, t, result=None):
        t = self._check_date(t)
        return asyncio.sleep(t - self.time(), result, loop=self._loop)

    def call_in(self, dt, func, *args):
        return self._loop.call_later(dt, func, *args)

    def call_at(self, t, func, *args):
        t = self._check_date(t)
        return self._loop.call_at(t, func, *args)


class ExternalClock(BaseClock):
    """A clock that can be set by external process in order to synchronize
    it with other systems.

    The initial UTC date *utc_start* may either be an
    :class:`arrow.arrow.Arrow` instance or something that
    :meth:`arrow.factory.ArrowFactory.get()` can parse.

    """
    def __init__(self, utc_start, init_time=0, loop=None):
        if not isinstance(utc_start, arrow.arrow.Arrow):
            utc_start = arrow.get(utc_start).to(tz='UTC')

        if loop is None:
            loop = asyncio.get_event_loop()

        self._time = init_time
        self._utc_start = utc_start
        self._loop = loop

        self._queue = []
        self._eid = itertools.count()

    def time(self):
        return self._time

    def utcnow(self):
        return self._utc_start.replace(seconds=self._time)

    def set_time(self, t):
        if t <= self._time:
            raise ValueError('Time must be > {} but is {}'
                             .format(self._time, t))
        self._time = t

        while self._queue and self._queue[0][0] <= t:
            _, _, future, result = heapq.heappop(self._queue)
            if not future.cancelled():
                future.set_result(result)

    def sleep(self, dt, result=None):
        if dt <= 0:
            raise ValueError('dt must be > 0 but is {}'.format(dt))
        return self.sleep_until(self._time + dt, result)

    def sleep_until(self, t, result=None):
        t = self._check_date(t)
        f = self._loop.create_future()
        heapq.heappush(self._queue, (t, next(self._eid), f, result))
        return f

    def call_in(self, dt, func, *args):
        if dt <= 0:
            raise ValueError('dt must be > 0 but is {}'.format(dt))
        return self.call_at(self._time + dt, func, *args)

    def call_at(self, t, func, *args):
        def cb(fut):
            func(*args)

        t = self._check_date(t)
        f = self.sleep_until(t)
        f.add_done_callback(cb)
        return TimerHandle(f, cb)


class TimerHandle:
    """This class lets you cancel calls scheduled by :class:`ExternalClock`."""
    def __init__(self, future, callback):
        self._future = future
        self._callback = callback

    def cancel(self):
        """Cancel the scheduled call represented by this handle."""
        self._future.remove_done_callback(self._callback)
        self._future.cancel()
