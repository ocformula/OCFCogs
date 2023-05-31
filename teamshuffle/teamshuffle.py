import random
import discord
from redbot.core import commands


class TeamShuffle(commands.Cog):
    """"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="teamshuffle")
    async def _teamshuffle(self, ctx, *args):
        users = []
        for arg in args:
            users.append(arg)

        if len(users) == 0:
            await ctx.send("유저 목록을 입력해주세요.")
            return
            
        elif len(users) % 2 == 1:
            users.append(None)

            random.shuffle(users)

            teams = [users[i::2] for i in range(2)]

            await ctx.send("1팀: {}".format(" ".join([str(user) for user in teams[0]])))
            await ctx.send("2팀: {}".format(" ".join([str(user) for user in teams[1]])))
