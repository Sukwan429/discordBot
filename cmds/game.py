import discord
import json
import random,os,asyncio
import numpy as np
from discord.ext import commands
from core.classes import Cog_Extension
import function.func as func
import time

#TODO OOXX之已放O或X的棋盤的重複bug

class game(Cog_Extension):
    @commands.command()
    async def ynq(self,ctx,question):
        i=random.randint(0,100)
        ans=["我覺得就是了啦",f'我覺得{i}%不是',f'我覺得{i}%是',"我覺得完全不是"]
        embed=discord.Embed(title=question, description=random.choice(ans), color = discord.Colour.random())
        embed.set_thumbnail(url="")
        await ctx.send(embed=embed)

    @commands.command()
    async def dice(self,ctx):
        await ctx.send(f"{ctx.author}擲到了{random.randint(3,19)}點")

    @commands.command()
    async def pick(self,ctx,*,cho):
        q=cho.split(" ")
        await ctx.send(random.choice(q))

    @commands.command()
    async def coin(self,ctx):
        await ctx.send(f"{ctx.author}擲出了硬幣...")
        time.sleep(1)
        a=random.choice(["正面","反面"])
        await ctx.send(embed=discord.Embed(description=f"硬幣最後是落在了...{a}!",color=discord.Colour.random()))
        
    @commands.command()
    async def ooxx(self,ctx):
        await ctx.send("OOXX，請輸入數字代表格子")
        search={1:":one:",2:":two:",3:":three:",4:":four:",5:":five:",6:":six:",7:":seven:",8:":eight:",9:":nine:",10:':o:',11:':x:'}
        board=[i for i in range(1,10)]

        already=set()#已經有放東西的index
        now_player=1 #1為O-1為X
        while func.check_OOXX_win(board):
            await ctx.send(func.draw(board))
            user_in= await self.bot.wait_for('message')
            try:
                num=int(user_in.content)-1

                if now_player==1 and num<=9:
                    board[num]=10
                elif now_player==-1 and num<=9:
                    board[num]=11
            except:
                while(ord(user_in.content)<49 or ord(user_in.content)>57):
                    await ctx.send("輸入錯誤")
                    user_in= await self.bot.wait_for('message')
                num=int(user_in.content)-1
                if now_player==1 and board[num]<=9:
                    board[num]=10
                elif now_player==-1 and board[num]<=9:
                    board[num]=11
            now_player*=-1
        if now_player==-1:
            await ctx.send("O方獲勝")
        elif now_player==1:
            await ctx.send("X方獲勝")
        await ctx.send(func.draw(board))
        
    @commands.command()
    async def guess(self,ctx):
        global lowernumber
        global highernumber
        def check(number):
            return number.author == ctx.author and number.channel == ctx.message.channel
        lowernumber = 1
        highernumber = 100
        
        number = random.randint(lowernumber, highernumber)
        # print(number)
        
        await ctx.send(f'{lowernumber}~{highernumber}，任意選一個數字')
        
        for i in range(0, 100):    
            response = await self.bot.wait_for('message',check=check)
            if response.content=="stop":
                await ctx.send("終極密碼已提前結束")
                return
            try : 
                guess = int(response.content) 
            
            except:
                await ctx.send("請輸入數字")
                
            if guess == number : 
                await ctx.send(f"猜對了，共花了{i}次")
                return
                
            if guess > 100 :
                await ctx.send(f"超過{highernumber}，格式錯誤")
                
            if guess < number:
                lowernumber = guess
                await ctx.send(f"比 {lowernumber}大，比 {highernumber} 小")
                
            if guess > number :
                highernumber = guess
                await ctx.send(f"比 {lowernumber}大，比 {highernumber} 小")

    @commands.command()
    async def ab(self,ctx):

        await ctx.send(embed=discord.Embed(title="1A2B遊戲已準備完成！",description="可開始輸入數字",color=discord.Colour.random()))
        num=["0","1","2","3","4","5","6","7","8","9"]
        s=random.sample(num,4)
        def check(number):
            return number.author == ctx.author and number.channel == ctx.message.channel
        for i in range(8):
            message=await self.bot.wait_for('message',check=check)
            message=message.content
            if message=="stop":
                await ctx.send("1A2B已提前結束")
                return
            a=0
            b=0
            for j in range(4):
                if s[j]==message[j]:
                    a+=1
                elif message[j] in s:
                    b+=1
            res=str(a)+'A'+str(b)+'B'
            if a==4:
                await ctx.send('正確！')
                return
            else:
                await ctx.send(res)
                res=""
        v=""
        for x in s:
            v+=x
        await ctx.send(embed=discord.Embed(title="Oops！失敗了",description=f"正確答案為{v}",color=discord.Colour.random()))

                
            



def setup(bot):
    bot.add_cog(game(bot))