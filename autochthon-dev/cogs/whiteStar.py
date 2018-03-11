import discord
from discord.ext import commands


class WhiteStar:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def ws(self, ctx):
        """"""

    @commands.has_any_role('Admin', 'Officer')
    @ws.command()
    async def grant(self, ctx, role: discord.Role, *members: discord.Member):
        for member in members:
            await member.add_roles(role)

    @commands.has_any_role('Admin', 'Officer')
    @ws.command()
    async def revoke(self, ctx, role: discord.Role, *members: discord.Member):
        for member in members:
            await member.remove_roles(role)

    @ws.command(aliases=['opt-in'])
    async def add(self, ctx, role: discord.Role):
        user = ctx.author
        await user.add_roles(role)

    @ws.command(aliases=['opt-out'])
    async def remove(self, ctx, role: discord.Role):
        user = ctx.author
        await user.remove_roles(role)

def setup(bot):
    bot.add_cog(WhiteStar(bot))