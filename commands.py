import discord
import time
import os
from utils import edit_db_dict, get_name
from replit import db

async def command_handler(message):
  guild_id = message.guild.id
  msg = message.content.split(db['prefix'+str(guild_id)], 1)[1]
  if msg.startswith('updateprefix') or msg.startswith('upp'):
    await update_prefix(message, msg)
  elif msg.startswith('puzzlepoints') or msg.startswith('pps'):
    await puzzle_points(message, msg)
  elif msg.startswith('time'):
    await puzzle_time(message,msg)
  elif msg.startswith('releasepuzzle') or msg.startswith('rpz'):
    await release_puzzle(message,msg)
  elif msg.startswith('tt') or msg.startswith('toptime'):
    await top_time(message,msg)
  elif msg.startswith('top'):
    await top_points(message,msg)
  elif msg.startswith('rank'):
    await rank(message, msg)
  elif msg.startswith('help'):
    await help(message, msg)
  elif msg.startswith('info'):
    await info(message, msg)
  #elif msg.startswith('setpps'):
    #temp for testing i think
    #await setpps(message,msg)



# updateprefix ''
async def update_prefix(message, msg):
  if not message.author.top_role.permissions.administrator:
    await message.channel.send('must be admin to use this command')
    return
  try:
    prefix = msg.split('updateprefix',1)[1].strip()
  except Exception:
    prefix = msg.split('upp',1)[1].strip()
  if prefix == '':
    await message.channel.send('must designate a prefix')
    return
  guild_id = message.guild.id
  db['prefix'+str(guild_id)] = prefix
  await message.channel.send('prefix set to ' + prefix)

# puzzle points
async def puzzle_points(message, msg):
  user_id = message.author.id
  puzzles = str(db['member'+str(user_id)]['puzzle_points'])
  embed = discord.Embed(title=f'`{puzzles}` puzzle points', color=message.author.color)
  embed.set_author(name=get_name(message.author), icon_url=message.author.avatar_url)
  await message.channel.send(embed=embed)

async def puzzle_time(message,msg):
  current_puzzle = db['current_puzzle']
  top = db[f'puzzle{current_puzzle}top']
  for id in top:
    if int(id) == int(message.author.id):
      embed = discord.Embed(title=f'puzzle `{current_puzzle}` solved in `{top[id]}`', color=message.author.color)
      embed.set_author(name=get_name(message.author), icon_url=message.author.avatar_url)
      await message.channel.send(embed=embed)
      return
  embed = discord.Embed(title=f'you haven\'t solved puzzle `{current_puzzle}` yet', color=message.author.color)
  embed.set_author(name=get_name(message.author), icon_url=message.author.avatar_url)
  await message.channel.send(embed=embed)

# release puzzle :)
# want to make a website thing at some point
async def release_puzzle(message,msg):
  member = message.author
  if str(member) == 'Wempt#3532':
    puzzle_number = msg.split()[1]
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
    embed.set_footer(text='DM this bot your answer to get puzzle points :)')
    await message.guild.get_channel(puzzle_channel_id).send(embed=embed)
    await message.delete()

# leader board
# maybe an website version at some point?
async def top_points(message,msg):
  try:  
    page = int(msg.split()[1])
  except Exception:
    page = 1
  if page < 0:
    embed = discord.Embed(description='p̶͙̟̲̱̭̮̃̋͒͊̈̿̑b̸͙̘͈̼͙̃̉̾̋͂͗̊͜a̷͉͎̟̰̪͊̐̌d̷̹̩̮̘͑̈́̽̑̎̚ḑ̴̱̘͈͌͐̉͘ǐ̶̞̺̟̺͓̳̐̈́͂̓́ê̴̦̮̞̈́͐͐ ̸͖̕͝w̸̬̲̻̣̒̉̽̄̂a̷̹͐̇̈́̆s̷͍̹͈̗͉̏͌͜ ̴̛̞̣͕̬̅h̸̢͚̘̻͇̪̱͛̿̋̏͒e̷̺̯͇̯̜͚̖̽̋͐͊͝r̷̛͓͓̯̖͚͎̄͐̾͝è̴̛͇̖̣̰̲͎͍̎̀̊̊͝ ̵̨͍̰͆̍͝͝:̵̳̭̥̐̍̿͜͜͠)̵̞̳͈̝̺̜̈́̉͋͜͝)̴̙͒̔͑̈́)̶̯͌̆̄̿)̷̘̘͙̖͈̟̓͛̚͜)̵̟̟̞̼̂̆͂͘)̸̡͎̞̱̪͓̃̾̕͜)̴̧̮͇̈́̍͊͌',color=message.author.color)
    embed.set_author(name='puzzle points leaderboard', icon_url=str(message.author.avatar_url))
    embed.set_footer(text=f'Page #{page}')
    await message.channel.send(embed=embed)
    return
  top = dict()
  for key in db.prefix('member'):
    member_id = int(key[6:])
    member = message.channel.guild.get_member(member_id)
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
    result = f'{result}\n{counter:<2}{emoji}`{sort_top[counter-1][1]}`:**{get_name(message.guild.get_member(sort_top[counter-1][0]))}**'
    counter += 1
  embed = discord.Embed(description=result,color=message.author.color)
  embed.set_author(name='puzzle points leaderboard', icon_url=str(message.author.avatar_url))
  embed.set_footer(text=f'Page #{page}')
  await message.channel.send(embed=embed)

async def top_time(message,msg):
  try:  
    page = int(msg.split()[1])
  except Exception:
    page = 1
  if page < 0:
    embed = discord.Embed(description='p̶͙̟̲̱̭̮̃̋͒͊̈̿̑b̸͙̘͈̼͙̃̉̾̋͂͗̊͜a̷͉͎̟̰̪͊̐̌d̷̹̩̮̘͑̈́̽̑̎̚ḑ̴̱̘͈͌͐̉͘ǐ̶̞̺̟̺͓̳̐̈́͂̓́ê̴̦̮̞̈́͐͐ ̸͖̕͝w̸̬̲̻̣̒̉̽̄̂a̷̹͐̇̈́̆s̷͍̹͈̗͉̏͌͜ ̴̛̞̣͕̬̅h̸̢͚̘̻͇̪̱͛̿̋̏͒e̷̺̯͇̯̜͚̖̽̋͐͊͝r̷̛͓͓̯̖͚͎̄͐̾͝è̴̛͇̖̣̰̲͎͍̎̀̊̊͝ ̵̨͍̰͆̍͝͝:̵̳̭̥̐̍̿͜͜͠)̵̞̳͈̝̺̜̈́̉͋͜͝)̴̙͒̔͑̈́)̶̯͌̆̄̿)̷̘̘͙̖͈̟̓͛̚͜)̵̟̟̞̼̂̆͂͘)̸̡͎̞̱̪͓̃̾̕͜)̴̧̮͇̈́̍͊͌',color=message.author.color)
    embed.set_author(name='puzzle points leaderboard', icon_url=str(message.author.avatar_url))
    embed.set_footer(text=f'Page #{page}')
    await message.channel.send(embed=embed)
    return
  current_puzzle = db['current_puzzle']
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
    result = f'{result}\n{counter:<2}{emoji}`{top[keys[counter-1]]}`:**{get_name(message.guild.get_member(int(keys[counter-1])))}**'
    counter += 1
    if (counter == 10):
      break
  embed = discord.Embed(description=result,color=message.author.color)
  embed.set_author(name=f'puzzle #{current_puzzle} leaderboard', icon_url=str(message.author.avatar_url))
  embed.set_footer(text=f'Page #{page}')
  await message.channel.send(embed=embed)

async def rank(message, msg):
  top = dict()
  for key in db.prefix('member'):
    member_id = int(key[6:])
    member = message.channel.guild.get_member(member_id)
    if member == None:
      continue
    top.update({member.id:db[key]['puzzle_points']})
  sort_top = sorted(top.items(), key=lambda x: x[1], reverse=True)
  counter = 1
  for member in sort_top:
    if member[0] == message.author.id:
      embed = discord.Embed(title=f'Rank: `#{counter}` Puzzle Points: `{member[1]}`', color=message.author.color)
      embed.set_author(name=get_name(message.author), icon_url=str(message.author.avatar_url))
      await message.channel.send(embed=embed)
      break
    else:
      counter += 1
  
async def help(message,msg):
  prefix = db['prefix'+str(message.guild.id)]
  embed = discord.Embed(description=f'**{prefix}help:** displays this message with a list of all commands\n**{prefix}info:** displays some information about the bot\n**{prefix}puzzlepoints/pps:** Displays how many puzzle points you have\n**{prefix}time:** Displays the time you solved the current puzzle in\n**{prefix}top:** shows the leaderboard for puzzle points\n**{prefix}toptime/tt:** shows the leaderboard for the solve time of the current puzzle\n**{prefix}rank:** shows your current rank with regards to puzzle points\n', color=message.author.color)
  embed.set_author(name='Commands:', icon_url=str(message.author.avatar_url))
  await message.channel.send(embed=embed)

async def info(message,msg):
  embed = discord.Embed(description=f'This bot was created by Wempt during winter break so that they didn\'t forget how to "do the code". The basics are that I will release a puzzle made by me or some other smart person, at which point people will be able to solve and dm the answer to this bot and recieve points based on the position they finished in. You can view the code for this bot at https://github.com/Wempt/puzzle_bot. Don\'t mind how messy the code is. ps don\'t bother looking in the github for puzzle answers you won\'t find them there ;)', color=message.author.color)
  embed.set_footer(text=' If you have any suggestions for features or find any bugs feel free to dm me aka Wempt :))')
  embed.set_author(name='Bot Information', icon_url=str(message.author.avatar_url))
  await message.channel.send(embed=embed)


# for testing
async def setpps(message,msg):
  values = msg.split()
  member_id = values[1][3:21]
  points = values[2]
  dic = db['member'+member_id]
  dic['puzzle_points'] = points
  db['member'+member_id] = dic
  print(db['member'+member_id])