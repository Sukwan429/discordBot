import discord
from datetime import datetime
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random,os,asyncio

with open('setting.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    jdata = json.load(jfile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata['call_channel']))
        await channel.send(f'{member} 嗨')

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(int(jdata['call_channel']))
        await channel.send(f'{member} 掰')

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content == '好爽':
            await msg.channel.send(f'不爽')
    #使用on_reaction_add->reaction->表情符號id user->用戶名稱

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        print(err)
        await ctx.send(err)

        


def setup(bot):
    bot.add_cog(Event(bot))    
    
    
    
    """
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,data):
        if str(data.emoji)==':yum:':
            print("有進來")
            guild=self.bot.get_guild(data.guild_id)
            role=guild.get_role(1059380906944626708)
            await data.member.add_roles(role)
    """