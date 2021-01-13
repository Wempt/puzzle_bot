import discord
import os
import time
from discord.ext import commands
from replit import db
from utils import edit_db_dict

class Other(commands.Cog):
  """Other commands that are used for various things :)"""

  def __init__(self, client):
    self.client = client

  def is_me(ctx):
    if ctx.author.id == 202150683619622921:
      return True
    return False

  @commands.command(aliases=['rpz'], hidden='True')
  @commands.check(is_me)
  async def release_puzzle(self, ctx, puzzle_number):
    """Release Puzzle\n For our dearest Wempt to release the puzzles."""
    db['current_puzzle'] = puzzle_number
    db[f'puzzle{puzzle_number}time'] = time.time()
    db[f'puzzle{puzzle_number}top'] = dict()
    for member in db.prefix('member'):
      edit_db_dict(member, 'solved', False)
    puzzle = os.getenv(f'PUZZLE{puzzle_number}')
    embed = discord.Embed(title=f'puzzle #{puzzle_number}',color=discord.Color.gold())
    if puzzle.startswith('https://i.imgur.com'):
      embed.set_image(url = puzzle)
    else:
      embed.description = puzzle
    puzzle_channel_id = int(os.getenv('PUZZLE_CHANNEL'))
    embed.set_footer(text=f'DM this bot $c \'your answer here\' {puzzle_number} to get puzzle points :)')
    await ctx.guild.get_channel(puzzle_channel_id).send(embed=embed)
    await ctx.guild.get_channel(puzzle_channel_id).last_message.pin()
    await ctx.message.delete()

  @commands.command()
  async def info(self, ctx):
    """Information about bot\nGives the basics of using the bot and a link to the source code on github"""
    embed = discord.Embed(description=f'This bot was created by Wempt during winter break so that they didn\'t forget how to "do the code". The basics are that I will release a puzzle made by me or some other smart person, at which point people will be able to solve and dm the answer to this bot and recieve points based on the position they finished in. You can view the code for this bot at https://github.com/Wempt/puzzle_bot. Don\'t mind how messy the code is. ps don\'t bother looking in the github for puzzle answers you won\'t find them there ;)', color=ctx.author.color)
    embed.set_footer(text=' If you have any suggestions for features or find any bugs feel free to dm me aka Wempt :))')
    embed.set_author(name='Bot Information', icon_url=str(ctx.author.avatar_url))
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Other(client))

