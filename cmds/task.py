import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime

class task(Cog_Extension):
    def __init__(self,*args,**kwargs):            #init-->case初始化設定
        super().__init__(*args,**kwargs)          #super()-->父類別(Cog_Extension)(繼承概念)
        self.counter=0

        async def time_task():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                now_time=datetime.datetime.now().strftime('%H%M')
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata=json.load(jfile)
                channel = self.bot.get_channel(int(jdata['time_task_channel']))
                if now_time==jdata['time']:
                    await channel.send(jdata["task_send_msg"])
                    self.counter=1
                else:
                    self.counter=0
                    pass
                await asyncio.sleep(5)    

        self.bg_task=self.bot.loop.create_task(time_task()) #創建新的背景作業
        
        
        
        
        
        """
        async def interval():
            await self.bot.wait_until_ready()
            self.channel=self.bot.get_channel(985226238509613098)
            while not self.bot.is_closed():
                await self.channel.send("Hi I'm running!")
                await asyncio.sleep(600) #單位：秒

        self.bg_task=self.bot.loop.create_task(interval()) #創建新的背景作業
        """
    
    
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

def setup(bot):
    bot.add_cog(task(bot))