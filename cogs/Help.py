from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from nextcord.ui import Select
from Lib.sherd import *
import asyncio
import os
from Lib.fun import *

repeat = False

cogs = {}
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):  # Limit the number of options
        cog_name = filename[:-3]

class select(ui.View):
    def __init__(self):
        super().__init__()
        
        options = []
        global cogs
        for filename in cogs:
            if len(options) < 25:  # Limit the number of options
                options.append(SelectOption(label=filename, value=f"Select_{filename}"))

        self.select = Select(options=options, placeholder="Select a cog...")
        self.add_item(self.select)

    @nextcord.ui.select(placeholder="Select a cog...")
    async def select_callback(self, select: nextcord.ui.Select, ctx: nextcord.Interaction):
        selected_cog = select.values[0]  # Assuming single selection
        await ctx.response.send_message(f"You selected: {selected_cog.split('_')[1]}")

class help(commands.Cog):
    def __init__(self, client:Client):
        self.client = client
    
    # @slash_command(name="help")
    # async def helper(self,ctx:init):
    #     hel ="""
    #         - Setups
    #         > ```/setup_tickt <LOG_CHANNEL> <TICKET_CREATE_CATEGORY>```
    #         > This command will make a ticket channel for you (More Features Will Added!)
    #         > ```/setup_bettervc <CATEGORY>```
    #         > This will make a Temp Voice Chats Works Only With Invite! (More Features Will Added!)
    #         > ```/setup_bettergroups <CATEGORY>```
    #         > This Will make anyone can make Groups INSIDE your server! (and he can change the permissions in his group / Channel)
    #         > ```/setup_logs <TEXT_LOG_CHANNEL> <VOICE_LOG_CHANNEL> <SERVER_LOG_CHANNEL> <MEMBERS_LOG_CHANNEL> <ROLES_LOG_CHANNEL> <INVITE_LOG_CHANNEL>```
    #         > This will send you anything happend in your server from changes and deleted message or edited message!
    #         I am too lazy to continue (=
    #     """
    #     await ctx.send(hel,ephemeral=True)
    @client.slash_command(name="help", description="List All Commands")
    async def help(self,ctx:init):
        await ctx.response.defer(ephemeral=True)
        slas = self.client.get_application_command(2342342234)
        commands = self.client.get_application_commands()
        #slas.parent_cog
        #{
        #    "Cog":[
        #        [
        #            "name",
        #            "dec"
        #        ],
        #    ]
        #}
        for command in commands:
            for i in cogs:
                if i in str(command.parent_cog):
                    cogs[i].append([command.name,command.description,[option for option in command.options]])
                    break
        await ctx.channel.send(f"```js\n{cogs}```")
        veiw = select()
        await ctx.send("Hi",view=veiw)
        

    @slash_command(name="console")
    async def console(self,ctx:init,command:str,boolean:bool = False,value1=None | str | int | bool,value2=None | str | int):
        await check_owner_persmsion(ctx)
        await ctx.send("wait!")
        if command == "servers":
            sercers = "```"
            temp = 0
            for i in ctx.client.guilds:
                temp+=1
                sercers += f"\n{temp}- {i.id:<20} {i.name:<50} {i.member_count}"
            sercers +=f"\n\nThe Bot Joined in {temp} Servers!```"
            await ctx.channel.send(sercers)
        elif command == "leave":
            dsd= self.client.get_guild(int(value1))
            await dsd.leave()
        elif command == "repeat":
            global repeat
            repeat= boolean
            await ctx.channel.send("OK!")
        elif command == "cls":
            clear()
        elif command == "invite":
            dsd= self.client.get_guild(int(value1))
            await ctx.send(str(await dsd.invites()))
            """Don't Worry It was For testing! (no for real)

        elif (command == "de") and(boolean == True):
            haha = ctx.guild.channels
            roles = ctx.guild.roles
            for i in haha:
                await i.delete()
            for i in roles:
                if (i.is_bot_managed() == True) or (i.is_default() == True):
                    continue
                await i.delete()
            """

            
    @commands.Cog.listener()
    async def on_message(self, message:Message):
        global repeat
        if (repeat == True) and (await check_owner_persmsion_message(message)):
            await message.delete()
            await message.channel.send(message.content)
        
        
        
        
    


def setup(client):
    client.add_cog(help(client))