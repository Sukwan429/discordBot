import discord
import json
import random,os,asyncio
import numpy as np
from discord.ext import commands
from core.classes import Cog_Extension
import function.func as func

number={0:"zero",1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven"}

#TODO 使用編輯訊息進行繪製棋盤
class chess(Cog_Extension):

    @commands.command()
    async def chess(self,ctx):
        ChessBoard=[[0 for i in range(8)] for i in range(8)] #初始化棋盤

        await ctx.send("請輸入座標下棋，黑方先下(格式：x y)範例輸入：0 0")

        last = 1 #1為黑-1為白

        game_finish=False
        while game_finish==False:
            che="<:emoji_18:1037033851257630852>:zero::one::two::three::four::five::six::seven:<:emoji_18:1037033851257630852>\n"

            ####
            for i in range(8):
                che=che+f':{number[i]}:'
                for j in range(8):
                    if ChessBoard[i][j]==0:
                        che=che+"<:plus:1057677224028930048>"
                    elif ChessBoard[i][j]==1:
                        che=che+"<:circle:1057677105355292722>"
                    elif ChessBoard[i][j]==2:
                        che=che+"<:WC:1058689460256124978>"
                che=che+f':{number[i]}:\n'
            await ctx.send(che)
            ####

            response = await self.bot.wait_for('message')
            x,y=response.content.split(' ')

            x=int(x)
            y=int(y)

            #
            while x>7 or x<0 or y>7 or y<0 or ChessBoard[x][y]!=0:#判斷棋步是否違法
                await ctx.send("錯誤，請重新選一格走")
                response = await self.bot.wait_for('message')
                x,y=response.content.split(' ')
                x=int(x)
                y=int(y)
            #

            if last == 1:
                ChessBoard[x][y]=1 #0為空1為黑2為白
                game_finish=func.check_chess_win(1,ChessBoard)
            
            elif last == -1:
                ChessBoard[x][y]=2
                game_finish=func.check_chess_win(2,ChessBoard)
                
            last=last*-1

        if last == -1:
            await ctx.send("黑方勝")
        elif last==1:
            await ctx.send("白方勝")

        che=":zero::one::two::three::four::five::six::seven:\n"

        ####
        for i in range(8):
            for j in range(8):
                if ChessBoard[i][j]==0:
                    che=che+"<:emoji_42:1057677224028930048>"
                elif ChessBoard[i][j]==1:
                    che=che+"<:emoji_42:1057677105355292722>"
                elif ChessBoard[i][j]==2:
                    che=che+"<:WC:1058689460256124978>"
            che=che+f'{i}\n'
        await ctx.send(che)
        ####


            


def setup(bot):
    bot.add_cog(chess(bot))