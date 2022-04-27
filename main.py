import asyncio
from contextlib import AsyncExitStack
from dis import disco
from http import client
from sys import prefix
import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
import random
import youtube_dl
import time
import music

cogs = [music]

client = commands.Bot(command_prefix='/', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("OTY4NTYyMTc5ODQ0NTA1NjQw.Ymgp0g.veq5HizVcXu_mV60ctXJup7NigA")




