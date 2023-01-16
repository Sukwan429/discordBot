import discord,json,os
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command
from core.classes import Cog_Extension
import datetime

with open("database/config.json","r",encoding="utf-8") as file:
    data = json.load(file)
GUILD, ADMIN = data["guild"], data["admin"]

class button_set(discord.ui.View):
    @discord.ui.button(label="給予該用戶錢錢",style=discord.ButtonStyle.green)
    async def add_button_callback(self, button, interaction):
        if ADMIN in [role.id for role in interaction.user.roles]:
            await interaction.response.send_modal(modal_add_money(title="給予用戶錢錢"))
        else:
            await interaction.response.send_message(f"只有<@&{ADMIN}>可以控制錢錢!",ephemeral=True)

    @discord.ui.button(label="減少該用戶錢錢",style=discord.ButtonStyle.red)
    async def del_button_callback(self, button, interaction):
        if ADMIN in [role.id for role in interaction.user.roles]:
            await interaction.response.send_modal(modal_del_money(title="減少用戶錢錢"))
        else:
            await interaction.response.send_message(f"只有<@&{ADMIN}>可以控制錢錢!",ephemeral=True)

class modal_add_money(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="要給予的數量"))

    async def callback(self, interaction):
        message, member = self.children[0].value, interaction.message.content
        try:
            int(message)
        except:
            await interaction.response.send_message("請輸入正確的數字",ephemeral=True,delete_after=10)
            return

        member = await interaction.guild.fetch_member(member)
        filepath = F"database/user/{member.id}/money.json"
        with open(filepath, "r") as file:
            data = json.load(file)
            data["money"] += int(message)
        with open(filepath,"w") as file: 
            json.dump(data,file)
        money = data["money"]
        content = F"已給予{member.mention} {message}錢錢\n他現在有`{money}`元"

        await interaction.response.send_message(content=content,ephemeral=True,delete_after=10)
        embed=discord.Embed(title=f"`{member}` 的錢包",
            description=f"{member.mention}還有{money}元",color=discord.Colour.random())
        await interaction.message.edit(embed=embed)

class modal_del_money(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="要扣除的數量"))

    async def callback(self, interaction):
        message, member = self.children[0].value, interaction.message.content
        try:
            int(message)
        except:
            await interaction.response.send_message("請輸入正確的數字",ephemeral=True,delete_after=10)
            return

        member = await interaction.guild.fetch_member(member)
        filepath = F"database/user/{member.id}/money.json"
        with open(filepath, "r") as file:
            data = json.load(file)
            data["money"] -= int(message)
        with open(filepath,"w") as file: 
            json.dump(data,file)
        money = data["money"]
        content = F"已扣除{member.mention} {message}錢錢\n他現在有`{money}`元"
        await interaction.response.send_message(content=content,ephemeral=True,delete_after=10)

        embed=discord.Embed(title=f"`{member}` 的錢包",
            description=f"{member.mention}還有{money}元",color=discord.Colour.random())
        await interaction.message.edit(embed=embed)

class money(Cog_Extension):

    @slash_command(description="查看用戶的錢錢")
    async def money(self,ctx,member:Option(discord.Member,"要查看的用戶",required=False)):


        with open("database/config.json","r",encoding="utf-8") as file:
            data = json.load(file)
            admin = data["admin"]
        try:
            ctx.guild.get_role(admin)
        except:
            await ctx.respond(F"找不到身分組 `{admin}`")
            return

        member = member or ctx.author
        path = F"database/user/{member.id}"
        filepath = F"{path}/money.json"
        if not os.path.isfile(filepath):
            os.makedirs(path)
            with open(filepath,"w",encoding="utf-8") as file:
                data = {"money":0,"daily":"9999"}
                json.dump(data,file)
        
        with open(filepath,"r",encoding="utf-8") as file: data = json.load(file)
        money = data["money"]
        embed=discord.Embed(title=f"`{member}` 的錢包",
            description=f"{member.mention}還有{money}元",color=discord.Colour.random())
        await ctx.respond(content=member.id,embed=embed, view=button_set())
        
    @slash_command(description="每日簽到")
    async def daily(self,ctx):
        member=ctx.author
        new_money=0
        path=f"database/user/{member.id}"
        filepath=f"{path}/money.json"
        now_time=datetime.datetime.now().strftime('%m%d')
        if not os.path.isfile(filepath):
            os.makedirs(path)
            with open(filepath,"w",encoding="utf-8") as file:
                data = {"money":1000,"daily":now_time}
                json.dump(data,file)
        else:
            with open(filepath,"r",encoding="utf-8") as file: data = json.load(file)
            if data["daily"]==now_time:
                await ctx.send("今天已領過，請等明天")
                return
            data["daily"] = now_time
            data["money"]+=1000
            new_money=data["money"]
            with open(filepath,"w",encoding="utf-8") as file:
                json.dump(data,file)
        await ctx.send(embed=discord.Embed(title=f"{member}的錢包"
                        ,description=f"{member.mention}還有{new_money}元",color=discord.Colour.random()))
        
    @commands.command()
    async def daily(self,ctx):
        member=ctx.author
        new_money=0
        path=f"database/user/{member.id}"
        filepath=f"{path}/money.json"
        now_time=datetime.datetime.now().strftime('%m%d')
        if not os.path.isfile(filepath):
            os.makedirs(path)
            with open(filepath,"w",encoding="utf-8") as file:
                data = {"money":1000,"daily":now_time}
                json.dump(data,file)
        else:
            with open(filepath,"r",encoding="utf-8") as file: data = json.load(file)
            if data["daily"]==now_time:
                await ctx.send("今天已領過，請等明天")
                return
            data["daily"] = now_time
            data["money"]+=1000
            new_money=data["money"]
            with open(filepath,"w",encoding="utf-8") as file:
                json.dump(data,file)
        await ctx.send(embed=discord.Embed(title=f"{member}的錢包"
                        ,description=f"{member.mention}還有{new_money}元",color=discord.Colour.random()))


def setup (bot):
    bot.add_cog(money(bot))