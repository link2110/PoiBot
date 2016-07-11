import discord
from discord.ext import commands


def is_admin():
    def predicate(ctx):
        role_list = [discord.Role.name for discord.Role in ctx.message.author.roles]
        return "Poi's Admiral" in role_list or ctx.message.author.id == "97097796372414464"

    return commands.check(predicate)


class Admin():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def purge(self, ctx, number: int):
        """Deletes <#> of messages from the channel it's used in"""
        await self.bot.purge_from(ctx.message.channel, limit=number + 1)

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def clean(self, ctx, number: int, member: discord.Member):
        """Deletes all messages from @user inside of <#> of messages
        For example, ?clean 50 @link2110 would delete all messages by @link2110 in the last 50 messages.
        """
        def member_check(msg):
            return member == msg.author
        await self.bot.purge_from(ctx.message.channel, limit=number + 1, check=member_check)

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def leaveserver(self, ctx):
        """Leaves the server"""
        await self.bot.say("Are you sure you want me to leave the server, Poi~?\n`y/n`")
        check = await self.bot.wait_for_message(timeout=30, author=ctx.message.author, channel=ctx.message.channel)
        if check.content.lower() == "y":
            await self.bot.say("Okay, goodbye, poi~ \U0001F626")
            await self.bot.leave_server(ctx.message.server)

    @commands.command(no_pm=True)
    @is_admin()
    async def kick(self, member:discord.Member):
        """Kicks a member from the server"""
        await self.bot.kick(member)
        msg = "Kicked {}".format(member.name)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def softban(self, ctx, member:discord.Member):
        """Bans a member from the server, then unbans them.
        Equivalent to kicking and deleting 2 days worth of their messages.
        """
        unban = member.id
        await self.bot.ban(member, delete_message_days=2)
        await self.bot.unban(ctx.message.server, discord.User(id=unban))
        msg = "Softbanned {}".format(member.name)
        await self.bot.say(msg)

    @commands.command(no_pm=True)
    @is_admin()
    async def ban(self, member:discord.Member):
        """Bans a member and deletes 3 days of their messages."""
        await self.bot.ban(member, delete_message_days=3)
        msg = "Banned {}".format(member.name)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def unban(self, ctx, member: discord.Member):
        """Unbans a member from the server"""
        await self.bot.unban(ctx.message.server, member)
        msg = "Unbanned {}".format(member.name)
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def mute(self, ctx, member: discord.Member):
        """
        Mutes the member passed.
        Requires a Muted role set up in each channel that you want people to be
        muted in, denying every permission but the two read ones.
        """
        role = discord.utils.get(ctx.message.server.roles, name="Muted")
        await self.bot.add_roles(member, role)
        await self.bot.say("Muted {}".format(member.name))

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes the member passed"""
        if ctx.message.mentions:
            role = discord.utils.get(ctx.message.server.roles, name="Muted")
            role_list = member.roles
        try:
            if role in role_list:
                role_list.remove(role)
            await self.bot.replace_roles(member, *role_list)
            await self.bot.say("Unmuted {}".format(member.name))
        except Exception as e:
            await self.bot.say("Could not unmute {}".format(member.name))
            await self.bot.say(e)

    @commands.command(no_pm=True, hidden=True)
    @is_admin()
    async def servers(self):
        connected = []
        if self.bot.servers:
            for s in self.bot.servers:
                connected.append(s.name)
            await self.bot.say("Connected to: " + str(connected).strip("[]"))
        else:
            print("Not connected to any servers.")

    @commands.command(no_pm=True, pass_context=True)
    @is_admin()
    async def addrole(self, ctx, user: discord.Member, *, role_name: str):
        """Adds a role to a user."""
        try:
            role = discord.utils.get(ctx.message.server.roles, name=role_name)
            await self.bot.add_roles(user, role)
            await self.bot.say("Sucessfully added {} to {}".format(user.name, role_name))
        except Exception as e:
            await self.bot.say("Could not add {} to {}".format(user.name, role_name))
            await self.bot.say(e)

    @commands.command(no_pm=True, pass_context=True)
    @is_admin()
    async def removerole(self, ctx, user: discord.Member, *, role_name: str):
        """Removes a role from a user."""
        if ctx.message.mentions:
            role = discord.utils.get(ctx.message.server.roles, name=role_name)
            role_list = user.roles
        try:
            if role in role_list:
                role_list.remove(role)
            await self.bot.replace_roles(user, *role_list)
            await self.bot.say("Sucessfully removed {} from {}".format(user.name, role_name))
        except Exception as e:
            await self.bot.say("Could not remove {} from {}".format(user.name, role_name))
            await self.bot.say(e)

    @commands.command(pass_context=True, no_pm=True)
    @is_admin()
    async def muteperms(self, ctx):
        """Adds Muted permissions to channel used in"""
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
        await self.bot.edit_channel_permissions(ctx.message.channel, discord.utils.get(ctx.message.server.roles, name="Muted"), overwrite)
        await self.bot.say("Set up Muted permissions for this channel")





def setup(bot):
    bot.add_cog(Admin(bot))