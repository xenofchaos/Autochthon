import discord

class ServerEvents:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        guild = member.guild
        defaultChannel = guild.system_channel
        admin = None
        officer = None
        for role in guild.roles:
            if role.name == 'Admin':
                admin = role
            elif role.name == 'Officer':
                officer = role

        await defaultChannel.send(f'Welcome {member.mention}!\nPlease submit your in-game name, corp, and preferred RS levels for processing.\nAn {admin.mention} or {officer.mention} will be with you shortly.')

    async def on_member_remove(self, member):
        guild = member.guild
        defaultChannel = guild.system_channel
        await defaultChannel.send(f'RIP {member.name}. You might be missed.')

def setup(bot):
    bot.add_cog(ServerEvents(bot))
