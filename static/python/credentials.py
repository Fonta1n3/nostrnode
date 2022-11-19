# credentials.py
import secp256k1
import binascii
import os
from static.python import rpcauth


class NostrCredentials:
    def __init__(self, fully_noded_pubkey, relay):
        self.private_key = secp256k1.PrivateKey()
        self.private_key_serialized = self.private_key.serialize()
        self.public_key = self.private_key.pubkey.serialize(compressed=True).hex()
        self.sub_id = binascii.hexlify(os.urandom(32)).decode()
        self.fully_noded_pubkey = fully_noded_pubkey or ''
        self.relay = relay or 'wss://nostr-relay.wlvs.space'


class BtcRpcCredentials:
    def __init__(self):
        (btc_rpc_pass, btc_rpc_auth) = rpcauth.main()
        self.auth = btc_rpc_auth
        self.password = btc_rpc_pass
        self.port = '18443'


class EncryptionWords:
    def __init__(self, encryption_words):
        self.encryption_words = encryption_words
