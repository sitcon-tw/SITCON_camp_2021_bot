#  import discord
from discord.ext import commands

#  from config import CONFIG
from core.classes import Cog_extension
import message


class Misc(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>Misc Ready!<<')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(message.MEMBER_JOINED.format(member=member))
        #  channel = self.bot.get_channel(CONFIG['CHANNEL_MAINROOM'])
        #  await channel.send(message.MEMBER_JOINED.format(member=member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(message.MEMBER_QUIT.format(member=member))
        #  channel = self.bot.get_channel(CONFIG['CHANNEL_MAINROOM'])
        #  await channel.send(message.MEMBER_QUIT.format(member=member))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # 檢查指令是否有自己的 error handler，如果有就略過
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(message.COMMAND_PARAMETER_REQUIRED)
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(message.COMMAND_NOT_FOUND)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')


def setup(bot):
    bot.add_cog(Misc(bot))
