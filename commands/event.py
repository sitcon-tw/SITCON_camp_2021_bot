import discord 
from discord.ext import commands
import json

from core.classes import Cog_extension
from database import db

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)


class Event(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print(">>SITCON camp Ready!<<")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} left!')
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        #藉由關鍵字觸發功能檢查學員给出的序號是否合法
        guild = msg.guild

        # 把組別的身分組序號存成 list 方便使用、辨別
        groups = []
        for i in range(1,11):
            #print(int(jdata[f'CHANNEL_ROLE_{i}']))
            groups.append(guild.get_role(int(jdata[f'CHANNEL_ROLE_{i}'])))
            #print(i, groups[i-1])

        if msg.content == '測試' and msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            
            flag = False
            if guild.get_role(int(jdata['CHANNEL_ROLE_1'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第一組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_2'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第二組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_3'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第三組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_4'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第四組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_5'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第五組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_6'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第六組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_7'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第七組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_8'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第八組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_9'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第九組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_10'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第十組的身分組')
            if flag == False:
                await msg.channel.send('沒有組別喔QwQ')

        elif msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            res, err = db.use_point_code(msg.content, 1) # TODO: user group

            if err is not None:
                if err == 'not exists':
                    await msg.channel.send('輸入的序號有錯喔QQ')
                elif err == 'used':
                    await msg.channel.send('這序號已經使用過囉！')
                else:
                    await msg.channel.send('發生了點錯誤')
            else:
                await msg.channel.send(f'葛萊芬多加 {res} 分！')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #檢查指令是否有自己的 error handler，如果有就略過
        if hasattr(ctx.command, 'on_error'):
            return
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('還需要補上參數喔QwQ')
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send('沒有這個指令耶QwQ')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        # 藉由反應分身分組，需要再根據伺服器 emoji 與身分組 id 到 setting.json 去設定
        guild = self.bot.get_guild(data.guild_id)
        if str(data.emoji) == jdata['CHANNEL_EMOJI_1']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_1'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_2']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_2'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_3']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_3'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_4']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_4'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_5']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_5'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_6']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_6'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_7']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_7'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_8']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_8'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_9']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_9'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_10']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_10'])))

        # 辨別是否是可以使用的分數兌換碼，如果是，學員按完反應就給學員所在小組加分數
        # TODO

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        # 藉由取消反應來刪除身分組，需要再根據伺服器 emoji 與身分組 id 到 setting.json 去設定
        guild = self.bot.get_guild(data.guild_id)
        user = guild.get_member(data.user_id)
        if str(data.emoji) == jdata['CHANNEL_EMOJI_1']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_1'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_2']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_2'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_3']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_3'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_4']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_4'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_5']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_5'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_6']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_6'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_7']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_7'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_8']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_8'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_9']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_9'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_10']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_10'])))
    

def setup(bot):
    bot.add_cog(Event(bot))
