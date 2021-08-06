from discord.ext import commands

from core.classes import Cog_extension
from utils import is_in_bot_channel


class Escape(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>Escape Ready!<<')

    @commands.command()
    @commands.check(is_in_bot_channel)
    async def solve(self, ctx, task_id: str, *, password: str):
        '''
        Log every single submission into database

        Trigger hint if the submitted password is close enough
        '''
        pass

    @commands.command()
    @commands.check(is_in_bot_channel)
    async def status():
        '''
        Show solving status of current group
        '''
        pass

    # TODO: a command for admin to get current solving status of every group?


def setup(bot):
    bot.add_cog(Escape(bot))
