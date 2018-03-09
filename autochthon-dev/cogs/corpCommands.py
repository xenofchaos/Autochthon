import discord
from discord.ext import commands


class CorpCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def corp(self, ctx):
        """Command group for corp administration."""
        await ctx.send(f'Please choose a subcommand.')

    def rsLevelWithinRange(self, lvl: int):
        return (lvl < 1 or lvl > 10)

    def checkRoleForSuffix(role, suffix):
        return (suffix in role.name)

    async def updateChannelWithNewRole(self, ctx, role, roleSuffix):
        guild = ctx.guild
        channels = guild.channels
        for channel in channels:
            rolesWithSuffix = [role for role in channel.changed_roles if roleSuffix in role.name]
            if len(rolesWithSuffix) > 0:
                await channel.set_permissions(role, read_messages=True)

    async def createRoles(self, ctx, rolePrefix: str, roleColor: discord.Color, minRs: int, maxRs: int):
        guild = ctx.guild
        span = 1 + (maxRs - minRs)
        wsRole = None
        try:

            corpRole = await guild.create_role(name=f'{rolePrefix}-corp', color=roleColor, mentionable=True, permissions=discord.Permissions(37084225))
            await ctx.send(f'Created role {rolePrefix}-corp')
            await self.updateChannelWithNewRole(ctx, corpRole, '-corp')
        except Exception as e:
            await ctx.send(f'Failed to create role named {rolePrefix}-corp\n Reason={type(e).__name__} : {e}')

        try:
            await guild.create_role(name=f'{rolePrefix}-officer', color=roleColor, mentionable=True, permissions=discord.Permissions(506846272))
            await ctx.send(f'Created role {rolePrefix}-officer')
            await self.updateChannelWithNewRole(ctx, corpRole, '-officer')
        except Exception as e:
            await ctx.send(f'Failed to create role named {rolePrefix}-officer\n Reason={type(e).__name__} : {e}')

        try:
            wsRole = await guild.create_role(name=f'{rolePrefix}-ws', color=roleColor, mentionable=True, permissions=discord.Permissions(37084225))
            await ctx.send(f'Created role {rolePrefix}-ws')
        except Exception as e:
            await ctx.send(f'Failed to create role named {rolePrefix}-ws\n Reason={type(e).__name__} : {e}')

        for i in range(span):
            currRs = i + minRs
            rsRole = f'{rolePrefix}-rs{currRs}'
            try:
                await guild.create_role(name=rsRole, color=roleColor, mentionable=True, permissions=discord.Permissions(1))
                await ctx.send(f'Created role {rsRole}')
            except Exception as e:
                await ctx.send(f'Failed to create role named {rsRole}\n Reason={type(e).__name__} : {e}')

        return wsRole

    async def createChannels(self, ctx, name: str, channelPrefix: str, wsRole):
        guild = ctx.guild
        try:
            categoryOverwrites = { guild.default_role: discord.PermissionOverwrite(read_messages=False) }
            category = await guild.create_category(name, overwrites=categoryOverwrites)
            try:
                corpRoles = [corpRole for corpRole in guild.roles if "-corp" in corpRole.name]
                channelOverwrites = { key: discord.PermissionOverwrite(read_messages=True) for key in corpRoles }
                channelOverwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=False)
                await guild.create_text_channel(f'{channelPrefix}-general', category=category, overwrites=channelOverwrites)
            except Exception as e:
                await ctx.send(f'Failed to create channel named {channelPrefix}-general\n Reason={type(e).__name__} : {e}')
            try:
                channelOverwrites = { wsRole: discord.PermissionOverwrite(read_messages=True), guild.default_role: discord.PermissionOverwrite(read_messages=False) }
                await guild.create_text_channel(f'{channelPrefix}-ws', category=category, overwrites=channelOverwrites)
            except Exception as e:
                await ctx.send(f'Failed to create channel named {channelPrefix}-ws\n Reason={type(e).__name__} : {e}')
        except Exception as e:
            await ctx.send(f'Failed to create category for {name}\n Reason={type(e).__name__} : {e}')

    @commands.has_any_role('Admin')
    @corp.command()
    async def create(self, ctx, name: str, channelPrefix: str, rolePrefix: str, roleColor: discord.Color, minRs: int, maxRs: int):
        if self.rsLevelWithinRange(minRs):
            await ctx.send(f'Min RS Level ({minRs}) is not within range [1, 10]')
        elif self.rsLevelWithinRange(maxRs):
            await ctx.send(f'Max RS Level ({maxRs}) is not within range [1, 10]')
        elif minRs > maxRs:
            await ctx.send(f'Min RS Level ({minRs}) is Greater Than Max RS Level ({maxRs})')
        else:
            wsRole = await self.createRoles(ctx, rolePrefix, roleColor, minRs, maxRs)
            await self.createChannels(ctx, name, channelPrefix, wsRole)

    @commands.has_any_role('Admin')
    @corp.command()
    async def remove(self, ctx, name: str, rolePrefix: str):
        guild = ctx.guild
        roles = list(guild.roles)
        roles.remove(guild.default_role)
        while len(roles) > 0:
            role = roles.pop()
            if rolePrefix in role.name:
                await ctx.send(f'Removing role: {role}')
                await role.delete()

        categories = list(guild.categories)
        while len(categories) > 0:
            category = categories.pop()
            if category.name == name:
                channels = list(category.channels)
                while len(channels) > 0:
                    channel = channels.pop()
                    await channel.delete()
                await category.delete()

    async def _assignUser(self, ctx, member: discord.Member, corpPrefix: str, *rsLevels: int):
        guild = ctx.guild
        guildRoles = guild.roles
        corpRoles = [role for role in guildRoles if role.name == f'{corpPrefix}-corp' or role.name == f'{corpPrefix}-ws']
        guildRsRoles = [role for role in guildRoles if f'{corpPrefix}-rs' in role.name or f'pub-rs' in role.name]
        rsRoles = [role for role in guildRsRoles for i in rsLevels if role.name == f'{corpPrefix}-rs{i}' or role.name == f'pub-rs{i}']
        corpRoles += rsRoles

        await member.add_roles(*corpRoles, atomic=True)
        await ctx.send(f'Added {member} to {corpRoles}')

    @commands.has_any_role('Admin', 'Officer')
    @corp.command()
    async def inductUser(self, ctx, member: discord.Member, nickname: str, corpPrefix: str, *rsLevels: int):
        await member.edit(nick=nickname)
        await self._assignUser(ctx, member, corpPrefix, *rsLevels)

    @commands.has_any_role('Admin', 'Officer')
    @corp.command()
    async def assignUser(self, ctx, member: discord.Member, corpPrefix: str, *rsLevels: int):
        await self._assignUser(ctx, member, corpPrefix, *rsLevels)

    @commands.has_any_role('Admin', 'Officer')
    @corp.command()
    async def removeUser(self, ctx, member: discord.Member, corpPrefix: str):
        rolesToRemove = [role for role in member.roles if corpPrefix in role.name or 'pub-rs' in role.name]
        await member.remove_roles(*rolesToRemove, atomic=True)
        await ctx.send(f'Removed {member} from {rolesToRemove}')


    @commands.has_any_role('Admin', 'Officer')
    @corp.command()
    async def moveUser(self, ctx, member: discord.Member, oldCorpPrefix: str, newCorpPrefix: str):
        rolesToRemove = [role for role in member.roles if oldCorpPrefix in role.name]
        roleSuffixes = [role.name.replace(f'{oldCorpPrefix}-', "") for role in rolesToRemove]
        rolesToAdd = [role for role in ctx.guild.roles for roleSuffix in roleSuffixes if role.name == f'{newCorpPrefix}-{roleSuffix}']
        await member.remove_roles(*rolesToRemove, atomic=True)
        await ctx.send(f'Removed {member} from {rolesToRemove}')
        await member.add_roles(*rolesToAdd, atomic=True)
        await ctx.send(f'Added {member} to {rolesToAdd}')
        


def setup(bot):
    bot.add_cog(CorpCommands(bot))
