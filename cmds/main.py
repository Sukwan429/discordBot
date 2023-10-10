import discord
from discord.ext import commands
import random
from discord.ui import Select ,View
from datetime import datetime
from core.classes import Cog_Extension
import json
import function.func as func
#TODO menuSelect



class main(Cog_Extension):     #繼承Cog_Extension

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'目前延遲約{round(self.bot.latency*1000)}ms')
    
    @commands.command()
    async def l(self,ctx):
        await ctx.send(self.bot.command_prefix)

    @commands.command()
    async def sayd(self,ctx,*,msg):                 #*後的argument 皆為msg
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def clean(self,ctx,num:int):             #argument:type  船入會是type型態
        await ctx.channel.purge(limit=num+1)       #會包含指令訊息，所以+1    ###   argument: before after around
    
    @commands.command()
    async def random_squad(self,ctx, num:int,s:int): #num為每隊人數，s為有幾隊
        online=[]
        for member in ctx.guild.members:
            if str(member.status)=='online' and member.bot==False:
                online.append(member.name)

        random_online=random.sample(online,k=num*s)
        grupe=[]
        for i in range(s):
            grupe.append(random.sample(random_online,k=num))
            for name in grupe[i]:
                random_online.remove(name)    
            await ctx.send(f'第{i+1}小隊:{grupe[i]}')

    @commands.command()
    async def getavatar(self,ctx,member:discord.Member=None):
        if not member:
            member=ctx.author
        await ctx.send(member.avatar)

    @commands.command()
    async def announcement(self,ctx,tt,key:str):
        with open("D:/Coding/xampp/htdocs/accouncement.json","r") as file:
            data=json.load(file)
        
        await ctx.message.delete()
        embed=discord.Embed(title=tt,description=data[key],color=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(alieases=["whois","ui"])
    async def userinfo(self,ctx,member:discord.Member=None):
        roles=[]
        if not member:
            member=ctx.author
        for role in member.roles:
            roles.append(str(role.mention))
        roles.reverse()
        embed=discord.Embed(title=f"{member}'s User Infomation",color = discord.Colour.random())
        embed.add_field(name="Username",value=member.name)
        embed.add_field(name="Discriminator",value=member.discriminator)
        embed.add_field(name="ID",value=member.id)
        embed.add_field(name="Created At",value=datetime.strftime(member.created_at,"%A, %B %d, %Y"))
        embed.add_field(name="Joined At",value=datetime.strftime(member.joined_at,"%A, %B %d, %Y"))
        if len(str(" | ".join([x.mention for x in member.roles]))) > 1024:
            embed.add_field(name=f"Roles [{len(member.roles)}]",value="Too many to display.")
        else:
            embed.add_field(name=f"Roles [{len(member.roles)}]",value=" | ".join(roles))
        embed.add_field(name="Role Color",value=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

"""
    @commands.group()
    async def codetest(self,ctx):
        pass
    @codetest.command()
    async def Python(self,ctx):
        await ctx.send('Python')
    @codetest.command()
    async def Java(self,ctx):
        await ctx.send('Java')
    @codetest.command()
    async def Cpp(self,ctx):
        await ctx.send('Cpp')
    """

async def setup(bot):
    await bot.add_cog(main(bot))