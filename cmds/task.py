import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime
import requests

class task(Cog_Extension):
    def __init__(self,*args,**kwargs):            #init-->case初始化設定
        super().__init__(*args,**kwargs)          #super()-->父類別(Cog_Extension)(繼承概念)
    
    async def setup_hook(self) -> None:
        self.bot.bg_task=self.bot.loop.create_task(self.channel_task())
    
    async def on_ready(self):
        print("Online")

    async def channel_task(self):
        await self.bot.wait_until_ready()
        with open("setting.json","r") as f:
            time=f["time"]
            msg=f["time_task_msg"]
            channel=self.bot.get_channel(f["time_task_channel"])
        while not self.bot.is_closed():
            await channel.send(msg)
            await asyncio.sleep(10)

    
    

    
class task_command(Cog_Extension):
    @commands.command()
    async def set_task_channel(self,ctx,ch):
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
        jdata['time_task_channel']=ch
        with open('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata,jfile,indent=4)
        channel = self.bot.get_channel(int(jdata['time_task_channel']))
        await ctx.send(f'Set Channel:{channel.mention}') #mention ->tag

    @commands.command()
    async def set_task_time(self,ctx,time):
        self.counter=0
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
        jdata['time']=time
        with open('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata,jfile,indent=4)
        await ctx.send(f"成功設定Task時間為{time}")

    @commands.command()
    async def set_task_msg(self,ctx,msg):
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
        jdata['task_send_msg']=msg
        with open('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata,jfile,indent=4)
        await ctx.send("成功重設time_task訊息")

async def setup(bot):
    await bot.add_cog(task(bot))