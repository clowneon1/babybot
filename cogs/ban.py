from discord.ext import commands
import datetime
import discord

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban',help='Ban a given user with a given reason')
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user : discord.Member = None, *, reason = None):
        if user is None:
            return await ctx.send('**Please specify a user to ban.**')
        if user.id == ctx.author.id:
            return await ctx.send('**You cannot ban yourself.**')
        if reason is None: reason = 'None'
        if user.top_role >= ctx.auther.top_role:
            return ctx.send(f'**{user.mention}** could not be banned, they have higher or equal roles to you.')

        try:
            await user.ban(reason=reason)
        except discord.errors.Forbidden:
            return await ctx.send(f'**{user.display_name}** could not be banned.')

        # for user
        userEmbed = discord.Embed(title=f'You have been banned from **{ctx.guild.name}**', colour=discord.Color.purple())
        userEmbed.add_field(name='Reason', value=reason)
        userEmbed.add_field(name='Date', value=str(datetime.now()))
        try:
            await user.send(embed=userEmbed)
        except discord.errors.Forbidden:
            pass

        # for channel
        channelEmbed = discord.Embed(title=f'{user.display_name} has been banned from **{ctx.guild.name}**', colour=discord.Color.purple())
        channelEmbed.add_field(name='Reason', value=reason)
        channelEmbed.add_field(name='Date', value=str(datetime.now()))
        await ctx.send(embed=channelEmbed)

def setup(bot):
    bot.add_cog(Ban(bot))