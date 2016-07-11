import discord
from discord.ext import commands

class Remind():
    def __init__(self, bot):
        self.bot = bot

#TODO: one day i'll do this


def setup(bot):
    bot.add_cog(Remind(bot))