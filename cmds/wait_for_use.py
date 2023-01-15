import discord
import json
import random,os,asyncio
from random import randrange
from discord.ext import commands
from core.classes import Cog_Extension
import function.func as func
import time


with open('setting.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    jdata = json.load(jfile)

    
class wait_for_use(Cog_Extension):
    
    @commands.command()
    async def ss(self,ctx):
        mes=await ctx.send("aa")
        await mes.add_reaction('⬆️')
        await mes.edit(content="成功")
        rea,user=await self.bot.wait_for("reaction_add")
        await mes.remove_reaction(rea.emoji,user)
        print(rea.emoji)
               
def setup(bot):
    bot.add_cog(wait_for_use(bot))
