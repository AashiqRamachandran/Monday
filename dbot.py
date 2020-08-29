import discord
import re
from start import *

TOKEN = 'NzQyMjQwNTU5NzMyNzUyMzg2.XzDPYw.B-wtFI6mJ_lnhvfJStGmhXY7EeQ'
client = discord.Client()

@client.event
async def on_message(message):
    # no self reply
    if message.author == client.user:
        return

    if message.content.startswith("scan"):
        msg=message.content
        ips = re.findall(r"[0-9]+(?:\.[0-9]+){3}", msg)
        keyword= re.findall(r"^(?:\w+ ){1}", msg)
        reply = "Hello {0.author.mention}! Starting a complete scan on the given IP".format(message)
        print("User message is: "+msg+" and the IP to scan is: "+str(ips[0])+" and keyword is: "+str(keyword[0]))
        await message.channel.send(reply)
        start(ips[0], keyword[0])
        await message.channel.send(file=discord.File('output.txt'))

    if message.content.startswith("selfcheck"):
        reply = "Hello {0.author.mention}! Starting self check module. Audit report will be sent once done".format(message)
        await message.channel.send(reply)
        selfcheck()
        await message.channel.send(file=discord.File('output.txt'))

@client.event
async def on_ready():
    print("Logged in as: "+client.user.name)
    print("Clent ID is: "+str(client.user.id))
    print("Awaiting commands")

client.run(TOKEN)
