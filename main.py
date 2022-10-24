"""import discord
import os # default module
from keep_alive import keep_alive

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

keep_alive()
bot.run(os.environ["token"]) # run the bot with the token"""
print("yo")