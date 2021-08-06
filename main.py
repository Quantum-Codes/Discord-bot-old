from discord.ext import commands
import discord, os, random, time
from keep_alive import keep_alive

token = os.environ["token"]

bot = commands.Bot("!")


@bot.event
async def on_ready():
  print("Bot is ready!")

@bot.command(name="ping",brief="completes word",description= "hi")
async def ping(ctx):
  await ctx.send("Pong")

@bot.command()
async def flipcoin(ctx):
	heads_tails = ['Heads', 'Tails']
	choice = random.choice(heads_tails)
	await ctx.send(choice)

@bot.command()
async def rand(ctx, num1=0, num2=10):
  if num2 >= num1:
    random_number = random.randint(int(num1), int(num2))
    await ctx.send(str(random_number))
  else:
    await ctx.send("Syntax: !<num1> <num2> and num1 is bigger or equal to num 2")


@bot.event
async def on_message(message):
  if message.content.lower() == "rude":
    await message.channel.send("Dont be a fool")
  
  if message.content.lower() == "online":
    await message.channel.send("yep")
  
  
    
  await bot.process_commands(message)#it neccesarry for the on_message stuff not to override the commands

keep_alive()
bot.run(token)