import discord
from discord.ext import commands
from replit import db
from utils import get_name

class Time(commands.Cog):
  """Commands that regard puzzle solve time"""

  def __init__(self, client):
    client.self = self

  @commands.command(aliases=['time'])
  async def puzzletime(self, ctx, puzzle=db['current_puzzle'], user=None):
    """Solve Time\nDisplays your solve time for the current puzzle, or a specified puzzle, and/or the solve time of a specified user."""
    user_id = ctx.author.id
    if user != None:
      user_id = user[3:21]

    current_puzzle = puzzle
    top = db[f'puzzle{current_puzzle}top']
    for id in top:
      if int(id) == int(user_id):
        embed = discord.Embed(title=f'puzzle `{current_puzzle}` solved in `{top[id]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.guild.get_member(int(id))), icon_url=ctx.guild.get_member(int(id)).avatar_url)
        await ctx.channel.send(embed=embed)
        return
    embed = discord.Embed(title=f'{get_name(ctx.guild.get_member(int(user_id)))} hasn\'t solved puzzle `{current_puzzle}` yet', color=ctx.author.color)
    embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=ctx.guild.get_member(int(user_id)).avatar_url)
    await ctx.channel.send(embed=embed)

def setup(client):
  client.add_cog(Time(client))