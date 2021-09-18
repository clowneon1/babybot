from discord.ext import commands, tasks
import discord
import random
from utils import config

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name="The best bot.", url='https://www.twitch.tv/xephirehd'))
        self.statusLooper.start()
        self.memberCount.start()
        self.onlineMemberCount.start()
        print('Bot ready')

    @tasks.loop(seconds=20)
    async def memberCount(self):
        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                if vc.id in config.total_members_vc_ids and vc.name != f'{guild.member_count} members':
                    await vc.edit(name = f'Members: {guild.member_count}')
                    break

    @tasks.loop(seconds=10)
    async def onlineMemberCount(self):
        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                if vc.id in config.online_members_vc_ids:
                    members = guild.members
                    onlineMembers = [member for member in members if member.status in [discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]]
                    if vc.name != f'{len(onlineMembers)} online members':
                        await vc.edit(name = f'Online Members: {len(onlineMembers)} online members')

    @tasks.loop(seconds=30)
    async def statusLooper(self):
        statuses = ['Quinmon best streamer','Your mum','The best bot','Eddie Mac C','Not a fridge']

        opt = random.randint(1,4)
        if opt == 1:
            await self.bot.change_presence(activity=discord.Streaming(name=random.choice(statuses), url='https://www.twitch.tv/xephirehd'))
        elif opt == 2:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(statuses)))
        elif opt == 3:
            await self.bot.change_presence(activity=discord.Game(name=random.choice(statuses)))
        elif opt == 4:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(statuses)))

def setup(bot):
    bot.add_cog(OnReady(bot))