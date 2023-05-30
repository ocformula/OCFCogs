import discord
from redbot.core import commands


class ChannelMessage(commands.Cog):
    """Send Messages as the bot!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="channelmessage")
    async def _channelmessage(self, ctx: commands.Context, server: discord.Guild, channel: discord.TextChannel, *, message=""):
        """Send an message to a specific channel."""
        try:
            await channel.send(message)
            return await ctx.tick()
        except discord.Forbidden:
            return await ctx.send("I do not have permissions to send that message!")
