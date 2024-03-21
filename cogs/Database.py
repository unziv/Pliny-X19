from nextcord import *
import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction as init
from Lib.sherd import *
import os
import json

import mysql.connector
conn = mysql.connector.connect(
    host="ptfra1.bisecthosting.com",
    user="u85611_OZHFdngB7A",
    password="nBbIU21S=qVt=iQ3Pg!TJh0T",
    database="s85611_messages",
    port=3306
)
cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS Messages (
    id BIGINT PRIMARY KEY,
    guild BIGINT,
    channel BIGINT,
    userid BIGINT,
    username TEXT,
    content TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
"""
cursor.execute(create_table_query)

class database(commands.Cog):
    def __init__(self, client:Client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot == True:
            return
        # Example: Insert data into the table
        insert_query = "INSERT INTO Messages (id, guild, channel, userid, username, content) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (message.id,message.guild.id,message.channel.id,
                message.author.id,message.author.name,message.content)
        cursor.execute(insert_query, data)

        # Commit changes to the database
        conn.commit()


def setup(client):
    client.add_cog(database(client))