from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import requests
import os
import json
import random

class CustomView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item = ui.Button(style=ButtonStyle.green, label="Add Item")

    @ui.button(label='➕')
    async def on_button_click(self, button: ui.Button, ctx: Interaction):
        guild = ctx.guild
        
        path = f"data/between/servers/{guild.id}"
        pathed = f"data/between/rooms.json"
        with open(f"{path}/data.json") as f:
            data = json.loads(f.read())
        try:
            with open(pathed) as f:
                rooms = dict(json.loads(f.read()))
        except:
            with open(pathed,"w") as f:
                f.write(json.dumps({}))
                rooms = {}
        room_code=create_random_id(data=rooms)
        catev = guild.get_channel(data["category"])
        created_room = await catev.create_text_channel(name=f"{room_code}") 
        room = {
            room_code:{
                "with"   :None,
                "channel":catev.id,
                "members": [
                    ctx.user.id
                ]
            }
        }
        rooms.update(room)
        



class between(commands.Cog):
    def __init__(self, client:Client):
        self.client = client

    async def create_or_update_webhook(self,channel_id,name,avatar_url):
        channel = self.client.get_channel(channel_id)
        webhook = await channel.create_webhook(name=name)

        # Download the avatar image from the URL
        avatar_response = requests.get(avatar_url)
        avatar_data = avatar_response.content

        # Update the webhook's avatar
        await webhook.edit(avatar=avatar_data)
        return webhook

    @slash_command(name="between_start",description="Start a Random Conversation")
    async def between_start(self,ctx:init):
        await check_owner_persmsion(ctx)
        await ctx.send("this will take sometime..")
        webhook = await self.create_or_update_webhook(ctx.channel_id,ctx.user.name,ctx.user.avatar.url)
        await webhook.send("Hi")
        await webhook.delete()
    
    @slash_command(name="setup_between",description="This is like Omgel.tv But in DISCORD!")
    async def setup_between(self,ctx:init):
        await check_persmsion(ctx,administrator=True)
        path = f"data/between/servers/{ctx.guild_id}"
        os.makedirs(path,exist_ok=True)
        await ctx.send("Wait..",ephemeral=True)
        embed = Embed(title="Between",
        description="This Is like Omegel.tv But in Disocrd!\ndo you want to give it a try?",
        color=0x420364)
        view = CustomView()
        message = await ctx.channel.send(embed=embed,view=view)
        data = {
            "channel" :ctx.channel_id,
            "category":ctx.channel.category_id,
            "message" :message.id
        }
        with open(f"{path}/data.json","w") as f:
            f.write(json.dumps(data))




def setup(client):
    client.add_cog(between(client))