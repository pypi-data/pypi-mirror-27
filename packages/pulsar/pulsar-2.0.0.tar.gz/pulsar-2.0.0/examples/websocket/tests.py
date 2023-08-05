'''Tests the websocket middleware in pulsar.apps.ws.'''
import unittest
import asyncio

from pulsar.api import send
from pulsar.apps.ws import WebSocket, WS
from pulsar.apps.http import HttpClient
from pulsar.apps.test import run_test_server

from examples.websocket.manage import server


class Echo(WS):

    def __init__(self, loop):
        self.queue = asyncio.Queue(loop=loop)

    def get(self):
        return self.queue.get()

    def on_message(self, ws, message):
        self.queue.put_nowait(message)

    def on_ping(self, ws, body):
        ws.pong(body)
        self.queue.put_nowait('PING: %s' % body.decode('utf-8'))

    def on_pong(self, ws, body):
        self.queue.put_nowait('PONG: %s' % body.decode('utf-8'))

    def on_close(self, ws):
        self.queue.put_nowait('CLOSE')


class TestWebSocket(unittest.TestCase):
    app_cfg = None
    concurrency = 'process'

    @classmethod
    async def setUpClass(cls):
        await run_test_server(cls, server)
        addr = cls.app_cfg.addresses[0]
        cls.ws_uri = 'ws://{0}:{1}/data'.format(*addr)
        cls.ws_echo = 'ws://{0}:{1}/echo'.format(*addr)

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)

    def http(self, **params):
        return HttpClient(**params)

    def test_hybikey(self):
        w = WebSocket('/', None)
        v = w.challenge_response('dGhlIHNhbXBsZSBub25jZQ==')
        self.assertEqual(v, "s3pPLMBiTxaQ9kYGzzhZRbK+xOo=")

    async def test_bad_requests(self):
        c = self.http()
        response = await c.post(self.ws_uri)
        self.assertEqual(response.status_code, 405)
        #
        response = await c.get(self.ws_uri,
                               headers=[('Sec-Websocket-Key', 'x')])
        self.assertEqual(response.status_code, 400)
        #
        response = await c.get(self.ws_uri,
                               headers=[('Sec-Websocket-Key', 'bla')])
        self.assertEqual(response.status_code, 400)
        #
        response = await c.get(self.ws_uri,
                               headers=[('Sec-Websocket-version', 'xxx')])
        self.assertEqual(response.status_code, 400)

    async def test_upgrade(self):
        c = self.http()
        handler = Echo(c._loop)
        ws = await c.get(self.ws_echo, websocket_handler=handler)
        response = ws.handshake
        self.assertEqual(response.status_code, 101)
        self.assertEqual(response.headers['upgrade'], 'websocket')
        self.assertEqual(ws.connection, response.connection)
        self.assertEqual(ws.handler, handler)
        #
        self.assertTrue(response.event('post_request').fired())
        self.assertFalse(ws.event('post_request').fired())
        # Send a message to the websocket
        ws.write('Hi there!')
        message = await handler.get()
        self.assertEqual(message, 'Hi there!')

    async def test_ping(self):
        c = self.http()
        handler = Echo(c._loop)
        ws = await c.get(self.ws_echo, websocket_handler=handler)
        #
        # ASK THE SERVER TO SEND A PING FRAME
        ws.write('send ping TESTING PING')
        message = await handler.get()
        self.assertEqual(message, 'PING: TESTING PING')

    async def test_pong(self):
        c = self.http()
        handler = Echo(c._loop)
        ws = await c.get(self.ws_echo, websocket_handler=handler)
        #
        ws.ping('TESTING CLIENT PING')
        message = await handler.get()
        self.assertEqual(message, 'PONG: TESTING CLIENT PING')

    async def test_close(self):
        c = self.http()
        handler = Echo(c._loop)
        ws = await c.get(self.ws_echo, websocket_handler=handler)
        self.assertEqual(ws.event('post_request').fired(), 0)
        ws.write('send close 1001')
        message = await handler.get()
        self.assertEqual(message, 'CLOSE')
        self.assertTrue(ws.close_reason)
        self.assertEqual(ws.close_reason[0], 1001)
        self.assertTrue(ws.connection.closed)

    async def test_home(self):
        c = self.http()
        response = await c.get(self.uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'],
                         'text/html; charset=utf-8')

    async def test_graph(self):
        c = self.http()
        handler = Echo(c._loop)
        ws = await c.get(self.ws_uri, websocket_handler=handler)
        self.assertEqual(ws.event('post_request').fired(), 0)
        ws.write('data')
        message = await handler.get()
        self.assertTrue(message)
