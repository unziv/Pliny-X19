from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
from nextcord.ui import Select
from Lib.sherd import *
import time


class ConfigView(nextcord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.options = options

    async def interaction_check(self, interaction: nextcord.Interaction):
        return interaction.user == self.settings.author

    @nextcord.ui.select(placeholder="Select a setting to change", min_values=1, max_values=1)
    async def dropdown(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
        setting = select.values[0]
        await interaction.response.send_message(f"You selected {setting}.")  # You can handle the selected setting here

class config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="config", description="Edit Config In your server!", guild_ids= [1206654839594156072])
    async def config(self, ctx: init):
        await ctx.response.defer()
        options = [
            SelectOption(label="Auto Role"),
            SelectOption(label="Better Group"),
            SelectOption(label="Cookies"),
            SelectOption(label="Database"),
            SelectOption(label="Log"),
            SelectOption(label="Ticket"),
        ]
        view = ConfigView(options)
        await ctx.send("Please select what setting you want to change:", view=view)

    @commands.Cog.listener()
    async def on_button_click(self, res):
        if res.component.label == "Ticket":
            print("ticket")
            pass
        elif res.component.label == "BetterVC":
            # Do something for BetterVC setting
            pass
        elif res.component.label == "Log":
            # Do something for Log setting
            pass
        elif res.component.label == "Database":
            # Do something for Database setting
            pass
        elif res.component.label == "Cookies":
            # Do something for Cookies setting
            pass
        elif res.component.label == "Boost":
            # Do something for Boost setting
            pass
        elif res.component.label == "Between":
            # Do something for Between setting
            pass
        elif res.component.label == "BetterGroup":
            # Do something for BetterGroup setting
            pass
        elif res.component.label == "Auto Role":
            # Do something for Auto Role setting
            pass

def setup(client):
    client.add_cog(config(client))