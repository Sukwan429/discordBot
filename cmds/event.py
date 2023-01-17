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
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):  # 偵測到添加反應
        with open("database/role.json", "r") as file:  # 用read模式開啟檔案
            data = json.load(file)  # 讀取檔案內容
        if not str(payload.message_id) in data:  # 如果檔案裡沒有資料
            return  # 結束運行
        if data[str(payload.message_id)]["emoji"] != payload.emoji.id:  # 判斷添加的反應是否是設置的反應
            return  # 結束運行
        guild = await self.bot.fetch_guild(payload.guild_id)  # 取得群組
        role = guild.get_role(data[str(payload.message_id)]["role"])  # 取得身分組
        await payload.member.add_roles(role, reason="反應身分組系統")  # 給予身份組
        try:
            await payload.member.send(F"已給予 {role}", delete_after=10)  # 私訊給予訊息
        except:
            pass
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):  # 偵測到添加反應
        with open("database/role.json", "r") as file:  # 用read模式開啟檔案
            data = json.load(file)  # 讀取檔案內容
        if not str(payload.message_id) in data:  # 如果檔案裡沒有資料
            return  # 結束運行
        if data[str(payload.message_id)]["emoji"] != payload.emoji.id:  # 判斷添加的反應是否是設置的反應
            return  # 結束運行
        guild = await self.bot.fetch_guild(payload.guild_id)  # 取得群組
        role = guild.get_role(data[str(payload.message_id)]["role"])  # 取得身分組
        member = await guild.fetch_member(payload.user_id)
        await member.remove_roles(role, reason="反應身分組系統")  # 移除身分組
        try:
            await member.send(F"已移除 {role}", delete_after=10)  # 私訊給予訊息
        except:
            pass

        


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