import discord
from discord.ext import commands
from replit import db
from utils import get_name

class Tops(commands.Cog):
  """Leaderboard commands"""

  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['toppoints','tp'])
  async def top(self, ctx, page=1):
    """Point Leaderboard\nShows the leaderboard with regards to points. Can also specify a page number."""
    if page < 0:
      embed = discord.Embed(description='p̶͙̟̲̱̭̮̃̋͒͊̈̿̑b̸͙̘͈̼͙̃̉̾̋͂͗̊͜a̷͉͎̟̰̪͊̐̌d̷̹̩̮̘͑̈́̽̑̎̚ḑ̴̱̘͈͌͐̉͘ǐ̶̞̺̟̺͓̳̐̈́͂̓́ê̴̦̮̞̈́͐͐ ̸͖̕͝w̸̬̲̻̣̒̉̽̄̂a̷̹͐̇̈́̆s̷͍̹͈̗͉̏͌͜ ̴̛̞̣͕̬̅h̸̢͚̘̻͇̪̱͛̿̋̏͒e̷̺̯͇̯̜͚̖̽̋͐͊͝r̷̛͓͓̯̖͚͎̄͐̾͝è̴̛͇̖̣̰̲͎͍̎̀̊̊͝ ̵̨͍̰͆̍͝͝:̵̳̭̥̐̍̿͜͜͠)̵̞̳͈̝̺̜̈́̉͋͜͝)̴̙͒̔͑̈́)̶̯͌̆̄̿)̷̘̘͙̖͈̟̓͛̚͜)̵̟̟̞̼̂̆͂͘)̸̡͎̞̱̪͓̃̾̕͜)̴̧̮͇̈́̍͊͌',color=ctx.author.color)
      embed.set_author(name='puzzle points leaderboard', icon_url=str(ctx.author.avatar_url))
      embed.set_footer(text=f'Page #{page}')
      await ctx.channel.send(embed=embed)
      return
    top = dict()
    for key in db.prefix('member'):
      member_id = int(key[6:])
      member = ctx.guild.get_member(member_id)
      if member == None:
        continue
      top.update({member.id:db[key]['puzzle_points']})
    sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
    result = ''
    counter = 1 + (10*(page-1))
    while counter <= 10*page and counter <= len(sort_top):
      emoji = ':medal:'
      if counter == 1:
        emoji = ':first_place:'
      elif counter == 2:
        emoji = ':second_place:'
      elif counter == 3:
        emoji = ':third_place:'
      result = f'{result}\n{counter:<2}{emoji}`{sort_top[counter-1][1]}`:**{get_name(ctx.guild.get_member(sort_top[counter-1][0]))}**'
      counter += 1
    embed = discord.Embed(description=result,color=ctx.author.color)

    embed.set_author(name='puzzle points leaderboard', icon_url=str(ctx.author.avatar_url))
    embed.set_footer(text=f'Page #{page}')
    await ctx.channel.send(embed=embed)

  @commands.command(aliases=['tt'])
  async def toptime(self, ctx, page=1, puzzle=db['current_puzzle']):
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
    embed.set_footer(text=f'Page #{page}')
    await ctx.channel.send(embed=embed)

def setup(client):
  client.add_cog(Tops(client))