'''Tests the "helloworld" example.'''
import unittest

from pulsar import SERVER_SOFTWARE
from pulsar.api import send, get_application, get_actor
from pulsar.apps.http import HttpClient
from pulsar.apps.test import dont_run_with_thread, run_test_server

from examples.helloworld.manage import server


class TestHelloWorldThread(unittest.TestCase):
    app_cfg = None
    concurrency = 'thread'

    @classmethod
    async def setUpClass(cls):
        await run_test_server(cls, server)
        cls.client = HttpClient()

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)

    async def testMeta(self):
        app = await get_application(self.app_cfg.name)
        self.assertEqual(app.name, self.app_cfg.name)
        monitor = get_actor().get_actor(app.name)
        self.assertTrue(monitor.is_running())
        self.assertEqual(app, monitor.app)
        self.assertEqual(str(app), app.name)
        self.assertEqual(app.cfg.bind, '127.0.0.1:0')

    async def testResponse(self):
        c = self.client
        response = await c.get(self.uri)
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertEqual(content, b'Hello World!\n')
        headers = response.headers
        self.assertTrue(headers)
        self.assertEqual(headers['content-type'], 'text/plain')
        self.assertEqual(headers['server'], SERVER_SOFTWARE)

    async def testTimeIt(self):
        c = self.client
        b = await c.timeit('get', 5, self.uri)
        self.assertTrue(b.taken >= 0)

    async def test405(self):
        c = self.client
        response = await c.post(self.uri, data={'bla': 'foo'})
        self.assertEqual(response.status_code, 405)


@dont_run_with_thread
class TestHelloWorldProcess(TestHelloWorldThread):
    concurrency = 'process'
