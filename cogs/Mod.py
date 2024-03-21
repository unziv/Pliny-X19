from nextcord import *
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord import Interaction
from nextcord import Interaction as init
import os
import datetime
from Lib.sherd import *
import random
import json











@slash_command(name="Name",description="Des")
async def Name(self,ctx:init):
    await ctx.send(f"Hello !")


class mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    #Kick
    async def kick_command(self,ctx:init,user:Member,reason:str =None):
        await check_persmsion(ctx,kick_members=True)
        if await high(ctx,user=member) == False:return
        try:
            await user.kick(reason=reason)
            await ctx.send(f"User {user.mention} has Been Kicked from server ")
        except Forbidden:
            await ctx.send(f"User {user} Is Higher Than The bot")
    @slash_command(name="kick",description="Kick Member")
    async def kick_slash(self,ctx:init,user:Member,reason:str =None):
        await self.kick_command(ctx,user,reason)
    @commands.command(name="kick",description="Kick Member")
    async def kick(self,ctx:commands.Context,user:Member,reason:str =None):
        ctx.user = ctx.author
        await self.kick_command(ctx,user,reason)


    #Ban
    async def ban_command(self,ctx,member:Member,reason:str = None):
        await check_persmsion(ctx,ban_members=True)
        if await high(ctx,user=member) == False:return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"User {member.mention} has Been Baned from the server")
        except Forbidden:
            await ctx.send(f"User {member} Is Higher Than The bot")
    @slash_command(name="ban",description="Ban Member")
    async def ban_slash(self,ctx:init,member:Member,reason:str = None):
        await self.ban_command(ctx,member,reason)
    @commands.command(name="ban",description="Ban Memberes")
    async def ban(self,ctx:commands.Context,member:Member,reason:str = None):
        ctx.user = ctx.author
        await self.ban_command(ctx,member,reason)
    



    async def unban_command(self,ctx,user:Member,reason:str =None):
        await check_persmsion(ctx,ban_members=True)
        try:
            await user.unban(reason=reason)
            await ctx.send(f"User {user.mention} has Been Unbaned from the server")
        except:
            await ctx.send(f"User {user} Isn't Banned")

    @slash_command(name="unban",description="Unban Member")
    async def unban_slash(self,ctx:init,user:Member,reason:str =None):
        await self.unban_command(ctx,user,reason)
    @commands.command(name="unban",description="Unban Member")
    async def unban(self,ctx:commands.Context,user:Member,reason:str =None):
        ctx.user = ctx.author
        await self.unban_command(ctx,user,reason)


    #Timeout
    async def timeout_command(self,ctx,member:Member,minutes:int,reason:str = None):
        await check_persmsion(ctx,moderate_members=True) #moderate_members = Timeout???
        if await high(ctx,user=member) == False:return
        try:
            timeout_duration = datetime.timedelta(minutes=minutes)
            await member.timeout(timeout_duration,reason=reason)
            await ctx.send(f"User {member.mention} has Been Timeout")
        except Forbidden:
            await ctx.send(f"User {member} Is Higher Than The bot")

    @slash_command(name="timeout",description="Timeout Member")
    async def timeout_slash(self,ctx:init,member:Member,minutes:int,reason:str = None):
        await self.timeout_command(ctx,member,minutes,reason) 
    @commands.command(name="timeout",description="Timeout Member")
    async def timeout(self,ctx:commands.Context,member:Member,minutes:int,reason:str = None):
        ctx.user = ctx.author
        await self.timeout_command(ctx,member,minutes,reason)


    # async def warn_command(self,ctx,user:Member,reason:str = None):
    #     await check_persmsion(ctx,moderate_members=True)
    #     await ctx.response.send_message(f"User {member} has Been Warned")
    #     os.makedirs(f"data/servers/{ctx.guild.id}",exist_ok=True)
    #     path = f"data/servers/{ctx.guild.id}/data_warns.json"
    #     data = {}
    #     try:
    #         with open(path, encoding="utf-8") as f:
    #             data = json.loads(f.read())
    #     except FileNotFoundError:
    #         data = {}
    #     Data().update({create_random_id(data):{
    #         "who"   : member.id,
    #         "by"    : ctx.user.id,
    #         "time"  : str(datetime.datetime.now()),
    #         "reason": reason
    #     }})
    #     with open(path, "w", encoding="utf-8") as i:
    #         i.write(json.dumps(data,indent=2))
    
    # @slash_command(name="warn",description="Warn Member")
    # async def warn_slash(self,ctx:init,user:Member,reason:str = None):
    #     await self.warn_command(ctx,user,reason)
    # @commands.command(name="warn",description="Warn Member")
    # async def warn(self,ctx:commands.Context,user:Member,reason:str = None):
    #     ctx.user = ctx.author
    #     await self.warn_command(ctx,user,reason)


    # async def list_member_warns_command(self,ctx:init | commands.Context,user:Member):
    #     await check_persmsion(ctx,moderate_members=True)
        

    # @slash_command(name="list_member_warns",description="List all Member Warns")
    # async def list_member_warns_slash(self,ctx:init,user:Member):
    #     await self.list_member_warns_command(ctx.user)
    # @commands.command(name="list_member_warns",description="List all Member Warns")
    # async def list_member_warns(self,ctx:commands.Context,user:Member):
    #     ctx.user = ctx.author
    #     await self.list_member_warns_command(ctx.user)

            

    async def clear_command(self,ctx:init | commands.Context,amount:int):
        await check_persmsion(ctx,manage_messages=True)
        await ctx.send("Deleting ...")
        await ctx.channel.purge(limit=int(amount) + 2)
    
    @slash_command(name="clear",description="Clear Messages")
    async def clear_slash(self,ctx:init,amount:int):
        await self.clear_command(ctx,amount,)
    @commands.command(name="clear",description="Clear Messages")
    async def clear(self,ctx:commands.Context,amount:int):
        ctx.user = ctx.author
        await self.clear_command(ctx,amount,)





def setup(client):
    client.add_cog(mod(client))