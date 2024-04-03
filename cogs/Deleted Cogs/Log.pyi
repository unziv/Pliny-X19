from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import os
import json
import datetime

async def read(server_id):
        folder= f"data/Servers Logs/{server_id}"
        try:
            with open(f"{folder}/data.json") as f:
                    return json.load(f)
        except FileNotFoundError:
            raise Exception("no")
async def timefor():
        now = datetime.datetime.utcnow()
        now = now + datetime.timedelta(hours=3)
        timestamp_code = f'<t:{int(now.timestamp())}:R>'
        return timestamp_code

class log(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    



    # @slash_command(name="setup_logs")
    async def commandName(self, ctx:init,text_logs_channel:TextChannel,voice_logs_channel:TextChannel
                          ,server_logs_channel:TextChannel,members_logs_channel:TextChannel,roles_logs_channel:TextChannel
                          ,invite_logs_channel:TextChannel):
        folder= f"data/Servers Logs/{ctx.guild.id}"
        data = {
            "text"    : text_logs_channel.id,
            "voice"   : voice_logs_channel.id,
            "server"  : server_logs_channel.id,
            "members" : members_logs_channel.id,
            "roles"   : roles_logs_channel.id,
            "invite"  : invite_logs_channel.id
        }
        os.makedirs(folder, exist_ok=True)
        with open(f"{folder}/data.json","w") as f:
            json.dump(data,f,indent=4)
        await ctx.send("Done!", ephemeral=True)
        await text_logs_channel.send("This is the Text Logs Channel")
        await voice_logs_channel.send("This is the Voice Logs Channel")
        await server_logs_channel.send("This is the Server Logs Channel")
        await members_logs_channel.send("This is the Members Logs Channel")
        await roles_logs_channel.send("This is the Roles Logs Channel")
        await invite_logs_channel.send("This is the Invite Logs Channel")


    @commands.Cog.listener()
    async def on_message_edit(self, before:Message, after:Message):
        if before.author.bot:
             return
        guild = before.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channel = guild.get_channel(data["text"])
        embed = Embed(title="**Message Edited**",
                      description=
f"""
> **Channel: 💬┇** <#{before.channel.id}> ({message.channel.name})
> **Message ID:** [{after.id}]({after.jump_url})
> **Message author:** <@{after.author.id}>
> **Message edited:** {await timefor()}""",
                      color=0xffaa00)
        embed.add_field(name="**Before**",value=before.content)
        embed.add_field(name="**After**",value=after.content)
        await channel.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_message_delete(self, message:Message):
        if message.author.bot:
             return
        guild = message.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channel = guild.get_channel(data["text"])
        embed = Embed(title="**Message Deleted**",
                      description=
f"""
> **Channel: 💬┇** <#{message.channel.id}> ({message.channel.name})
> **Message ID:** [{message.id}]({message.jump_url})
> **Message author:** <@{message.author.id}>
> **Message deleted:** {await timefor()}""",
                      color=0xce3636)
        embed.add_field(name="**Message**",value=message.content)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel:abc.GuildChannel):
        guild = channel.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["server"])
        embed = Embed(title="**Channel Created**",
                      description=
f"""
> **Channel: 🎪┇** <#{channel.id}> ({channel.name})
> **ID:** [{channel.id}]({channel.jump_url})
> **Channel created:** {await timefor()}""",
                      color=0x36ce36)
        await channe.send(embed=embed)         
    

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel:abc.GuildChannel):
        guild = channel.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["server"])
        embed = Embed(title="**Channel Deleted**",
                      description=
f"""
> **Channel: 🎪┇** {channel.name}
> **ID:** {channel.id}
> **Channel deleted:** {await timefor()}""",
                      color=0xce3636)
        await channe.send(embed=embed)  


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before:abc.GuildChannel, after:abc.GuildChannel):
        if before.name.startswith("ticket"):
            return
        if after.name == before.name:
            return
        guild = before.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["server"])
        embed = Embed(title="**Channel Edited**",
                      description=
f"""
> **Channel: 🎪┇** <#{after.id}> ({after.name})
> **ID:** [{after.id}]({after.jump_url})
> **Channel edited:** {await timefor()}""",
                      color=0xffaa00)
        embed.add_field(name="**Name Before**",value=before.name)
        embed.add_field(name="**Name After**",value=after.name)
        await channe.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member:Member):
        guild = member.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["members"])
        embed = Embed(title="**User Joined**",
                      description=
f"""
> **User:** <@{member.id}> ({member.name})
> **ID:** {member.id}
> **Member joined:** {await timefor()}
> **Members:** {member.guild.member_count}""",
                      color=0x36ce36)
        icon = str(member.avatar.url)
        embed.set_thumbnail(icon)
        await channe.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_ban(self, guild:Guild, user:User):
        try: 
            data = await read(guild.id)
        except Exception:
            return
        async for entry in guild.audit_logs(limit=1):
            reasohn = entry.reason
        channe = guild.get_channel(data["members"])
        embed = Embed(title="**User Banned**",
                      description=
f"""
> **User:** <@{user.id}> ({user.name})
> **ID:** {user.id}
> **Member Banned:** {await timefor()}
> **Reason:** {reasohn}
> **Members:** {guild.member_count}""",
                      color=0x4d1414)
        icon = str(user.avatar.url)
        embed.set_thumbnail(icon)
        await channe.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member:Member):
        guild = member.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["members"])
        async for entry in guild.audit_logs(limit=1):
            reasohn = entry.reason
        embed = Embed(title="**User Left**",
                      description=
f"""
> **User:** <@{member.id}> ({member.name})
> **ID:** {member.id}
> **Member left:** {await timefor()}
> **Reason:** {reasohn}
> **Members:** {member.guild.member_count}""",
                      color=0xce3636)
        icon = str(member.avatar.url)
        embed.set_thumbnail(icon)
        await channe.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_unban(self, guild:Guild, user:User):
        try: 
            data = await read(guild.id)
        except Exception:
            return
        async for entry in guild.audit_logs(limit=1):
            reasohn = entry.reason
        channe = guild.get_channel(data["members"])
        embed = Embed(title="**User Unbanned**",
                      description=
f"""
> **User:** <@{user.id}> ({user.name})
> **ID:** {user.id}
> **Member Unbanned:** {await timefor()}
> **Reason:** {reasohn}
> **Members:** {guild.member_count}""",
                      color=0x185200)
        icon = str(user.avatar.url)
        embed.set_thumbnail(icon)
        await channe.send(embed=embed)

    
#    @commands.Cog.listener()
#    async def on_member_update(self, before:Member, after:Member):
#        guild = member.guild
#        try: 
#            data = await read(guild.id)
#        except Exception:
#            return
#        channe = guild.get_channel(data["server"])
#        embed = Embed(title="**User Joined**",
#                      description=
#f"""
#> **User:** <@{member.id}> ({member.name})
#> **ID:** {member.id}
#> **Member updated:** {await timefor()}""",
#                      color=0x36ce36)
#        icon = str(member.avatar.url)
#        embed.set_thumbnail(icon)
#        await channe.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_guild_role_create(self, role:Role):
        guild = role.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["roles"])
        embed = Embed(title="**Role Created**",
                      description=
f"""
> **Role:** {role.mention} ({role.name})
> **ID:** {role.id}
> **Role created:** {await timefor()}""",
                      color=0x36ce36)
        await channe.send(embed=embed)         


    @commands.Cog.listener()
    async def on_guild_role_delete(self, role:Role):
        guild = role.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["roles"])
        embed = Embed(title="**Role Deleted**",
                      description=
f"""
> **Role:** {role.name}
> **ID:** {role.id}
> **Role deleted:** {await timefor()}""",
                      color=0xce3636)
        await channe.send(embed=embed)  


    @commands.Cog.listener()
    async def on_guild_role_update(self, before:abc.GuildChannel, after:abc.GuildChannel):
        if after.name == before.name:
             return
        guild = before.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["roles"])
        embed = Embed(title="**Role Edited**",
                      description=
f"""
> **Role: 🎪┇** {after.mention} ({after.name})
> **ID:** {after.id}
> **Role edited:** {await timefor()}""",
                      color=0xffaa00)
            
        embed.add_field(name="**Name Before**",value=before.name)
        embed.add_field(name="**Name After**",value=after.name)
        await channe.send(embed=embed)


    @commands.Cog.listener()
    async def on_invite_create(self, invite:Invite):
        guild = invite.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["invite"])
        embed = Embed(title="**Invite Created**",
                      description=
f"""
> **User:** {invite.inviter.mention} ({invite.inviter.name})
> **Code:** {invite.code}
> **Expire:** {invite.expires_at}
> **Channel:** {invite.channel.mention} ({invite.channel.name})
> **Max uses:** {invite.max_uses}
> **Invite created:** {await timefor()}""",
                      color=0x36ce36)
        icon = str(invite.inviter.avatar.url)
        embed.set_thumbnail(icon)
        await channe.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite:Invite):
        guild = invite.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["invite"])
        embed = Embed(title="**Invite Deleted**",
                      description=
f"""
> **Code:** {invite.code}
> **Channel:** {invite.channel.mention} ({invite.channel.name})
> **Max uses:** {invite.max_uses}
> **Invite deleted:** {await timefor()}""",
                      color=0xce3636)
        await channe.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member:Member, before:VoiceState, after:VoiceState):
        guild = member.guild
        try: 
            data = await read(guild.id)
        except Exception:
            return
        channe = guild.get_channel(data["voice"])
        if after.channel != None:
            embed = Embed(title="**User Joined Voice Chat**",
                          description=
                            f"""
                            > **User:** <@{member.id}> ({member.name})
                            > **Channel:** {after.channel.mention} ({after.channel.name})
                            > **Users:** {len(after.channel.members)}/{after.channel.user_limit}
                            > **Member joined voice chat:** {await timefor()}""",
                          color=0x36ce36)
            icon = str(member.avatar.url)
            embed.set_thumbnail(icon)
            await channe.send(embed=embed)
        else:
            embed = Embed(title="**User Left Voice Chat**",
              description=
                f"""
                > **User:** <@{member.id}> ({member.name})
                > **Channel:** {before.channel.mention} ({before.channel.name})
                > **Users:** {len(before.channel.members)}/{before.channel.user_limit}
                > **Member Left voice chat:** {await timefor()}""",
              color=0xce3636)
            icon = str(member.avatar.url)
            embed.set_thumbnail(icon)
            await channe.send(embed=embed)

        
         

def setup(client):
    client.add_cog(log(client))