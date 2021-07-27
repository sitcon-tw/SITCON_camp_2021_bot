import discord
from discord.ext import commands
import json
import random

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)

from core.classes import Cog_extension

class React(Cog_extension):
    @commands.command()
    async def 我要圖片(self, ctx):
        random_pic = jdata['pic']
        pic = discord.File(random_pic)
        await ctx.send(file=pic)

def setup(bot):
    bot.add_cog(React(bot))
