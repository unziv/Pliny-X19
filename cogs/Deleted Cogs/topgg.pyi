import topgg

# This example uses topggpy's autopost feature to post guild count to Top.gg every 30 minutes
# as well as the shard count if applicable.

from nextcord import *
import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import os
import json

class topgg(commands.Cog):
    def __init__(self, client:Client):
        self.client = client
        self.dbl_token = "Top.gg token"  # set this to your bot's Top.gg token
        self.client.topggpy = topgg.DBLClient(self.client, dbl_token, autopost=True, post_shard_count=True)


    @client.event
    async def on_autopost_success():
        print(
            f"Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})"
        )



def setup(client):
    client.add_cog(topgg(client))