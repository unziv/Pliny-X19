from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import json
import datetime
import os

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

class CustomView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="➕", style= ButtonStyle.green)
    async def on_buttonP_click(self, button: Button, ctx: init):
        for i in data["Teams"]:
            for j in data["Teams"][i]["members"]:
                if ctx.user.id == j:
                    await ctx.response.send_message(f"You are In a {i} Team\nYou can't Create A Team",ephemeral=True)
                    return
        view = ida()
        await ctx.response.send_modal(modal=view)


    @ui.button(label="🗑️", style= ButtonStyle.red)
    async def on_button_click(self, button: Button, ctx: init):
        view = sure()
        await ctx.response.send_message("Are You Sure??\n(It Will Delete Everything From Roles To Channels Even Inside Minecraft)",view=view,ephemeral=True)
        

    @ui.button(label="📃", style= ButtonStyle.gray)
    async def on_buttonB_click(self, button: Button, ctx: init):
        for i in data["Teams"]:
            if ctx.user.id == data["Teams"][i]["owner"]:
                global nn
                global dd
                nn=data["Teams"][i]["name"]
                dd=data["Teams"][i]["des"]
                view = chanageee()
                await ctx.response.send_modal(modal=view)
        else:
            await ctx.response.send_message("You Don't Have Team",ephemeral=True)

class boost(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    @slash_command(name="setup_boost")
    async def setup_boost(self,ctx:init,boost_role:Role):
        await check_owner_persmsion()
        ebed = Embed(title="Hi",color=0xa1231a)
        await ctx.send("Sended!",ephemeral=True)
        message = await ctx.channel.send(embed=ebed)
        folder= f"data/Servers Boost/{ctx.guild.id}"
        data = {
            "role"      : boost_role.id,
            "channel"   : message.channel.id,
            "message_id": message.id
            }
        os.makedirs(folder, exist_ok=True)
        with open(f"{folder}/data.json","w") as f:
            json.dump(data,f,indent=4)


def setup(client):
    client.add_cog(boost(client))