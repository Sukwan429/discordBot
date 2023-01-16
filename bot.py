#導入 Discord.py
import discord
from discord.ext import commands
from discord.ui import Select,View
import json
from datetime import datetime
from discord.commands import Option
import random,os,asyncio,sys

with open('setting.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    jdata = json.load(jfile)
with open("database/config.json", "r", encoding="UTF-8") as file:
    config = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(help_command=None,command_prefix='*',intents = intents)

@bot.event
async def on_ready():
    try:
        guild = await bot.fetch_guild(config["guild"])
    except:
        print("錯誤:找不到群組")
        await asyncio.sleep(10)
        await sys.exit()
    else:
        game = discord.Game(F"developed by hesperus")
        await bot.change_presence(status=discord.Status.online, activity=game)
        print(f"哈囉，又見面了!")

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Load {extension} done.')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Unload {extension} done.')

@bot.command()
async def reload(ctx,extension):
        bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reload {extension} done.')


@bot.slash_command(description="設置反應身分組")
async def reaction_role(ctx,
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

@bot.event
async def on_raw_reaction_add(payload):  # 偵測到添加反應
    with open("database/role.json", "r") as file:  # 用read模式開啟檔案
        data = json.load(file)  # 讀取檔案內容
    if not str(payload.message_id) in data:  # 如果檔案裡沒有資料
        return  # 結束運行
    if data[str(payload.message_id)]["emoji"] != payload.emoji.id:  # 判斷添加的反應是否是設置的反應
        return  # 結束運行
    guild = await bot.fetch_guild(payload.guild_id)  # 取得群組
    role = guild.get_role(data[str(payload.message_id)]["role"])  # 取得身分組
    await payload.member.add_roles(role, reason="反應身分組系統")  # 給予身份組
    try:
        await payload.member.send(F"已給予 {role}", delete_after=10)  # 私訊給予訊息
    except:
        pass

@bot.event
async def on_raw_reaction_remove(payload):  # 偵測到添加反應
    with open("database/role.json", "r") as file:  # 用read模式開啟檔案
        data = json.load(file)  # 讀取檔案內容
    if not str(payload.message_id) in data:  # 如果檔案裡沒有資料
        return  # 結束運行
    if data[str(payload.message_id)]["emoji"] != payload.emoji.id:  # 判斷添加的反應是否是設置的反應
        return  # 結束運行
    guild = await bot.fetch_guild(payload.guild_id)  # 取得群組
    role = guild.get_role(data[str(payload.message_id)]["role"])  # 取得身分組
    member = await guild.fetch_member(payload.user_id)
    await member.remove_roles(role, reason="反應身分組系統")  # 移除身分組
    try:
        await member.send(F"已移除 {role}", delete_after=10)  # 私訊給予訊息
    except:
        pass


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cmds.{filename[:-3]}')
            print(f'✅   已加載 {filename}')
        except Exception as error:
            print(f'❎   {filename} 發生錯誤  {error}')
if __name__ == "__main__":
    bot.run(jdata['TOKEN'])