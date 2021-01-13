import discord
from discord.ext import commands
from replit import db
from utils import get_name

class Time(commands.Cog):
  """Commands that regard puzzle solve time"""

  def __init__(self, client):
    client.self = self

  @commands.command(aliases=['time'])
  async def puzzletime(self, ctx):
    """Solve Time\nDisplays your solve time for the current puzzle"""
    current_puzzle = db['current_puzzle']
    top = db[f'puzzle{current_puzzle}top']
    for id in top:
      if int(id) == int(ctx.author.id):
        embed = discord.Embed(title=f'puzzle `{current_puzzle}` solved in `{top[id]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        return
    embed = discord.Embed(title=f'you haven\'t solved puzzle `{current_puzzle}` yet', color=ctx.author.color)
    embed.set_author(name=get_name(ctx.author), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)

def setup(client):
  client.add_cog(Time(client))