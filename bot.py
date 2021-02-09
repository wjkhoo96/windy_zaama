# bot.py
import os

import discord
from dotenv import load_dotenv
import lyricsgenius
from pykakasi import kakasi
# import pandas as pd
# import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# # init banlist
# df = pd.read_csv("banlist.csv")

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.content.lower().startswith('!cp '):
        artist, song = message.content.split(" ",1)[1].split(' - ')
        romanized_lyric = get_lyric(artist, song)
        # init embed
        embed = discord.Embed(title = song + " by " + artist, color=0x00ff00)
        num_of_embeds = len(romanized_lyric)//2048 + 1
        for i in range(num_of_embeds):
            embed.description = romanized_lyric[i*2048:i+1*2048]
            await message.channel.send(embed=embed)

    ### doesn't work on rythm bot
    # # force skip banlisted songs
    # if message.content.lower().startswith('!p ') or message.content.lower().startswith('!ps '):
    #     queued_song = message.content.split(" ",1)[1]
    #     banlist = df['song'].tolist()
    #     time.sleep(3)
    #     if any(item in queued_song for item in banlist):
    #         await message.channel.send("!fs")

    # # add to banlist
    # if message.content.lower().startswith('!bla '):
    #     song_name = message.content.split(" ",1)[1]
    #     if song_name is not None:
    #         d_f = df.append({'song': song_name},ignore_index=True)
    #         d_f.to_csv('banlist.csv', mode='w')
    #         await message.channel.send("added "+song_name+" to banlist")

    # # remove from banlist
    # if message.content.lower().startswith('!blr '):
    #     song_name = message.content.split(" ",1)[1]
    #     if song_name is not None:
    #         d_f = df[df.song != song_name]
    #         d_f.to_csv('banlist.csv',mode='w')
    #         await message.channel.send("removed "+song_name+" from banlist")

    # # list banlist
    # if message.content.lower().startswith('!blv'):
    #     d_f = pd.read_csv("banlist.csv")
    #     banlist = d_f['song'].tolist()
    #     # init embed
    #     embed = discord.Embed(title = "banlist", color=0x00ff00)
    #     embed.description = "\n".join(banlist)
    #     await message.channel.send(embed=embed)

def get_lyric(artist, song_name):
    GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')
    genius = lyricsgenius.Genius(GENIUS_TOKEN)
    song = genius.search_song(song_name, artist)
    if song is not None:
        romanized_lyric = convert_lyric(song.lyrics)
        return romanized_lyric
    else:
        return "No results found for: " + song_name + " by "+ artist

def convert_lyric(lyric):
    kks = kakasi()
    kks.setMode("H","a") # Hiragana to ascii, default: no conversion
    kks.setMode("K","a") # Katakana to ascii, default: no conversion
    kks.setMode("J","a") # Japanese to ascii, default: no conversion
    kks.setMode("r","Hepburn") # default: use Hepburn Roman table
    kks.setMode("s", True) # add space, default: no separator
    kks.setMode("C", True) # capitalize, default: no capitalize
    conv = kks.getConverter()
    result = conv.do(lyric)
    return result

client.run(TOKEN)