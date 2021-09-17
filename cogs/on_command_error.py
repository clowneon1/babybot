from discord.ext import commands
import discord

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass

def setup(bot):
    bot.add_cog(OnCommandError(bot))