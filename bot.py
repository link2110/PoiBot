import discord
from discord.ext import commands
import arrow
import aiohttp
import random


start_time = arrow.utcnow().replace(microsecond=0)
# asset_pos = "H:\Documents\Bot Folder\PoiBot\\assets"
startup_extensions = ["cogs.Admin", "cogs.Commands", "cogs.Fun", "cogs.Remind", "cogs.Repl", "cogs.Special",
                      "cogs.Tags", "cogs.Timezone"]

description = """I'm a bot made by link2110 (ID: 97097796372414464)\n
To use Admin commands, you must have the role "Poi's Admiral" This is made upon server join, so you just have to assign it.\n
PM @link2110 if you have ideas/suggestions for the bot!\n
Command Catagories:
"""
bot = commands.Bot(command_prefix='?', description=description, pm_help=None)

pm_msg = False

def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == "97097796372414464"
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        role_list = [discord.Role.name for discord.Role in ctx.message.author.roles]
        return "Poi's Admiral" in role_list or ctx.message.author.id == "97097796372414464"
    return commands.check(predicate)

@bot.command()
async def poi():
    """Poi~"""
    poi_chance = random.randint(0, 100)
    if 0 <= poi_chance <= 74:
        await bot.say("Poi!")
    if 75 <= poi_chance <= 85:
        await bot.say("http://i.imgur.com/EkjuUcB.png")
    if 86 <= poi_chance <= 96:
        await bot.say("http://i.imgur.com/d1iS6iK.jpg")
    if 97 <= poi_chance <= 99:
        await bot.say("http://i.imgur.com/Nl9tyhE.png")
    if poi_chance == 100:
        await bot.say("http://i.imgur.com/tv4FB9Q.png")

@bot.command(hidden=True)
@is_admin()
async def uptime():
    current_time = arrow.utcnow().replace(microsecond=0)
    difference = current_time - start_time
    hours, remainder = divmod(int(difference.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        fmt = "{} days, {} hours, {} minutes, and {} seconds".format(days, hours, minutes, seconds)
    else:
        fmt = "{} hours, {} minutes, and {} seconds".format(hours, minutes, seconds)
    msg = "I have been running for: **{}**".format(fmt)
    await bot.say(msg)

@bot.command(pass_context=True, hidden=True)
@is_owner()
async def changenick(ctx, name:str):
    await bot.change_nickname(ctx.message.server.me, name)
    await bot.say("\U0001F44D")

@bot.command(hidden=True)
@is_owner()
async def changename(name:str):
    await bot.edit_profile(username=name)
    await bot.say("\U0001F44D")

@bot.command(hidden=True)
@is_owner()
async def changegame(game:str):
    await bot.change_status(game=discord.Game(name=game))
    await bot.say("\U0001F44D")

@bot.command(hidden=True)
@is_owner()
async def changeava(url:str):
    with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            ava = await resp.read()
            await bot.edit_profile(avatar=ava)
            await bot.say("\U0001F44D")

@bot.command(hidden=True, pass_context=True)
async def chid(ctx):
    """Gets current channel ID"""
    await bot.say(ctx.message.channel.id)

@bot.command(hidden=True, pass_context=True)
async def sid(ctx):
    """Gets current server ID"""
    await bot.say(ctx.message.server.id)

@bot.command(hidden=True)
async def getid(member:discord.Member):
    """Gets the user ID of mentioned user"""
    await bot.say(member.id)

@bot.command()
async def url():
    """Generates an invite link to bring Yuudachi to your server"""
    oauth_url = discord.utils.oauth_url("181157059130163207", permissions=discord.Permissions.all())
    msg = "Please use this link to add me to your server, Poi~ \n{}".format(oauth_url)
    await bot.say(msg)

@bot.command(hidden=True)
@is_owner()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command(hidden=True)
@is_owner()
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension("cogs.{}".format(extension_name))
    await bot.say("{} unloaded.".format(extension_name))

@bot.command(hidden=True)
@is_owner()
async def reload(extension_name:str):
    """Reloads an extension"""
    bot.unload_extension("cogs.{}".format(extension_name))
    await bot.say("{} unloaded.".format(extension_name))
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command(hidden=True)
@is_owner()
async def pmmention(option: str):
    if option == "yes":
        global pm_msg
        pm_msg = True

    if option == "no":
        global pm_msg
        pm_msg = False


@bot.event
async def on_server_join(server):
    """Create the Admin role, Muted role, and then add Muted perms to every channel, given correct perms."""
    await bot.create_role(server, name="Poi's Admiral")
    muted = await bot.create_role(server, name="Muted", permissions=discord.Permissions(permissions=1115136))
    await make_muted_perms(server, muted)
    await bot.send_message(server, "Hello! I'm a bot invited to the server to make your life a little easier and more fun! Please move the `Yuudachi Kai` role to underneath your Admin role and then move the `Muted` role underneath that so that I can mute people properly! Everything else has been set up already if you gave me the `Administrator` permission. Thanks!")


async def make_muted_perms(server, muted):
    """This adds muted perms to every channel, easier than getting admins to do it manually"""
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    overwrite.embed_links = False
    overwrite.attach_files = False
    overwrite.create_instant_invite = False
    overwrite.manage_messages = False
    overwrite.send_tts_messages = False
    overwrite.mention_everyone = False
    overwrite.speak = False
    overwrite.use_voice_activation = False
    for channel in server.channels:
        await bot.edit_channel_permissions(channel, muted, overwrite)


@bot.event
async def on_message(message):
    if message.author.id == "97097796372414464" and message.server is None and pm_msg is True:
        await bot.send_message(discord.User(id=97097796372414464), message.content)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    users = str(len(set(bot.get_all_members())))
    servers = str(len(bot.servers))
    channels = str(len([c for c in bot.get_all_channels()]))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("Connected to:")
    print(servers + " servers")
    print(channels + " channels")
    print(users + " users")
    print('------')
    await bot.change_status(game=discord.Game(name="Poi~"))

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

token_file = open("H:\Documents\Bot Folder\PoiBot\credentials\\token.txt")
token = token_file.read()
bot.run(token)
