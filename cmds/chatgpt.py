import openai
import discord
import numpy as np
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json',mode='r',encoding='utf8') as jfile:#r==read,utf8解碼
    jdata = json.load(jfile)


openai.api_key = jdata["chatgpt_key"]  #你自己的ChatGPT API key
messages = [
        {"role": "system", "content": "You are a helpful assistant."},
]
class chatgpt(Cog_Extension):
    @commands.command()
    async def chat(self,ctx):
        def check(number):
            return number.author == ctx.author and number.channel == ctx.message.channel
        message = "哈囉"
        while True:
            if message=="end":
                return 
            elif message[0]=="*":
                continue
            elif message:
                messages.append(
                        {"role": "user", "content": message},
                )
                chat_completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                )
            answer = chat_completion.choices[0].message.content
            await ctx.send(answer)
            messages.append({"role": "assistant", "content": answer})
            message = await self.bot.wait_for("message",check=check)
            message=str(message.content)


async def setup(bot):
    await bot.add_cog(chatgpt(bot))