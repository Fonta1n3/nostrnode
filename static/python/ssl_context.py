# credentials.py
import ssl
import pathlib
from static.python.cert_gen import gen


class SSLContext:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        gen()
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.load_verify_locations(cafile=f'{pathlib.Path(__file__).parent}/cert.pem')
