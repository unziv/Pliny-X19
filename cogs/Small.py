from nextcord import * #type: ignore
from nextcord.ext import commands
from Lib.sherd import *
from nextcord import Interaction as init




class small_commands(commands.Cog):
    def __init__(self, client):
        self.client = client



    @slash_command()
    async def embed(self,ctx):
        await check_persmsion(ctx,administrator=True)
        with open ("data/rolesE.txt", encoding='utf-8') as i:
            Roles = str(i.read())
        Rolesu = Embed(
            title="Server Roles",
            description=Roles,color=0xfac61c
            )
        await ctx.response.send_message("Sended",ephemeral=True)
        await ctx.channel.send(embed=Rolesu)
    #End

    #Msg People
    @slash_command(description="Message Member")
    async def msg(self,interaction:Interaction,user:Member,message:str):
        await interaction.response.send_message("Sended",ephemeral=True)
        embed = Embed(title=message,color=0x31F9FF)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.add_field(name=f"",value=f"From <@{interaction.user.id}>")
        await user.send(embed=embed)

    @slash_command(description="Create Embeds")
    async def create(self,interaction:init,title:str,des=str):
        embed = Embed(
            title=title,
            description=des,color=0x31F9FF
        )
        embed.set_author(name=interaction.user.mention, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message("Sended",ephemeral=True)
        await interaction.channel.send(embed=embed)
    @slash_command(name="ping",description="Ping Bot")
    async def ping(self,ctx:init):
        await ctx.response.send_message("Pong",ephemeral=True)
        
def setup(client):
    client.add_cog(small_commands(client))