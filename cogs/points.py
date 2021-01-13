import discord
from discord.ext import commands
from replit import db
from utils import get_name

class Points(commands.Cog):
  """Commands that regard puzzle points"""
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['pps'])
  async def puzzlepoints(self, ctx):
    """Puzzle Points\nDisplays your current number of puzzle points"""
    user_id = ctx.author.id
    puzzles = str(db['member'+str(user_id)]['puzzle_points'])
    embed = discord.Embed(title=f'`{puzzles}` puzzle points', color=ctx.author.color)
    embed.set_author(name=get_name(ctx.author), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

  @commands.command()
  async def rank(self, ctx):
    """Puzzle Points Rank\nDisplays your current rank with regards to puzzle points"""
    top = dict()
    for key in db.prefix('member'):
      member_id = int(key[6:])
      member = ctx.guild.get_member(member_id)
      if member == None:
        continue
      top.update({member.id:db[key]['puzzle_points']})
    sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
    counter = 1
    for member in sort_top:
      if member[0] == ctx.author.id:
        embed = discord.Embed(title=f'Rank: `#{counter}` Puzzle Points: `{member[1]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.author), icon_url=str(ctx.author.avatar_url))
        await ctx.send(embed=embed)
        break
      else:
        counter += 1

def setup(client):
  client.add_cog(Points(client))