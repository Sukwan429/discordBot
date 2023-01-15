import discord
import json
import random,os,asyncio
from discord.ext import commands
from core.classes import Cog_Extension



class rule(Cog_Extension):
    @commands.group()
    async def rule(self,ctx):
        pass
    @rule.command()
    async def chess(self,ctx):
        await ctx.send()

def setup(bot):
    bot.add_cog(rule(bot))