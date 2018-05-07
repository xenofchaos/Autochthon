import discord

async def set_rs_roles(ctx, member: discord.Member, levels: int):
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles for i in levels if role.name == f'rs{i}']
        await member.add_roles(*roles, atomic=True)
        return [role.name for role in roles]

async def remove_rs_roles(ctx, member: discord.Member, levels: int):
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles for i in levels if role.name == f'rs{i}']
        await member.remove_roles(*roles, atomic=True)
        return [role.name for role in roles]

async def set_ws_role(ctx, member: discord.Member):
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles if role.name == 'ws']
        await member.add_roles(*roles, atomic=True)
        return [role.name for role in roles]

async def remove_ws_role(ctx, member: discord.Member):
        guildRoles = ctx.guild.roles
        roles = [role for role in guildRoles if role.name == 'ws']
        await member.remove_roles(*roles, atomic=True)
        return [role.name for role in roles]