import asyncio,random,json,discord
from discord.ext import commands
from core.classes import Cog_Extension
class pet(Cog_Extension):
    pass
def setup(bot):
    bot.add_cog(pet(bot))