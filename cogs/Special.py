import discord
from discord.ext import commands
import random
import os
import asyncio
import datetime
import shelve

approved_servers = ["137463604311097345", "107915021203304448", "136548137929146368"]
dq_user_list = []
color_change_db = "H:\Documents\Bot Folder\PoiBot\\assets\db stuff\colorchange"

def is_admin():
    def predicate(ctx):
        role_list = [discord.Role.name for discord.Role in ctx.message.author.roles]
        return "Poi's Admiral" in role_list or ctx.message.author.id == "97097796372414464"

    return commands.check(predicate)

def is_r_anime():
    def predicate(ctx):
        return ctx.message.server.id == "107915021203304448"
    return commands.check(predicate)

def is_r_LL():
    def predicate(ctx):
        return ctx.message.server.id == "137463604311097345"
    return commands.check(predicate)

class Special:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True, pass_context=True, no_pm=True)
    async def o7(self, ctx):
        if ctx.message.server.id not in approved_servers:
            return
        o7_list = ["http://i.imgur.com/KsGrJFa.gif", "http://i.imgur.com/qYwvw4L.gifv", "http://i.imgur.com/bG5I7my.gif", "http://i.imgur.com/NL1oyAO.gif"]
        randpic = random.randint(0, len(o7_list) - 1)
        await self.bot.say(o7_list[randpic])

    @commands.command(hidden=True, pass_context=True, no_pm=True)
    async def mimowink(self, ctx):
        if ctx.message.server.id not in approved_servers:
            return
        mimo_list = ["http://i.imgur.com/jvs90i9.gif", "http://i.imgur.com/HsU7iKA.gif", "http://i.imgur.com/SbmG0q9.gif", "http://i.imgur.com/VEIlO6Y.gif",
                     "http://i.imgur.com/kvry4EI.gif", "http://i.imgur.com/XeH5ovB.gif", "http://i.imgur.com/ABayQT6.gif", "http://i.imgur.com/0OPPzis.gif",
                     "http://i.imgur.com/LElvWp2.gif", "http://i.imgur.com/1NNnMfz.gif", "http://i.imgur.com/tYbCTmZ.gif"]
        randpic = random.randint(0, len(mimo_list) - 1)
        await self.bot.say(mimo_list[randpic])

    @commands.command(hidden=True, no_pm=True)
    async def mimotink(self):
        await self.bot.say("http://i.imgur.com/Pz1jzuw.png")

    @commands.command(hidden=True, no_pm=True, pass_context=True)
    async def dq(self, ctx):
        dq_user_list.append(ctx.message.author.id)
        msg = "{} you're registered, Poi~".format(ctx.message.author.mention)
        await self.bot.say(msg)
        
    @commands.command(hidden=True, no_pm=True, pass_context=True)
    async def readycheck(self, ctx):
        if ctx.message.server.id not in approved_servers:
            return
        readylist = {}
        readycount = 0
        usernumber = len(dq_user_list)
        print(dq_user_list)
        for x in range(usernumber):
            dq_user = discord.User(id=dq_user_list[x])
            msg = "<@{}> ready? Answer yes if ready, no if you're not, Poi~".format(dq_user_list[x])
            await self.bot.say(msg)
            status = await self.bot.wait_for_message(timeout=60, author=dq_user, channel=ctx.message.channel)
            if status is None:
                readylist[dq_user_list[x]] = "no"
            elif status.content.lower() == "yes":
                readylist[dq_user_list[x]] = "yes"
            else:
                readylist[dq_user_list[x]] = "no"
        for y in range(usernumber):
            if readylist[dq_user_list[y]] == "no":
                msg = "<@{}> is not ready\nPlease use ?readycheck when you're ready".format(dq_user_list[y])
                await self.bot.say(msg)
                break
            if readylist[dq_user_list[y]] == "yes":
                readycount += 1
        if readycount == len(dq_user_list):
            dq_user_list[:] = []
            msg = "Countdown!\n5"
            await self.bot.say(msg)
            await asyncio.sleep(1)
            msg2 = "4"
            await self.bot.say(msg2)
            await asyncio.sleep(1)
            msg3 = "3"
            await self.bot.say(msg3)
            await asyncio.sleep(1)
            msg4 = "2"
            await self.bot.say(msg4)
            await asyncio.sleep(1)
            msg5 = "1"
            await self.bot.say(msg5)
            await asyncio.sleep(1)
            msg6 = "Go!"
            await self.bot.say(msg6)

    @commands.command(hidden=True, no_pm=True)
    async def dqclear(self):
        global dq_user_list
        dq_user_list = []
        await self.bot.say("DQ list has been cleared")

    @commands.command(hidden=True, pass_context=True, no_pm=True)
    @is_admin()
    async def remake(self, ctx, *, name: str):
        """Renames and cleans the channel"""
        name = name.replace(" ", "-").lower()
        await self.bot.edit_channel(ctx.message.channel, name=name)
        await self.bot.purge_from(ctx.message.channel, limit=5000)

    @commands.command(pass_context=True, no_pm=True)
    async def card(self, ctx, card_id:str):
        """Looks up the SIF card ID specified"""
        data = await get_json(card_id)
        try:
            name = data["idol"]["name"]
            rarity = data["rarity"]
            attribute = data["attribute"]
            smile = data["idolized_maximum_statistics_smile"]
            pure = data["idolized_maximum_statistics_pure"]
            cool = data["idolized_maximum_statistics_cool"]
            skill = data["skill"]
            if data["is_promo"]:
                image = data["card_idolized_image"]
            else:
                image = data["card_image"]
            msg = "{} Here's data for card {}. \n **Name:** {}, **Rarity:** {}, **Attribute:** {}, **Skill:** {}, **Max Idolized Smile:** {}, **Max Idolized Pure:** {}, **Max Idolized Cool:** {} \n {}".format(
                ctx.message.author.mention, card_id, name, rarity, attribute, skill, smile, pure, cool, image)
            await self.bot.say(msg)

        except Exception as e:
            await self.bot.say("This card does not exist yet.")
            raise e

    @commands.command(pass_context=True, no_pm=True)
    @is_r_anime()
    async def joinchannel(self, ctx, *, channel_name: str):
        """Adds you to the selected hidden channel"""
        try:
            role = discord.utils.get(ctx.message.server.roles, name=channel_name)
            channel_name = channel_name.replace(" ", "-")
            channel_ref = discord.utils.get(ctx.message.server.channels, name=channel_name)
            await self.bot.add_roles(ctx.message.author, role)
            await self.bot.say("Welcome to <#{}>".format(channel_ref.id))
        except AttributeError:
            if "#" in channel_name:
                await self.bot.say("Could not add you to the channel. Don't use # in the channel name.")
            else:
                await self.bot.say("Could not add you to the channel\nChannel {} does not exist".format(channel_name))
        except Exception as e:
            await self.bot.say("Could not add you to the channel")
            await self.bot.say(e)
            raise e
        
    @commands.command(pass_context=True, no_pm=True)
    @is_r_anime()
    async def leavechannel(self, ctx, *, channel_name: str):
        """Removes you from the selected hidden channel"""
        try:
            role = discord.utils.get(ctx.message.server.roles, name=channel_name)
            channel_name = channel_name.replace(" ", "-")
            channel_ref = discord.utils.get(ctx.message.server.channels, name=channel_name)
            role_list = ctx.message.author.roles
            if role in role_list:
                role_list.remove(role)
                await self.bot.replace_roles(ctx.message.author, *role_list)
                await self.bot.send_message(ctx.message.author, "You have left {}".format(channel_ref.name))
            else:
                return
        except AttributeError:
            if "#" in channel_name:
                await self.bot.say("Could not remove you from the channel. Don't use # in the channel name.")
            else:
                await self.bot.say("Could not remove you from the channel\nChannel {} does not exist".format(channel_name))
        except Exception as e:
            raise e

    @commands.command(pass_context=True, no_pm=True, aliases=["color"])
    async def colour(self, ctx, hex_color: str):
        """Lets you change your role colour"""
        role_list = ctx.message.author.roles
        timenow = datetime.datetime.utcnow()
        with shelve.open(color_change_db, flag="c", writeback=True) as db:

            try:
                last_changed = db[ctx.message.author.id]["date"]
                if (timenow - last_changed) > datetime.timedelta(days=7):
                    for role in role_list:
                        if role.name.startswith("#"):
                            color_role = role
                            data = {"name": ctx.message.author.name, "id": ctx.message.author.id, "date": timenow}
                            await self.bot.edit_role(ctx.message.server, color_role, name="#" + hex_color, color=discord.Color(value=int(hex_color, 16)))
                            db[ctx.message.author.id] = data
                            await self.bot.say("Role color changed to {}".format(hex_color))
                else:
                    msg = "You cannot change your role colour more than once per week. Your last change was on {}".format(last_changed.strftime("%b %d %I:%M %p UTC"))
                    await self.bot.say(msg)
                    return

            except KeyError:
                for role in role_list:
                    if role.name.startswith("#"):
                        color_role = role
                        data = {"name": ctx.message.author.name, "id": ctx.message.author.id, "date": timenow}
                        await self.bot.edit_role(ctx.message.server, color_role, name="#" + hex_color, color=discord.Color(value=int(hex_color, 16)))
                        db[ctx.message.author.id] = data
                        await self.bot.say("Role color changed to {}".format(hex_color))

            except Exception:
                raise

    @commands.command(pass_context=True, hidden=True, no_pm=True)
    @is_admin()
    @is_r_LL()
    async def niconama(self, ctx, *, message: str):
        """Niconama annoucement"""
        role = discord.utils.get(ctx.message.server.roles, name="Niconama")
        async for del_msg in self.bot.logs_from(ctx.message.channel, limit=1):
            await self.bot.delete_message(del_msg)
        await self.bot.edit_role(ctx.message.server, role, mentionable=True)
        await self.bot.say("{} {}".format(role.mention, message))
        await self.bot.edit_role(ctx.message.server, role, mentionable=False)

async def get_json(cardid):
    import re
    import json
    imgsave = "H:\Documents\PyCharmProjects\ChatBot\SavedCards\JSON"
    for filename in os.listdir(imgsave):
        if re.match(str(cardid) + "\w", filename):
            path = os.path.join(imgsave, filename)
            with open(path) as data_file:
                data = json.load(data_file)
                return data

def setup(bot):
    bot.add_cog(Special(bot))