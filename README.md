# nostrnode
Your node, on nostr!

<img width="764" alt="Screenshot 2022-11-19 at 13 40 08" src="https://user-images.githubusercontent.com/30832395/202874073-0a50602d-f6cb-4738-b277-ca480205c0b9.png">

nostrnode is a minimal python app (flask) which uses nostr to hole punch into your Bitcoin 
Core http server. nostrnode speaks `http` to Bitcoin Core's `rpcport` meaning it can control 
wallets! nostrnode has no database and all credenitals are forgotten when the app quits.


⚠️ This project is for demo purposes only, only use the cli version if you are #reckless 
enough for mainnet. I have not personally vetted the dependencies. Please refer to them 
in the `requirements.txt`. This is currently an expirement but works really well! Use at 
your own risk.


## Why?

Tired of slow, unreliable connections to your Bitcoin Core and lightning node over Tor?

Want to configure your own private setup but don't know how to install and configure Tor 
or VPNs?

Feeling sad and ovewhelmed bc you lost all your funds on FTX but now want to take some
responsibility to hodl in a more self sovereign way?

Try nostrnode! A way to connect your mobile device to any Bitcoin Core light client. 
For now Fully Noded is the only wallet that works with Bitcoin rpc as a backend via http.

## How 

- Fully Noded is a nostr client as is nostrnode, they deal only in `ephemeral` event types.

- nostrnode is hardcoded to speak `http` to your local Bitcoin Core `http` server which by 
  default is exposed to `localhost`.
  
- The user needs to add the `rpcauth=xxx` from nostrnode to their `bitcoin.conf`, subscribe 
  a Bitcoin Core light client (like Fully Noded) to nostrnode's public key and vice-versa.
  
-  Encryption words are used as a cross platfrom encryption key thanks to `rncryptor`. Input 
   the words yourself or let Fully Noded handle it by deriving a 12 word mnemonic from the 
   cryptographically secure random number generator for you (FN trims it down to 5 words).
  
- You'll need to subscribe to pubkeys, Fully Noded and nostr node create them on your behalf, 
  just paste them in.

## Whats next?

- Incorporating our own private nostr relay which should make it faster, easier, and more private/secure.
- Try `py-script` to make it work via localhost as a pwa?
- Add Join Market and maybe lightning http functionality.
  

