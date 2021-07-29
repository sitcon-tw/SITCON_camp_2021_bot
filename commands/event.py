import discord
from discord.ext import commands
import json

from core.classes import Cog_extension
from database import db
from utils import get_group_id_by_role
import message

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)


class Event(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print(">>SITCON camp Ready!<<")

        # get all group roles
        group_roles = [jdata[f'CHANNEL_ROLE_{i}'] for i in range(1, 10)]
        all_roles = [role for guild in self.bot.guilds for role in guild.roles]

        roles = list(filter(lambda role: role.id in group_roles, all_roles))
        self.roles = sorted(roles, key=lambda val: group_roles.index(val.id))

        # get group reactions
        self.emojis = [jdata[f'CHANNEL_EMOJI_{i}'] for i in range(1, 10)]

        # send banner
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        self.group_selection_message = await channel.send(message.BANNER)
        for emoji in self.emojis:
            await self.group_selection_message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(message.MEMBER_JOINED.format(member=member))
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        await channel.send(message.MEMBER_JOINED.format(member=member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(message.MEMBER_QUIT.format(member=member))
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        await channel.send(message.MEMBER_QUIT.format(member=member))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # 檢查指令是否有自己的 error handler，如果有就略過
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(message.COMMAND_PARAMETER_REQUIRED)
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(message.COMMAND_NOT_FOUND)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        # 藉由反應分身分組，需要再根據伺服器 emoji 與身分組 id 到 setting.json 去設定
        user = data.member
        if user.bot:
            return

        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))

        # if member already has one role, remove it and do nothing
        roles = list(set(user.roles).intersection(self.roles))
        if len(roles) == 1:
            await channel.send(message.ROLE_ALREADY_EXISTS.format(mention=user.mention, role_name=roles[0].name))
            await self.group_selection_message.remove_reaction(emoji=data.emoji, member=user)
            return

        group_id = self.emojis.index(data.emoji.name) + 1

        guild = self.bot.get_guild(data.guild_id)
        role = guild.get_role(jdata[f'CHANNEL_ROLE_{group_id}'])
        await user.add_roles(role)
        await channel.send(message.ROLE_ADDED.format(mention=user.mention, role_name=role.name))
        await self.group_selection_message.remove_reaction(emoji=data.emoji, member=user)

    @commands.command()
    async def hello(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f'Hello, {member.name}!')

    @commands.command()
    async def use(self, ctx, ticket: str):
        author_roles = ctx.author.roles

        # ensure there are only one role for author
        # TODO: remove it since we already ensure that every member has only one role
        roles = list(set(author_roles).intersection(set(self.roles)))
        if len(roles) == 0:
            await ctx.send(message.ROLE_NOT_EXISTS)
            return

        if len(roles) != 1:
            await ctx.send(message.ROLE_TOO_MANY)
            return

        group_id = get_group_id_by_role(roles[0])

        res, err = db.use_point_code(ticket, group_id)
        if err is not None:
            if err == 'not exists':
                await ctx.send(message.CODE_NOT_EXISTS)
            elif err == 'used':
                await ctx.send(message.CODE_USED)
            else:
                await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.POINT_ADDED.format(group=group_id, point=res))

    @commands.command()
    @commands.has_any_role('管理員')  # TODO: allowed roles
    async def gen(self, ctx, point: int, amount: int):
        res, err = db.gen_point_code(point, amount)
        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.CODE_GENERATED.format(amount=amount, point=point, codes='\n'.join(res)))

    @commands.command()
    @commands.has_any_role('管理員')  # TODO: allowed roles
    async def delete(self, ctx, code: str):
        _, err = db.delete_point_code(code)
        if err is not None:
            if err == 'used':
                await ctx.send(message.CODE_USED)
            else:
                await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.CODE_DELETED.format(code=code))

    @commands.command()
    #  @commands.has_any_role() # TODO: who can see the rank?
    async def rank(self, ctx):
        res, err = db.get_group_point()
        if err is not None:
            await ctx.send(message.UNKNOWN_ERROR)
        else:
            await ctx.send(message.RANK_TABLE.format(table=res))


def setup(bot):
    bot.add_cog(Event(bot))
