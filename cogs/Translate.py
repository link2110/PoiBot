from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

class Translate:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def translate(self, origin_lang: str, dest_lang: str, *, str_to_translate: str):
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}%dt=t&q={}"
        with aiohttp.ClientSession() as session:
            client = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
            async with session.get(url.format(origin_lang, dest_lang, str_to_translate), headers=client) as resp:
                text = await resp.text()
                print(text)

#broken until i can find a way to strip the results :< RIP

def setup(bot):
    bot.add_cog(Translate)