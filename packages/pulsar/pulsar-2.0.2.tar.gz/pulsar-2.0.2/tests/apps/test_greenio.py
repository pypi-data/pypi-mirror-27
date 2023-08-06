import sys
import unittest
import asyncio
import traceback
from unittest import mock

from pulsar.api import send, create_future
from pulsar.apps import wsgi

from examples.echo.manage import server, Echo

try:
    from pulsar.apps import greenio
    from pulsar.apps.greenio.pool import _DEFAULT_WORKERS
    run_in_greenlet = greenio.run_in_greenlet
except ImportError:
    greenio = None

    def run_in_greenlet(x):
        return x


def raise_error():
    raise RuntimeError


class EchoGreen(Echo):

    def __call__(self, message):
        return greenio.wait(super().__call__(message))


@unittest.skipUnless(greenio, 'Requires the greenlet package')
class TestGreenIO(unittest.TestCase):

    @classmethod
    async def setUpClass(cls):
        s = server(name=cls.__name__.lower(), bind='127.0.0.1:0',
                   parse_console=False)
        cls.server_cfg = await send('arbiter', 'run', s)
        cls.client = EchoGreen(cls.server_cfg.addresses[0])

    @classmethod
    def tearDownClass(cls):
        if cls.server_cfg:
            return send('arbiter', 'kill_actor', cls.server_cfg.name)

    def request(self, **kwargs):
        environ = wsgi.test_wsgi_environ(**kwargs)
        return wsgi.WsgiRequest(environ)

    async def test_pool(self):
        pool = greenio.GreenPool()
        self.assertTrue(pool._loop)
        self.assertEqual(pool._loop, asyncio.get_event_loop())
        self.assertFalse(pool._greenlets)
        future = pool.submit(lambda: 'Hi!')
        self.assertIsInstance(future, asyncio.Future)
        result = await future
        self.assertEqual(result, 'Hi!')
        self.assertEqual(len(pool._greenlets), 1)
        self.assertEqual(len(pool._available), 1)

    async def test_greenlet_methods(self):
        pool = greenio.GreenPool()
        self.assertFalse(pool.in_green_worker)
        self.assertFalse(pool.getcurrent().parent)

        def _greenlet_methods():
            self.assertTrue(pool.in_green_worker)
            self.assertTrue(pool.getcurrent().parent)

        await pool.submit(_greenlet_methods)

    async def test_error_in_pool(self):
        # Test an error
        pool = greenio.GreenPool()
        with self.assertRaises(RuntimeError):
            await pool.submit(raise_error)
        self.assertEqual(len(pool._greenlets), 1)
        self.assertEqual(len(pool._available), 1)

    @run_in_greenlet
    def test_echo(self):
        result = self.client(b'ciao luca')
        self.assertEqual(result, b'ciao luca')

    @run_in_greenlet
    def test_large(self):
        '''Echo a 3MB message'''
        msg = b''.join((b'a' for x in range(2**13)))
        result = self.client(msg)
        self.assertEqual(result, msg)

    async def test_shutdown(self):
        # Test an error
        pool = greenio.GreenPool()
        self.assertEqual(pool._max_workers, _DEFAULT_WORKERS)
        self.assertEqual(await pool.submit(lambda: 'OK'), 'OK')
        self.assertEqual(len(pool._greenlets), 1)
        self.assertEqual(len(pool._available), 1)
        a = pool.submit(lambda: 'a')
        b = pool.submit(lambda: 'b')
        self.assertEqual(len(pool._greenlets), 2)
        self.assertEqual(len(pool._available), 0)
        result = await asyncio.gather(a, b)
        self.assertEqual(result[0], 'a')
        self.assertEqual(result[1], 'b')
        self.assertEqual(len(pool._greenlets), 2)
        self.assertEqual(len(pool._available), 2)
        self.assertEqual(pool.closed, False)
        await pool.shutdown()
        self.assertEqual(pool.closed, True)
        self.assertEqual(len(pool._greenlets), 0)
        self.assertEqual(len(pool._available), 0)

    def test_lock_error(self):
        lock = greenio.GreenLock()
        self.assertFalse(lock.locked())
        self.assertRaises(RuntimeError, lock.acquire)
        self.assertFalse(lock.locked())
        self.assertRaises(RuntimeError, lock.release)

    @run_in_greenlet
    def test_lock(self):
        green = greenio.getcurrent()
        lock = greenio.GreenLock()
        self.assertTrue(lock.acquire())
        self.assertEqual(lock.locked(), green)

        def _test_lock(l):
            return l.acquire()
        #
        # create a new greenlet
        child = greenio.greenlet(_test_lock)
        future = child.switch(lock)

        self.assertIsInstance(future, asyncio.Future)
        self.assertEqual(lock.locked(), green)

        # release the lock
        lock.release()
        self.assertTrue(future.done())
        self.assertEqual(lock.locked(), green)
        #
        # self.assertEqual(lock.locked(), child)

    def test_greenwsgi(self):
        wsgi = mock.MagicMock()
        pool = greenio.GreenPool()
        green = greenio.GreenWSGI(wsgi, pool)
        self.assertEqual(green.middleware[0], wsgi)
        self.assertEqual(green.pool, pool)

    async def test_uncatched_stopiteration(self):
        pool = greenio.GreenPool()
        with self.assertRaises(RuntimeError) as cm:
            await pool.submit(lambda: next(iter([])))
        self.assertIsInstance(cm.exception.__cause__, StopIteration)

    async def test_async_in_greenlet(self):
        pool = greenio.GreenPool()
        result = await pool.submit(async_function, self)
        self.assertEqual(result, True)

    @run_in_greenlet
    def test_green_http(self):
        http = greenio.GreenHttp()
        response = http.get('http://quantmind.com')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text)

    async def test_run_in_greenlet_error(self):

        def error():
            return 'foo' + 1

        @run_in_greenlet
        def green_test():
            return error()

        try:
            await green_test()
        except TypeError:
            exc = sys.exc_info()
        else:
            raise RuntimeError
        info = traceback.format_tb(exc[2])
        self.assertEqual(len(info), 4)
        self.assertTrue(info[3].endswith("return 'foo' + 1\n"))


async def async_function(test):
    future = create_future()
    future._loop.call_later(1, future.set_result, True)
    result = await future
    test.assertEqual(result, True)
    return result
