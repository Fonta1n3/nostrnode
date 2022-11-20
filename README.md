# nostrnode
Your node, on nostr!

<img width="764" alt="Screenshot 2022-11-19 at 13 40 08" src="https://user-images.githubusercontent.com/30832395/202874073-0a50602d-f6cb-4738-b277-ca480205c0b9.png">

nostrnode allows Bitcoin Core light clients (Fully Noded users) to easily connect to Bitcoin Core running on any operating 
system that supports python. It's fast, easy and decentralized! nostrnode is generic, it encrypts all Bitcoin related comms 
thanks to `rncryptor` and in theory should be very easy to integrate into any Bitcoin Core/nostr client. 

⚠️ nostrnode is new, beta and experimental, use at your own risk.

This repo is for the pwa (progressive web app) version, if you run nostrnode on Chrome or any browser that supports pwa 
you can install it locally as a pwa. Setting up this python project to work as a pwa was not easy, the structure of this 
repo is a great template to get a pwa on python up and running. Having said that the cli version makes much more sense 
for real world use, find the repo [here]().

## Installation
You will need python 3.9
```
git clone nostrnode....
cd nostrnode
source venv/bin/activate
pip install -r requirements.txt
flask --app app --debug run
```
Open a browser and enter `127.0.0.1:5000` to access the UI. See also the cli version.


## Integration

- light clients encrypt a dict containing a bitcoin-cli command, optional param dict and wallet name to construct the url 
  on nostrnode and forward the request to the Bitcoin Core http server.
- Fully Noded and nostrnode use `rncryptor` to encrypt/decrypt the command and response dict, here is a swift example 
  from Fully Noded (BTC_CLI_COMMAND represents a string of the command and its params as json):
```swift
func executeNostrRpc(method: BTC_CLI_COMMAND) {
    var walletName:String?
    if isWalletRPC(command: method) {
        walletName = UserDefaults.standard.string(forKey: "walletName")
    }
    let dict:[String:Any] = ["command":method.stringValue,"paramDict":["param":method.paramDict],"wallet":walletName ?? ""]
    guard let jsonData = try? JSONSerialization.data(withJSONObject: dict, options: .prettyPrinted) else {
        #if DEBUG
        print("converting to jsonData failing...")
        #endif
        return
    }
    guard let node = activeNode,
          let encryptedWords = node.nostrWords,
        let decryptedWords = Crypto.decrypt(encryptedWords),
          let words = decryptedWords.utf8String else { onDoneBlock!((nil, "Error encrypting content...")); return }
    
    let encryptedContent = Crypto.encryptNostr(jsonData, words)!.base64EncodedString()
    writeEvent(content: encryptedContent)
    }
```

- nostrnode encrypts the response from bitcoin-cli as a dict to base64 text as the nostr event content and forwards to 
  Fully Noded (the light client):
```python
json_content = http_response_from_bitcoin_core
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
```

## Debugging
nostrnode logs the subscription request and an `EOSE` response confirming the connection to your relay is working. If 
anything goes wrong you should see an http status code in the output. There is a `Status` button which attempts to make 
a bitcoin-cli command to your local Bitcoin Core server, if it succeeds you will see `Bitcoin Core is connected..` 
output, if not you should see the http code to give us clues as to what went wrong. 


