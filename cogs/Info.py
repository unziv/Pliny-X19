from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from nextcord.ext.commands import has_permissions
from Lib.sherd import *
import os

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command()
    async def server_info(self,interaction:init):
        name = str(interaction.guild.name)
        des = str(interaction.guild.description)
        idd = str(interaction.guild.id)
        region = str(interaction.guild.region)
        mebercount = str(interaction.guild.member_count)
        icon = str(interaction.guild.icon)
    
        whyyyy = Embed(
            title=name + " Server Info",
            description=des,
            color=0x31F9FF
        )
        whyyyy.set_thumbnail(url=icon)
        whyyyy.add_field(name="🆔Id", value=idd,inline=True)
        whyyyy.add_field(name="👑Owner", value=f"{interaction.guild.owner.mention}",inline=True)
        whyyyy.add_field(name="👥Members", value=mebercount,inline=True)
        whyyyy.add_field(name=f"💬Channels ({len(interaction.guild.channels)})",value=f"**{len(interaction.guild.text_channels)}** Text|**{len(interaction.guild.voice_channels)}** Voice")
        whyyyy.add_field(name="🌍Region", value=region,inline=True)
        whyyyy.add_field(name="🔐Roles",value=len(interaction.guild.roles))
        await interaction.send(embed=whyyyy)



def setup(client):
    client.add_cog(info(client))