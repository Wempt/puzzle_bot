import os
import discord
import time
from utils import seconds_to_dd_hh_mm_ss, edit_db_dict, update_db_dict, give_points, get_name, position
from replit import db

async def dm_handler(message, client):
  msg = message.content
  current_puzzle = db['current_puzzle']
  if msg == os.getenv(f'ANSWER{current_puzzle}'):
    await correct(message,msg, client)
  else:
    await incorrect(message,msg)

async def correct(message, msg, client):
  #for testing v
  #edit_db_dict(f'member{message.author.id}', 'solved', False)
  #for testing ^

  if not db[f'member{message.author.id}']['solved']:
    edit_db_dict(f'member{message.author.id}', 'solved', True)
    current_puzzle = db['current_puzzle']
    time_taken = seconds_to_dd_hh_mm_ss(int(time.time() - db[f'puzzle{current_puzzle}time']))
    update_db_dict(f'puzzle{current_puzzle}top', message.author.id, time_taken)
    place = len(db[f'puzzle{current_puzzle}top'])
    points = 1
    if place == 5:
      points = 2
    elif place == 4:
      points = 3
    elif place == 3:
      points = 4
    elif place == 2:
      points = 5
    elif place == 1:
      points = 7
    give_points(f'member{message.author.id}', points)
    await message.channel.send(f'Solved in {time_taken}. Awarded {points} puzzle points for finishing {position(place)}')
    puzzle_channel_id = int(os.getenv('PUZZLE_CHANNEL'))

    embed = discord.Embed(description=f'Solved in `{time_taken}`. Awarded `{points}` puzzle points for finishing `{position(place)}`',color=client.get_guild(int(os.getenv('GUILD'))).get_member(message.author.id).color)
    embed.set_author(name=get_name(client.get_guild(int(os.getenv('GUILD'))).get_member(message.author.id)), icon_url=message.author.avatar_url)
    await client.get_guild(int(os.getenv('GUILD'))).get_channel(puzzle_channel_id).send(embed=embed)

  else:
    await message.channel.send('You already solved this but nice try :)')

async def incorrect(message, msg):
  await message.channel.send('no >:(')