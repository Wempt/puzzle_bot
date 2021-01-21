import discord
from discord.ext import commands
from replit import db
from utils import get_name

class Puzzles_Solved(commands.Cog):
  """Commands that regard the amount of solved puzzles"""
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['pzs'])
  async def puzzlessolved(self, ctx, user=None):
    """Solved Puzzles\nDisplays your current number of solved puzzles, or the amount of solved puzzles of a specified user"""
    user_id = ctx.author.id
    if user != None:
      user_id = user[3:21]
    puzzles_solved = str(db['member'+str(user_id)]['puzzle_solved'])
    embed = discord.Embed(title=f'`{puzzles_solved}` solved puzzles', color=ctx.author.color)
    embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=ctx.guild.get_member(int(user_id)).avatar_url)
    await ctx.send(embed=embed)


  @commands.command(aliases=['sr'])
  async def srank(self, ctx, user=None):
    """Puzzles Solved Rank\nDisplays your current rank with regards to solved puzzles, or the puzzles solved rank of a specified user"""
    top = dict()
    for key in db.prefix('member'):
      member_id = int(key[6:])
      member = ctx.guild.get_member(member_id)
      if member == None:
        continue
      top.update({member.id:db[key]['puzzle_solved']})
    sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
    counter = 1
    user_id = ctx.author.id
    if user != None:
      user_id = int(user[3:21])
    for member in sort_top:
      if member[0] == user_id:
        embed = discord.Embed(title=f'Rank: `#{counter}` Puzzles Solved: `{member[1]}`', color=ctx.author.color)
        embed.set_author(name=get_name(ctx.guild.get_member(int(user_id))), icon_url=str(ctx.guild.get_member(int(user_id)).avatar_url))
        await ctx.send(embed=embed)
        break
      else:
        counter += 1
  

  @commands.command(aliases=['st'])
  async def stop(self, ctx, page=1):
    """Solved Puzzles Leaderboard\nShows the leaderboard with regards to the amount of puzzles solved. Can also specify a page number."""
    if page < 0:
      embed = discord.Embed(description='p̶͙̟̲̱̭̮̃̋͒͊̈̿̑b̸͙̘͈̼͙̃̉̾̋͂͗̊͜a̷͉͎̟̰̪͊̐̌d̷̹̩̮̘͑̈́̽̑̎̚ḑ̴̱̘͈͌͐̉͘ǐ̶̞̺̟̺͓̳̐̈́͂̓́ê̴̦̮̞̈́͐͐ ̸͖̕͝w̸̬̲̻̣̒̉̽̄̂a̷̹͐̇̈́̆s̷͍̹͈̗͉̏͌͜ ̴̛̞̣͕̬̅h̸̢͚̘̻͇̪̱͛̿̋̏͒e̷̺̯͇̯̜͚̖̽̋͐͊͝r̷̛͓͓̯̖͚͎̄͐̾͝è̴̛͇̖̣̰̲͎͍̎̀̊̊͝ ̵̨͍̰͆̍͝͝:̵̳̭̥̐̍̿͜͜͠)̵̞̳͈̝̺̜̈́̉͋͜͝)̴̙͒̔͑̈́)̶̯͌̆̄̿)̷̘̘͙̖͈̟̓͛̚͜)̵̟̟̞̼̂̆͂͘)̸̡͎̞̱̪͓̃̾̕͜)̴̧̮͇̈́̍͊͌',color=ctx.author.color)
      embed.set_author(name='puzzles solved leaderboard', icon_url=str(ctx.author.avatar_url))
      embed.set_footer(text=f'Page #{page}')
      await ctx.send(embed=embed)
      return
    top = dict()
    for key in db.prefix('member'):
      member_id = int(key[6:])
      member = ctx.guild.get_member(member_id)
      if member == None:
        continue
      top.update({member.id:db[key]['puzzle_solved']})
    sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
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
      result = f'{result}\n{counter:<2}{emoji}`{sort_top[counter-1][1]}`:**{get_name(ctx.guild.get_member(sort_top[counter-1][0]))}**'
      counter += 1
      if (counter == 10):
        break
    embed = discord.Embed(description=result,color=ctx.author.color)
    embed.set_author(name=f'puzzles solved leaderboard', icon_url=str(ctx.author.avatar_url))
    embed.set_footer(text=f'Page #{page}/{int(len(top)/10)+int(len(top)%10>0)}')
    await ctx.channel.send(embed=embed)


def setup(client):
  client.add_cog(Puzzles_Solved(client))