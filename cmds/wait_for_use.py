import discord
import json
import random,os,asyncio
from random import randrange
from discord.ext import commands
from core.classes import Cog_Extension
import function.func as func
import time


    
class wait_for_use(Cog_Extension):
    pass


async def setup(bot):
    await bot.add_cog(wait_for_use(bot))
