from datetime import datetime
from discord import Role
from discord.channel import TextChannel
from discord.ext import commands
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


class BotChannelOnly(commands.CheckFailure):
    pass


class CodeChannelOnly(commands.CheckFailure):
    pass


def is_in_bot_channel(ctx) -> bool:
    if ctx.channel.id in CONFIG['CHANNEL_BOT'].values():
        return True

    raise BotChannelOnly


def is_in_code_channel(ctx) -> bool:
    if ctx.channel.id == CONFIG['CHANNEL_CODE']:
        return True

    raise CodeChannelOnly


def is_in_code_or_bot_channel(ctx) -> bool:
    if ctx.channel.id in CONFIG['CHANNEL_BOT'].values():
        return True

    if ctx.channel.id == CONFIG['CHANNEL_CODE']:
        return True

    raise BotChannelOnly


class EscapeNotStarted(commands.CheckFailure):
    pass


class EscapeEnded(commands.CheckFailure):
    pass


def is_escape_running(_):
    now = datetime.now()
    start_time = datetime.fromisoformat(CONFIG['ESCAPE_START'])
    end_time = datetime.fromisoformat(CONFIG['ESCAPE_END'])

    if now < start_time:
        raise EscapeNotStarted

    if now >= end_time:
        raise EscapeEnded

    return True


class ScoreboardFrozen(commands.CheckFailure):
    pass


def is_scoreboard_available(_):
    now = datetime.now()
    frozen_time = datetime.fromisoformat(CONFIG['ESCAPE_FROZEN'])

    if now >= frozen_time:
        raise ScoreboardFrozen

    return True
