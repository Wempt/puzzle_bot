import discord
from discord.ext import commands
from pretty_help import PrettyHelp
import os
from replit import db
from commands import command_handler
from dm import dm_handler
from keep_alive import keep_alive
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '$', intents = intents)




    #old method of storing but you can use dicts so :))))
    #if ('puzzle'+str(member_id)) not in db.keys() and not member.bot:
    #  db['puzzle'+str(member_id)] = 0





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

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

keep_alive()
client.run(os.getenv('TOKEN'))