from discord.ext import commands
from utils import config
import discord

class MemberJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.id in config.welcome_channel_ids and channel in member.guild.text_channels:
                    await channel.send(f'Welcome to **{member.guild.name}**, {member.mention}, enjoy your stay!')
                    return await member.add_roles(discord.utils.get(member.guild.roles, name=config.welcome_roles[member.guild.id]))
                    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.id in config.leave_channel_ids and channel in member.guild.text_channels:
                    return await channel.send(f'{member.mention} just left **{member.guild.name}**, what a shame.')

def setup(bot):
    bot.add_cog(MemberJoinLeave(bot))