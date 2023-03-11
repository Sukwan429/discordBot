import openai
import discord
import numpy as np
from discord.ext import commands
from core.classes import Cog_Extension

openai.api_key = "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"
messages = [
        {"role": "system", "content": "You are a helpful assistant."},
]
class chatgpt(Cog_Extension):
    @commands.command()
    async def chat(self,ctx,qu):
        def check(number):
            return number.author == ctx.author and number.channel == ctx.message.channel
        message = qu
        while True:
            if message=="end":
                return 
            if message:
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