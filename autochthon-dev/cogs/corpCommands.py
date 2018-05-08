import discord
from .utils import roleManagement
from discord.ext import commands


class CorpCommands:
    def __init__(self, bot):
        self.bot = bot

    async def induct_member(self, ctx, member: discord.Member, nickname: str, levels: int):
        await member.edit(nick=nickname)
        return await roleManagement.set_rs_roles(ctx, member, levels)

    async def assign_moc(self, ctx, member: discord.Member, nickname: str, levels: int):
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles if role.name == 'moc' or role.name == 'ws']
        roleNames = [role.name for role in roles]
        await member.add_roles(*roles, atomic=True)
        roleNames += await self.induct_member(ctx, member, nickname, levels)
        await ctx.send(f'{member.name} has been granted the roles {roleNames}')

    async def assign_ally(self, ctx, member: discord.Member, nickname: str, levels: int):
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles if role.name == 'Ally']
        roleNames = [role.name for role in roles]
        await member.add_roles(*roles, atomic=True)
        roleNames += await self.induct_member(ctx, member, nickname, levels)
        await ctx.send(f'{member.name} has been granted the roles {roleNames}')

    async def remove_member(self, ctx, member: discord.Member):
        roles = [role for role in member.roles if role != ctx.guild.default_role]
        roleNames = [role.name for role in roles if role]
        await member.remove_roles(*roles, atomic=True)
        await ctx.send(f'{member.name} has been removed from {roleNames}')

    async def make_guest(self, ctx, member: discord.Member, nickname: str):
        await self.remove_member(ctx, member)
        await member.edit(nick=nickname)
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles if role.name == 'Guest']
        roleNames = [role.name for role in roles]
        await member.add_roles(*roles, atomic=True)
        await ctx.send(f'{member.name} has been granted the roles {roleNames}')

# Assign Commands #############################################################

    @commands.guild_only()
    @commands.has_any_role('Admin', 'Officer')
    @commands.group(aliases=['add', 'give'], invoke_without_command=True)
    async def assign(self, ctx):
        await ctx.send(f'Please choose a subcommand.')

    @assign.command()
    async def moc(self, ctx, member: discord.Member, nickname: str, *levels: int):
        await self.assign_moc(ctx, member, nickname, levels)

    @assign.command(name='rs')
    async def ass_rs(self, ctx, member: discord.Member, *levels: int):
        roleNames = await roleManagement.set_rs_roles(ctx, member, levels)
        await ctx.send(f'{member.name} has been granted the roles {roleNames}')

    @assign.command(name='ws')
    async def ass_ws(self, ctx, member: discord.Member):
        roleNames = await roleManagement.set_ws_role(ctx, member)
        await ctx.send(f'{member.name} has been granted the role {roleNames}')

    @assign.command()
    async def ally(self, ctx, member: discord.Member, nickname: str, *levels: int):
        await self.assign_ally(ctx, member, nickname, levels)

    @assign.command()
    async def guest(self, ctx, member: discord.Member, nickname: str):
        await self.make_guest(ctx, member, nickname)

# Revoke Commands #############################################################

    @commands.guild_only()
    @commands.has_any_role('Admin', 'Officer')
    @commands.group(aliases=['remove'], invoke_without_command=True)
    async def revoke(self, ctx):
        await ctx.send(f'Please choose a subcommand.')

    @revoke.command()
    async def roles(self, ctx, member: discord.Member):
        await self.remove_member(ctx, member)

    @revoke.command(name='rs')
    async def rem_rs(self, ctx, member: discord.Member, *levels: int):
        roleNames = await roleManagement.remove_rs_roles(ctx, member, levels)
        await ctx.send(f'{member.name} has been removed from {roleNames}')

    @revoke.command(name='ws')
    async def rem_ws(self, ctx, member: discord.Member):
        roleNames = await roleManagement.remove_ws_role(ctx, member)
        await ctx.send(f'{member.name} has been removed from {roleNames}')

###############################################################################

    @commands.guild_only()
    @commands.has_any_role('Admin', 'Officer')
    @commands.command(aliases=['addMember', 'moc-ify'])
    async def inductMember(self, ctx, member: discord.Member, nickname: str, *levels: int):
        await self.assign_moc(ctx, member, nickname, levels)

    @commands.guild_only()
    @commands.has_any_role('Admin', 'Officer')
    @commands.command(aliases=['de-moc-ify'])
    async def removeMember(self, ctx, member: discord.Member):
        await self.remove_member(ctx, member)

    @commands.guild_only()
    @commands.has_any_role('Admin', 'Officer')
    @commands.command()
    async def makeAlly(self, ctx, member: discord.Member, nickname: str, *levels: int):
        await self.assign_ally(ctx, member, nickname, levels)

    @commands.guild_only()
    @commands.has_any_role('Admin', 'Officer')
    @commands.command(aliases=['guestify'])
    async def makeGuest(self, ctx, member: discord.Member, nickname: str):
        await self.make_guest(ctx, member, nickname)

def setup(bot):
    bot.add_cog(CorpCommands(bot))
