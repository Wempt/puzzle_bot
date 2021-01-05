from replit import db
import discord

def seconds_to_dd_hh_mm_ss(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if seconds >= 86400:
      return f'{d}d,{h}h,{m}m,{s}s'
    elif seconds >= 3600:
      return f'{h}h,{m}m,{s}s'
    elif seconds >= 60:
      return f'{m}m,{s}s'
    else:
      return f'{s}s'

def update_db_dict(dbkey, key, value):
  edit = db[dbkey]
  edit.update({key:value})
  db[dbkey] = edit


def edit_db_dict(dbkey, key, value):
  edit = db[dbkey]
  edit[key] = value
  db[dbkey] = edit

def give_points(dbkey, points):
  edit = db[dbkey]
  edit['puzzle_points'] = edit['puzzle_points'] + points
  db[dbkey] = edit

def get_name(member):
  if member.nick == None:
    return member.name
  return member.nick