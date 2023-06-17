import discord,json,os
from discord.ext import commands
from core.classes import Cog_Extension
import datetime

with open("database/config.json","r",encoding="utf-8") as file:
    data = json.load(file)
class button_set(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="給予用戶錢錢",style=discord.ButtonStyle.green)
    async def add(self,interaction:discord.Interaction,button:discord.ui.Button):
        pass

    @discord.ui.buttion(label="減少用戶錢錢",style=discord.ButtonStyle.red)
    async def sub(self,interaction:discord.Interaction,button:discord.ui.Button):
        pass
class add_money(discord.ui.Modal, title='增加用戶的錢錢'):
    resp = discord.ui.TextInput(label='金額', style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        pass
class modal_add_money(discord.ui.Modal,title="給予用戶錢錢"):
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

    @commands.hybrid_command(name="money",description="查看使用者的錢錢")
    async def money(self,ctx,member:discord.Member=None):
        if member is None:
            member=ctx.author
        with open("database/config.json","r",encoding="utf-8") as file:
            data = json.load(file)
            admin = data[str(ctx.guild.id)]
        try:
            ctx.guild.get_role(admin)
        except:
            await ctx.respond(F"找不到身分組 `{admin}`")
            return
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
        await ctx.send(content=member.id,embed=embed, view=button_set())
        
        
    @commands.hybrid_command(name="daily",description="每日簽到")
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
        await ctx.send(embed=discord.Embed(title=f"`{member}`的錢包"
                        ,description=f"{member.mention}還有{new_money}元",color=discord.Colour.random()))

    @commands.command()
    async def add_money_role(self,ctx,role:discord.Role):
        if not ctx.author.guild_permissions.administrator:  # 如果使用者沒管理權限
            await ctx.send("只有管理員能使用此指令",delete_after=10)
            return  # 結束運行
        with open("database/config.json","r",encoding="utf-8") as file:
            data = json.load(file)
        if str(ctx.guild.id) in data.keys():
            await ctx.send("一個伺服器只可有一個管理錢錢的身分組",delete_after=10)
            return
        data[str(ctx.guild.id)] = role.id
        with open("database/config.json","w",encoding='utf-8') as file: 
            json.dump(data,file)
        await ctx.send(f"已成功將金錢管理身分組設為`{role.name}`")

    @commands.command()
    async def remove_money_role(self,ctx):
        if not ctx.author.guild_permissions.administrator:  # 如果使用者沒管理權限
            await ctx.send("只有管理員能使用此指令",delete_after=10)
            return  # 結束運行
        with open("database/config.json","r",encoding="utf-8") as file:
            data = json.load(file)
        if str(ctx.guild.id) not in data.keys():
            await ctx.send("此伺服器尚未設置金錢管理身分組",delete_after=10)
            return
        data.pop(str(ctx.guild.id))
        with open("database/config.json","w",encoding='utf-8') as file:
            json.dump(data,file)
        await ctx.send(f"已成功移除金錢管理身分組，需重新新增一個才能使用金錢系統喔~")



async def setup (bot):
    await bot.add_cog(money(bot))