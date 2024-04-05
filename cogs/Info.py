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
    
    # @slash_command(name="rules",description="Send Ready Rules")
    # async def Name(self,ctx:init):
    #     await check_persmsion(ctx,administrator=True)
    #     os.makedirs(f"data/rules/{ctx.guild.id}")
    #     with open("data/rules.txt", encoding='utf-8') as f:
    #         why = Embed(title="قوانين", description=f.read(),color=0x420364)
    #     with open("data/rulesE.txt", encoding='utf-8') as f:
    #         whyE = Embed(title="Rules", description=f.read(),color=0x420364)
    #     with open("data/rulesJ.txt", encoding='utf-8') as f:
    #         whyJ = Embed(title="ルール", description=f.read(),color=0x420364)
    #     messgagee= await ctx.channel.send(embeds=[whyJ,whyE,why])
    #     await ctx.send("Sended!",ephemeral=True)
    #     with open(f"data/rules/{ctx.guild.id}/message","w") as f:
    #         f.write(str(messgagee.id))
    #     with open(f"data/rules/{ctx.guild.id}/channel","w") as f:
    #         f.write(str(messgagee.channel.id))

    @slash_command(name="update_rules",description="Update Ready Rules")
    async def update_rules(self,ctx:init):
        await check_persmsion(ctx,administrator=True)
        os.makedirs(f"data/rules/{ctx.guild.id}")
        with open(f"data/rules/{ctx.guild.id}/message","r") as f:
            idd =int(f.read())
        with open(f"data/rules/{ctx.guild.id}/channel","r") as f:
            idd2 =int(f.read())
        
        with open("data/rules.txt", encoding='utf-8') as f:
            why = Embed(title="قوانين", description=f.read(),color=0x420364)
        with open("data/rulesE.txt", encoding='utf-8') as f:
            whyE = Embed(title="Rules", description=f.read(),color=0x420364)
        with open("data/rulesJ.txt", encoding='utf-8') as f:
            whyJ = Embed(title="ルール", description=f.read(),color=0x420364)
            await ctx.guild.get_channel(idd2).get_partial_message(idd).edit(embeds=[whyJ,whyE,why])
        await ctx.send("Edited!",ephemeral=True)
        





def setup(client):
    client.add_cog(info(client))