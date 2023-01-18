import asyncio,random,json,discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,os
class Pet(Cog_Extension):
    
    @commands.group()
    async def pet(self,ctx):
        pass

    @pet.command()
    async def help(self,ctx):
        with open("database/help/pet.txt","r",encoding='utf8') as file:
            help=file.read()
        embed=discord.Embed(title="寵物相關指令列表",description=help,color=discord.Colour.random())
        await ctx.send(embed=embed)

    @pet.command()
    async def shop(self,ctx):
        with open("database/pet_price.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
        embed=discord.Embed(title="寵物商店",color=discord.Colour.random())
        for i in data:
            embed.add_field(name=i,value=data[i],inline=False)
        await ctx.send(embed=embed,content="可使用`*pet buy <寵物名稱>`購買寵物")
    
    @pet.command()
    async def buy(self, ctx,petname:str):
        path=f"database/user/{ctx.author.id}"
        filepath=f"{path}/money.json"
        if not os.path.isfile(filepath):
            os.makedirs(path)
            with open(filepath,"w",encoding="utf-8") as file:
                data = {"money":0,"daily":"9999"}
                json.dump(data,file)
        with open(filepath,"r",encoding="utf-8") as file:
            data=json.load(file)
        if petname in data.keys():
            await ctx.send(f"你只能擁有一隻{petname}")
            return
        with open("database/pet_price.json","r",encoding="utf-8") as file:
            pet_money=json.load(file)
        if data["money"]<pet_money[petname]:
            await ctx.send("餘額不足")
            return
        await ctx.send("請幫你的寵物取一個名字")
        
        def check(name):
            return ctx.author==name.author
        msg=await self.bot.wait_for("message",check=check)
        msg=msg.content
        data.setdefault(petname,{"name":msg})
        with open(filepath,"w",encoding="utf-8") as f:
            json.dump(data,f)
        await ctx.send(f"成功收編{petname} {msg}")



def setup(bot):
    bot.add_cog(Pet(bot))