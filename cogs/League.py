import discord
from discord.ext import commands
import aiohttp
import asyncio

class League:
    def __init__(self, bot):
        self.bot = bot

#TODO: one day ill do this as well

def setup(bot):
    bot.add_cog(League(bot))