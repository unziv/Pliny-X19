from nextcord import *
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ext.commands import MissingPermissions
from nextcord import Interaction as init
from Lib.sherd import *

class Group(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="setup_bettergroups")
    async def crea(self, ctx: init, category: CategoryChannel):
        await check_persmsion(ctx,administrator=True)
        guild = ctx.guild
        catid = category.id
        voice_channel = await guild.create_voice_channel('➕Create Group', category=category)

        voiceid = voice_channel.id
        data ={"makechannel":voiceid,"cat":catid}
        Data().save(ctx.guild.id,"BetterGP",data)
        await ctx.response.send_message(f"Channel Created 👍",ephemeral=True)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data= Data().load(member.guild.id,"BetterGP")
        if Data().check(member.guild.id,"BetterGP") == False:return
        
        channel_id = data["makechannel"]
        catid = data["cat"]
        cat = member.guild.get_channel(catid)
        if after.channel is not None and after.channel.id == channel_id:
            guild = member.guild
            voice_channel = await guild.create_text_channel(f'{member.display_name}', category=cat)
            everyone_role = guild.default_role
            overwrite = PermissionOverwrite()
            overwrite.view_channel = False
            await voice_channel.set_permissions(everyone_role, overwrite=overwrite)
            overwrite.view_channel = True
            overwrite.manage_channels = True
            overwrite.manage_permissions = True
            overwrite.send_messages = True
            overwrite.embed_links = True
            overwrite.attach_files = True
            overwrite.add_reactions = True
            overwrite.manage_messages = True
            overwrite.use_slash_commands = False
            await voice_channel.set_permissions(member, overwrite=overwrite)
            voice_channeldaw = member.voice.channel
            await member.disconnect()
        

def setup(client):
    client.add_cog(Group(client))