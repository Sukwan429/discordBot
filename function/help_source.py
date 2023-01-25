
import discord
from discord.ext import commands
import asyncio,random
from datetime import datetime
import json 
with open('database\help.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    helptext = json.load(jfile)

main_help_embed=discord.Embed(title=helptext["main_title"],description=helptext["main_description"],color=0xFF69B4)
main_help_embed.set_footer(text="彈力鯊鍋余頭")
main_help_embed.set_thumbnail(url=helptext["bot_avatar_url"])

money_help_embed=discord.Embed(title=helptext["money_title"],description=helptext["money_description"],color=discord.Colour.random())
money_help_embed.set_footer(text="彈力鯊鍋余頭")
money_help_embed.set_thumbnail(url=helptext["bot_avatar_url"])

game_embed=discord.Embed(title="遊戲",color=discord.Colour.random())
nm_embed=discord.Embed(title="一般",color=discord.Colour.random())
EX_embed=discord.Embed(title="特殊",color=discord.Colour.random())


nm={"1":discord.Embed(title="查詢ping值",description=helptext["nm"]["01"],color = discord.Colour.random()),
        "2":discord.Embed(title="取得使用者頭像",description=helptext["nm"]["02"],color = discord.Colour.random()),
        "3":discord.Embed(title="查詢使用者資料",description=helptext["nm"]["03"],color = discord.Colour.random()),
        "4":discord.Embed(title="讓機器人說話",description=helptext["nm"]["04"],color = discord.Colour.random()),
        "5":discord.Embed(title="隨機抽籤",description=helptext["nm"]["05"],color=discord.Colour.random()),
        "6":discord.Embed(title="幫你選一個答案",description=helptext["nm"]["06"],color=discord.Colour.random()),
        "7":discord.Embed(title="計算機",description=helptext["nm"]["07"],color=discord.Colour.random()),
        "8":discord.Embed(title="隨機組隊",description=helptext["nm"]["08"],color=discord.Colour.random()),
        "9":discord.Embed(title="大聲公",description=helptext["nm"]["09"],color=discord.Colour.random()),
        "10":discord.Embed(title="base64編碼",description=helptext["nm"]["10"],color=discord.Colour.random()),
        "98":discord.Embed(title="hentai",description=helptext["nm"]["98"],color=discord.Colour.random()),
        "99":discord.Embed(title="開發人員",description=helptext["nm"]["99"],color=0xFFFF00)
        }
gm={"0":discord.Embed(title="查看規則",description=helptext["gm"]["00"],color=discord.Colour.random()),
    "1":discord.Embed(title="2048",description=helptext["gm"]["01"],color=discord.Colour.random()),
    "2":discord.Embed(title="五子棋",description=helptext["gm"]["02"],color=discord.Colour.random()),
    "3":discord.Embed(title="終極密碼",description=helptext["gm"]["03"],color=discord.Colour.random()),
    "4":discord.Embed(title="OOXX",description=helptext["gm"]["04"],color=discord.Colour.random()),
    "5":discord.Embed(title="擲骰子",description=helptext["gm"]["05"],color=discord.Colour.random()),
    "6":discord.Embed(title="猜正反",description=helptext["gm"]["06"],color=discord.Colour.random()),
    "7":discord.Embed(title="1A2B",description=helptext["gm"]["07"],color=discord.Colour.random()),
    "10":discord.Embed(title="金錢系統",description=helptext["gm"]["10"],color=discord.Colour.random()),
    }
money={"1":discord.Embed(title="查看錢包",description=helptext["money"]["00"],color=discord.Colour.random()),
"2":discord.Embed(title="每日簽到",description=helptext["money"]["01"],color=discord.Colour.random()),
"98":discord.Embed(title="設置金錢管理身分組",description=helptext["money"]["98"],color=discord.Colour.random()),
"99":discord.Embed(title="移除金錢管理身分組",description=helptext["money"]["99"],color=discord.Colour.random())
}

EX={"1":discord.Embed(title="設定排程時間",description=helptext["EX"]["01"],color=discord.Colour.random()),
    "2":discord.Embed(title="設定排程執行頻道",description=helptext["EX"]["02"],color=discord.Colour.random()),
    "3":discord.Embed(title="設定排程執行語句",description=helptext["EX"]["03"],color=discord.Colour.random()),
    "4":discord.Embed(title="設定身分組訊息",description=helptext["EX"]["04"],color=discord.Colour.random()),
    }

for i in nm:
    nm[i].set_thumbnail(url=helptext["bot_avatar_url"])
    nm[i].set_footer(text=nm[i].title)
for i  in gm:
    gm[i].set_thumbnail(url=helptext["bot_avatar_url"])
    gm[i].set_footer(text=gm[i].title)
for i in EX:
    EX[i].set_thumbnail(url=helptext["bot_avatar_url"])
    EX[i].set_footer(text=EX[i].title)

class select_main(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="一般",value='1',description="一些查詢類型的指令"),
            discord.SelectOption(label="遊戲",value='2',description="一些小遊戲"),
            discord.SelectOption(label="特殊",value='3',description="關於設置的指令"),
            ]
        super().__init__(placeholder="點我",min_values=1, max_values=1,options=options)
    async def callback(self,interaction:discord.Interaction):
        if self.values[0]=="1":
            no=normal()
            await interaction.response.edit_message(embed=nm_embed,view=no)     
        if self.values[0]=="2":
            no=game()
            await interaction.response.edit_message(embed=game_embed,view=no)
        if self.values[0]=="3":
            no=ex()
            await interaction.response.edit_message(embed=EX_embed,view=no)
class select_normal(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="查詢ping值",value="1"),
            discord.SelectOption(label="取得使用者頭像",value="2"),
            discord.SelectOption(label="使用者資料",value="3"),
            discord.SelectOption(label="讓機器人說話",value="4"),
            discord.SelectOption(label="隨機抽籤",value="5"),
            discord.SelectOption(label="幫你選一個答案",value="6"),
            discord.SelectOption(label="計算機",value="7"),
            discord.SelectOption(label="隨機組隊",value="8"),
            discord.SelectOption(label="大聲公",value="9"),
            discord.SelectOption(label="base64編碼",value="10"),
            discord.SelectOption(label="hentai",value="98"),
            discord.SelectOption(label="開發人員",value="99"),
            discord.SelectOption(label="回上一頁",value="100") 
            ]
        super().__init__(placeholder="點我",min_values=1, max_values=1,options=options)
    async def callback(self,interaction:discord.Interaction):
        if self.values[0]=="100":
            view=Myselect()
            await interaction.response.edit_message(view=view,embed=main_help_embed)
        else:
            await interaction.response.edit_message(embed=nm[self.values[0]])

class select_game(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="查看規則",value="0"),
            discord.SelectOption(label="2048",value="1"),
            discord.SelectOption(label="五子棋",value="2"),
            discord.SelectOption(label="終極密碼",value="3"),
            discord.SelectOption(label="OOXX",value="4"),
            discord.SelectOption(label="擲骰子",value="5"),
            discord.SelectOption(label="猜正反",value="6"),
            discord.SelectOption(label="1A2B",value="7"),
            discord.SelectOption(label="金錢系統",value="10"),
            discord.SelectOption(label="待推出......",value="99"),
            discord.SelectOption(label="回上一頁",value="100")
            ]
        super().__init__(placeholder="點我",min_values=1, max_values=1,options=options)

    async def callback(self,interaction:discord.Interaction):
        if self.values[0]=="100":
            view=Myselect()
            await interaction.response.edit_message(view=view,embed=main_help_embed)
        elif self.values[0]=="10":
            view=mon()
            await interaction.response.edit_message(view=view,embed=money_help_embed)
        else:
            await interaction.response.edit_message(embed=gm[self.values[0]])
class select_ex(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="設定排程時間",value="1"),
            discord.SelectOption(label="設定排程執行頻道",value="2"),
            discord.SelectOption(label="設定排程執行語句",value="3"),
            discord.SelectOption(label="設定身分組訊息",description="僅限伺服器管理員",value="4"),
            discord.SelectOption(label="回上一頁",value="100")
            ]
        super().__init__(placeholder="點我",min_values=1, max_values=1,options=options)
    async def callback(self,interaction:discord.Interaction):
    
        if self.values[0]=="100":
            view=Myselect()
            await interaction.response.edit_message(view=view,embed=main_help_embed)
        else:
            await interaction.response.edit_message(embed=EX[self.values[0]])

class select_mon(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="查看錢包",value="1"),
            discord.SelectOption(label="每日簽到",value="2"),
            discord.SelectOption(label="設置金錢管理身分組",description="僅限伺服器管理員",value="98"),
            discord.SelectOption(label="移除金錢管理身分組",description="僅限伺服器管理員",value="99"),
            discord.SelectOption(label="回上一頁",value="100")
            ]
        super().__init__(placeholder="點我",min_values=1, max_values=1,options=options)

    async def callback(self,interaction:discord.Interaction):
    
        if self.values[0]=="100":
            view=game()
            await interaction.response.edit_message(view=view,embed=game_embed)
        else:
            await interaction.response.edit_message(embed=money[self.values[0]])

class Myselect(discord.ui.View):
    def __init__(self,*,timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(select_main())

class normal(discord.ui.View):
    def __init__(self,*,timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(select_normal())

class game(discord.ui.View):
    def __init__(self,*,timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(select_game())

class ex(discord.ui.View):
    def __init__(self,*,timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(select_ex())

class mon(discord.ui.View):
    def __init__(self,*,timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(select_mon())

        