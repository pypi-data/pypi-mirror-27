import unittest

from pulsar.api import send

try:
    from pulsar.apps import greenio
    run_in_greenlet = greenio.run_in_greenlet
except ImportError:
    greenio = None

    def run_in_greenlet(f):
        return f


from examples.echo.manage import server, Echo


class EchoGreen(Echo):
    '''An echo client which uses greenlets to provide implicit
    asynchronous code'''

    def __call__(self, message):
        return greenio.wait(super().__call__(message))


@unittest.skipUnless(greenio, "Requires the greenlet module")
class TestGreenIo(unittest.TestCase):
    __benchmark__ = True
    __number__ = 2000

    @classmethod
    async def setUpClass(cls):
        s = server(name=cls.__name__.lower(), bind='127.0.0.1:0')
        cls.server_cfg = await send('arbiter', 'run', s)
        cls.client = Echo(cls.server_cfg.addresses[0])
        cls.green = EchoGreen(cls.server_cfg.addresses[0])
        cls.msg = b'a'*2**13
        cls.pool = greenio.GreenPool()

    async def test_yield_io(self):
        result = await self.client(self.msg)
        self.assertEqual(result, self.msg)

    @run_in_greenlet
    def test_green_io(self):
        result = self.green(self.msg)
        self.assertEqual(result, self.msg)

    async def test_green_pool(self):
        result = await self.pool.submit(self.green, self.msg)
        self.assertEqual(result, self.msg)
