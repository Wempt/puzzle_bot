from replit import db
import discord
from discord.ext import commands
from utils import startup, clear_db

class Events(commands.Cog):
  
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    #clear_db()
    startup(self.client)
    print(f'{self.client.user} connected')

  @commands.Cog.listener()
  async def on_member_join(self, ctx):
    member_id = ctx.id
    dic = {'name':str(ctx.name), 'puzzle_points':0, 'solved':False}
    if('member'+str(member_id)) not in db.keys() and not ctx.bot:
      db['member'+str(member_id)] = dic
      print(db['member'+str(member_id)])
  
  @commands.Cog.listener()
  async def on_member_remove(self, ctx):
    member_id = ctx.id
    if('member'+str(member_id)) in db.keys() and not ctx.bot:
      del db['member'+str(member_id)]


def setup(client):
  client.add_cog(Events(client))