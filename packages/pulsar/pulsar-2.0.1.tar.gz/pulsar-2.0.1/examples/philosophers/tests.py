import unittest
import asyncio

from pulsar.api import send
from pulsar.apps.test import test_timeout

from examples.philosophers.manage import DiningPhilosophers


class TestPhilosophers(unittest.TestCase):
    """Integration tests for the philosophers app
    """
    app_cfg = None

    @classmethod
    async def setUpClass(cls):
        app = DiningPhilosophers(name='plato', parse_console=False)
        cls.app_cfg = await send('arbiter', 'run', app)

    @test_timeout(60)
    async def test_info(self):
        while True:
            await asyncio.sleep(0.5)
            info = await send('plato', 'info')
            all = []
            for data in info.get('workers', []):
                p = data.get('philosopher')
                if p and p.get('eaten', 0) > 0:
                    all.append(p)
            if len(all) == 5:
                break

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            return send('arbiter', 'kill_actor', cls.app_cfg.name)
