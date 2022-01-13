import jwt


# (1)
def getEmbeddedWalletUrl():
    pass


# (2)
def getAppDefinerUrl():
    pass


# (3)
def openIFrame():
    pass


# (5), (11)
def getDefinedUrl():
    pass


# (6), (12)
def performRequestOnATWallet():
    pass


# indirect function
def encodeJWT(app_guid=""):
    encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    return encoded_jwt


encodeJWT(input())
