#https://stackoverflow.com/questions/66724687/how-to-solve-a-429-too-many-requests-when-running-discord-py-bot-on-repl-it 
#read if get 429 error
from discord.ext import commands
import discord, os, random, time, requests
from keep_alive import keep_alive
import json, asyncio
from replit import db


def _reset():
  db["lastbump"] = 10
  db["reminded"] = False
  exit()

token = os.environ["token"]
intents=discord.Intents.all()

bot = commands.Bot(command_prefix="!",intents=intents)
bot.remove_command('help')
guilds = [871696913987162112]


class userdata:
  def __init__(self):
    pass
  
  def getdata(self, username):
    try:
      x = requests.get(f"https://scratchdb.lefty.one/v3/user/info/{username}", timeout=10)
    except Exception as e:
      return ["....","Scratchdb took too long to respond"+str(e)]
    statuscode = x.status_code
    if statuscode != 200:
      return ["...",statuscode]
    x = x.json()
    self.username = x["username"]
    self.id = str(x["id"])
    self.pfp = f"https://cdn2.scratch.mit.edu/get_image/user/{self.id}_90x90.png?v="
    self.rank = x["status"]
    self.joined = x["joined"]
    self.WIWO = x["work"]
    self.AM = x["bio"]
    self.country = x["country"]
    self.followers = x["statistics"]["followers"]
    self.following = x["statistics"]["following"]
    return "done"

def _joke(typeofjoke):
  x = requests.get(f"https://official-joke-api.appspot.com/jokes/{typeofjoke}/random")
  if x.status_code != 200:
    return "An error has occurred. please try again later."
  x = x.json()
  if len(x) == 0:
    return "An error has occurred. please try again later."
  x = x[0]
  return [x["setup"],x["punchline"]]

def _fact():
  x = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
  if x.status_code != 200:
    return "An error has occurred. please try again later."+str(x.status_code)
  else:
    return x.json()["text"]


user = userdata()


@bot.event
async def on_ready():
  print("Bot is ready!")
  channel = bot.get_channel(877770366741803062)
  while True:
    t = (db["lastbump"] + 2*60*60) - int(time.time()//1)
    if t <= 0:
      if db["reminded"] == False:
        db["reminded"] = True
        await channel.send("Time to bump! use `!d bump` command to bump.")
    
    await asyncio.sleep(1)

@bot.event
async def on_member_join(member):
  role = discord.utils.get(member.guild.roles, name="member")
  print(bool(role == 875675800886726666))
  await member.add_roles(role)
  await member.send("Hey, this feature is in testing. Please go to #general in scratchers hub and confirm you got this DM. Thanks.")

@bot.command() #name
async def tester(ctx):
  await ctx.send("I do work!")



@bot.command()
async def help(ctx, command=None):
  title = ["Flip a coin","Random Number","Say pong","Roll a dice","Calculator","Scratch User Search","Tell a joke","Tell a fact","Tell bots password"]
  value = ["`!flipcoin`","`!rand <num> <num>` with `<num>` being optional","`!ping`","`!rolldice <num>`where <num> is optional. it specifies number of dice.","`!calc <equation>`","`!stats <username>` where <username> is mandatory","`!joke <type>` where `<type>` is optional.\n Type has 3 options:\n General (default), programming, knock-knock","`!fact`", "`!password`"]
  inline= [False, False, False, False,False,False,False,False,False]
  comms = ["flipcoin","rand","ping","rolldice","calc","stats","joke","fact","password"] #everything in comms should be lowercase
  
  if command == None:
    embed = discord.Embed(title="Commands", description="All commands must start with the prefix `!`",color=discord.Colour.blue())
    for a, b, c in zip(title,value,inline):
      embed.add_field(name = a ,value = b ,inline = c)
  
  else:
    if not command.lower() in comms:
      embed = discord.Embed(title="Command not found", description=f"{command} was not found. type `!help` to see all commands",color=discord.Colour.red())

      embed.add_field(name="not found...",value=f"{command} not found. Type `!help` to see all commands.")
    else:
      indexcomms = comms.index(command.lower())
      embed = discord.Embed(title=title[indexcomms], description=value[indexcomms],color=discord.Colour.dark_green())

  embed.set_footer(text="`!help <command>` will help you find only the specific command's info. example: `!help flipcoin`")
  await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
  await ctx.send("Pong")

@bot.command()
async def sleep(ctx):
    await ctx.send("Thanks! bye 👋 zzzzz....")
    await asyncio.sleep(10)
    await ctx.send("Im back! Thanks for the nap time!")

@bot.command()
async def member(ctx):
  member = await ctx.message.guild.query_members(user_ids=[ctx.author.id])
  member = member[0]
  await member.add_roles(discord.utils.get(member.guild.roles, name="member")) 
  await ctx.send(f"{ctx.message.author.mention} your got member role.")

@bot.command()
async def rolldice(ctx, num=1):
  numberdice = random.randint(1,6*num)
  print(type(num))
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

@bot.command()
async def joke(ctx,t="general"):
  res = _joke(t)
  if "error" in res:
    await ctx.send(f"{ctx.message.author.mention} {res}.\n type `!help joke` for info on command.")
  else:
    await ctx.send(f"{ctx.message.author.mention}\n{res[0]}\n{res[1]}")

@bot.command()
async def fact(ctx):
  x = _fact()
  await ctx.send(f"{ctx.message.author.mention} {x}")
  """
  with open("test.json","r") as file:
    alljoke = json.load(file)
    alljoke.append(x)
  with open("test.json","w") as file:
    json.dump(alljoke)
  """

@bot.command()
async def password(ctx):
  await ctx.send(f"{ctx.message.author.mention}\nhttps://tenor.com/view/rick-astley-rick-roll-dancing-dance-moves-gif-14097983\nWhat did you expect?")

@bot.command()
async def d(ctx, bump=None):
  if bump == "bump":
    t = (db["lastbump"] + 2*60*60) - int(time.time()//1)
    if t <= 0:
      db["lastbump"] = int(time.time()//1)
      db["reminded"] = False
      t = (db["lastbump"] + 2*60*60) - int(time.time()//1)
      await ctx.send(f"{ctx.message.author.mention} Thanks to bump!\n{t} secs left to bump next time.")
    else:
      await ctx.send(f"Please wait {t} secs before bumping. :)")
      

@bot.command()
async def stats(ctx,username=None):
  if username == None:
    await ctx.send("Syntax: `!stats <user>` where <user> is mandatory")
  else:
    code = user.getdata(username)
    if "..." in code:
      if code[1] == 404:
        await ctx.send(f"{ctx.message.author.mention} User doesn't exist")
      else:
        await ctx.send(f"{ctx.message.author.mention} An error occurred. please try again")
    elif "...." in code:
      await ctx.send(f"{ctx.message.author.mention} {code[1]}")
    else:
      embed = discord.Embed(title = user.username, description=f"Stats of {user.username} on Scratch \n https://scratch.mit.edu/users/{user.username}",color=discord.Colour.orange())
      embed.set_thumbnail(url=user.pfp)
      embed.add_field(name = "User ID:",value= f"`{user.id}`", inline = True)
      embed.add_field(name = "Country:",value=f"`{user.country}`", inline = True)
      embed.add_field(name = "Followers:",value=f"`{user.followers}`",inline=True)
      embed.add_field(name = "Rank:",value=f"`{user.rank}`", inline = True)
      embed.add_field(name = "Joined:",value=f"`{user.joined}`", inline = True)
      embed.add_field(name = "Following:",value=f"`{user.following}`",inline=True)
      embed.add_field(name = "About Me:",value= f"`{user.AM}`", inline = False)
      embed.add_field(name = "What I'm Working On:",value=f"`{user.WIWO}`", inline = False)
      embed.set_footer(text="Data from https://scratchdb.lefty.one/ created by @datonelefty")
      await ctx.send(embed=embed)


@bot.command()
async def calc(ctx, eqn=None):
  if eqn == None:
    await ctx.send("What??!!")
  else:
    await ctx.send("WIP. gotta calculate "+eqn)

keys = ["rude","online","spam","good","lol"]
ans = ["don't be a fool","yep","Heyheyhey!! ","thx!",":rofl:",]
mentioning = [True, False,True,False,False]
@bot.event
async def on_message(message):
  if bot.user.mentioned_in(message):
    await message.channel.send('Why u pinged me?? I was sleeping :( .\nUse `!sleep` to make me sleep again')
  
  elif message.mentions and not message.author.bot:
    mentions = ""
    for member in message.mentions: #member.name also exists
      ping = f"<@!{member.id}>"
      if ping in message.content:
        mentions += member.mention + ", "
    if mentions != "":
      await message.channel.send(f"Dont ping {mentions[:-2]}")
  
  for key, val, ment in zip(keys, ans, mentioning):
    if message.content.lower() == key:
      if ment:
        await message.channel.send(f"{message.author.mention} "+val)
      else:
        await message.channel.send(val)
      
  await bot.process_commands(message)#it neccesarry for the on_message stuff not to override the commands


keep_alive()
bot.run(token)