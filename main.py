import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from replit import db
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '$', intents = intents)

if db['current_puzzle'] == None:
  db['current_puzzle'] = 0

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

keep_alive()
client.run(os.getenv('TOKEN'))