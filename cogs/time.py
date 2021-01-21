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


  @commands.command(aliases=['tr'])
  async def trank(self, ctx, puzzle=db['current_puzzle'], user=None):
    """Puzzle Solve Time Rank\nDisplays your current rank with regards to puzzle solve time of the current or specified puzzle, also allows you to specify a user"""
    top = db[f'puzzle{puzzle}top']
    counter = 1
    user_id = ctx.author.id
    if user != None:
      user_id = int(user[3:21])
    for member in top:
      if int(member) == int(user_id):
        embed = discord.Embed(title=f'Rank: `#{counter}` Solve Time: `{top[member]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=str(ctx.guild.get_member(int(user_id)).avatar_url))
        await ctx.send(embed=embed)
        break
      else:
        counter += 1


  @commands.command(aliases=['tt'])
  async def ttop(self, ctx, page=1, puzzle=db['current_puzzle']):
    """Time Leaderboard\nShows the leaderboard with regards to the solve time of the current puzzle. Can also specify a page number."""
    if page < 0:
      embed = discord.Embed(description='p̶͙̟̲̱̭̮̃̋͒͊̈̿̑b̸͙̘͈̼͙̃̉̾̋͂͗̊͜a̷͉͎̟̰̪͊̐̌d̷̹̩̮̘͑̈́̽̑̎̚ḑ̴̱̘͈͌͐̉͘ǐ̶̞̺̟̺͓̳̐̈́͂̓́ê̴̦̮̞̈́͐͐ ̸͖̕͝w̸̬̲̻̣̒̉̽̄̂a̷̹͐̇̈́̆s̷͍̹͈̗͉̏͌͜ ̴̛̞̣͕̬̅h̸̢͚̘̻͇̪̱͛̿̋̏͒e̷̺̯͇̯̜͚̖̽̋͐͊͝r̷̛͓͓̯̖͚͎̄͐̾͝è̴̛͇̖̣̰̲͎͍̎̀̊̊͝ ̵̨͍̰͆̍͝͝:̵̳̭̥̐̍̿͜͜͠)̵̞̳͈̝̺̜̈́̉͋͜͝)̴̙͒̔͑̈́)̶̯͌̆̄̿)̷̘̘͙̖͈̟̓͛̚͜)̵̟̟̞̼̂̆͂͘)̸̡͎̞̱̪͓̃̾̕͜)̴̧̮͇̈́̍͊͌',color=ctx.author.color)
      embed.set_author(name='puzzle points leaderboard', icon_url=str(ctx.author.avatar_url))
      embed.set_footer(text=f'Page #{page}')
      await ctx.send(embed=embed)
      return
    current_puzzle = puzzle
    top = db[f'puzzle{current_puzzle}top']
    keys = list(top.keys())
    result = ''
    counter = 1 + (10*(page-1))
    while counter <= 10*page and counter <= len(top):
      emoji = ':medal:'
      if counter == 1:
        emoji = ':first_place:'
      elif counter == 2:
        emoji = ':second_place:'
      elif counter == 3:
        emoji = ':third_place:'
      result = f'{result}\n{counter:<2}{emoji}`{top[keys[counter-1]]}`:**{get_name(ctx.guild.get_member(int(keys[counter-1])))}**'
      counter += 1
      if (counter == 10):
        break
    embed = discord.Embed(description=result,color=ctx.author.color)
    embed.set_author(name=f'puzzle #{current_puzzle} leaderboard', icon_url=str(ctx.author.avatar_url))
    embed.set_footer(text=f'Page #{page}/{int(len(top)/10)+int(len(top)%10>0)}')
    await ctx.channel.send(embed=embed)

def setup(client):
  client.add_cog(Time(client))