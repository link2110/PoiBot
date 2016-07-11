import discord
from discord.ext import commands
import aiohttp
import asyncio
import time
import json
import shelve
import datetime

class AniList:
    def __init__(self, bot):
        self.bot = bot

    async def _get_readonly(self):
        with open("H:\Documents\Bot Folder\PoiBot\credentials\\credentials.txt") as f:
            creds = json.load(f)
            cid = creds["anilist_client_id"]
            csecret = creds["anilist_client_secret"]
            data = {'grant_type': 'client_credentials', 'client_id': cid, 'client_secret': csecret}
            url = "https://anilist.co/api/auth/access_token"
            with aiohttp.ClientSession() as session:
                async with session.post(url, params=data) as resp:
                    get_token = await resp.json()
                    with shelve.open("H:\Documents\Bot Folder\PoiBot\credentials\\temp", flag="c", writeback=True) as db:
                        db["Expiration"] = get_token["expires"]
                        db["AccessToken"] = get_token["access_token"]

    async def get_token(self):
        with shelve.open("H:\Documents\Bot Folder\PoiBot\credentials\\temp", flag="w", writeback=True) as db:
            expiration = db["Expiration"]
            if time.time() >= int(expiration):
                with open("H:\Documents\Bot Folder\PoiBot\credentials\\credentials.txt") as f:
                    creds = json.load(f)
                    cid = creds["anilist_client_id"]
                    csecret = creds["anilist_client_secret"]
                    data = {'grant_type': 'client_credentials', 'client_id': cid, 'client_secret': csecret}
                    url = "https://anilist.co/api/auth/access_token"
                    with aiohttp.ClientSession() as session:
                        async with session.post(url, params=data) as resp:
                            get_token = await resp.json()
                            db["Expiration"] = get_token["expires"]
                            db["AccessToken"] = get_token["access_token"]
                            return get_token["access_token"]
            else:
                return db["AccessToken"]

    async def parse_anime(self, id):
        with shelve.open("H:\Documents\Bot Folder\PoiBot\credentials\\temp", flag="r") as db:
            data = {'access_token': db["AccessToken"]}
            url = "https://anilist.co/api/anime/" + str(id)
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as resp:
                    data = await resp.json()
                    return data

    @commands.command(no_pm=True, pass_context=True)
    async def searchanime(self, ctx, *, anime_title: str):
        """Searches for an anime title and returns information on it."""
        with shelve.open("H:\Documents\Bot Folder\PoiBot\credentials\\temp", flag="r") as db:
            data = {'access_token': db["AccessToken"]}
            url ="https://anilist.co/api/anime/search/" + anime_title.replace(" ", "%20")
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as resp:
                    raw_data = await resp.text()
                    if raw_data == "/n" or resp.status == 404:
                        await self.bot.say("No results found for {}".format(anime_title))
                    else:
                        get_id = json.loads(raw_data)
                        ani_data = await self.parse_anime(self, get_id[0]["id"])
                        msg = "**{}** / **{}**\n**Status:** {} | **Average score:** {}/100\n{}\n**Genres:** {}\n**Description:** {}\n{}".format(
                        ani_data["title_romaji"], ani_data["title_japanese"], ani_data["airing_status"], ani_data["average_score"],
                        "**Next Episode:** Episode {} in {} hrs".format(ani_data["airing"]["next_episode"], ":".join(
                            str(datetime.timedelta(seconds=int(ani_data["airing"]["countdown"]))).split(":")[:2])) if ani_data[
                             "airing_status"].lower() == "currently airing" else "**Episodes:** {}".format(ani_data["total_episodes"]),
                        str(ani_data["genres"]).strip("[]").replace("'", ""), str(ani_data["description"]).replace("<br>", ""),
                        "http://anilist.co/anime/{}/".format(ani_data["id"]))
                        await self.bot.say(msg)


    @commands.command(pass_context=True)
    async def test(self):
        with open("H:\Documents\Bot Folder\PoiBot\credentials\\credentials.txt") as f:
            data = json.load(f)





def setup(bot):
    bot.add_cog(AniList)
