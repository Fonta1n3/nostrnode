# nostrnode
Your node, on nostr!

<img width="764" alt="Screenshot 2022-11-19 at 13 40 08" src="https://user-images.githubusercontent.com/30832395/202874073-0a50602d-f6cb-4738-b277-ca480205c0b9.png">

nostrnode allows Fully Noded users to easily connect to Bitcoin Core running on any operating system that supports python.
It's fast, easy and decentralized! nostrnode is generic, it encrypts all Bitcoin related comms thanks to `rncryptor` and
in theory should be very easy to incorporate into any Bitcoin Core/nostr client. 

⚠️ nostrnode is new and experimental, use at your own risk.

## Installation
```
git clone nostrnode....
cd nostrnode
source venv/bin/activate
pip install requirements.txt
flask --app app --debug run
```
You can then open any browser and enter `127.0.0.1:5000` to access the UI. See also the cli version...

