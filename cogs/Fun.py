from discord.ext import commands
import random
from PIL import ImageFont, ImageDraw, Image, ImageOps, ImageFilter, ImageChops
import textwrap
import aiohttp
import os
import io

asset_pos = "H:\Documents\Bot Folder\PoiBot\\assets"

class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def headpat(self):
        """Gives headpats. Can be directed to a user"""
        headpat_list = ["http://i.imgur.com/IiQwK12.gif", "http://i.imgur.com/JCXj8yD.gif", "http://i.imgur.com/qqBl2bm.gif",
                   "http://i.imgur.com/eOJlnwP.gif",
                   "https://45.media.tumblr.com/229ec0458891c4dcd847545c81e760a5/tumblr_mpfy232F4j1rxrpjzo1_r2_500.gif",
                   "https://media.giphy.com/media/KZQlfylo73AMU/giphy.gif",
                   "https://media.giphy.com/media/12hvLuZ7uzvCvK/giphy.gif",
                   "https://49.media.tumblr.com/8e8a099c4eba22abd3ec0f70fd087cce/tumblr_nxovj9oY861ur1mffo1_500.gif ",
                   "http://i.imgur.com/wJ5x5cp.gif", "http://i.imgur.com/maXcnyC.gif"]
        pat = random.randint(0, len(headpat_list))
        await self.bot.say(headpat_list[pat])

    @commands.command(hidden=True, no_pm=True)
    async def say(self, *, thing_to_say:str):
        """Bot echos what you typed"""
        await self.bot.say(thing_to_say)

    @commands.command(no_pm=True)
    async def roll(self, dice: str):
        """Rolls a dice in NdN format"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command()
    async def lod(self):
        """Bot gives you the look of dissaproval ಠ_ಠ"""
        await self.bot.say("ಠ_ಠ")

    @commands.command()
    async def itsudemo(self):
        """ITSUDEMO"""
        await self.bot.say("(✿◠‿◠) 〜いつでも (✿◠‿◠) 〜")

    @commands.command()
    async def chun(self):
        """CHUN CHUN"""
        await self.bot.say("( ⋅ 8 ⋅ )♡")

    @commands.command()
    async def lenny(self):
        """( ͡° ͜ʖ ͡°)"""
        await self.bot.say("( ͡° ͜ʖ ͡°)")

    @commands.command(pass_context=True)
    async def shrug(self, ctx):
        """Random shrug emote"""
        if ctx.message.server.id == "137463604311097345":
            shrug_list = ["╮(─▽─)╭", "¯\_(ツ)_/¯", "╮(╯∀╰)╭", "┐(´ー｀)┌", "ヽ(´ー`)ノ", "ʅ（´◔౪◔）ʃ", "ლ(•ω •ლ)", "ヽ(~～~ )ノ", "乁〳 ❛ д ❛ 〵ㄏ", "╮(╯_╰)╭", "http://i.imgur.com/E79rheb.png"]
        else:
            shrug_list = ["╮(─▽─)╭", "¯\_(ツ)_/¯", "╮(╯∀╰)╭", "┐(´ー｀)┌", "ヽ(´ー`)ノ", "ʅ（´◔౪◔）ʃ", "ლ(•ω •ლ)", "ヽ(~～~ )ノ", "乁〳 ❛ д ❛ 〵ㄏ", "╮(╯_╰)╭"]
        random_shrug = random.randint(0, len(shrug_list))
        await self.bot.say(shrug_list[random_shrug])

    @commands.command(pass_context=True, no_pm=True)
    async def rip(self, ctx, member_or_text: str):
        """RIP\nCreates a tombstone for either a member or some text. Mention a member to get the avatar + name"""
        if ctx.message.mentions:
            user_name = ctx.message.mentions[0].name.replace(" ", "%20")
            rip_member = ctx.message.mentions[0]
            ava_url = rip_member.avatar_url
            url = "https://ripme.xyz/{}"
            msg = url.format(user_name)

            tomb = Image.open(os.path.join(asset_pos, "tombstone.png"))
            base_img = Image.new("RGBA", (tomb.width, tomb.height), color="White")
            with aiohttp.ClientSession() as session:
                async with session.get(ava_url) as resp:
                    ava = await resp.content.read()

            ava_img = Image.open(io.BytesIO(ava))
            ava_img_greyscale = ImageOps.autocontrast(ava_img.convert("L").filter(ImageFilter.CONTOUR)).filter(
                ImageFilter.SMOOTH).resize((200, 200))
            base_img.paste(ava_img_greyscale, (140, 380, 340, 580))
            final = ImageChops.multiply(base_img, tomb)
            f = ImageFont.truetype(os.path.join(asset_pos, "Symbola.ttf"), size=35)
            d = ImageDraw.Draw(final)
            w, h = d.textsize(rip_member.name, font=f)
            d.multiline_text(((60 + ((350 - w) / 2)), 315), rip_member.name, fill="Black", font=f, align="center")
            final.save(os.path.join(asset_pos, "rip.png"))
            await self.bot.send_file(ctx.message.channel, os.path.join(asset_pos, "rip.png"), content=msg)
        else:
            content = ctx.message.content.partition(" ")
            user_name = content[2].replace(" ", "_")
            url = "https://ripme.xyz/{}"
            msg = url.format(user_name)
            base_img = Image.new("RGB", (520, 640), color="White")
            tomb = Image.open(os.path.join(asset_pos, "tombstone.png"))
            base_img.paste(tomb)
            f = ImageFont.truetype(os.path.join(asset_pos, "Symbola.ttf"), size=35)
            d = ImageDraw.Draw(base_img)
            text = textwrap.shorten(content[2], width=25, placeholder="")
            w, h = d.textsize(text, font=f)
            d.text(((60 + ((350 - w) / 2)), 315), text, fill="Black", font=f, align="center")
            d.text((160, 450), "2016 - 2016", fill="Black", font=f)
            base_img.save(os.path.join(asset_pos, "rip.jpeg"))
            await self.bot.send_file(ctx.message.channel, os.path.join(asset_pos, "rip.jpeg"), content=msg)


def setup(bot):
    bot.add_cog(Fun(bot))