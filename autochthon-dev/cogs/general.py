import discord
from time import sleep
from discord.ext import commands
from functools import reduce

async def executeReminder(ctx, message, mentions):
    """"""

def convertToSeconds(token):
    if token.endswith('h'):
        int(filter(str.isdigit, token)) * 3600
    elif token.endswith('m'):
        int(filter(str.isdigit, token)) * 60
    elif token.endswith('s'):
        int(filter(str.isdigit, token))
    else:
        0


def user_input_time(ctx, *, arguments):
    timeTokens = [time for time in arguments.split()]
    return reduce((lambda x, y: x+y), map(convertToSeconds, timeTokens))


class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindMe(self, ctx, message, **timeToRemind):

        seconds = 0
        if 'hours' in timeToRemind:
            seconds += (timeToRemind['hours'] * 3600)
        if 'h' in timeToRemind:
            seconds += (timeToRemind['h'] * 3600)
        if 'minutes' in timeToRemind:
            seconds += (timeToRemind['minutes'] * 60)
        if 'm' in timeToRemind:
            seconds += (timeToRemind['m'] * 60)
        if 'seconds' in timeToRemind:
            seconds = timeToRemind['seconds']
        if 's' in timeToRemind:
            seconds = timeToRemind['s']

        sleep(seconds)
        await ctx.send(message)

def setup(bot):
    bot.add_cog(General(bot))