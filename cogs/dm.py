import discord
import time
import os
from discord.ext import commands
from replit import db
from utils import seconds_to_dd_hh_mm_ss, edit_db_dict, update_db_dict, give_points, get_name, position

class DM(commands.Cog):
  """Commands that are used while DMing the bot"""
  def __init__(self, client):
    self.client = client

  def is_dm(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      return True
    return False

  def blacklist(ctx):
    blacklist = os.getenv('BLACKLIST').split(',')
    if str(ctx.author.id) not in blacklist:
      return True
    return False

  @commands.command(aliases=['c'])
  @commands.check(is_dm)
  @commands.check(blacklist)
  async def check(self, ctx, answer, current_puzzle=db['current_puzzle']):
    """Allows you to check your answer to the current puzzle, as well as older puzzles."""
    if answer != os.getenv(f'ANSWER{current_puzzle}'):
      await ctx.send('Not the correct answer sorry :/.')
      return

    #for testing v
    #edit_db_dict(f'member{ctx.author.id}', 'solved', False)
    #for testing ^

    if not db[f'member{ctx.author.id}']['solved']:
      edit_db_dict(f'member{ctx.author.id}', 'solved', True)
      current_puzzle = db['current_puzzle']
      time_taken = seconds_to_dd_hh_mm_ss(int(time.time() - db[f'puzzle{current_puzzle}time']))
      update_db_dict(f'puzzle{current_puzzle}top', ctx.author.id, time_taken)
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
      give_points(f'member{ctx.author.id}', points)
      edit_db_dict(f'member{ctx.author.id}','puzzle_solved',(db[f'member{ctx.author.id}']['puzzle_solved']+1))
      await ctx.send(f'Solved in {time_taken}. Awarded {points} puzzle points for finishing {position(place)}')
      puzzle_channel_id = int(os.getenv('PUZZLE_CHANNEL'))
      embed = discord.Embed(description=f'Solved in `{time_taken}`. Awarded `{points}` puzzle points for finishing `{position(place)}`',color=self.client.get_guild(int(os.getenv('GUILD'))).get_member(ctx.author.id).color)
      embed.set_author(name=get_name(self.client.get_guild(int(os.getenv('GUILD'))).get_member(ctx.author.id)), icon_url=ctx.author.avatar_url)
      await self.client.get_guild(int(os.getenv('GUILD'))).get_channel(puzzle_channel_id).send(embed=embed)
      role = self.client.get_guild(int(os.getenv('GUILD'))).get_role(int(os.getenv('SOLVED')))
      await self.client.get_guild(int(os.getenv('GUILD'))).get_member(ctx.author.id).add_roles(role)


    else:
      await ctx.send('You already solved this but nice try :)')

def setup(client):
  client.add_cog(DM(client)) 