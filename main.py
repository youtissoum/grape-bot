import discord
from discord.ext import commands, tasks
import config
import time
from itertools import cycle
from important_bot_files.commands import Commands_executor

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

client.add_cog(Commands_executor(client))

#########
# OTHER #
#########

client.run(config.token)
