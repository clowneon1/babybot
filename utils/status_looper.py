from discord.ext import tasks
import discord
import random
from main import bot

@tasks.loop(seconds=30)
async def statusLooper():
    statuses = ['Quinmon best streamer','Your mum','The best bot','Eddie Mac C','Not a fridge']

    options = [
        bot.change_presence(activity=discord.Streaming(name=random.choice(statuses), url='https://www.twitch.tv/xephirehd')),
        bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(statuses))),
        bot.change_presence(activity=discord.Game(name=random.choice(statuses))),
        bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(statuses)))
    ]

    opt = random.randint(1,4)
    await options[opt]