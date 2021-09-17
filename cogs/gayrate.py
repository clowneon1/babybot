from discord.ext import commands
import discord
import random

class Gayrate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gayrate", help="Rates a user's 'gayness'")
    async def gayrate(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.message.author
        if user.id in [757991078296027238, 476384449362264074]:
            with open('../media/gaygif.gif','rb') as f:
                em = discord.Embed(title='How Gay Are They', description=f'{user.mention} is mega gay!', colour=discord.Color.purple())
                picture = discord.File(f)
                return await ctx.send(embed=em,file=picture)

        gayLevel = random.randint(0,100)
        em = discord.Embed(title='How Gay Are They', description=f'{user.mention} is {gayLevel}% gay.', colour=discord.Color.purple())
        return await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Gayrate(bot))