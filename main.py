from discord.ext import commands
import discord
from utils import config
from utils import keep_alive
import os

bot = commands.Bot(command_prefix=config.prefix, activity=config.starting_activity, intents=discord.Intents.all())

bot.remove_command("help")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
         bot.load_extension(f"cogs.{filename[:-3]}")

TOKEN = os.environ.get("TOKEN")

keep_alive.keep_alive()
bot.run(TOKEN)