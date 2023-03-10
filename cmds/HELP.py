import discord
from discord.ext import commands
from discord.ui import Select,View
import asyncio,random
from datetime import datetime
from core.classes import Cog_Extension
import function.help_source as help_source


class HELP(Cog_Extension):
    @commands.slash_command(name="help",description="查看彈力鯊鍋余頭的指令列表")
    async def slash_help(self,ctx):
        view=help_source.Myselect()
        await ctx.send(embed=help_source.main_help_embed,view=view)
    @commands.command()
    async def help(self,ctx):
        view=help_source.Myselect()
        await ctx.send(embed=help_source.main_help_embed,view=view)
        



def setup(bot):
    bot.add_cog(HELP(bot))    