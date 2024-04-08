from nextcord import *
import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import os
import json
import requests


class cloning(commands.Cog):
    def __init__(self, client:Client):
        self.client = client
    
    @slash_command(name="clone",description="Clone Entire Category")
    async def clone(self,ctx:init,category:CategoryChannel, replace_name:str = None):
        await check_persmsion(ctx,administrator=True)
        guild = ctx.guild
        if replace_name == None:replace_name = category.name
        channels = category.channels
        cate = await category.clone(name=replace_name)
        for channel in channels:
            if channel.type == ChannelType.text:
                channel = await cate.create_text_channel(channel.name)
                channel.topic = channel.topic
            elif channel.type == ChannelType.voice:
                channel = await cate.create_voice_channel(channel.name)
            elif channel.type == ChannelType.stage_voice:
                channel = await cate.create_stage_channel(channel.name)
            elif channel.type == ChannelType.forum_channel:
                channel = await cate.create_forum_channel(channel.name)
            else:
                await ctx.channel.send(f"{channel.name} is not supported")
        else:
            await ctx.send(f"{category.name} has been cloned to {cate.name}!")
            


def setup(client):
    client.add_cog(cloning(client))