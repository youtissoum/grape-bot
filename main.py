import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
from TOKEN import token

client = commands.Bot(command_prefix=None, help_command=None)

@client.event
async def on_ready():
    print(f"{client.user} has been started succesfully !")
    change_status.start()

@tasks.loop(seconds=10.0)
async def change_status():
    statuses = cycle(['the dev suffering', 'everybody else that lost the competition'])
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(statuses)))

client.run(token)