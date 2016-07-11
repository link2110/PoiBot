from discord.ext import commands
import asyncio
import traceback
import discord

"""
Repl written by Danny/Rapptz https://github.com/Rapptz/RoboDanny/blob/master/cogs/repl.py
Debug written by TwentySix https://github.com/Twentysix26/Red-DiscordBot/blob/develop/cogs/owner.py
"""

def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == "97097796372414464"
    return commands.check(predicate)

class REPL:
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def repl(self, ctx):
        msg = ctx.message

        repl_locals = {}
        repl_globals = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'last': None
        }

        await self.bot.say('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for_message(author=msg.author, channel=msg.channel,
                                                       check=lambda m: m.content.startswith('`'))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await self.bot.say('Exiting.')
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await self.bot.say(self.get_syntax_error(e))
                    continue

            repl_globals['message'] = response

            fmt = None

            try:
                result = executor(code, repl_globals, repl_locals)
                if asyncio.iscoroutine(result):
                    result = await result
            except Exception as e:
                fmt = '```py\n{}\n```'.format(traceback.format_exc())
            else:
                if result is not None:
                    fmt = '```py\n{}\n```'.format(result)
                    repl_globals['last'] = result

            try:
                if fmt is not None:
                    await self.bot.send_message(msg.channel, fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await self.bot.send_message(msg.channel, 'Unexpected error: `{}`'.format(e))

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def debug(self, ctx, *, code):
        """Evaluates code
        Modified function, originally made by Rapptz"""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        local_vars = locals().copy()
        local_vars['bot'] = self.bot

        try:
            result = eval(code, globals(), local_vars)
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return

        if asyncio.iscoroutine(result):
            result = await result

        result = python.format(result)
        await self.bot.say(result)

def setup(bot):
    bot.add_cog(REPL(bot))