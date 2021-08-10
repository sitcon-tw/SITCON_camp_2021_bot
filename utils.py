from discord import Role
from discord.channel import TextChannel
from discord.guild import Guild
from os import urandom

from config import CONFIG


def gen_code() -> str:
    return urandom(16).hex()


def get_group_id_by_role(role: Role) -> int:
    try:
        return {v: k for k, v in CONFIG['CHANNEL_ROLE'].items()}[int(role.id)]
    except:
        return 0


def get_group_id_by_bot_channel(channel: TextChannel) -> int:
    try:
        return {v: k for k, v in CONFIG['CHANNEL_BOT'].items()}[int(channel.id)]
    except:
        return 0


def get_group_id_by_guild(guild: Guild):
    try:
        return {v: k for k, v in CONFIG['SERVER'].items()}[int(guild.id)]
    except:
        return 0


def is_in_bot_channel(ctx) -> bool:
    return ctx.channel.id in CONFIG['CHANNEL_BOT'].values()


def is_in_code_channel(ctx) -> bool:
    return ctx.channel.id == CONFIG['CHANNEL_CODE']
