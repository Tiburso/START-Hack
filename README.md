# Hash Game Store - START Hack Report
**Hash Game Store** is an online videogame store that allows developers to reach more players in a decentralized manner and gives users true ownership of their games via **cryptocurrency payment methods** and **InterPlanetary File System, peer-to-peer** file distribution.  

# Challenge - BLOCKFINANCE EGO AG

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

###### Step 5 -- Set up your Bitcoin Payment Server (BTCPay) and connect it to your own Bitcoin node

We set up the BTCPay Server in a docker and it can be seen running in the following steps.

###### Step 6 -- Create your first invoice and send the link to Blockfinance ECO AG staff for review (3 points). Use 5€ as the total payment amount.
![image](https://user-images.githubusercontent.com/47680931/227307657-48beff77-5e24-4e2b-93f5-cb143fe3ce14.png)

###### Step 7 -- Access the API of the Bitcoin payment server and write a wrapper in a scripting language of your choice or set up a small website to: Set up a product for sale; Generate an automated invoice using the API for this product; Check if the invoice was paid, save everything related to the payment in a local database of your choice; Automatically move 75% of the invoice money to your company vault wallet. (https://docs.btcpayserver.org/CustomIntegration/, https://docs.btcpayserver.org/API/Greenfield/v1/)

All of this behaviour can be seen in `\server\schemas.py` and `\server\app.py` - We set up a Flask instance that stores **videogame access keys**, **users**, and even features a **back-office for generating Mnemonics for the employees of the company**. When a game is bought, 75% of its value is instead sent to the 'vault' address of our company. This can all be seen in the following pictures:



###### 
