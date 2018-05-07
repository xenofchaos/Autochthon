import discord
from .utils import roleManagement
from discord.ext import commands


class StarCommands:
    def __init__(self, bot):
        self.bot = bot

    async def set_rs_roles(self, ctx, levels: int):
        roleNames = await roleManagement.set_rs_roles(ctx, ctx.author, levels)
        await ctx.send(f'You have been granted the roles {roleNames}')

    async def remove_rs_roles(self, ctx, levels: int):
        pass
        roleNames = await roleManagement.remove_rs_roles(ctx, ctx.author, levels)
        await ctx.send(f'You have been removed from {roleNames}')

# Assign Commands #############################################################

    @commands.guild_only()
    @commands.group(aliases=['opt-in'], invoke_without_command=True)
    async def iam(self, ctx):
        await ctx.send(f'Please choose a subcommand.')

    @commands.has_any_role("moc", "Ally")
    @iam.command()
    async def rs(self, ctx, *levels: int):
        await self.set_rs_roles(ctx, levels)

    @commands.has_role("moc")
    @iam.command()
    async def ws(self, ctx):
        roleNames = await roleManagement.set_ws_role(ctx, ctx.author)
        await ctx.send(f'You have been granted the role {roleNames}')

    @commands.has_any_role("moc", "Ally")
    @iam.command()
    async def rs5(self, ctx):
        await self.set_rs_roles(ctx, [5])

    @commands.has_any_role("moc", "Ally")
    @iam.command()
    async def rs6(self, ctx):
        await self.set_rs_roles(ctx, [6])

    @commands.has_any_role("moc", "Ally")
    @iam.command()
    async def rs7(self, ctx):
        await self.set_rs_roles(ctx, [7])

    @commands.has_any_role("moc", "Ally")
    @iam.command()
    async def rs8(self, ctx):
        await self.set_rs_roles(ctx, [8])

# Revoke Commands #############################################################

    @commands.guild_only()
    @commands.group(aliases=['opt-out'], invoke_without_command=True)
    async def iamnot(self, ctx):
        await ctx.send(f'Please choose a subcommand.')

    @commands.has_any_role("moc", "Ally")
    @iamnot.command()
    async def rs(self, ctx, *levels: int):
        await self.remove_rs_roles(ctx, levels)

    @commands.has_any_role("moc")
    @iamnot.command()
    async def ws(self, ctx):
        roleNames = await roleManagement.remove_ws_role(ctx, ctx.author)
        await ctx.send(f'You have been removed from {roleNames}')

    @commands.has_any_role("moc", "Ally")
    @iamnot.command()
    async def rs5(self, ctx):
        await self.remove_rs_roles(ctx, [5])

    @commands.has_any_role("moc", "Ally")
    @iamnot.command()
    async def rs6(self, ctx):
        await self.remove_rs_roles(ctx, [6])

    @commands.has_any_role("moc", "Ally")
    @iamnot.command()
    async def rs7(self, ctx):
        await self.remove_rs_roles(ctx, [7])

    @commands.has_any_role("moc", "Ally")
    @iamnot.command()
    async def rs8(self, ctx):
        await self.remove_rs_roles(ctx, [8])

def setup(bot):
    bot.add_cog(StarCommands(bot))