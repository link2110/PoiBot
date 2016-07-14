import discord
from discord.ext import commands
import pyowm
from pint import UnitRegistry
import datetime as dt
import aiohttp
import random
import json
from PyDictionary import PyDictionary

with open("H:\Documents\Bot Folder\PoiBot\credentials\\credentials.txt") as f:
    creds = json.load(f)
    token = creds["owm"]
    owm = pyowm.OWM(token)
# owm = pyowm.OWM("cd7db42523c1c1e4e4a5af9d2df6b168")
registry = owm.city_id_registry()
ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
Q_ = ureg.Quantity

class Commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def convert(self, number:str, source_unit:str, *, converted_unit:str):
        """Converts one amount of unit to another"""
        source_and_amount = number + " " + source_unit
        converted_unit = converted_unit.lstrip("to ")
        try:
            result = Q_(source_and_amount).to(converted_unit)
            msg = truncate(result, 3)
            await self.bot.say(msg)
        except Exception as e:
            msg = "Something's not right, either the units, type, or spelling"
            await self.bot.say(msg)
            await self.bot.say(e)
            
    @commands.command(no_pm=True)
    async def currency(self, number:str, source_currency:str, *, target_currency:str):
        """Converts <#> of currency 1 to currency 2"""
        url = "https://www.google.com/finance/converter?a={}&from={}&to={}"
        target_currency = target_currency.lstrip("to ")
        try:
            with aiohttp.ClientSession() as session:
                async with session.get(url.format(number, source_currency, target_currency)) as resp1:
                    data = await resp1.text()
                    text = data.partition('<span class=bld>')
                    targetamount = text[2].partition(" ")
            msg = "{} {}".format(truncate(targetamount[0], 3), target_currency)
            await self.bot.say(msg)
        except Exception as e:
            msg = "Something's not right, please make you're using currency codes and it's spaced out properly."
            await self.bot.say(msg)
            await self.bot.say(e)

    @commands.command(no_pm=True)
    async def temp(self, number:float, unit:str):
        """Converts F to C or vice versa\nExample: ?temp 100 F | ?temp 40 C"""
        if unit.lower() == "f":
            celcius = truncate(((number - 32) / 1.8), 3)
            msg = "{}\u00B0 Celcius".format(celcius)
            await self.bot.say(msg)
        if unit.lower() == "c":
            fahrenheit = truncate(((number * 1.8) + 32), 3)
            msg = "{}\u00B0 Fahrenheit".format(fahrenheit)
            await self.bot.say(msg)

    @commands.command(no_pm=True)
    async def height(self, number:str):
        """Converts ft'in to cm and vice versa\nExample useage: ?height 5'11 | ?height 180cm"""
        if "'" in number:
            units = number.partition("'")
            if units[2] == "":
                inches = (int(units[0]) * 12)
            else:
                inches = (int(units[0]) * 12) + int(units[2])
            cm = truncate((inches * 2.54), 3)
            msg = "{} cm".format(cm)
            await self.bot.say(msg)
        if "cm" in number:
            cm = number.strip("cm")
            inches = int(cm) * 0.393701
            feet = inches // 12
            remInches = truncate((inches % 12), 3)
            msg = "{} feet {} inches".format(feet, remInches)
            await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def mention(self, ctx, number: int = 1):
        """
        Gets the last time you were mentioned, along with context messages
        If <number> is passed, it gets the last <number> of times mentioned.
        """
        #TODO: use mentioned_in instead of checking for ID, maybe make this send one message per mention instead of 3 (use 3 codeblocks with /n between)
        before_msg = []
        before_auth = []
        before_time = []
        after_msg = []
        after_auth = []
        after_time = []
        mention_count = 0
        mention_id = ctx.message.author.id
        try:
            async for message in self.bot.logs_from(ctx.message.channel, limit=5000):
                if discord.User(id=mention_id) in message.mentions:
                    mention_count += 1
                    async for x in self.bot.logs_from(ctx.message.channel, limit=3, before=message):
                        before_msg.append(x.content)
                        before_auth.append(x.author.name)
                        before_time.append(x.timestamp)
                    async for y in self.bot.logs_from(ctx.message.channel, limit=3, after=message):
                        after_msg.append(y.content)
                        after_auth.append(y.author.name)
                        after_time.append(y.timestamp)
                    before_msg.reverse()
                    before_auth.reverse()
                    before_time.reverse()
                    after_msg.reverse()
                    after_auth.reverse()
                    after_time.reverse()
                    msg1 = "Your last mention:\nBefore:\n```\n{} {} said:\n{}\n\n{} {} said:\n{}\n\n{} {} said:\n{}\n```".format(
                        before_time[0].strftime("On %a %b %d at %H:%M:%S UTC"), before_auth[0], before_msg[0],
                        before_time[1].strftime("On %a %b %d at %H:%M:%S UTC"), before_auth[1], before_msg[1],
                        before_time[2].strftime("On %a %b %d at %H:%M:%S UTC"), before_auth[2], before_msg[2]
                    )
                    await self.bot.send_message(ctx.message.author, msg1)

                    msg = "Message:\n```\n{} {} said:\n{}\n```".format(
                        message.timestamp.strftime("On %a %b %d at %H:%M:%S UTC"), message.author.name,
                        message.clean_content
                    )
                    await self.bot.send_message(ctx.message.author, msg)

                    msg2 = "After:\n```\n{} {} said:\n{}\n\n{} {} said:\n{}\n\n{} {} said:\n{}\n```".format(
                        after_time[0].strftime("On %a %b %d at %H:%M:%S UTC"), after_auth[0], after_msg[0],
                        after_time[1].strftime("On %a %b %d at %H:%M:%S UTC"), after_auth[1], after_msg[1],
                        after_time[2].strftime("On %a %b %d at %H:%M:%S UTC"), after_auth[2], after_msg[2]
                    )
                    await self.bot.send_message(ctx.message.author, msg2)

                    if mention_count >= number:
                        await self.bot.say("\U0001F4EC")
                        return
            if mention_count == 0:
                await self.bot.say("Could not find a mention of you in the last 5000 messages, or the message was a role mention.")
        except Exception as e:
            await self.bot.send_message(ctx.message.author, e)
            
    @commands.command(no_pm=True)
    async def weather(self, *, city:str):
        """Gets current weather for <city>"""
        if registry.id_for(city) is not None:
            observation = owm.weather_at_id(registry.id_for(city))
        else:
            observation = owm.weather_at_place(city)
        location = observation.get_location()
        w = observation.get_weather()
        temp = w.get_temperature(unit="celsius")
        tempf = w.get_temperature(unit="fahrenheit")
        humidity = w.get_humidity()
        wind = w.get_wind()
        pressure = w.get_pressure()
        cloud = w.get_clouds()
        weather_status = w.get_detailed_status()
        weather_icon = w.get_weather_icon_name()
        sunrise_seconds = w.get_sunrise_time()
        sunset_seconds = w.get_sunset_time()

        url = "http://api.timezonedb.com/?lat={}&lng={}&key=Q81W68EC91UL&format=json"
        with aiohttp.ClientSession() as session:
            async with session.get(url.format(location.get_lat(), location.get_lon())) as resp:
                offset_data = await resp.json()
                offset_time = offset_data["gmtOffset"]

        sunrise_seconds += int(offset_time)
        sunset_seconds += int(offset_time)

        sunrise = dt.datetime.utcfromtimestamp(sunrise_seconds)
        sunset = dt.datetime.utcfromtimestamp(sunset_seconds)

        msg = "\U0001F30E **Current weather** for {}\n\U0001F4CF**Lat/Long:**({}/{}) **Conditions:** {} {} {}\n\U0001F321 **Current Temperature** {}\u00B0C/{}\u00B0F | **Low:** {}\u00B0C/{}\u00B0F | **High:** {}\u00B0C/{}\u00B0F\n\U0001F39B **Pressure:** {} kPa | {} mmHG | {} bar \U0001F613 **Humidity:** {}%\n\U0001F4A8 **Windspeed:** {} km/hr | {} mph {} \u2601 **Cloud coverage:** {}%\n\U0001F307 **Sunrise:** {}  \U0001F303 **Sunset:** {}".format(
            location.get_name(), location.get_lat(), location.get_lon(), get_icon(weather_icon), weather_status,
            get_icon(weather_icon), str(temp["temp"]), str(tempf["temp"]), str(temp["temp_min"]),
            str(tempf["temp_min"]), str(temp["temp_max"]), str(tempf["temp_max"]),
            str(truncate((pressure["press"] / 10), 3)),
            str(truncate(pressure["press"] * 0.75, 3)), str(truncate(pressure["press"] * 0.001, 3)), str(humidity),
            str(truncate(wind["speed"] * 3.6, 2)), str(truncate(wind["speed"] * 2.36, 3)), get_deg(wind["deg"]),
            str(cloud), sunrise.strftime("%I:%M %p"), sunset.strftime("%I:%M %p"))
        await self.bot.say(msg)

    @commands.command(no_pm=True)
    async def forecast(self, *, city: str):
        #TODO: Actually get this to look nice,or maybe not. ¯\_(ツ)_/¯
        #TODO: Use TerminalTables for formatting
        """Gets the 7 day forecast for the city entered"""
        fc = owm.daily_forecast(city, limit=7)

        f = fc.get_forecast()
        weather_list = []
        for weather in f:
            weather_list.append(weather.get_status())
        await self.bot.say("```\n{}\n```".format(weather_list))

    @commands.command(no_pm=True)
    async def rate(self, *, thing_to_rate: str):
        """Rates a thing out of 10"""
        good_user = ["link", "yuudachi", "shigure", "myself"]
        num_rate = random.randint(0,10)
        if thing_to_rate.lower() in good_user:
            num_rate = "10"
        msg = "I rate {} a {}/10".format(thing_to_rate, num_rate)
        await self.bot.say(msg)

    @commands.command(no_pm=True)
    async def choose(self, *choices: str):
        """Chooses between multiple choices"""
        await self.bot.say("I pick {}".format(random.choice(choices)))

    @commands.command(no_pm=True)
    async def lmgtfy(self, *, search_term: str):
        """Since you can't search this yourself."""
        url = "http://lmgtfy.com/?q={}"
        search_term = search_term.replace(" ", "+")
        await self.bot.say(url.format(search_term))

    @commands.command(no_pm=True, pass_context=True)
    async def topic(self, ctx):
        """Prints the channel topic, since nobody reads them anyways"""
        msg = "**Channel topic for #{}:**\n\n{}".format(ctx.message.channel.name, ctx.message.channel.topic)
        #TODO: suppress links somehow
        await self.bot.say(msg)

    @commands.command(no_pm=True, pass_context=True)
    async def id(self, ctx):
        """Gets your discord ID"""
        msg = "{} your ID is {}".format(ctx.message.author.mention, ctx.message.author.id)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def bedtime(self, ctx, member: discord.Member = None):
        """Tells a user to go to sleep. If no user is mentioned, will use you"""
        sleep_list = ["http://i.imgur.com/OC7uI2m.png", "http://i.imgur.com/0xflepR.png", "http://i.imgur.com/KklC7Zb.png", "http://i.imgur.com/1XGIPZ9.jpg", "http://i.imgur.com/xrDXOst.png", "http://i.imgur.com/Un08Qd7.png", "http://i.imgur.com/psj3lkd.png",
                      "http://i.imgur.com/omBWRDQ.png", "http://i.imgur.com/TQgVrk0.png", "http://i.imgur.com/SV6wNJw.png", "http://i.imgur.com/LZgLYc1.png", "http://i.imgur.com/MaTF2cy.png", "http://i.imgur.com/qj5PPHM.gif", "http://i.imgur.com/CcTBuVx.jpg",
                      "http://i.imgur.com/a6FFUer.png", "http://i.imgur.com/r9vuptx.jpg", "http://i.imgur.com/6eqbXNZ.png", "http://i.imgur.com/340X9UY.png", "http://i.imgur.com/5yfZssd.png", "http://i.imgur.com/uUEEgH4.png", "http://i.imgur.com/aHcB6gB.png",
                      "http://i.imgur.com/ALpZVs9.png", "http://i.imgur.com/etvcqTQ.png", "http://i.imgur.com/5Hp7FqP.jpg", "http://i.imgur.com/GNqhhTA.jpg", "http://i.imgur.com/Aqam15S.png", "http://i.imgur.com/9z7OQPi.png", "http://i.imgur.com/tgLP4VE.png",
                      "http://i.imgur.com/zm6OAhl.png", "http://i.imgur.com/0VnDJ30.png", "http://i.imgur.com/7qiTA2y.png", "http://i.imgur.com/U5lWjIO.jpg", "http://i.imgur.com/ihdDaW2.png", "http://i.imgur.com/DcPImeK.png", "http://i.imgur.com/zUpPCg8.png"]
        if member is None:
            member = ctx.message.author
        randpic = random.randint(0, len(sleep_list)-1)
        caption = "{} Should you still be up, poi?".format(member.mention)
        await self.bot.say("{}\n{}".format(sleep_list[randpic], caption))

    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx, member: str = None):
        """Gets some basic info about the user"""
        if len(ctx.message.mentions) < 1:
            member = ctx.message.author if member is None else await getmember(member, ctx.message)
        else:
            member = ctx.message.mentions[0]
        status = "{} **playing** {}".format(member.status, member.game) if member.game else member.status
        roles = ", ".join(str(role) for role in member.roles).lstrip("@everyone, ")
        msg = "**Name:** {}\n**ID:** {}\n**Joined server:** {}\n**Account created:** {}\n**Status:** {}\n**Roles:** {}".format(
            member.name, member.id, member.joined_at.strftime("%A %B %d %Y %H:%M %p UTC"),
            member.created_at.strftime("%A %B %d %Y %H:%M %p UTC"), status, roles)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Gets info about the server"""
        msg = "**{}** (ID: {})\n**Owner:** {} (ID: {})\n**Members:** {}\n**Channels:** {} text, {} voice\n**Roles:** {}\n**Created on:** {}\n**Default channel:** {}\n**Region:** {}\n**Icon:** <{}>".format(
            ctx.message.server.name, ctx.message.server.id, ctx.message.server.owner, ctx.message.server.owner.id,
            len(ctx.message.server.members), sum(1 for c in ctx.message.server.channels if c.type == discord.ChannelType.text),
            sum(1 for c in ctx.message.server.channels if c.type == discord.ChannelType.voice),
            len(ctx.message.server.roles), ctx.message.server.created_at.strftime("%A %B %d %Y %H:%M %p UTC"),
            ctx.message.server.default_channel.mention, ctx.message.server.region, ctx.message.server.icon_url)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def ava(self, ctx, member: discord.Member = None):
        """Gets a mentioned users avatar"""
        if ctx.message.mentions:
            await self.bot.say(member.avatar_url)

    @commands.command(no_pm=True)
    async def define(self, word: str):
        dictionary = PyDictionary()
        await self.bot.say(dictionary.meaning(word))




def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def get_icon(icon):
    if icon in ["01d", "01n"]:
        return "\u2600"
    if icon in ["02d", "02n"]:
        return "\u26C5"
    if icon in ["03d", "03n", "04d", "04n"]:
        return "\u2601"
    if icon in ["09d", "09n"]:
        return "\U0001F326"
    if icon in ["10d", "10n"]:
        return "\U0001F327"
    if icon in ["11d", "11n"]:
        return "\u26C8"
    if icon in ["13d", "13n"]:
        return "\U0001F328"
    else:
        return ""

def get_deg(deg):
    if 0 < deg < 11.25:
        return "North"
    if 11.26 < deg < 33.75:
        return "NNE"
    if 33.76 < deg < 56.25:
        return "NE"
    if 56.26 < deg < 78.75:
        return "ENE"
    if 78.76 < deg < 101.25:
        return "East"
    if 101.26 < deg < 123.75:
        return "ESE"
    if 123.76 < deg < 146.25:
        return "SE"
    if 146.25 < deg < 168.75:
        return "SSE"
    if 168.76 < deg < 191.25:
        return "South"
    if 191.26 < deg < 213.75:
        return "SSW"
    if 213.76 < deg < 236.25:
        return "SW"
    if 236.26 < deg < 258.75:
        return "WSW"
    if 258.76 < deg < 281.25:
        return "West"
    if 281.26 < deg < 303.75:
        return "WNW"
    if 303.76 < deg < 326.25:
        return "NW"
    if 326.26 < deg < 348.75:
        return "NNW"
    if 348.76 < deg < 360:
        return "North"

async def getmember(member, message):
    for x in message.server.members:
        if member in x.name.lower() and "Expired" not in x.name:
            return x

def setup(bot):
    bot.add_cog(Commands(bot))