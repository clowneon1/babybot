from discord.ext import commands
import datetime
import discord

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick',help='Kick a given user with a given reason')
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.Member = None, *, reason = None):
        if user is None:
            return await ctx.send('**Please specify a user to kick.**')
        if user.id == ctx.author.id:
            return await ctx.send('**You cannot kick yourself.**')
        if reason is None: reason = 'None'
        if user.top_role >= ctx.auther.top_role:
            return ctx.send(f'**{user.mention}** could not be kicked, they have higher or equal roles to you.')

        try:
            await user.kick(reason=reason)
        except discord.errors.Forbidden:
            return await ctx.send(f'**{user.mention}** could not be kicked.')

        # for user
        userEmbed = discord.Embed(title=f'You have been kicked from **{ctx.guild.name}**', colour=discord.Color.purple())
        userEmbed.add_field(name='Reason', value=reason)
        userEmbed.add_field(name='Date', value=str(datetime.now()))
        try:
            await user.send(embed=userEmbed)
        except discord.errors.Forbidden:
            pass

        # for channel
        channelEmbed = discord.Embed(title=f'{user.display_name} has been kicked from **{ctx.guild.name}**', colour=discord.Color.purple())
        channelEmbed.add_field(name='Reason', value=reason)
        channelEmbed.add_field(name='Date', value=str(datetime.now()))
        await ctx.send(embed=channelEmbed)

def setup(bot):
    bot.add_cog(Kick(bot))