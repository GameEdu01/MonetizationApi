# stellar-sdk >= 2.0.0 required
# create a completely new and unique pair of keys
# see more about KeyPair objects: https://stellar-sdk.readthedocs.io/en/latest/api.html#keypair
# The SDK does not have tools for creating test accounts, so you'll have to
# make your own HTTP request.
# if you're trying this on Python, install the `requests` library.

"""Create Account A valid keypair, however, does not make an account: in order to prevent unused accounts from
bloating the ledger, Stellar requires accounts to hold a minimum balance of 1 XLM before they actually exist. Until
it gets a bit of funding, your keypair doesn't warrant space on the ledger.

On the public network, where live users make live transactions, your next step would be to acquire XLM, which you can
do by consulting our lumen buying guide. Because this tutorial runs on the test network, you can get 10,000 test XLM
from Friendbot, which is a friendly account funding tool.

To do that, send Friendbot the public key you created. It’ll create and fund a new account using that public key as
the account ID.

Now for the last step: getting the account’s details and checking its balance. Accounts can carry multiple
balances — one for each type of currency they hold.

Stellar uses public key cryptography to ensure that every transaction is secure: every Stellar account has a keypair
consisting of a public key and a secret key. The public key is always safe to share — other people need it to identify
your account and verify that you authorized a transaction. It’s like an email address. The secret key, however, is
private information that proves you own — and gives you access to — your account. It’s like a password, and you
should never share it with anyone."""

from stellar_sdk import Server
from stellar_sdk import Keypair

import requests


def StellarBalance():
    server = Server("https://horizon-testnet.stellar.org")
    publicStellarKeyFile = open("StellarFunctional/keys/publicStellarKey", "r")

    public_key = publicStellarKeyFile.read()
    account = server.accounts().account_id(public_key).call()
    for balance in account['balances']:
        print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")


# Test environment, real require Lumens
def RegisterStellarAccount():
    publicStellarKeyFile = open("StellarFunctional/keys/publicStellarKey", "r")

    public_key = publicStellarKeyFile.read()
    response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
    if response.status_code == 200:
        print(f"SUCCESS! You have a new account :)\n{response.text}")
    else:
        print(f"ERROR! Response: \n{response.text}")


def KeyPairGen():
    pair = Keypair.random()
    publicStellarKeyFile = open("StellarFunctional/keys/publicStellarKey", "w")
    secretStellarKeyFile = open("StellarFunctional/keys/secretStellarKey", "w")

    secretStellarKeyFile.write(pair.secret)
    publicStellarKeyFile.write(pair.public_key)

    secretStellarKeyFile.close()
    publicStellarKeyFile.close()


def main():
    KeyPairGen()
    RegisterStellarAccount()
    StellarBalance()


if __name__ == "__main__":
    main()
