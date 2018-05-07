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

        await defaultChannel.send(f'Welcome {member.mention}!\nAn {admin.mention} or {officer.mention} will be with you shortly. (Assuming any of them are sober or give two shits)')

    async def on_member_remove(self, member):
        guild = member.guild
        defaultChannel = guild.system_channel
        await defaultChannel.send(f'Goodbye and good riddance {member.name}. You might be missed.')

def setup(bot):
    bot.add_cog(ServerEvents(bot))
