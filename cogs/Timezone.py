import discord
from discord.ext import commands
import datetime as dt
import redis
import re
import json
import arrow
import pytz
from terminaltables import AsciiTable

r_server = redis.Redis("localhost")
nadstflag = True
eudstflag = True
ausdstflag = False


class Timezone():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def timenow(self):
        """Current time around the world"""
        now = dt.datetime.utcnow().replace(tzinfo=pytz.utc)
        ast = now.astimezone(pytz.timezone("US/Alaska"))
        pst = now.astimezone(pytz.timezone("US/Pacific"))
        mst = now.astimezone(pytz.timezone("US/Mountain"))
        cst = now.astimezone(pytz.timezone("US/Central"))
        est = now.astimezone(pytz.timezone("US/Eastern"))
        adt = now.astimezone(pytz.timezone("America/Halifax"))
        ndt = now.astimezone(pytz.timezone("America/St_Johns"))
        bst = now.astimezone(pytz.timezone("Europe/London"))
        cest = now.astimezone(pytz.timezone("Europe/Paris"))
        eest = now.astimezone(pytz.timezone("Europe/Helsinki"))
        msk = now.astimezone(pytz.timezone("Europe/Moscow"))
        gst = now.astimezone(pytz.timezone("Asia/Dubai"))
        ict = now.astimezone(pytz.timezone("Asia/Bangkok"))
        chst = now.astimezone(pytz.timezone("Asia/Shanghai"))
        jst = now.astimezone(pytz.timezone("Asia/Tokyo"))
        aedt = now.astimezone(pytz.timezone("Australia/Brisbane"))
        aest = now.astimezone(pytz.timezone("Australia/Melbourne"))
        table_data = [
            ["Timezone (UTC Offset)", "Current Time"],
            ["US/Alaska - AKST/AKDT ({})".format(ast.strftime("%z")), ast.strftime("%I:%M %p %a %B %d")],
            ["US/Pacific - PST/PDT ({})".format(pst.strftime("%z")), pst.strftime("%I:%M %p %a %B %d")],
            ["US/Mountain - MST/MDT ({})".format(mst.strftime("%z")), mst.strftime("%I:%M %p %a %B %d")],
            ["US/Central - CST/CDT ({})".format(cst.strftime("%z")), cst.strftime("%I:%M %p %a %B %d")],
            ["US/Eastern - EST/EDT ({})".format(est.strftime("%z")), est.strftime("%I:%M %p %a %B %d")],
            ["America/Halifax - AST/ADT ({})".format(adt.strftime("%z")), adt.strftime("%I:%M %p %a %B %d")],
            ["America/St.Johns - NST/NDT ({})".format(ndt.strftime("%z")), ndt.strftime("%I:%M %p %a %B %d")],
            ["Universal Coordinated - UTC ({})".format(now.strftime("%z")), now.strftime("%I:%M %p %a %B %d")],
            ["Europe/London- BST ({})".format(bst.strftime("%z")), bst.strftime("%I:%M %p %a %B %d")],
            ["Europe/Paris - CET/CEST ({})".format(cest.strftime("%z")), cest.strftime("%I:%M %p %a %B %d")],
            ["Europe/Helsinki - EET/EEST ({})".format(eest.strftime("%z")), eest.strftime("%I:%M %p %a %B %d")],
            ["Europe/Moscow - MSK ({})".format(msk.strftime("%z")), msk.strftime("%I:%M %p %a %B %d")],
            ["Asia/Dubai - GST ({})".format(gst.strftime("%z")), gst.strftime("%I:%M %p %a %B %d")],
            ["Asia/Bangkok - ICT ({})".format(ict.strftime("%z")), ict.strftime("%I:%M %p %a %B %d")],
            ["Asia/Singapore - SGT ({})".format(chst.strftime("%z")), chst.strftime("%I:%M %p %a %B %d")],
            ["Asia/Tokyo - JST ({})".format(jst.strftime("%z")), jst.strftime("%I:%M %p %a %B %d")],
            ["Australia/Brisbane - AEST ({})".format(aedt.strftime("%z")), aedt.strftime("%I:%M %p %a %B %d")],
            ["Australia/Sydney - AEST/AEDT ({})".format(aest.strftime("%z")), aest.strftime("%I:%M %p %a %B %d")]
        ]
        table = AsciiTable(table_data)
        await self.bot.say("```xl\n{}\n```".format(table.table))

    @commands.command(pass_context=True)
    async def register(self, ctx):
        """
        Registers your timezone
        This lets other users check your local time easily
        """
        if ctx.message.server:
            await self.bot.say("Please register in a pm {}".format(ctx.message.author.mention))
            return

        offset = None
        msg = "Please don't send any other messages until you've completed registration. \nLet's start with your commonly called name (i.e link2110 would be link)"
        await self.bot.say(msg)
        name = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
        msg2 = "What is your UTC offset? (i.e UTC-7 with no space in between. Use non-DST offset.)\n"
        await self.bot.say(msg2)
        offset = await self.bot.wait_for_message(timeout=30, author=ctx.message.author, channel=ctx.message.channel, check=utcCheck)

        if offset is None:
            await self.bot.say("You didn't provide a valid offset in time, please re-run `?register`")
            return

        msg3 = "Are you affected by/does your timezone observe DST? Please answer with yes or no."
        await self.bot.say(msg3)
        dstoption = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
        if dstoption.content.lower() == "yes":
            msg4 = "Are you in North America, Europe, or Australia? Please answer NA, EU, or AUS"
            await self.bot.say(msg4)
            dstarea = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
            if dstarea.content.lower() == "na":
                dstregion = "North America"
            if dstarea.content.lower() == "eu":
                dstregion = "Europe"
            if dstarea.content.lower() == "aus":
                dstregion = "Australia"
            msg5 = "Thanks for completing registration!"
            await self.bot.say(msg5)
        else:
            dstregion = "none"
            msg6 = "Thanks for completing registration!"
            await self.bot.say(msg6)
        data = {"name": name.content.lower(), "offset": offset.content, "dst_option": dstoption.content.lower(), "dst_region": dstregion, "id": ctx.message.author.id}
        json_data = json.dumps(data)
        r_server.set(name.content.lower(), json_data)
        r_server.save()

    @commands.command(no_pm=True)
    async def timezone(self, *, name:str):
        """Returns time in <name>'s timezone"""
        try:
            tz_data = json.loads(r_server.get(name.lower()).decode("UTF-8"))
            currenttime = arrow.utcnow()
            if tz_data["dst_option"] == "yes":
                if tz_data["dst_region"] == "North America":
                    if nadstflag:
                        getoffset = tz_data["offset"].strip("UTC")
                        offset = int(getoffset) + 1
                    if not nadstflag:
                        offset = tz_data["offset"].strip("UTC")
                if tz_data["dst_region"] == "Europe":
                    if eudstflag:
                        getoffset = tz_data["offset"].strip("UTC")
                        offset = int(getoffset) + 1
                    if not eudstflag:
                        offset = tz_data["offset"].strip("UTC")
                if tz_data["dst_region"] == "Australia":
                    if ausdstflag:
                        getoffset = tz_data["offset"].strip("UTC")
                        offset = int(getoffset) + 1
                    if not ausdstflag:
                        offset = tz_data["offset"].strip("UTC")
            if tz_data["dst_option"] == "no":
                offset = tz_data["offset"].strip("UTC")

            convertedtime = currenttime.replace(hours=int(offset), microsecond=0)
            msg = "Current time in {}'s timezone is {}".format(tz_data["name"], convertedtime.strftime("%I:%M %p on %a %d %b %Y"))
            await self.bot.say(msg)
        except AttributeError:
            msg = "Something's wrong. Make sure the person you're trying to check is registered by using ?timekey <name>"
            await self.bot.say(msg)
        except Exception as e:
            raise e

    @commands.command(no_pm=True)
    async def timekey(self, *, name:str):
        """Checks that a user has registered their timezone"""
        tz_data = json.loads(r_server.get(name.lower()).decode("UTF-8"))
        try:
            await self.bot.say(tz_data)
        except AttributeError:
            await self.bot.say("That name is not registered")



def utcCheck(msg):
    is_valid_offset = re.match("UTC([+-][\d]+)?", msg.content)
    return is_valid_offset


def setup(bot):
    bot.add_cog(Timezone(bot))