from pathlib import Path
from random import randrange
from static.python.credentials import NostrCredentials, BtcRpcCredentials, EncryptionWords
from flask import Flask, render_template, request, make_response
from base64 import b64decode, b64encode
from datetime import datetime
from static.python.ssl_context import SSLContext
from static.python.event import Event
import websockets
import asyncio
import json
from static.python import encryption, addresses
import hashlib
import requests
import uuid

app = Flask(__name__)
subscribed = False
nostr_credentials: NostrCredentials
btc_credentials: BtcRpcCredentials
encryption_words: EncryptionWords


async def listen():
    async with websockets.connect(nostr_credentials.relay, ssl=SSLContext().ssl_context) as ws:
        req = ['REQ', nostr_credentials.sub_id, {'authors': [nostr_credentials.fully_noded_pubkey[2:]]}]
        print(f'sent: {req} to {nostr_credentials.relay}')
        await ws.send(json.dumps(req))
        while True:
            msg = await ws.recv()
            msg_json = json.loads(msg)
            msg_type = msg_json[0]
            if msg_type == 'EOSE':
                print(f'{msg_json}')
                global subscribed
                subscribed = True
            elif msg_type == 'EVENT':
                event = msg_parse(msg_json)
                if event is not None:
                    await ws.send(event)


def msg_parse(msg_json):
    for i, value in enumerate(msg_json):
        if i == 2:
            if msg_json[0] == 'EVENT':
                nostr_event = Event.from_JSON(value)
                if nostr_event.is_valid():
                    return parse_event(value)


def parse_event(event):
    for (key, value) in event.items():
        if key == 'content':
            decrypted_content = encryption.decrypt(b64decode(value), encryption_words)
            json_content = json.loads(decrypted_content)
            (command, wallet, param_json) = parse_received_command(json_content)
            response = make_command(command, wallet, param_json)
            if response.status_code != 200:
                print(f'http status code: {response.status_code}')
            if response.status_code == 200:
                content = response.content
                json_content = json.loads(content)
                error_desc = ""
                if not json_content["error"] is None:
                    error_check = json_content["error"]
                    if "message" in error_check:
                        error_desc = error_check["message"]
                        print(f'ERROR: {error_desc}')
                else:
                    if "result" in json_content:
                        part = {"response": json_content["result"], "errorDesc": error_desc}
                        json_part_data = json.dumps(part).encode('utf8')
                        encrypted_content = encryption.encrypt(json_part_data, encryption_words)
                        b64_encrypted_content = b64encode(encrypted_content).decode("ascii")
                        created_at = int(datetime.now().timestamp())
                        raw_event = f'''[
                            0,
                            "{nostr_credentials.public_key[2:]}",
                            {created_at},
                            20001,
                            [],
                            "{b64_encrypted_content}"
                        ]'''
                        event_id = hashlib.sha256(raw_event.encode('utf8')).hexdigest()
                        event_dict = {
                            'id': event_id,
                            'pubkey': nostr_credentials.public_key[2:],
                            'created_at': created_at,
                            'kind': 20001,
                            'tags': [],
                            'content': b64_encrypted_content,
                            'sig': None
                        }
                        event = Event.from_JSON(event_dict)
                        event.sign(nostr_credentials.private_key_serialized)
                        if event.is_valid():
                            e = ['EVENT', event.event_data()]
                            return json.dumps(e)
                        else:
                            print('Event invalid!')


def parse_received_command(json_content):
    command = None
    wallet = None
    param_value = None
    if "command" in json_content:
        command = json_content['command']
    if "wallet" in json_content:
        wallet = json_content['wallet']
    if "paramDict" in json_content:
        param_dict = json_content['paramDict']
        param_value = param_dict['param']
        if param_value == "":
            param_value = []

    return command, wallet, param_value


def make_command(command, wallet, param):
    headers = {
        'Content-Type': 'text/plain',
    }
    url = f'http://nostrnode:{btc_credentials.password}@localhost:{btc_credentials.port}'
    if wallet != "":
        url += f'/wallet/{wallet}'
    req_id = uuid.uuid4().hex
    data = {'jsonrpc': '1.0', 'id': req_id, 'method': command, 'params': param}
    json_data = json.dumps(data)
    return requests.post(url,
                         data=json_data.encode('utf8'),
                         headers=headers,
                         auth=('nostrnode', f'{btc_credentials.password}'))


def start_listening():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(listen())


@app.route("/", methods=['POST', 'GET'])
def index():
    global btc_credentials
    btc_credentials = BtcRpcCredentials()
    global nostr_credentials
    nostr_credentials = NostrCredentials('', '')
    addrs = addresses.addresses

    return render_template('index.html', rpc_auth_string=btc_credentials.auth,
                           our_nostr_pubkey=nostr_credentials.public_key,
                           address=addrs[randrange(101)])


@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
    output = request.form.to_dict()
    if 'fully_noded_pubkey' in output:
        nostr_credentials.fully_noded_pubkey = output['fully_noded_pubkey']
        nostr_credentials.relay = output['relay'] or 'wss://nostr-relay.wlvs.space/'
        btc_credentials.port = output['btc_rpc_port'] or '18443'
        global encryption_words
        encryption_words = EncryptionWords(output['encryption_words']).encryption_words
        context = {
            'log_string': "nostrnode credentials submitted...",
        }

        return render_template("session.html", **context)


@app.route("/status", methods=['POST', 'GET'])
def status():
    response = make_command('getblockchaininfo', '', {})
    if response.status_code == 200:
        log_string = 'Connected to Bitcoin Core'
    else:
        log_string = f'Not connected to Bitcoin Core, http status code: {response.status_code}'

    return render_template("session.html", log_string=log_string)


@app.route('/start_to_listen')
def start_to_listen():
    if not subscribed:
        start_listening()
    return 'nothing'


@app.get("/service-worker.js")
def worker():
    js = Path(__file__).parent / 'static' / 'js' / 'service-worker.js'
    text = js.read_text()
    resp = make_response(text)
    resp.content_type = 'application/javascript'
    resp.headers['Service-Worker-Allowed'] = '/'

    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
