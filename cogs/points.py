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

  @commands.command(aliases=['pr'])
  async def prank(self, ctx, user=None):
    """Puzzle Points Rank\nDisplays your current rank with regards to puzzle points, or the rank of a specified user"""
    top = dict()
    for key in db.prefix('member'):
      member_id = int(key[6:])
      member = ctx.guild.get_member(member_id)
      if member == None:
        continue
      if db[key]['puzzle_points'] ==0:
        continue
      top.update({member.id:db[key]['puzzle_points']})
    sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
    counter = 1
    user_id = ctx.author.id
    if user != None:
      user_id = int(user[3:21])
    for member in sort_top:
      if member[0] == user_id:
        embed = discord.Embed(title=f'Rank: `#{counter}` Puzzle Points: `{member[1]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=str(ctx.guild.get_member(int(user_id)).avatar_url))
        await ctx.send(embed=embed)
        break
      else:
        counter += 1

  @commands.command(aliases=['toppoints','ppt'])
  async def pptop(self, ctx, page=1):
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
      if db[key]['puzzle_points'] ==0:
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
    embed.set_footer(text=f'Page #{page}/{int(len(sort_top)/10)+int(len(sort_top)%10>0)}')
    await ctx.channel.send(embed=embed)

def setup(client):
  client.add_cog(Points(client))