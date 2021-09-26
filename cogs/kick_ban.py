from discord.ext import commands
import datetime
import discord

class KickBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick",help="Kick a given user with a given reason")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.Member = None, *, reason = None):
        if user is None:
            em = discord.Embed(title="**Please specify a user to kick.**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        if user.id == ctx.author.id:
            em = discord.Embed(title="**You cannot kick yourself.**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        if user.top_role >= ctx.author.top_role:
            em = discord.Embed(title=f"{user.name} could not be kicked, they have higher or equal roles to you.", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        try:
            await user.kick(reason=str(reason))
        except discord.errors.Forbidden:
            em = discord.Embed(title=f"{user.name} could not be kicked.", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)


        # for user
        userEmbed = discord.Embed(title=f"You have been kicked from {ctx.guild.name}", colour=discord.Color.purple())
        userEmbed.add_field(name="Reason", value=str(reason))
        userEmbed.add_field(name="Date", value=str(datetime.datetime.now()))
        try:
            await user.send(embed=userEmbed)
        except Exception:
            pass

        # for channel
        channelEmbed = discord.Embed(title=f"{user.display_name} has been kicked from {ctx.guild.name}", colour=discord.Color.purple())
        channelEmbed.add_field(name="Reason", value=str(reason))
        channelEmbed.add_field(name="Date", value=str(datetime.datetime.now()))
        await ctx.send(embed=channelEmbed)

    @commands.command(name="ban",help="Ban a given user with a given reason")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user : discord.Member = None, *, reason = None):
        if user is None:
            em = discord.Embed(title="**Please specify a user to ban.**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        if user.id == ctx.author.id:
            em = discord.Embed(title="**You cannot ban yourself.**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        if user.top_role >= ctx.author.top_role:
            em = discord.Embed(title=f"{user.name} could not be banned, they have higher or equal roles to you.", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        try:
            await user.ban(reason=str(reason))
        except discord.errors.Forbidden:
            em = discord.Embed(title=f"{user.name} could not be banned.", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)


        # for user
        userEmbed = discord.Embed(title=f"You have been banned from {ctx.guild.name}", colour=discord.Color.purple())
        userEmbed.add_field(name="Reason", value=str(reason))
        userEmbed.add_field(name="Date", value=str(datetime.datetime.now()))
        try:
            await user.send(embed=userEmbed)
        except Exception:
            pass

        # for channel
        channelEmbed = discord.Embed(title=f"{user.display_name} has been banned from {ctx.guild.name}", colour=discord.Color.purple())
        channelEmbed.add_field(name="Reason", value=str(reason))
        channelEmbed.add_field(name="Date", value=str(datetime.datetime.now()))
        await ctx.send(embed=channelEmbed)

    @commands.command(name="unban",help="Unbans a given user followed by their discriminator")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member = None):

        if member is None:
            em =  discord.Embed(title="**Please enter a user's ID or name followed by their discriminator.**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        member_name, member_discriminator = member.split("#")

        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            user = ban_entry.user

            if (member_name, member_discriminator) == (user.name, user.discriminator):
                await ctx.guild.unban(user)
                em =  discord.Embed(title=f"Unbanned {user.name}", colour=discord.Color.purple())
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=em)
        em =  discord.Embed(title="**The given user either doesn't exist or is not banned.**", colour=discord.Color.purple())
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(KickBan(bot))