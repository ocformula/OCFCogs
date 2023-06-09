"""NetSpeed cog for Red-DiscordBot by PhasecoreX."""
import asyncio
import concurrent

import discord
import speedtest
from redbot.core import checks, commands


class NetSpeed(commands.Cog):
    """Test your servers internet speed.

    Note that this is the internet speed of the server your bot is running on,
    not your internet speed.
    """

    __author__ = "PhasecoreX"
    __version__ = "1.0.0"

    #
    # Red methods
    #

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Show version in help."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, **kwargs
    ):  # pylint: disable=unused-argument
        """Nothing to delete."""
        return

    #
    # Command methods: netspeed
    #

    @commands.command(aliases=["speedtest"])
    @checks.is_owner()
    async def netspeed(self, ctx):
        """Test your servers internet speed.

        Note that this is the internet speed of the server your bot is running on,
        not your internet speed.
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_event_loop()
        speed_test = speedtest.Speedtest(secure=True)
        the_embed = await ctx.send(
            embed=self.generate_embed(0, speed_test.results.dict())
        )
        await loop.run_in_executor(executor, speed_test.get_servers)
        await loop.run_in_executor(executor, speed_test.get_best_server)
        await the_embed.edit(embed=self.generate_embed(1, speed_test.results.dict()))
        await loop.run_in_executor(executor, speed_test.download)
        await the_embed.edit(embed=self.generate_embed(2, speed_test.results.dict()))
        await loop.run_in_executor(executor, speed_test.upload)
        await the_embed.edit(embed=self.generate_embed(3, speed_test.results.dict()))

    @staticmethod
    def generate_embed(step: int, results_dict):
        """Generate the embed."""
        measuring = ":mag: Measuring..."
        waiting = ":hourglass: Waiting..."

        color = discord.Color.red()
        title = "Measuring internet speed..."
        message_ping = measuring
        message_down = waiting
        message_up = waiting
        if step > 0:
            message_ping = f"**{results_dict['ping']}** ms"
            message_down = measuring
        if step > 1:
            message_down = f"**{results_dict['download'] / 1_000_000:.2f}** mbps"
            message_up = measuring
        if step > 2:
            message_up = f"**{results_dict['upload'] / 1_000_000:.2f}** mbps"
            title = "NetSpeed Results"
            color = discord.Color.green()
        embed = discord.Embed(title=title, color=color)
        embed.add_field(name="Ping", value=message_ping)
        embed.add_field(name="Download", value=message_down)
        embed.add_field(name="Upload", value=message_up)
        return embed
