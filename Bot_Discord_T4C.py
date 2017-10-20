import discord
import asyncio
from discord.ext import commands
import random
import mysql.connector
import datetime
import sys
import signal
import os

#Variable pour connexion à la base T4C
mysql_host = ""
mysql_user = ""
mysql_password = ""
mysql_base = ""

#Variable pour le bot Discord
channelCimetiere = ""
channelCC = ""
botKey = ""


description = '''An example bot to for T4C'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Commands T4C

# Boucle toutes les 5 minutes et annonce les morts depuis les 5 derniéres minutes
@asyncio.coroutine
def background_loop():
    yield from bot.wait_until_ready()
    while not bot.is_closed:
        channel = bot.get_channel(channelCimetiere)
        conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password, database=mysql_base)
        cursor = conn.cursor()
        cursor.execute("""select Victime,Assassin,date_format(TimeStamp,'%H:%i:%S') as formatted_date from logdeath2 where TimeStamp > date_format(date_sub(now(), interval 1 minute),'%Y%m%d%H%i%S')""")
        rows = cursor.fetchall()
        for row in rows:
            #await bot.say('{0} : {1}'.format(row[0],row[1]))
            yield from bot.send_message(channel,'{0} : {1} a tué {2}'.format(row[2],row[1],row[0]))
        conn.close()
        yield from asyncio.sleep(60)

bot.loop.create_task(background_loop())

# Boucle toutes les 5 minutes et annonce les discussions des CC des 5 derniéres minutes
@asyncio.coroutine
def background_loop_shout():
    yield from bot.wait_until_ready()
    while not bot.is_closed:
        channel2 = bot.get_channel(channelCC)
        conn2 = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password, database=mysql_base)
        cursor2 = conn2.cursor()
        cursor2.execute("""select TimeStamp,LogInfo from logshouts where TimeStamp > date_format(date_sub(now(), interval 1 minute),'%Y%m%d%H%i%S')""")
        rows2 = cursor2.fetchall()
        for row in rows2:
            #await bot.say('{0} : {1}'.format(row[0],row[1]))
            yield from bot.send_message(channel2,'{0} : {1}'.format(row[0],row[1]))
        conn2.close()
        yield from asyncio.sleep(60)

bot.loop.create_task(background_loop_shout())



# Commande cimetiere, annonce le top 10 XP
@bot.command()
@asyncio.coroutine
def top10():
        conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password, database=mysql_base)
        cursor = conn.cursor()
        cursor.execute("""SELECT PlayerName,CurrentLevel FROM playingcharacters ORDER BY CurrentLevel DESC LIMIT 10""")
        rows = cursor.fetchall()
        for row in rows:
                yield from bot.say('{0} - lvl {1}'.format(row[0],row[1]))
        conn.close()

bot.run(botKey)
