from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError


def sendPayment(destinationId="GA2C5RFPE6GCKMY3US5PAB6UZLKIGSPIUKSLRB6Q723BM2OARMDUYEJ5",
                amountToSend=10,
                transactionMessage="Test Transaction"):
    server = Server("https://horizon-testnet.stellar.org")
    secretStellarKeyFile = open("StellarFunctional/keys/secretStellarKey", "w")
    source_key = Keypair.from_secret(secretStellarKeyFile.read())

    # First, check to make sure that the destination account exists.
    # You could skip this, but if the account does not exist, you will be charged
    # the transaction fee when the transaction fails.
    try:
        server.load_account(destinationId)
    except NotFoundError:
        # If the account is not found, surface an error message for logging.
        raise Exception("The destination account does not exist!")

    # If there was no error, load up-to-date information on your account.
    source_account = server.load_account(source_key.public_key)

    # Let's fetch base_fee from network
    base_fee = server.fetch_base_fee()

    # Start building the transaction.
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,  # Test version
            base_fee=base_fee,
        )
            # Because Stellar allows transaction in many currencies, you must specify the asset type.
            # Here we are sending Lumens.
            .append_payment_op(destination=destinationId, asset=Asset.native(), amount=str(amountToSend))
            # A memo allows you to add your own metadata to a transaction. It's
            # optional and does not affect how Stellar treats the transaction.
            .add_text_memo(transactionMessage)
            # Wait a maximum of three minutes for the transaction
            .set_timeout(10)
            .build()
    )

    # Sign the transaction to prove you are actually the person sending it.
    transaction.sign(source_key)

    try:
        # And finally, send it off to Stellar!
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}")
