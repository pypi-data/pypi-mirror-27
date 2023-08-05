# -*- coding: utf-8 -*-

from __future__ import print_function

import threading
import time

try:
    from queue import Queue, Full, Empty
except ImportError:
    from Queue import Queue, Full, Empty

from fluent import sender
from fluent.sender import EventTime

__all__ = ["EventTime", "FluentSender"]

_global_sender = None

DEFAULT_QUEUE_TIMEOUT = 0.05
DEFAULT_QUEUE_MAXSIZE = 100
DEFAULT_QUEUE_CIRCULAR = False


def _set_global_sender(sender):  # pragma: no cover
    """ [For testing] Function to set global sender directly
    """
    global _global_sender
    _global_sender = sender


def setup(tag, **kwargs):  # pragma: no cover
    global _global_sender
    _global_sender = FluentSender(tag, **kwargs)


def get_global_sender():  # pragma: no cover
    return _global_sender


def close():  # pragma: no cover
    get_global_sender().close()


class CommunicatorThread(threading.Thread):
    def __init__(self, tag,
                 host='localhost',
                 port=24224,
                 bufmax=1 * 1024 * 1024,
                 timeout=3.0,
                 verbose=False,
                 buffer_overflow_handler=None,
                 nanosecond_precision=False,
                 msgpack_kwargs=None,
                 queue_timeout=DEFAULT_QUEUE_TIMEOUT,
                 queue_maxsize=DEFAULT_QUEUE_MAXSIZE,
                 queue_circular=DEFAULT_QUEUE_CIRCULAR, *args, **kwargs):
        super(CommunicatorThread, self).__init__(**kwargs)
        self._queue = Queue(maxsize=queue_maxsize)
        self._do_run = True
        self._queue_timeout = queue_timeout
        self._queue_maxsize = queue_maxsize
        self._queue_circular = queue_circular
        self._conn_close_lock = threading.Lock()
        self._sender = sender.FluentSender(tag=tag, host=host, port=port, bufmax=bufmax, timeout=timeout,
                                           verbose=verbose, buffer_overflow_handler=buffer_overflow_handler,
                                           nanosecond_precision=nanosecond_precision, msgpack_kwargs=msgpack_kwargs)

    def send(self, bytes_):
        if self._queue_circular and self._queue.full():
            # discard oldest
            try:
                self._queue.get(block=False)
            except Empty:   # pragma: no cover
                pass
        try:
            self._queue.put(bytes_, block=(not self._queue_circular))
        except Full:
            return False
        return True

    def run(self):
        while self._do_run:
            try:
                bytes_ = self._queue.get(block=True, timeout=self._queue_timeout)
            except Empty:
                continue
            with self._conn_close_lock:
                self._sender._send(bytes_)

    def close(self, flush=True, discard=True):
        if discard:
            while not self._queue.empty():
                try:
                    self._queue.get(block=False)
                except Empty:
                    break
        while flush and (not self._queue.empty()):
            time.sleep(0.1)
        self._do_run = False
        self._sender.close()

    def _close(self):
        with self._conn_close_lock:
            self._sender._close()

    @property
    def last_error(self):
        return self._sender.last_error

    @last_error.setter
    def last_error(self, err):
        self._sender.last_error = err

    def clear_last_error(self, _thread_id=None):
        self._sender.clear_last_error(_thread_id=_thread_id)

    @property
    def queue_timeout(self):
        return self._queue_timeout

    @queue_timeout.setter
    def queue_timeout(self, value):
        self._queue_timeout = value

    @property
    def queue_maxsize(self):
        return self._queue_maxsize

    @property
    def queue_blocking(self):
        return not self._queue_circular

    @property
    def queue_circular(self):
        return self._queue_circular


class FluentSender(sender.FluentSender):
    def __init__(self,
                 tag,
                 host='localhost',
                 port=24224,
                 bufmax=1 * 1024 * 1024,
                 timeout=3.0,
                 verbose=False,
                 buffer_overflow_handler=None,
                 nanosecond_precision=False,
                 msgpack_kwargs=None,
                 queue_timeout=DEFAULT_QUEUE_TIMEOUT,
                 queue_maxsize=DEFAULT_QUEUE_MAXSIZE,
                 queue_circular=DEFAULT_QUEUE_CIRCULAR,
                 **kwargs): # This kwargs argument is not used in __init__. This will be removed in the next major version.
        super(FluentSender, self).__init__(tag=tag, host=host, port=port, bufmax=bufmax, timeout=timeout,
                                           verbose=verbose, buffer_overflow_handler=buffer_overflow_handler,
                                           nanosecond_precision=nanosecond_precision, msgpack_kwargs=msgpack_kwargs,
                                           **kwargs)
        self._communicator = CommunicatorThread(tag=tag, host=host, port=port, bufmax=bufmax, timeout=timeout,
                                                verbose=verbose, buffer_overflow_handler=buffer_overflow_handler,
                                                nanosecond_precision=nanosecond_precision, msgpack_kwargs=msgpack_kwargs,
                                                queue_timeout=queue_timeout, queue_maxsize=queue_maxsize,
                                                queue_circular=queue_circular)
        self._communicator.start()

    def _send(self, bytes_):
        return self._communicator.send(bytes_=bytes_)

    def _close(self):
        # super(FluentSender, self)._close()
        self._communicator._close()

    def _send_internal(self, bytes_):
        assert False    # pragma: no cover

    def _send_data(self, bytes_):
        assert False    # pragma: no cover

    # override reconnect, so we don't open a socket here (since it
    # will be opened by the CommunicatorThread)
    def _reconnect(self):
        return

    def close(self):
        self._communicator.close(flush=True)
        self._communicator.join()
        return super(FluentSender, self).close()

    @property
    def last_error(self):
        return self._communicator.last_error

    @last_error.setter
    def last_error(self, err):
        self._communicator.last_error = err

    def clear_last_error(self, _thread_id=None):
        self._communicator.clear_last_error(_thread_id=_thread_id)

    @property
    def queue_timeout(self):
        return self._communicator.queue_timeout

    @queue_timeout.setter
    def queue_timeout(self, value):
        self._communicator.queue_timeout = value

    @property
    def queue_maxsize(self):
        return self._communicator.queue_maxsize

    @property
    def queue_blocking(self):
        return self._communicator.queue_blocking

    @property
    def queue_circular(self):
        return self._communicator.queue_circular

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        # give time to the comm. thread to send its queued messages
        time.sleep(0.2)
        self.close()
