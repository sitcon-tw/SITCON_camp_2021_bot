from datetime import datetime
from discord.ext import commands

from config import CONFIG
from core.classes import Cog_extension
from database import db
from utils import (
    is_in_bot_channel,
    is_in_code_channel,
    is_in_code_or_bot_channel,
    get_group_id_by_bot_channel,
    BotChannelOnly,
    CodeChannelOnly,
)
import message


class Event(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>SITCON camp Ready!<<')

        # get all group roles
        group_roles = [CONFIG['CHANNEL_ROLE'][i] for i in range(1, 10)]
        all_roles = [role for guild in self.bot.guilds for role in guild.roles]

        roles = list(filter(lambda role: role.id in group_roles, all_roles))
        self.roles = sorted(roles, key=lambda val: group_roles.index(val.id))

        # get group reactions
        self.emojis = [CONFIG['CHANNEL_EMOJI'][i] for i in range(1, 10)]

        res, err = db.get_group_selection_message_id()
        channel = self.bot.get_channel(CONFIG['CHANNEL_MAINROOM'])
        if err is not None:
            if err == 'not exists':
                # send banner if message not exists
                self.group_selection_message = await channel.send(message.BANNER)
                db.store_group_selection_message_id(self.group_selection_message.id)
                for emoji in self.emojis:
                    await self.group_selection_message.add_reaction(emoji)
            else:
                await channel.send(message.UNKNOWN_ERROR)
        else:
            self.group_selection_message = await channel.fetch_message(res)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        # 藉由反應分身分組，需要再根據伺服器 emoji 與身分組 id 到 setting.json 去設定
        user = data.member
        if user.bot:
            return

        if data.message_id != self.group_selection_message.id:
            return

        # if member already has one role, remove it and do nothing
        roles = list(set(user.roles).intersection(self.roles))
        if len(roles) == 1:
            await self.group_selection_message.remove_reaction(emoji=data.emoji, member=user)
            return

        # if add emoji other than 1~9, remove them
        try:
            group_id = self.emojis.index(data.emoji.name) + 1
        except ValueError:
            await self.group_selection_message.remove_reaction(emoji=data.emoji, member=user)
            return

        guild = self.bot.get_guild(data.guild_id)
        role = guild.get_role(CONFIG['CHANNEL_ROLE'][group_id])
        await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        guild = self.bot.get_guild(data.guild_id)
        user = await guild.fetch_member(data.user_id)

        if user.bot:
            return

        if data.message_id != self.group_selection_message.id:
            return

        try:
            group_id = self.emojis.index(data.emoji.name) + 1
        except ValueError:
            return

        guild = self.bot.get_guild(data.guild_id)
        role = guild.get_role(CONFIG['CHANNEL_ROLE'][group_id])
        await user.remove_roles(role)

    @commands.command()
    @commands.check(is_in_bot_channel)
    async def use(self, ctx, code: str):
        group_id = get_group_id_by_bot_channel(ctx.channel)

        print(f'[code] group {group_id} tried to use {code}')

        res, err = db.use_point_code(code, group_id)
        if err is not None:
            if err == 'not exists':
                await ctx.send(message.CODE_NOT_EXISTS)
            elif err == 'used':
                await ctx.send(message.CODE_USED)
            else:
                await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.POINT_ADDED.format(group=group_id, point=res))
            print(f'[code] group {group_id} used {code}')

    @use.error
    async def use_error(self, ctx, error):
        if isinstance(error, BotChannelOnly):
            await ctx.send(message.GO_TO_YOUR_SERVER)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(message.COMMAND_USAGE.format(command='//use <code>'))
            return

    @commands.command()
    @commands.has_any_role('卍序號a支配者卍')
    @commands.check(is_in_code_channel)
    async def gen(self, ctx, point: int, amount: int):
        res, err = db.gen_point_code(point, amount)
        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.CODE_GENERATED.format(amount=amount, point=point, codes='\n'.join(res)))
            print(f'[code] {amount} code with {point} point have generated')

    @gen.error
    async def gen_error(self, ctx, error):
        if isinstance(error, CodeChannelOnly):
            await ctx.send(message.GO_TO_CODE_CHANNEL)
            return

        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send(message.PERMISSIONS_MISSING)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(message.COMMAND_USAGE.format(command='//gen <point> <amount>'))
            return

    @commands.command()
    @commands.check(is_in_code_channel)
    @commands.has_any_role('卍序號a支配者卍')
    async def delete(self, ctx, code: str):
        _, err = db.delete_point_code(code)
        if err is not None:
            if err == 'used':
                await ctx.send(message.CODE_USED)
            else:
                await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.CODE_DELETED.format(code=code))
            print(f'[code] {code} deleted')

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, CodeChannelOnly):
            await ctx.send(message.GO_TO_CODE_CHANNEL)
            return

        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send(message.PERMISSIONS_MISSING)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(message.COMMAND_USAGE.format(command='//delete <code>'))
            return

    @commands.command()
    @commands.check(is_in_code_or_bot_channel)
    async def rank(self, ctx):
        res, err = db.get_group_point()
        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
            return

        now = datetime.now()
        ended = datetime.fromisoformat(CONFIG['ESCAPE_END'])
        show_escape = now >= ended

        # construct table
        if show_escape:
            sort_key = lambda x: (
                x['code'] + x['escape'],
                x['code'],
                x['escape'],
                -x['group'],
            )

            table = '''```
╔═══════╤════════════╤═════════════╤═════════╗
║ Group │ Code Point │ Event Point │  Total  ║
╠═══════╪════════════╪═════════════╪═════════╣
'''
            table_delimiter = '╠═══════╪════════════╪═════════════╪═════════╣\n'
            table_row = '║   {group_id}   │ {code:^10} │ {escape:^11} │ {total:^7} ║\n'
            table_footer = '╚═══════╧════════════╧═════════════╧═════════╝```'
        else:
            sort_key = lambda x: (
                x['code'],
                -x['group'],
            )

            table = '''```
╔═══════╤════════════╤═════════╗
║ Group │ Code Point │  Total  ║
╠═══════╪════════════╪═════════╣
'''
            table_delimiter = '╠═══════╪════════════╪═════════╣\n'
            table_row = '║   {group_id}   │ {code:^10} │ {total:^7} ║\n'
            table_footer = '╚═══════╧════════════╧═════════╝```'

        res.sort(key=sort_key, reverse=True)
        for idx, data in enumerate(res):
            if idx:
                table += table_delimiter

            table += table_row.format(
                group_id=data['group'],
                code=data['code'],
                escape=data['escape'],
                total=data['code'] + data['escape'] if show_escape else data['code'],
            )

        table += table_footer

        await ctx.send(table)

    @rank.error
    async def rank_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(message.GO_TO_YOUR_SERVER)
            return

    @commands.command()
    @commands.check(is_in_code_channel)
    async def announce(self, ctx, group: str, *, msg: str):
        print(f'[announce] trying to announce to {group} with message\n<{msg}>')

        try:
            if group == 'all':
                target = CONFIG['ANNOUNCEMENT'].values()
            else:
                target = [CONFIG['ANNOUNCEMENT'][int(i)] for i in group.split(',')]

            for channel_id in target:
                channel = self.bot.get_channel(channel_id)
                await channel.send(msg)

            await ctx.send(message.ANNOUNCEMENT_SENT)
            print(f'[announce] success')

        except (KeyError, ValueError):
            await ctx.send(message.PARAMETER_TYPE_ERROR)

        except Exception as err:
            print(err)
            await ctx.send(message.UNKNOWN_ERROR)

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, CodeChannelOnly):
            await ctx.send(message.GO_TO_CODE_CHANNEL)
            return


def setup(bot):
    bot.add_cog(Event(bot))
