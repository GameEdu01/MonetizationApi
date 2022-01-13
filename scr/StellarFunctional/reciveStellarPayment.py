from stellar_sdk import Server


def load_last_paging_token():
    # Get the last paging token from a local database or file
    return "now"


def save_paging_token(paging_token):
    # In most cases, you should save this to a local database or file so that
    # you can load it next time you stream new payments.
    pass


def receiveStellarPayment():
    server = Server("https://horizon-testnet.stellar.org")
    account_id = "GC2BKLYOOYPDEFJKLKY6FNNRQMGFLVHJKQRGNSSRRGSMPGF32LHCQVGF"

    # Create an API call to query payments involving the account.
    payments = server.payments().for_account(account_id)

    # If some payments have already been handled, start the results from the
    # last seen payment. (See below in `handle_payment` where it gets saved.)
    last_token = load_last_paging_token()
    if last_token:
        payments.cursor(last_token)

    # `stream` will send each recorded payment, one by one, then keep the
    # connection open and continue to send you new payments as they occur.
    for payment in payments.stream():
        # Record the paging token so we can start from here next time.
        save_paging_token(payment["paging_token"])

        # We only process `payment`, ignore `create_account` and `account_merge`.
        if payment["type"] != "payment":
            continue

        # The payments stream includes both sent and received payments. We
        # only want to process received payments here.
        if payment['to'] != account_id:
            continue

        # In Stellar’s API, Lumens are referred to as the “native” type. Other
        # asset types have more detailed information.
        if payment["asset_type"] == "native":
            asset = "Lumens"
        else:
            asset = f"{payment['asset_code']}:{payment['asset_issuer']}"
        print(f"{payment['amount']} {asset} from {payment['from']}")
