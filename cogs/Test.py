from discord.ext import commands
from .utils import checks


class Test:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def test(self, ctx, *, name: str):
        pass

def setup(bot):
    bot.add_cog(Test(bot))