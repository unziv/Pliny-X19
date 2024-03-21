from nextcord import *
import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import os
import json

class auto_role(commands.Cog):
    def __init__(self, client:Client):
        self.client = client

    @slash_command(name="setup_auto_role",description="Make the members Get a Role when they Enter (Even BOTS!)")
    async def setup_auto_role(self,ctx:init,member_role:Role,bot_role:Role = None):
        await check_persmsion(ctx,administrator=True)
        if bot_role == None:
            idd = None
        else:
            idd = bot_role.id

        Data().save(ctx.guild_id,"Auto role",{
            "member_role":member_role.id,
            "bot_role"   :idd
        })
        await ctx.send("Auto Role Set!")
        
            
    @commands.Cog.listener()
    async def on_member_join(self, member:Member):
        guild = member.guild
        if Data().check(member.guild.id,"Auto role"):
            data = Data().load(member.guild.id,"Auto role")
            if data == None:
                return
            if (member.bot) and (data["bot_role"] != None):
                await member.add_roles(guild.get_role(data["bot_role"]))
            if member.bot == False:
                await member.add_roles(guild.get_role(data["member_role"]))


def setup(client):
    client.add_cog(auto_role(client))