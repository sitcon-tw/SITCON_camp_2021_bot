import discord
from discord.ext import commands

from core.classes import Cog_extension

class Main(Cog_extension):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'... maybe {self.bot.latency} sec?')

def setup(bot):
    bot.add_cog(Main(bot))