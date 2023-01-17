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

    @commands.slash_command(description="設置反應身分組")
    async def reaction_role(self,ctx,
                        內容: Option(str, "嵌入訊息內容"),
                        role: Option(discord.Role, "要領取的身分組"),
                        emoji: Option(discord.PartialEmoji, "要添加的反應")):  # 斜線指令選項
        await ctx.defer()  # 延遲回覆
        if not ctx.author.guild_permissions.administrator:  # 如果使用者沒管理權限
            await ctx.respond("只有管理員能使用此指令")
            return  # 結束運行
        embed = discord.Embed(title="領取身分組", description=內容)
        message = await ctx.send(embed=embed)  # 傳送領取訊息
        await message.add_reaction(emoji)  # 加入第一個反應
        with open("database/role.json", "r") as file:  # 用閱讀模式開啟資料儲存檔案
            data = json.load(file)  # data = 資料裡的字典{}
        with open("database/role.json", "w") as file:  # 用write模式開啟檔案
            data[str(message.id)] = {"role": role.id, "emoji": emoji.id}  # 新增字典資料
            json.dump(data, file, indent=4)  # 上載新增後的資料
        await ctx.respond("設置完畢", delete_after=3)


def setup(bot):
    bot.add_cog(react(bot))