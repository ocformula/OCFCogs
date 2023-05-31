import random
import discord
from redbot.core import commands


class TeamShuffle(commands.Cog):
    """"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="teamshuffle", required=True)
    async def _teamshuffle(self, ctx, *args):
        users = []
        for arg in args:
            users.append(arg)

        if len(users) % 2 == 1:
            users.append(None)

        random.shuffle(users)

        teams = [users[i::2] for i in range(2)]

        await ctx.send("1팀: {}".format(" ".join([str(user) for user in teams[0]])))
        await ctx.send("2팀: {}".format(" ".join([str(user) for user in teams[1]])))
