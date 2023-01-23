
import asyncio,random,json,discord
from discord.ext import commands
from discord.ui import Select,View
from datetime import datetime
from core.classes import Cog_Extension

with open("database/gamerule.json", "r", encoding="UTF-8") as file:
    GData = json.load(file)
gm={
    "1":discord.Embed(title="2048",description=GData["2048"],color=discord.Colour.random()),
    "2":discord.Embed(title="五子棋",description=GData["chess"],color=discord.Colour.random()),
    "3":discord.Embed(title="終極密碼",description=GData["guess"],color=discord.Colour.random()),
    "4":discord.Embed(title="OOXX",description=GData["ooxx"],color=discord.Colour.random()),
    "5":discord.Embed(title="1A2B",description=GData["ab"],color=discord.Colour.random()),
    "10":discord.Embed(title="金錢系統",description=GData["money"],color=discord.Colour.random()),
    }
for i  in gm:
    gm[i].set_thumbnail(url=GData["bot_avatar_url"])
    gm[i].set_footer(text=gm[i].title)

class game_rule(View):
    @discord.ui.select(
        placeholder="點我以查看遊戲規則",
        options=[
            discord.SelectOption(label="2048",value="1"),
            discord.SelectOption(label="五子棋",value="2"),
            discord.SelectOption(label="終極密碼",value="3"),
            discord.SelectOption(label="OOXX",value="4"),
            discord.SelectOption(label="1A2B",value="5"),
            discord.SelectOption(label="金錢系統",value="10"),
            ]
    )
    async def select_callback(self,select,interaction):
        select.disabled=True
        await interaction.response.edit_message(embed=gm[select.values[0]])
class rule(Cog_Extension):
    @commands.command()
    async def gamerule(self,ctx):
        view=game_rule()
        await ctx.send(view=view)
        
    @commands.slash_command(name="gamerule",description="遊戲規則~")
    async def slash_gamerule(self,ctx):
        view=game_rule()
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(rule(bot))