import duo_client

def authenticate_intent():
    try:
        auth_client = duo_client.Auth(
            ikey='DI2915C2QQOW6T1TAOBU',
            skey='QsufyeqbDYdI5Sh4EMkroCorfcANCMMoF3E5F10l',
            host="api-53df2292.duosecurity.com",
        )
        status = auth_client.auth(device="auto",factor="push",username="amar")
        return status['status']
    except:
        return "deny"

if __name__ == "__main__":
    authenticate_intent()