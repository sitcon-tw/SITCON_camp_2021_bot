from discord.ext import commands

import os
from core.classes import Cog_extension
from utils import is_in_code_channel


class Manage(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>Manage Ready!<<')

    @commands.command()
    @commands.check(is_in_code_channel)
    async def load(self, ctx, extension):
        if os.path.isfile(f'./commands/{extension}.py'):
            self.bot.load_extension(f'commands.{extension}')
            await ctx.send(f'loaded extension \'{extension}\'!')
        else:
            await ctx.send(f'extension \'{extension}\' not found!')

    @commands.command()
    @commands.check(is_in_code_channel)
    async def unload(self, ctx, extension):
        if os.path.isfile(f'./commands/{extension}.py'):
            self.bot.unload_extension(f'commands.{extension}')
            await ctx.send(f'unloaded extension \'{extension}\'!')
        else:
            await ctx.send(f'extension \'{extension}\' not found!')

    @commands.command()
    @commands.check(is_in_code_channel)
    async def reload(self, ctx, extension):
        if os.path.isfile(f'./commands/{extension}.py'):
            self.bot.reload_extension(f'commands.{extension}')
            await ctx.send(f'reloaded extension \'{extension}\'!')
        else:
            await ctx.send(f'extension \'{extension}\' not found!')


def setup(bot):
    bot.add_cog(Manage(bot))
