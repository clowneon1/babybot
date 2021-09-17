from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    @commands.command(name='unban',help='Unbans a given user followed by their discriminator (hashtag number)')
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member):

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name.lower(), user.discriminator.lower()) == (member_name.lower(), member_discriminator.lower()):
                await ctx.guild.unban(user)
                return await ctx.send(f'Unbanned {user.mention}')
        await ctx.send("**The given user either doesn't exist or is not banned.**")

def setup(bot):
    bot.add_cog(Unban(bot))