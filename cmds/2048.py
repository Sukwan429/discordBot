import discord
import json
import random,os,asyncio
import numpy as np
from discord.ext import commands
from core.classes import Cog_Extension
import function.func as func

class tzfe(Cog_Extension):
    @commands.command(name='2048')
    async def TZFE(self,ctx):
        gu=[[0 for j in range(4)] for i in range(4)]
        now_block_quan=0
        score=0
        inloc=[i for i in range(16)]
        def move_right(now_block_quan,score):
            for x in range(4):
                while func.is_zero(1,gu,x):
                    for y in range(3):
                        if gu[x][y] != 0:
                            if gu[x][y + 1] == gu[x][y]:
                                gu[x][y + 1] = gu[x][y] * 2
                                gu[x][y] = 0
                                inloc.append(x*4+y)
                                now_block_quan-=1
                                score+=gu[x][y+1]
                            elif gu[x][y + 1] == 0:
                                gu[x][y + 1] = gu[x][y]
                                gu[x][y] = 0
                                inloc.append(x*4+y)
                                inloc.remove(x*4+y+1)
            return now_block_quan,score
                    

        def move_left(now_block_quan,score):
            for x in range(4):
                while func.is_zero(2,gu,x):
                    for y in range(3, 0, -1):
                        if gu[x][y] != 0:
                            if gu[x][y - 1] == gu[x][y]:
                                gu[x][y - 1] = gu[x][y] * 2
                                gu[x][y] = 0
                                now_block_quan-=1
                                inloc.append(x*4+y)
                                score+=gu[x][y-1]
                            elif gu[x][y - 1] == 0:
                                gu[x][y - 1] = gu[x][y]
                                gu[x][y] = 0
                                inloc.append(x*4+y)
                                inloc.remove(x*4+y-1)
            return now_block_quan,score
        def move_up(now_block_quan,score):
            for x in range(4):
                while func.is_zero(3,gu,x):
                    for y in range(3, 0, -1):
                        if gu[y][x]!= 0:
                            if gu[y - 1][x] == gu[y][x]:
                                gu[y - 1][x] = gu[y][x] * 2
                                gu[y][x] = 0
                                now_block_quan-=1
                                inloc.append(y*4+x)
                                score+=gu[y-1][x]
                            elif gu[y - 1][x] == 0:
                                gu[y - 1][x] = gu[y][x]
                                gu[y][x] = 0
                                now_block_quan-=1
                                inloc.append(y*4+x)
                                inloc.remove((y-1)*4+x)
            return now_block_quan,score
        def move_down(now_block_quan,score):
            for x in range(4):
                while func.is_zero(4,gu,x):
                    for y in range(3):
                        if gu[y][x]!= 0:
                            if gu[y + 1][x] == gu[y][x]:
                                gu[y + 1][x] = gu[y][x] * 2
                                gu[y][x] = 0
                                now_block_quan-=1
                                inloc.append(y*4+x)
                                score+=gu[y+1][x]
                            elif gu[y + 1][x] == 0:
                                gu[y + 1][x] = gu[y][x]
                                gu[y][x] = 0
                                now_block_quan-=1
                                inloc.append(y*4+x)
                                inloc.remove((y+1)*4+x)       
            return now_block_quan,score
        times=0
        while not func.check_2048(gu,now_block_quan):
            locinloc = random.choice(inloc)
            inloc.remove(locinloc)
            if now_block_quan<=8:
                gu[locinloc//4][locinloc%4]=2
            else:
                gu[locinloc//4][locinloc%4]=random.choice([2,4])
            now_block_quan+=1
            if times==0:
                mes=await ctx.send(func.draw_board(gu),embed=discord.Embed(title=f"目前分數：{score}",color=discord.Colour.random()))
                times+=1
            else:
                await mes.edit(content=func.draw_board(gu),embed=discord.Embed(title=f"目前分數：{score}",color=discord.Colour.random()))
            await mes.add_reaction('➡️')
            await mes.add_reaction('⬇️')
            await mes.add_reaction('⬅️')
            await mes.add_reaction('⬆️')
            await mes.add_reaction('🚫')
            def check(reaction, user):
                return not user.bot
            rea,user=await self.bot.wait_for('reaction_add',check=check)
            await mes.remove_reaction(rea.emoji,user)
            if str(rea)=="➡️":
                now_block_quan,score = move_right(now_block_quan,score)
            elif str(rea)=='⬇️':
                now_block_quan,score=move_down(now_block_quan,score)
            elif str(rea)=='⬅️':
                now_block_quan,score=move_left(now_block_quan,score)
            elif str(rea)=="⬆️":
                now_block_quan,score=move_up(now_block_quan,score)
            elif str(rea)=="🚫":
                await ctx.send("已提前結束")
                return
        await ctx.send("結束")
        



    @commands.command()
    async def aaa(self,ctx):
        lis=[]
        for i in range(4):
            lis.append(random.choices([0,2,4,8,16,32,64,128,256,512,1024,2048],k=4))
        await ctx.send(func.draw_board(lis,4))




def setup(bot):
    bot.add_cog(tzfe(bot))