#導入 Discord.py
import discord
from discord.ext import commands
from discord.ui import Select,View
import json
from datetime import datetime
from discord.commands import Option
import random,os,asyncio,sys

with open('setting.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(help_command=None,command_prefix='*',intents = intents)

@bot.event
async def on_ready():
    game = discord.Game(F"developed by hesperus")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f"哈囉，又見面了!")

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Load {extension} done.')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Unload {extension} done.')

@bot.command()
async def reload(ctx,extension):
        bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reload {extension} done.')



for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cmds.{filename[:-3]}')
            print(f'✅   已加載 {filename}')
        except Exception as error:
            print(f'❎   {filename} 發生錯誤  {error}')
if __name__ == "__main__":
    bot.run(jdata['TOKEN'])