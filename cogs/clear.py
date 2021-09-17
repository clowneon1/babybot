from discord.ext import commands
import asyncio

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='clear',aliases=['c'],help='Clears the current text channel')
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount : int = None):
        global confirmMsgID, confirmMsgUserID

        if ctx.author.guild_permissions.manage_messages:
            if amount is None:
                confirmMsg = await ctx.send('React to this message with :no_entry_sign: to confirm clearing the whole text channel. (This message automatically deletes after 5 seconds)', delete_after=5)
                await confirmMsg.add_reaction('\N{NO ENTRY SIGN}')
                confirmMsgID = confirmMsg.id
                confirmMsgUserID = ctx.author.id
                await asyncio.sleep(0.5)
                return
            
            if isinstance(amount, int) and amount > 0:
                await ctx.channel.purge(limit=amount+1)
                delMsg = await ctx.send(f'**{amount}** messages were deleted')
                await asyncio.sleep(2)
                await delMsg.delete()
                await asyncio.sleep(0.5)
            else:
                return await ctx.send('Please specify a valid number of messages to delete')
        else:
            permErrorMsg = await ctx.send('You do not have permission to use this command')
            await asyncio.sleep(2)
            await permErrorMsg.delete()
            
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try: confirmMsgID
        except NameError: return
        if reaction.message.id == confirmMsgID and reaction.emoji == '\N{NO ENTRY SIGN}' and user.id != self.bot.user.id and user.id == confirmMsgUserID:
            await reaction.message.channel.purge(limit=None)
            await asyncio.sleep(0.5)
            delMsg = await reaction.message.channel.send('This channel was cleared')
            await asyncio.sleep(1)
            return await delMsg.delete()

def setup(bot):
    bot.add_cog(Clear(bot))