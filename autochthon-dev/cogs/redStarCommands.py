
import discord
from discord.ext import commands


class RedStarCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True, hidden=True)
    async def rs(self, ctx):
        """
        A test command, Mainly used to show how commands and cogs should be laid out.
        """
        await ctx.send('Please choose a subcommand.')

    @commands.has_any_role('Admin', 'Officer')
    @rs.command()
    async def give(self, ctx, *levels):
        member = ctx.message.author
        roles = list(member.roles)
        corpPfx = ''
        for role in roles:
            if '-corp' in role.name:
                """Get role prefix"""
        #for level in levels:
            

def setup(bot):
    bot.add_cog(RedStarCommands(bot))