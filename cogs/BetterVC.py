from nextcord import *
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ext.commands import MissingPermissions
from nextcord import Interaction as init
from nextcord import ui
from Lib.sherd import *

class vc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voices = []

    @slash_command(name="setup_bettervc")
    async def cree(self, ctx: init, category: CategoryChannel):
        await check_persmsion(ctx,administrator=True)
        guild = ctx.guild
        catid = category.id
        voice_channel = await guild.create_voice_channel('➕Create Channel', category=category)

        voiceid = voice_channel.id
        data = {
            "DEFAULT":{
                "makechannel":voiceid,
                "cat":catid
            },
            "CREATED":self.voices
        }
        Data().save(ctx.guild.id,"BetterVC",data)
        await ctx.response.send_message(f"Channel Created 👍\n",ephemeral=True)
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data=Data().load(member.guild.id,"BetterVC")
        if data == None:
            return
        channel_id = data['DEFAULT']['makechannel']
        catid = data['DEFAULT']['cat']
        cat = member.guild.get_channel(catid)
        strlist = data['CREATED']
        self.voices = strlist
        if after.channel is not None and after.channel.id == channel_id:
            guild = member.guild
            voice_channel = await guild.create_voice_channel(f'{member.display_name}', category=cat)
            voiceid = voice_channel.id
            self.voices.append(voiceid)
            Data().save(member.guild.id,"BetterVC",data)
            channeld = member.guild.get_channel(voiceid)
            await member.move_to(channeld)
            overwrite = PermissionOverwrite()
            overwrite.connect = True
            await voice_channel.set_permissions(member, overwrite=overwrite)
            everyone_role = guild.default_role
            overwrite = PermissionOverwrite()
            overwrite.connect = False
            overwrite.view_channel = True
            await channeld.set_permissions(everyone_role, overwrite=overwrite)
        if channel is not None and after.channel is None:
            # A member left a voice channel
            for i in self.voices:
                try:
                    int(i)
                except ValueError:
                    continue
                if int(i) == int(before.channel.id):
                    if before.channel.members == []:
                        await before.channel.delete()
                        self.voices.remove(i)
                        Data().save(member.guild.id,"BetterVC",data)
    @user_command(name="Party: Invite")                
    async def inviteee(self,ctx:init,user:Member):
        member = ctx.guild.get_member(ctx.user.id)
        try:
            voice_state = member.voice
            voice_channel = voice_state.channel
        except:
            await ctx.response.send_message(f"<@{ctx.user.id}> You Are Not In Channel",ephemeral=True)
            return

        
        overwrite = PermissionOverwrite()
        overwrite.connect = True
        await voice_channel.set_permissions(user, overwrite=overwrite)
        await user.send(f"Come Join Us <@{user.id}>! We Are In <#{voice_channel.id}>\nSent By<@{ctx.user.id}>")
        await ctx.response.send_message(f"<@{ctx.user.id}> You Invited {user.display_name}",ephemeral=True)
        pass
    @user_command(name="Party: Kick")                
    async def kickkd(self,ctx:init,user:Member):
        member = ctx.guild.get_member(ctx.user.id)
        member2 = ctx.guild.get_member(user.id)
        try:
            voice_state = member.voice
            voice_channel = voice_state.channel
        except:
            await ctx.response.send_message(f"<@{ctx.user.id}> You Are Not In Channel",ephemeral=True)
            return
        try:
            voice_state2 = member2.voice
            voice_channel2 = voice_state2.channel
        except:
            await ctx.response.send_message(f"{user.name} Is Not In Channel",ephemeral=True)
        if (voice_channel == voice_channel2) and (member.voice.channel.name == ctx.user.name):
            overwrite = PermissionOverwrite()
            overwrite.connect = False
            await voice_channel.set_permissions(user, overwrite=overwrite)
            await user.disconnect()
            await user.send(f"<@{user.id}>You Kicked By <@{ctx.user.id}> \nFrom <#{voice_channel.id}>")
            await ctx.response.send_message(f"<@{ctx.user.id}> You Kicked {user.name}",ephemeral=True)
        else:
            await ctx.response.send_message(f"{user.name} Not With You",ephemeral=True)
        
    


def setup(client):
    client.add_cog(vc(client))