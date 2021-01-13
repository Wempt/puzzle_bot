import discord
from discord.ext import commands
from replit import db
from utils import get_name

class Points(commands.Cog):
  """Commands that regard puzzle points"""
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['pps'])
  async def puzzlepoints(self, ctx, user=None):
    """Puzzle Points\nDisplays your current number of puzzle points, or the puzzle points of a specified user"""
    user_id = ctx.author.id
    if user != None:
      user_id = user[3:21]
    puzzles = str(db['member'+str(user_id)]['puzzle_points'])
    embed = discord.Embed(title=f'`{puzzles}` puzzle points', color=ctx.author.color)
    embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=ctx.guild.get_member(int(user_id)).avatar_url)
    await ctx.send(embed=embed)

  @commands.command()
  async def rank(self, ctx, user=None):
    """Puzzle Points Rank\nDisplays your current rank with regards to puzzle points, or the rank of a specified user"""
    top = dict()
    for key in db.prefix('member'):
      member_id = int(key[6:])
      member = ctx.guild.get_member(member_id)
      if member == None:
        continue
      top.update({member.id:db[key]['puzzle_points']})
    sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
    counter = 1
    user_id = ctx.author.id
    if user != None:
      user_id = int(user[3:21])
    print(user_id)
    for member in sort_top:
      if member[0] == user_id:
        embed = discord.Embed(title=f'Rank: `#{counter}` Puzzle Points: `{member[1]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=str(ctx.guild.get_member(int(user_id)).avatar_url))
        await ctx.send(embed=embed)
        break
      else:
        counter += 1

def setup(client):
  client.add_cog(Points(client))