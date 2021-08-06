from discord.ext import commands
import discord, os, random, time
from keep_alive import keep_alive

token = os.environ["token"]

bot = commands.Bot("!")
bot.remove_command('help')

@bot.event
async def on_ready():
  print("Bot is ready!")

@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Commands", description="All commands must start with the prefix `!`",color=discord.Colour(0x2ecc71))
  embed.add_field(name="Flip a coin", value="`!flipcoin`", inline=False)
  embed.add_field(name="Random Number", value="`!rand <num> <num>` with `<num>` being optional")
  await ctx.send(embed=embed)

@bot.command(name="ping",brief="completes word",description= "hi")
async def ping(ctx):
  await ctx.send("Pong")

@bot.command()
async def rolldice(ctx, num=1):
  numberdice = random.randint(1,6*num)
  await ctx.send(f"You rolled a {numberdice}")

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

keys = ["rude","online","spam","@mgr8t","good"]
ans = ["don't be a fool","yep","Heyheyhey!! ","why u pinging him huh?","thx!"]
@bot.event
async def on_message(message):
  for key, val in zip(keys, ans):
    if message.content.lower() == key:
      await message.channel.send(f"{message.author.mention} "+val)

  await bot.process_commands(message)#it neccesarry for the on_message stuff not to override the commands

keep_alive()
bot.run(token)