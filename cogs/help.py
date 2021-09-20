from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        em = discord.Embed(title='Help', description='A discord.py multi-use bot, with many useful and fun features. [Source code](https://github.com/Xephire/utils-bot-rewrite)', colour=discord.Color.purple())
        em.add_field(name='Join', value='Join the vc that the current user is in')
        em.add_field(name='Leave', value='Leave the vc that the current user is in')
        em.add_field(name='Play', value='Play a song, given either a url or a search term')
        em.add_field(name='Pause', value='Pauses current song')
        em.add_field(name='Loop', value = 'Loops through the current or next song until disabled.')
        em.add_field(name='Skip', value='Skips current song')
        em.add_field(name='Stop', value='Stops playing and clears queue')
        em.add_field(name='ClearQueue', value='Clears the queue')
        em.add_field(name='Ban', value='Bans a user')
        em.add_field(name='Kick', value='Kicks a user')
        em.add_field(name='Unban', value='Unbans a user')
        em.add_field(name="GayRate",value="Rates a user's 'gayness'")
        await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Help(bot))  