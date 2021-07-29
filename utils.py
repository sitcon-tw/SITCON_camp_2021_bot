from discord import Role
from os import urandom
import json


def gen_code() -> str:
    return urandom(16).hex()


def get_group_id_by_role(role: Role) -> int:
    with open('setting.json', mode='r', encoding='utf-8') as jfile:
        jdata = json.load(jfile)

    for i in range(1, 11):
        if jdata[f'CHANNEL_ROLE_{i}'] == int(role.id):
            return i

    return 0

