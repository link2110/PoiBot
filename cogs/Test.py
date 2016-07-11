import discord
from discord.ext import commands

#For testing things idk

class Test():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def test(self, ctx):
        """test stuff here"""

def setup(bot):
    bot.add_cog(Test(bot))