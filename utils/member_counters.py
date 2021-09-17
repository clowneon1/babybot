from discord.ext import tasks
from utils import config
import discord
from main import bot

@tasks.loop(seconds=20)
async def memberCount():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if vc.id in config.total_members_vc_ids and vc.name != f'{guild.member_count} members':
                await vc.edit(name = f'{guild.member_count} members')
                break

@tasks.loop(seconds=10)
async def onlineMemberCount():
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            if vc.id in config.online_members_vc_ids:
                members = guild.members
                onlineMembers = [member for member in members if member.status in [discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]]
                if vc.name != f'{len(onlineMembers)} online members':
                    await vc.edit(name = f'{len(onlineMembers)} online members')
