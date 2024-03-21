from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import json
import os
import ast
import random

version = 1.2

async def excport(ctx:init,channel_id=None):
    if channel_id == None:
        channel_id = ctx.channel.id
        await ctx.send(f"Wait! This will take some time.")
    data = {
        "version": version,
        "channels":{
            "Category":{},
            "Voice"   :[],
            "Channels":[]
        },
        "roles"   :[],
        "bot_name":[]
    }
    for i in ctx.guild.channels:
        if str(i.type) == "category":
            data["channels"]["Category"].update({i.id:i.name})
        elif str(i.type) == "voice":
            data["channels"]["Voice"].append([i.name,i.category_id])
        else:
            try:
                data["channels"]["Channels"].append([i.name,i.category_id,i.topic])
            except ApplicationInvokeError:
                data["channels"]["Channels"].append([i.name,i.category_id,None])
    for i in reversed(ctx.guild.roles):
        data["roles"].append([i.name,i.color.value,i.permissions.value])
    for i in ctx.guild.bots:
        data["bot_name"].append(i.display_name)
    os.makedirs(f"temp/{ctx.guild_id}",exist_ok=True)
    with open(f"temp/{ctx.guild_id}/backup.json", 'w', encoding='utf-8') as f:
        json.dump(data,f,indent=2)
    await ctx.channel.send(file=File(f"temp/{ctx.guild_id}/backup.json"))
    os.remove(f"temp/{ctx.guild_id}/backup.json")
    os.removedirs(f"temp/{ctx.guild_id}")


class ida(ui.Modal):
    def __init__(self):
        super().__init__("Backup",timeout=None)
        self.Title_input = ui.TextInput(label='The Code',
                                        placeholder="Title",min_length=2,max_length=50,required=True)
        self.add_item(self.Title_input)
    #async def callback(self, ctx: init) -> None:


class CustomView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="➕", style= ButtonStyle.green)
    async def on_buttonP_click(self, button: Button, ctx: init):
        view = ida()
        await ctx.response.send_modal(modal=view)

class backup(commands.Cog):
    def __init__(self, client:Client):
        self.client = client
    

    @slash_command(name="export",description="this will export Roles, Channels, Bots Names and more!")
    async def export(self,ctx:init):
        await check_persmsion(ctx,administrator=True)
        await excport(ctx)
        

    @slash_command(name="import",description="This will import Roles, Channels, Bots Names and more!")
    async def imported(self,ctx:init,file:Attachment):
        await check_persmsion(ctx,administrator=True)
        # path= f"temp/messages/{ctx.id}"
        # os.makedirs(path)
        # with open(f"{path}/temp","w", encoding='utf-8') as f:
        #     data = str(await file.read())
        #     f.write(data)
        # with open(f"{path}/temp", 'r', encoding='utf-8') as f:
        #     temp = binary(f.read())
        #     print(temp)
        #     temp = temp.encode('utf-8').decode('unicode_escape')
        #     data = dict(json.loads(temp))
        # os.remove(f"{path}/temp")
        # os.removedirs(path)
        temp = await file.read()
        # temp = temp.encode('utf-8').decode('unicode_escape')
        data = dict(json.loads(temp))
        if data.get("version") == version:
            await ctx.send("Okie, It will take some Time to Import Everything")
        else:
            await ctx.send("""
                           ⚠️The Backup Version is Outdated⚠️
    and we will import it for you, BUT
    If it didn't work do a new backup!
                            """)
        
        temp = {}
        for i in data["channels"]["Category"]:
            haha = await ctx.guild.create_category(data["channels"]["Category"][i])
            temp.update({i:haha})
        for i in data["channels"]["Voice"]:
            gg = None
            if i[1] != None:
                for j in temp:
                    if str(j) == str(i[1]):
                        gg = j
            await ctx.guild.create_voice_channel(i[0],category=temp.get(gg))
        for i in data["channels"]["Channels"]:
            gg = None
            if i[1] != None:
                for j in temp:
                    if j == str(i[1]):
                        gg = j
            await ctx.guild.create_text_channel(i[0],category=temp.get(gg),topic=i[2])
        for i in data["roles"]:
            if i[0] == "@everyone":
                await ctx.guild.default_role.edit(permissions=Permissions(i[2]))
                continue
            await ctx.guild.create_role(name=i[0],color=Color(i[1]),permissions=Permissions(i[2]))
        chasss = await ctx.guild.create_text_channel("more-info")
        names = "Bots Names:\n"
        for i in data["bot_name"]:
            names += i +"\n"
        await chasss.send(names)
        await chasss.send("Finished Everything")

    @slash_command(name="auto_export",description="this will enable auto exporting")
    async def auto_export(self,ctx:init,boolean:bool):
        await check_persmsion(ctx,administrator=True)
        guilded = Guild(await self.client.get_guild(1207614991553789993))
        cate = CategoryChannel(await guilded.get_channel(1207615645030809600))
        channele = await cate.create_text_channel(ctx.guild_id)
        channele.edit(topic=ctx.guild.name)
        path = f"backups servers/free/{ctx.guild.id}"
        if boolean == False:
            os.remove(f"{path}/data.json")
            os.removedirs(path)
            return
        code = random.randint(11111111111111111111,99999999999999999999)
        os.makedirs(path,exist_ok=True)
        data = {"channel":channele.id,"code":code}
        with open(f"{path}/data.json","w") as f:
            f.write(json.dumps(data))

        await ctx.send(f"The Code Is:```{code}```Enter The server And go to Enter a Code Channel\nhttps://discord.gg/aCyRmxGcma\n\nAnd DON'T GIVE ANYONE THAT CODE!")

    @slash_command(name="setup_owner_thingy")
    async def setup_owner_thingy(self,ctx:init):
        await check_owner_persmsion(ctx)
        guild = ctx.guild
        whyyyy = Embed(
            title="Enter a Code",
            description="To Enter a Code react with 📃",
            color=0xff0000
        )
        message = await ctx.channel.send(embed=whyyyy)
        view = CustomView()
        await message.edit(view=view)

        data = ({"makechannel":message.channel.id,
                              "message_id":message.id})
            
        with open("server/auto.json", "w", encoding='utf-8') as json_file:
            json_file.write(json.dumps(data,indent=4))
        await ctx.response.send_message(f"Message Sended 👍",ephemeral=True)

        await ctx.send(f"Hello !")

        

        
        

        

    


def setup(client):
    client.add_cog(backup(client))