import discord
from discord.ext import commands, tasks
from itertools import cycle
from BotViews import HelpView
import os
from TOKEN import token

client = commands.Bot(command_prefix="$", help_command=None)

@client.event
async def on_ready():
    print(f"{client.user} has been started succesfully !")
    change_status.start()

@tasks.loop(seconds=10.0)
async def change_status():
    statuses = cycle(['the dev suffering', 'everybody else that lost the competition'])
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(statuses)))

testing_servers = [911372583042162748, 809824925660479539, 1012804209982308362]

@client.slash_command(description = "Get help about this bot", test_guilds=testing_servers)
async def help(ctx: discord.Message):
    view = HelpView()
    
    await ctx.respond("sent the help message", ephemeral=True)
    
    message = await ctx.send("_ _", view=view)
    await view.init(message)

client.run(token)