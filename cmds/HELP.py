import discord
from discord.ext import commands
from discord.ui import Select,View
import asyncio,random
from datetime import datetime
from core.classes import Cog_Extension
import function.help_source as help_source


class HELP(Cog_Extension):
        
    @commands.hybrid_command(name="help")
    async def help_command(self, ctx: commands.Context) -> None:
        view=help_source.Myselect()
        await ctx.send(embed=help_source.main_help_embed,view=view)


async def setup(bot):
    await bot.add_cog(HELP(bot))    