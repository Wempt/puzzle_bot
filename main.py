# TODO
# Figure out flask to control bot from webpage
# Set puzzle on webpage and store in db
# ** done ** set up dm answer handler and point giver
# **done i think** leaderboard?
# add pages to leader board and an easter egg - number
# ** done ** rank command
# **ezpz** timing puzzle solving
# ** done, have to update guild manually ** channel for puzzle # release and announce time solves
# ** done ** clean dead user/guilds
# ** done ** add users and guilds as they join
# blacklist for solving puzzles
# ** done until new commands are added ** help command
# ** mostly done ** make embeds nicer
# error handling :/
# info command
# **done** time command
# gift command?
# ** fixed ** fix nick thing


import discord
import os
from replit import db
from commands import command_handler
from dm import dm_handler
from keep_alive import keep_alive
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents = intents)

def clear_db():
  for key in db.keys():
    print('deleted ' + str(key) + ' ' + str(db[key]))
    del db[key]

def startup():
  setup_guild()
  setup_user()

def setup_guild():
  for guild in client.guilds:
    id = guild.id
    if ('prefix' + str(id)) not in db.keys():
      db['prefix' + str(id)] = '$'

def setup_user():
  for member in client.get_all_members():
    member_id = member.id
    dic = {'name':str(member.name), 'puzzle_points':0, 'solved':False}
    if('member'+str(member_id)) not in db.keys() and not member.bot:
      db['member'+str(member_id)] = dic
      print(db['member'+str(member_id)])
    #old method of storing but you can use dicts so :))))
    #if ('puzzle'+str(member_id)) not in db.keys() and not member.bot:
    #  db['puzzle'+str(member_id)] = 0

@client.event
async def on_ready():
  #clear_db()
  startup()
  print(f'{client.user} connected')

@client.event
async def on_message(message):
  if message.author.bot:
    return
  elif isinstance(message.channel, discord.channel.DMChannel):
    await dm_handler(message, client)
  else:
    id = message.guild.id
    prefix = db['prefix' + str(id)]
    if message.content.startswith(prefix):
      await command_handler(message)

@client.event
async def on_member_join(member):
  member_id = member.id
  dic = {'name':str(member.name), 'puzzle_points':0, 'solved':False}
  if('member'+str(member_id)) not in db.keys() and not member.bot:
    db['member'+str(member_id)] = dic
    print(db['member'+str(member_id)])

@client.event
async def on_member_remove(member):
  member_id = member.id
  if('member'+str(member_id)) in db.keys() and not member.bot:
    del db['member'+str(member_id)]

@client.event
async def on_guild_join(guild):
  id = guild.id
  if ('prefix' + str(id)) not in db.keys():
    db['prefix' + str(id)] = '$'

@client.event
async def on_guild_remove(guild):
  id = guild.id
  if ('prefix' + str(id)) in db.keys():
    del db['prefix'+str(id)]

keep_alive()
client.run(os.getenv('TOKEN'))