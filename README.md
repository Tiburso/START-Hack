![image](https://user-images.githubusercontent.com/47680931/227472947-3df0e6f9-3dff-400d-9164-ed65eddce1a6.png)

# Hash Game Store - START Hack Report
**Hash Game Store** is an online videogame store that allows developers to reach more players in a decentralized manner and gives users true ownership of their games via **cryptocurrency payment methods** and **InterPlanetary File System, peer-to-peer** file distribution.  

# Challenge - BLOCKFINANCE ECO AG

###### Step 1 --   Setting up a Bitcoin wallet structure using BIP-85 (Bitcoin Improvement Proposal 85) involves creating a hierarchical deterministic (HD) wallet to securely store and manage your company's Bitcoin funds. BIP-85 provides a way to structure the HD wallet into multiple segments or accounts, allowing you to allocate specific funds for accounting, salaries, fundraising, etc. By creating multiple BIP39 seeds, you can ensure that each account has its own unique seed for added security and backup purposes. This structure ensures that your company's Bitcoin funds are managed in a secure and organized manner, making it easier to track and access them as needed. (10 points)
For this step we decided to create our own system to generate BIP39 seeds from a single BIP85. We based ourselves on the original BIP-85 proposal on GitHub and wrote a small function that takes a single mnemonic (the 'master key') and originates others based on the index (an integer) given: 
```py
from  bip32utils  import  BIP32Key
from bip85_master.bip85.app import bip39
from config import HGS_KEY_PHRASE

""" Example Usage:
> TEST_MNENONIC = "install scatter logic circle pencil average fall shoe quantum disease suspect usage"
> generate_mnemonic_from_seed(TEST_MNENONIC, 12, 0)
Returns -> "jelly zero knife tumble cliff original hawk submit cute raccoon present fringe"
"""
def  generate_mnemonic_from_seed(index: int, mnemonic: str = HGS_KEY_PHRASE, language: str = 'english'):
	seed = BIP32Key.fromEntropy(mnemonic.encode('utf-8')).ExtendedKey()
	num_words = len(mnemonic.split(' '))
	return bip39(seed, language, num_words, index)
```
---
###### Step 2 -- Create a Bitcoin company vault wallet that will be used to fund the company derived from the BIP-85 seed. (5 points)
We created a single BIP-85 wallet with pass phrase `trap chest ... ... ... ... ... ... ... ...`

We then used derived a BIP-39 wallet mnemonic with Index 0, becoming our fundraising wallet that we used for the next few challenges.

---

###### Step 3 -- Raise funds on your fundraising Bitcoin wallet, which is also set up from the BIP-85 wallets, and get funded from the angel investor at the Blockfinance ECO AG booth. To receive your angel investment, you need to sign a message from one of your addresses in your Bitcoin fundraising wallet and send it to the Blockfinance ECO AG team on Discord or personally. Use the  [https://github.com/Blockfinance-ECO/Bitcoin-Value-Assert](https://github.com/Blockfinance-ECO/Bitcoin-Value-Assert)  tool to create the timestamp and message of your fundraising Bitcoin wallet. (10 points)

We sent our Angel Investor proof of a specific wallet being ours through our data and QR code: `https://i.imgur.com/ZpaeRu8.jpg`
![image](https://user-images.githubusercontent.com/47680931/227306927-629dbd9e-5d90-4df4-861d-432d9b723634.png)


```py
bitcoin_address: "3FcKtQqbAx13LowQQvmC29QaWXs5mmk9Gu"
message: "Hello world!"
application: "Hash Game Store"
timestamp: "1679540120"
purpose: "Angel Investment"
nounce: "0d209ddd3982274a5203e6d42ef173714aa472192c01641f351a7a23fbfba9f7"
```
**Hash**: c498ba920fd3e4d41ae102cd6a9a746bab0d8ced02cadf7cb8ea6cb2fae0a855
**Derived Key**: 739b34c2494bff2d7e36c89269ecf360f1d11b28e4fd1ee71856d3f052c287b7

---

###### Step 4 -- Ensure you run your Bitcoin node with API access and txindex=1 in your bitcoin.conf file. (10 points)

We set up the node as it can be seen on the laptop.

---

###### Step 5 -- Set up your Bitcoin Payment Server (BTCPay) and connect it to your own Bitcoin node

We set up the BTCPay Server in a docker and it can be seen running in the following steps.

---

###### Step 6 -- Create your first invoice and send the link to Blockfinance ECO AG staff for review (3 points). Use 5€ as the total payment amount.
![image](https://user-images.githubusercontent.com/47680931/227307657-48beff77-5e24-4e2b-93f5-cb143fe3ce14.png)


---

###### Step 7 -- Access the API of the Bitcoin payment server and write a wrapper in a scripting language of your choice or set up a small website to: Set up a product for sale; Generate an automated invoice using the API for this product; Check if the invoice was paid, save everything related to the payment in a local database of your choice; Automatically move 75% of the invoice money to your company vault wallet. (https://docs.btcpayserver.org/CustomIntegration/, https://docs.btcpayserver.org/API/Greenfield/v1/)

All of this behaviour can be seen in `\server\schemas.py` and `\server\app.py` - We set up a Flask instance that stores **videogame access keys**, **users**, and even features a **back-office for generating Mnemonics for the employees of the company**. When a game is bought, 75% of its value is instead sent to the 'vault' address of our company. We were asked to store all of the invoice data should be stored in a local database, but we realized the BTCPAY API actually stores all of the invoices automatically so we instead just feature a query to this specific endpoint.

![Screenshot from 2023-03-24 09-52-07](https://user-images.githubusercontent.com/47680931/227471291-5b6f531b-368a-466b-8c78-9bbfc31e3f17.png)

![Screenshot from 2023-03-24 09-52-36](https://user-images.githubusercontent.com/47680931/227471992-2a1d7167-bd57-4751-b20d-f7c0e179c747.png)

When the player buys a game, we use an API request to create an invoice. Then, we use two separate webhooks to process whether or not the transaction has been paid and to issue the actual ownership of the game.

The webhook that processes the payment then forwards 75% of the BTC received to the vault account.

Uniquely to our store, there is also a **resale marketplace**. If a player buys from the community, those 75% will instead be refunded to the original owner of the gamer whose copy was sold.

Instead of using a local database to get a list of invoices, we instead used the Greenfield API's built-in feature to check for all invoice and relevant information. In the metadata we also include which player and game were associated with each transaction, and even which player sold the copy of the game (if applicable).

---

###### Step 8 -- Provide accounting statements of all your Bitcoin wallets using the Bitcoin wallet of choice or the CryptoWorkspace with the transaction lookups and CSV exports. Add additional metadata to each transaction for your accountant to understand each transaction. (5 points)

The accounting statements were obtained through the CryptoWorkspace using the Address Lookup functionality. We opted to include both the PDF exports and the CSV.

---

###### Step 9 -- Extract the hidden message in the Bitcoin Genesis Block (https://en.bitcoin.it/wiki/Genesis_block) using your Bitcoin node. (5 points)

Block Data:
```
oem@BFECO-02:/opt/bitcoind/bin$ ./bitcoin-cli -rpcuser=bitcoin -rpcpassword=bitcoin getblockhash 0
000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
oem@BFECO-02:/opt/bitcoind/bin$ ./bitcoin-cli -rpcuser=bitcoin -rpcpassword=bitcoin getblock 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f 2

{
  "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
  "confirmations": 782163,
  "height": 0,
  "version": 1,
  "versionHex": "00000001",
  "merkleroot": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
  "time": 1231006505,
  "mediantime": 1231006505,
  "nonce": 2083236893,
  "bits": "1d00ffff",
  "difficulty": 1,
  "chainwork": "0000000000000000000000000000000000000000000000000000000100010001",
  "nTx": 1,
  "nextblockhash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
  "strippedsize": 285,
  "size": 285,
  "weight": 1140,
  "tx": [
    {
      "txid": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
      "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
      "version": 1,
      "size": 204,
      "vsize": 204,
      "weight": 816,
      "locktime": 0,
      "vin": [
        {
          "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
          "sequence": 4294967295
        }
      ],
      "vout": [
        {
          "value": 50.00000000,
          "n": 0,
          "scriptPubKey": {
            "asm": "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f OP_CHECKSIG",
            "desc": "pk(04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f)#vlz6ztea",
            "hex": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac",
            "type": "pubkey"
          }
        }
      ],
      "hex": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000"
      }
  ]
}

oem@BFECO-02:/opt/bitcoind/bin$ echo "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000" | xxd -r -p
����M��EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks�����*CAg����UH'g�q0�\֨(�9  �yb��a޶I��?L�8��U���\8M��
```

Decoded Message: `The Times 03/Jan/2009 Chancellor on brink of second bailout for banks`

---

###### Step 10 -- Write a script that looks for Bitcoin messages in every other Bitcoin block. (5 points)

This is done in `\server\listener.py`. We listen to the latest 10 blocks and then activate a scanner that is constantly looking for new incoming blocks to read out. This is the output:

```
Starting from 10 blocks behind...

<#> Block Height 782168 --------------- <#>
    Transaction fbf9c0af8088a730eec8d91f3702a50b8219473a503a2006fd25ed933677b4e8 contains messages:
        > =:BNB.BNB:bnb1nsjz09w9luhgd2csv0eg7jxy9f9m7epf2ksg52:14848602:te:0
    Transaction 46de97e4fd59195b3d1fcfb887b8f253c1f99f8f730aa900f158fce7694dfbb9 contains messages:
        > =:ETH.ETH:0xFB1bf28eF42e35fCe73538D78BFB3Fc159927A81:3991298::0
    Transaction ba14fa3b285309a53cf8153ad4190786e0d594608555ecabff555979c730b6f9 contains messages:
        > =:ETH.ETH:0xF36776d5D4EFd1d92253cA47879aCb0F3ff3D547:8797303::0
    Transaction 59b3c15a5c1a23f99a8b7768f985e38ce09341061ac5fb37c4e83459292980c6 contains messages:
        > =:BNB.BUSD-BD1:bnb1k9thwlfqfsu40cr4zrq6jld5emgu7lr9ta00c5:39291380785::0
<#> Block Height 782169 --------------- <#>
    Transaction 0eea058ab67f2fe216aec9044181f5f4bd652e24d85e92ec1db65b703b94b1e6 contains messages:
        > +:BTC/BTC::bc1q3f787hr38pmal87yxtpq8tng09q60ljjqqd759:0
    Transaction 223ef1168b8c1ed8a52b82f284c788efbc9ae7fb8219668e9c5d4315ee8ebd04 contains messages:
        > REFUND:4C0C5543A19CD605E58DF360B36E182D5B54B258312FE4FD05B02D4DF75B3364
    Transaction 4ca4520c66c94db2685276f3b2b1030e337fc40ebd7c052e61b0d0a22b70136a contains messages:
        > REFUND:BA14FA3B285309A53CF8153AD4190786E0D594608555ECABFF555979C730B6F9
<#> Block Height 782170 --------------- <#>
<#> Block Height 782171 --------------- <#>
    Transaction 05267d25efe965a5c0210f19c524f9ba7fc09bfc6b41d236926ffa416582bc22 contains messages:
        > =:ETH.ETH:0xAAe24Fb18c49bC4034EEb2081B160bE1c40AF425:6116969::0
```

---

###### Step 11 -- Create one paperwallet for a newborn baby of one of your employees. (don’t fund it , just create one with a greeting card) (5 points)

![image](https://user-images.githubusercontent.com/47680931/227311856-437c6d1e-a2a9-4ccd-8da6-1d7794afda06.png)

---

###### Step 12 -- Participants should make sure to acquire the necessary documentation for onboarding with the designated Bitcoin exchange, CryptoBus, to buy or sell Bitcoin for Swiss Francs. They should approach the exchange during the Hack-Challenge and provide their company name to begin the onboarding process. It is important to inquire with the exchange regarding any specific requirements for onboarding. You need to independelty look for the CryptoBus to get a chance for onboarding. (15 points)

After approaching the exchange during the Hack-Challenge, and providing our company name, there were two requirements requested by the exchange: A source of funds for our wallet, and a proof of ownership of the wallet. We obtained the first one through the functionality Address Lookup in the CryptoWorkspace and the NonBlacklist certificate. Using the CryptoWorkspace, this task was significantly easier than using traditional methods. All of the files mentioned above can be found in the git repo.

---

###### Step 13 -- Be creative surprise us and show how it adds value (5 points).

Right now, Steam and other big gaming platforms are fully centralized and can go down at any moment (like Google's platform, Stadia), meaning gamers can lose their games at any moment and not be able to download them anymore.
By decentralizing both the payment method and the file distribution system (all files are stored in IPFS), we have actually made it so that players can buy games and own them permantently, even if they don't have enough space in their computer to store all their games at once. If they've purchased the game, they'll forever have the link and don't need to concern themselves.


