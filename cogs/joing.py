from nextcord import *
import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import os
import json

class joining(commands.Cog):
    def __init__(self, client:Client):
        self.client = client
    """
    Type You Code Here
    @commands.Cog.listener()
    """


def setup(client):
    client.add_cog(joining(client))