from os import urandom

def gen_code() -> str:
    return urandom(16).hex()

