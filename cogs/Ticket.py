from nextcord import *
from nextcord import CategoryChannel
from nextcord.ext import commands
from nextcord import Interaction as init
from nextcord.ui import button, View
import datetime
import os
import shutil
from Lib.sherd import *




def numbernow(server_id:int):
    data = Data()
    count = Data().load(server_id,"ticket","count")
    if count != None:
        count += 1
    else:
        count = 1
    Data().save(server_id,"ticket",count,"count")
    return count


class afterclose(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.delete_button = ui.Button(style=ButtonStyle.red, label="⛔ Delete")
        self.save_button = ui.Button(style=ButtonStyle.gray, label="📑 Save")

    @ui.button(label='⛔ Delete',style=ButtonStyle.gray)
    async def on_delete_button_click(self, button: ui.Button, ctx: Interaction):
        channel = ctx.channel
        await channel.delete()

    @ui.button(label='📑 Save')
    async def on_save_button_click(self, button: ui.Button, ctx: Interaction):
        data = Data().load(ctx.guild.id,"ticket")
        logID = data['log']
        await ctx.response.send_message(f"Please Wait... it will take long for the attachments\nwe will send to you in <#{logID}>")
        channel = ctx.channel
        filename_prefix = f"data/tickets/{channel.name}"
        messages_filename = f"{filename_prefix}_messages.txt"
        attachments_dirname = f"{filename_prefix}_attachments"
        messages = []
        async for message in channel.history(limit=None):
            messages.append(message)


        with open(messages_filename, "w", encoding="utf-8") as f:
            for message in reversed(messages):
                timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] [{message.author}] {message.content}\n")
                if message.attachments:
                    for attachment in message.attachments:
                        if not os.path.exists(attachments_dirname):
                            os.makedirs(attachments_dirname)
                        url = attachment.url
                        filename = f"{attachments_dirname}/{attachment.filename}"
                        await attachment.save(filename)
        
        log_channel = ctx.guild.get_channel(logID)

        with open(messages_filename, "rb") as f:
            file = File(f)
            await log_channel.send(f"Here is The File From {channel.name}", file=file)
        if os.path.exists(attachments_dirname):
            shutil.make_archive(attachments_dirname, "zip", attachments_dirname)
            with open(f"{attachments_dirname}.zip", "rb") as f:
                file = File(f)
                await log_channel.send(f"Here are the Attachments From {channel.name}", file=file)
        await ctx.channel.send("Done")

        os.remove(messages_filename)
        if os.path.exists(attachments_dirname):
            shutil.rmtree(attachments_dirname)
            os.remove(f"{attachments_dirname}.zip")

    
        






class Close(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item = ui.Button(style=ButtonStyle.red, label="Add Item")

    @ui.button(label='🔒 Close')
    async def on_button_click(self, button: ui.Button, ctx: Interaction):
        data = Data().load(ctx.guild.id,"ticket")
        team_id = data['role']
        embed1=Embed(description=f"Closing By <@{ctx.user.id}>",
                    color=0xfbfe32)
        await ctx.response.send_message(embed=embed1)
        ch = ctx.channel
        overwrite = PermissionOverwrite()
        overwrite.view_channel = False
        allowed_users = [u for u in ch.members if (not u.bot) and (u.top_role.permissions.administrator == False) and (u.get_role(team_id) == None)]
        embed=Embed(description=f"Closed By <@{ctx.user.id}>",
                    color=0xfbfe32)
        for i in allowed_users:
            await ch.set_permissions(i, overwrite=overwrite)
        msg = await ctx.channel.send(embed=embed)
        view = afterclose()
        await msg.edit(view=view)



class CustomView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item = ui.Button(style=ButtonStyle.gray, label="Add Item")

    @ui.button(label='📩')
    async def on_button_click(self, button: ui.Button, ctx: Interaction):
        guild = ctx.guild
        data = dict(Data().load(ctx.guild.id,"ticket"))
        forbidden_id = data.get("forbidden")
        try:
            forbidden = ctx.user.get_role(forbidden_id)
        except:
            pass

        if (forbidden_id == None) or (forbidden == None):
            Create = data['create']
            team_id = data['role']
            if Create != 0:
                Create_Channel = guild.get_channel(Create)
                channell = await Create_Channel.create_text_channel('ticket-'+ str(numbernow(ctx.guild.id)))
            else:
                channell = await guild.create_text_channel('ticket-'+ str(numbernow(ctx.guild.id)))
            team = guild.get_role(team_id)
            embed=Embed(description="Support will be with you shortly.\n"+
                        "To close this ticket react with 🔒",
                        color=0x1ec45b)
            everyone_role = guild.default_role
            overwrite = PermissionOverwrite()
            overwrite.view_channel = False
            await channell.set_permissions(everyone_role, overwrite=overwrite)
            overwrite = PermissionOverwrite()
            overwrite.view_channel = True
            overwrite.send_messages = True
            overwrite.attach_files = True
            await channell.set_permissions(ctx.user, overwrite=overwrite)
            await ctx.send(f"Ticket Opened! <#{channell.id}>",ephemeral=True)
            if guild.id != 1206654839594156072:
                msg = await channell.send(f"<@{ctx.user.id}> Welcome\n||{team.mention}||", embed=embed)
            else:
                msg = await channell.send(f"<@{ctx.user.id}> Welcome\n||{team.mention}<@{829806976702873621}>||", embed=embed)
            
            view = Close()
            await msg.edit(view=view)
        else:
            await ctx.send(f"You are {forbidden.mention} so You cannot create a Ticket",ephemeral=True)



class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @slash_command(name="setup_tickt",description="Setup Ticket")
    async def send(self,ctx:init,log_channel:TextChannel,ticket_team:Role,forbidden_role:Role = None,ticket_create_category:CategoryChannel = None):
        await check_persmsion(ctx,administrator=True)
        try: 
            int(ticket_create_category.id)
        except:
            ticket_create_category.id = 0
        whyyyy = Embed(
            title="Ticket",
            description="To create a ticket react with 📩",
            color=0xfb8d1a
        )
        message = await ctx.channel.send(embed=whyyyy)
        view = CustomView()
        await message.edit(view=view)
        if forbidden_role == None:forbidden_role_id=None
        elif forbidden_role != None:forbidden_role_id=forbidden_role.id
        data = {"message"  :message.id,
                "channel"  :message.channel.id,
                "role"     :ticket_team.id,
                "forbidden":forbidden_role_id,
                "log"      :log_channel.id,
                "create"   :ticket_create_category.id}
        Data().save(ctx.guild.id,"ticket",data)
        if Data().check_global("ticket","servers"):
            srvID = list(Data().load_global("ticket","servers"))
            if ctx.guild.id not in srvID:
                srvID.append(ctx.guild.id)
                Data().save_global("ticket",srvID,"servers")
        else:
            print("Creating.. Please Wait")
            Data().save_global("ticket",[ctx.guild.id],"servers")
        await ctx.response.send_message(f"Message Sended👍",ephemeral=True)
    @commands.Cog.listener()
    async def on_ready(self):
        view = CustomView()
        
        if Data().check_global("ticket","servers") ==False:return
        srvID = list(Data().load_global("ticket","servers"))
        for i in srvID:
            print(f"Checking {i}")
            data = Data().load(i,"ticket")
            chnlID = data['channel']
            msgID = data["message"]
            channel = self.client.get_channel(chnlID)
            if channel is None:
                srvID.pop(i)
                Data().save_global("ticket",srvID,"servers")
                continue
            try:
                message = await channel.fetch_message(msgID)
            except NotFound:
                srvID.pop(i)
                Data().save_global("ticket",srvID,"servers")
                print(f"Unable to find message with ID {msgID} in channel {channel}")
                continue
            await message.edit(view=view)
    
def setup(client):
    client.add_cog(Ticket(client))