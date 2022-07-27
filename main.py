import io
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import config
import time
from itertools import cycle
from important_bot_files.views import HelpView
import json
from calculator.main import calculate_
from cmmmPreviewer.CodePreviewer import parse_any, preview_level
from PIL import Image
from TOKEN import token

value = "empty"
status = cycle(['the dev suffering', 'everybody else losing the competition'])

global client
client = commands.Bot(command_prefix='$', help_command=None)

##########
# EVENTS #
##########

@client.event
async def on_ready():
    print(f"{client.user} connected to discord !")
    change_status.start()

@tasks.loop(seconds=10.0)
async def change_status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(status)))

@client.event
async def on_message(message):
  correct = True
  for w in config.swear_words:
    if w in message.content:
      correct = False
      prevention = await message.channel.send(
      f"{message.author.mention} don't swear here please")
      print(f"someone said {w}")
      if message:
        await message.delete()
      time.sleep(3)
      await prevention.delete()
  if correct:
    await client.process_commands(message)


@client.event
async def on_member_join(member):
    await member.send(f"Thank you {member.name} for joining this server")

############
# COMMANDS #
############

test_servers = [911372583042162748, 809824925660479539]

@client.slash_command(description = "Get help about the bot")
async def help(ctx: discord.Message):
    about_embed=discord.Embed(title="Help", color=0x6f2da8)
    about_embed.add_field(name="About this bot", value="This bot was made for a bot competition on a unpopular server wich he won.", inline=True)
    commands_embed=discord.Embed(title="Help", color=0x6f2da8)
    commands_embed.add_field(name="Commands", value="1. **store/load** - stores or load a data that you give with an argument (note : You can use -h on $load to make it hide the \"value : \")\n2. **rules** - Prints out the rules of the server\n3. **echo** - makes the bot say what you give it (note : if you add delete to the end of \"echo\" it auto deletes your message\n4. **mimic** - mimics a user (note : you can disable/enable it for you with $mimicset))\n5. **message** - sends a message that the next user that uses the command sees\n6. **betterrickroll** - Rick rolls someone (please don't spam)\n7. **calculate** - calculates what you give it (supports +, -, *, /, ^ and paranthesis, uses correct mathematical operation order)", inline=False)

    view = HelpView(about_embed, commands_embed)

    temp = await ctx.respond("a", delete_after=0.1)

    message = await ctx.send(embed=about_embed, view=view)
    await view.init(message)

@client.slash_command(description="outputs the last stored value")
async def load(ctx):
    with open('storage.json', "r") as f:
        data = json.load(f)
        await ctx.respond(f"{data['stored_value']}")


@client.slash_command(description = "stores the value you give it")
async def store(ctx, value: str):
    with open('storage.json', "w") as f:
        if "@" in value:
            await ctx.respond("no")
            return

        data = {}
        data['stored_value'] = value

        json.dump(data, f)

        await ctx.respond(f"stored the value : {value}")


@commands.command(brief="shows the rules")
async def rules(ctx):
    await ctx.channel.send(
        "1. No spamming\n2. Dont say a slur/swear\n3. Bee nice to the bots\n4. Bee nice to people, too\n5. No advertising\n6. No personal info\n7. Make sure your brain is in your head beefore typing\n8. Follow the rules\n9. No excessive use of emojis\n10. If you have a question, dm a moderator"
    )


@client.slash_command(brief = "make the bot say anything")
async def echo(ctx, *, message):
    await ctx.respond("message succesfully said", delete_after = 2)
    await ctx.send(message)

mimicGroup = client.create_group("mimic", "mimics a user")

@mimicGroup.command(description = "mimic a user")
async def send(ctx: discord.Message, user: discord.Member, message: str):
    avatar: bytes = await user.avatar.read()
    webhook = await ctx.channel.create_webhook(name=user.display_name, reason="mimic command", avatar=avatar)
    data = {}
    with open('mimic_table.json', 'r') as f:
        data = json.load(f)
    
    if f"{user.id}" in data and data[f"{user.id}"] == "False":
        await ctx.respond("This user disabled mimicing")
    else:
        await webhook.send(message)
        await ctx.respond(f"Sent by {ctx.author.name}#{ctx.author.discriminator}", delete_after=5)
    await webhook.delete()

#@mimic.error
async def on_mimic_error(ctx, error):
    await ctx.channel.send(f"error : {error}")

@mimicGroup.command(brief="disable or enable mimicing")
async def set(ctx, parameter: bool):
    data = {}
    with open('mimic_table.json', 'r') as f:
        data = json.load(f)
    with open('mimic_table.json', 'w') as f:
        if parameter == "yes":
            data[ctx.author.id] = None
            data[ctx.author.id] = "True"
            await ctx.channel.send("mimicing set to true")
        elif parameter == "no":
            data[ctx.author.id] = None
            data[ctx.author.id] = "False"
            await ctx.channel.send("mimicing set to false")
        else:
            await ctx.channel.send("the argument must be yes or no")
        json.dump(data, f)

@client.command(brief="send a message for the next user to see")
async def message(ctx, *, message):
    with open('message_command.json', 'r') as f:
        data = json.load(f)
        await ctx.channel.send(data['message'])
    with open('message_command.json', 'w') as f:
        data = {}
        data['message'] = message
        json.dump(data, f)
    await ctx.message.delete()

@commands.command(brief="rick roll someone (removed)")
async def betterrickroll(ctx, user: discord.Member, parameter="none"):
    await user.send("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")
    answer = await ctx.channel.send("user rick rolled succesfully!")
    if not parameter == "-i":
        time.sleep(3)
        await answer.delete()
        await ctx.message.delete()
        await user.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    #await ctx.channel.send("command removed")


@betterrickroll.error
async def on_rickroll_error(ctx, error):
    await ctx.channel.send(error)

@client.slash_command(brief="forgot to do your math ?", guild_ids = test_servers)
async def calculate(ctx, *, calculation):
    value = calculate_(calculation)
    await ctx.respond(value)

@calculate.error
async def on_caculate_error(ctx, error):
    await ctx.channel.send(error)

@client.slash_command(description = "preview a cmmm level", guild_ids = test_servers)
async def preview(ctx: discord.Message, level: str):
    print(f"{ctx.author.name}#{ctx.author.discriminator} sent {level}")

    try:
        level = parse_any(level)
    except Exception as e:
        await ctx.respond(f"There was an error parsing your level : {e}")

    img: Image = preview_level(level)

    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.respond(level[3], file=discord.File(fp=image_binary, filename='preview.png'))

#########
# OTHER #
#########

client.run(token)
