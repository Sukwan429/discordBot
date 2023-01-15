import discord
import json
import random,os,asyncio
from random import randrange
from discord.ext import commands
from discord.commands import Option
from core.classes import Cog_Extension
from math import *
import base64
with open('setting.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    jdata = json.load(jfile)

def Guess(n):
    tmp = random.randint(1, 5)
    a = ['false', 'true']
    s = f'right ans is {tmp}, your ans is {a[n == tmp]}'
    return s
def operation(s):
    s = s.replace(' ', '')
    s = s.replace('^', '**')
    s = s.replace('log', 'log10')
    s = s.replace('ln', 'log')
    i, t = len(s) - 1, 0
    while i >= 0: # 處理 "factorial 階乘"
        if s[i] == '!':
            if s[i - 1].isdigit():
                t, i = i, i - 1
                while s[i].isdigit():
                    i -= 1
                tmp = s[i + 1: t]
                s = s[:i + 1] + 'factorial(' + tmp + ')' + s[t + 1:]
            else:
                t, right, i = i, 1, i - 2
                while right:
                    if s[i] == ')':
                        right += 1
                    if s[i] == '(':
                        right -= 1
                    i -= 1
                tmp = s[i + 1:t]
                s = s[:i + 1] + 'factorital(' + tmp + ')' + s[t + 1:]
        i -= 1
    # print(s)
    try:
        res = round(eval(s), 3)
        return res
    except:
        res = '(type error or too difficult)'
        return res
class react(Cog_Extension):
    @commands.command()
    async def ayame(seif,ctx):
        random_ayame = random.choice(jdata['ayame'])
        pic = discord.File(random_ayame)
        await ctx.send(file=pic)
        await ctx.send('@sukwanlin_429#7426')
    @commands.command()
    async def hentai(seif,ctx):
        await ctx.send('不可以瑟瑟')
    
    @commands.command()
    async def guessss(self,ctx, n : int):
        await ctx.send(Guess(n))

    @commands.command()
    async def calc(self,ctx, *, s):
        ans = operation(s)
        await ctx.send(f'result of ({s}) is {ans}')

    @commands.command()
    async def base64encode(self,ctx,*,s:str):
        await ctx.channel.purge(limit=1)
        await ctx.send(f"`{base64.b64encode(s.encode('UTF-8'))}`")



def setup(bot):
    bot.add_cog(react(bot))