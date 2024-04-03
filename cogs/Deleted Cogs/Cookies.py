from nextcord import *
from nextcord.ext import commands
from nextcord import Interaction as init
import random
import threading
import time
import os
import datetime
import json
import locale

def chance(num:int):
        rn = random.random()
        num /= 100
        if rn < num:
          return True
        else:
          return False

class cookies(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.defult_new = {
            "max":5000,
            "now":0,
            "jar":0,
            "created":0
        }
    
    def expire(self,id:int,times:int):
        with open(f"data/users/{id}.claimc","w") as i:
            i.write("")
        mintus = times * 60
        time.sleep(mintus)
        if os.path.isfile(f"data/users/{id}.claimc"):
            os.remove(f"data/users/{id}.claimc")
        return
    def timefor(self):
        now = datetime.datetime.utcnow()
        now = now + datetime.timedelta(hours=3)
        timestamp_code = f'<t:{int(now.timestamp())}:R>'
        return timestamp_code
    def format_timestamp(self,timestamp):
        unix_timestamp = int(timestamp.split(":")[1])
        datetime_obj = datetime.datetime.fromtimestamp(unix_timestamp)
        time_difference = datetime.datetime.now() - datetime_obj
        if time_difference.days > 365:
            return f"{time_difference.days // 365} years ago"
        elif time_difference.days > 30:
            return f"{time_difference.days // 30} months ago"
        elif time_difference.days > 0:
            return f"{time_difference.days} days ago"
        elif time_difference.seconds > 3600:
            return f"{time_difference.seconds // 3600} hours ago"
        elif time_difference.seconds > 60:
            return f"{time_difference.seconds // 60} minutes ago"
        elif time_difference.seconds > 5:
            return f"{time_difference.seconds} seconds ago"
        else:
            return "just now"
    def addto_account(self,id:int,addjar=0,added=0,addmax=0):
        try:
            if not os.path.isfile(f'data/users/{id}.json'):
                with open(f'data/users/{id}.json',"w") as i:
                    temp = self.defult_new
                    temp["created"] = self.timefor()
                    temp["max"] = addmax + int(temp["max"])
                    temp["now"] = added  + int(temp["now"])
                    temp["jar"] = addjar + int(temp["jar"])
                    json.dump(temp, i)
                    return
            with open(f'data/users/{id}.json','r') as i:
                temp = json.load(i)

            temp["max"] = addmax + int(temp["max"])
            temp["now"] = added  + int(temp["now"])
            temp["jar"] = addjar + int(temp["jar"])
            with open(f'data/users/{id}.json','w') as i:
                json.dump(temp, i)
        except IOError as e:
            print(f"Error: {e}")
    def check_account(self,id:int):
        if not os.path.isfile(f'data/users/{id}.json'):
            with open(f'data/users/{id}.json',"w") as i:
                temp = self.defult_new
                temp["created"] = self.timefor()
                json.dump(temp, i)
            return temp
        with open(f'data/users/{id}.json','r') as i:
            temp = json.load(i)
        return temp
    def check_amount(self,id:int,amount:int):
        temb = self.check_account(id)
        # 500 <= 600
        if temb["jar"] >= amount:
            return True # HE IS DOING THIS
        else:
            return False
    def removeto_account(self,id:int,addjar=0,added=0,addmax=0):
        try:
            if not os.path.isfile(f'data/users/{id}.json'):
                with open(f'data/users/{id}.json',"w") as i:
                    temp = self.defult_new
                    temp["created"] = self.timefor()
                    temp["max"] = int(temp["max"]) - addmax
                    temp["now"] = int(temp["now"]) - added 
                    temp["jar"] = int(temp["jar"]) - addjar
                    json.dump(temp, i)
                    return
            with open(f'data/users/{id}.json','r') as i:
                temp = json.load(i)
    
            temp["max"] = int(temp["max"]) - addmax
            temp["now"] = int(temp["now"]) - added 
            temp["jar"] = int(temp["jar"]) - addjar
            with open(f'data/users/{id}.json','w') as i:
                json.dump(temp, i,indent=4)
        except IOError as e:
            print(f"Error: {e}")

            
            
        
    @commands.Cog.listener()
    async def on_message(self, ctx:Message):
        if ctx.author.bot:
            return
        if os.path.isfile(f'data/users/{ctx.author.id}.claimc'):
            return
        if ctx.channel.name.startswith("ticket"):
            return
        if chance(1):
            whyyy= Embed(title="DROP",description=f"<@{ctx.author.id}> You Got DROP",color=0x31F9FF)
            whyyy.add_field(name="How to Claim it?",value="Say /claim")
            whyyy.add_field(name="When it will expired?",value="after 5 minutes")
            await ctx.channel.send(embed=whyyy,delete_after=30)
            t1 = threading.Thread(target=self.expire, args=(ctx.author.id, 5))
            t1.start()
    @slash_command("claim","Claim Your Drop")
    async def claim(self,ctx:init):
        why =Embed(title="Drops",description="You don't have Drop",color=0x31F9FF)
        if not os.path.isfile(f'data/users/{ctx.user.id}.claimc'):
            await ctx.response.send_message(embed=why,ephemeral=True)
            return
        os.remove(f'data/users/{ctx.user.id}.claimc')
        ad = random.randint(5,20)
        self.addto_account(ctx.user.id,ad)
        whyx =Embed(title="Drops",description=f"Added {ad} Cookies🍪",color=0x31F9FF)
        await ctx.response.send_message(embed=whyx,ephemeral=True)
    @slash_command("profile", "See Your Profile in Cookie Game")
    async def profile(self,ctx:init):
        temb = self.check_account(ctx.user.id)
        locale.setlocale(locale.LC_ALL, '')
        tebm = int(temb["jar"]) + int(temb["now"])
        temb["jar"] = locale.format_string("%d", int(temb["jar"]), grouping=True)
        temb["max"] = locale.format_string("%d", int(temb["max"]), grouping=True)
        temb["now"] = locale.format_string("%d", int(temb["now"]), grouping=True)
        tebm = locale.format_string("%d", int(tebm), grouping=True)
        server = self.client.get_guild(1114642571461935114)
        jar_em = utils.get(server.emojis, name="jar")
        va_em = utils.get(server.emojis, name="vault")
        why = Embed(title="⠀\n__Total__➜ "+"```"+str(tebm)+" 🍪```\n⠀",color=0x31F9FF)
        why.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
        why.set_thumbnail("https://i.ibb.co/ZMVvyNH/JAr-5.png")
        why.add_field(name=f"{jar_em}Jar",value="```"+str(temb["jar"])+" 🍪```")
        why.add_field(name=f"{va_em}Vault",value= "```"+str(temb["now"])+"/"+str(temb["max"])+" 🍪```")
        why.add_field(name=f"🕒 Account Created",value=f"```"+ self.format_timestamp(str(temb["created"])) +"```")
        
        await ctx.response.send_message(embed=why,ephemeral=True)
    @slash_command("transfer",
                   "Transfer Your Cookies To Other Account (it will take from your jar only)")
    async def transfer(self,ctx:init,user:Member,amount:int):
        if self.check_amount(ctx.user.id,amount):
            self.removeto_account(ctx.user.id,amount)
            self.addto_account(user.id,amount)
            await ctx.response.send_message("Done 👍",ephemeral=True)
        else:
            await ctx.response.send_message(f"Sorry You Don't Have {amount} 🍪",ephemeral=True)
            





            
    @user_command(name="Cookies: Profile")                
    async def invitesee(self,ctx:init,user:Member):
        if user.bot is True:
            await ctx.send("Aren't you trying to play with Bot?",ephemeral=True)
            return
        temb = self.check_account(user.id)
        locale.setlocale(locale.LC_ALL, '')
        tebm = int(temb["jar"]) + int(temb["now"])
        temb["jar"] = locale.format_string("%d", int(temb["jar"]), grouping=True)
        temb["max"] = locale.format_string("%d", int(temb["max"]), grouping=True)
        temb["now"] = locale.format_string("%d", int(temb["now"]), grouping=True)
        tebm = locale.format_string("%d", int(tebm), grouping=True)
        server = self.client.get_guild(1114642571461935114)
        jar_em = utils.get(server.emojis, name="jar")
        va_em = utils.get(server.emojis, name="vault")
        why = Embed(title="⠀\n__Total__➜ "+"```"+str(tebm)+" 🍪```\n⠀",color=0x31F9FF)
        why.set_author(name=user.name, icon_url=user.avatar.url)
        why.set_thumbnail("https://i.ibb.co/ZMVvyNH/JAr-5.png")
        why.add_field(name=f"{jar_em}Jar",value="```"+str(temb["jar"])+" 🍪```")
        why.add_field(name=f"{va_em}Vault",value= "```"+str(temb["now"])+"/"+str(temb["max"])+" 🍪```")
        why.add_field(name=f"🕒 Account Created",value=f"```"+ self.format_timestamp(str(temb["created"])) +"```")
        await ctx.response.send_message(embed=why,ephemeral=True)

        pass

        



def setup(client):
    client.add_cog(cookies(client))