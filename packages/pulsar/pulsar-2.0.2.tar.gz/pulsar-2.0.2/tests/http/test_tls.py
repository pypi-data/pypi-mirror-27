import os

from pulsar.apps.http import SSLError, HttpClient
from pulsar.utils.system import platform

from tests.http import base


crt = os.path.join(os.path.dirname(__file__), 'ca_bundle')


if platform.type != 'win':

    class TestTlsHttpClient(base.TestHttpClient):
        with_tls = True

        async def test_verify(self):
            c = HttpClient()
            with self.assertRaises(SSLError):
                await c.get(self.httpbin())
            response = await c.get(self.httpbin(), verify=False)
            self.assertEqual(response.status_code, 200)
            response = await c.get(self.httpbin(), verify=crt)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request.verify, crt)
