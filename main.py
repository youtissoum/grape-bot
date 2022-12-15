import discord
from discord.ext import commands, tasks
from itertools import cycle
from BotViews import HelpView
from TOKEN import token
import json

client = commands.Bot(command_prefix="$", help_command=None)

with open('bot_data.json', 'r') as f:
    bot_data = json.loads(f.read())

@client.event
async def on_ready():
    print(f"{client.user} has been started succesfully !")
    change_status.start()
    save_data.start()

@tasks.loop(seconds=10.0)
async def change_status():
    statuses = cycle(['the dev suffering', 'everybody else that lost the competition'])
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(statuses)))

@tasks.loop(seconds=30.0)
async def save_data():
    with open('bot_data.json', 'w') as f:
        f.write(json.dumps(bot_data))

testing_servers = [911372583042162748, 809824925660479539, 1012804209982308362]

@client.slash_command(description = "Get help about this bot", test_guilds=testing_servers)
async def help(ctx: discord.Message):
    view = HelpView()
    
    await ctx.respond("sent the help message", ephemeral=True)
    
    message = await ctx.send("_ _", view=view)
    await view.init(message)

@client.slash_command(description = "Make the bot say anything you want", test_guilds=testing_servers)
async def echo(ctx, message: str):
    await ctx.respond(message)

mimic_group = client.create_group("mimic", "tools for mimicing other users", test_guilds=testing_servers)

@mimic_group.command(description = "send a message as a user")
async def send(ctx: discord.Message, user: discord.Member, message: str):
    strid = str(ctx.author.id)
    if strid not in bot_data['mimicing']:
        bot_data['mimicing'][strid] = True

    vstrid = str(user.id)
    if vstrid not in bot_data['mimicing']:
        bot_data['mimicing'][vstrid] = True

    if bot_data['mimicing'][strid] and bot_data['mimicing'][vstrid]:
        await ctx.respond("success!", ephemeral=True)
        avatar: bytes = await user.avatar.read()
        webhook = await ctx.channel.create_webhook(name=user.display_name, reason=f"{ctx.author.display_name} is mimicing {user.display_name}", avatar=avatar)
        await webhook.send(message)
        await webhook.delete()
    else:
        await ctx.respond("either you or the person you are trying to mimic has mimicing disabled", ephemeral=True)

client.run(token)
with open('bot_data.json', 'w') as f:
    f.write(json.dumps(bot_data))