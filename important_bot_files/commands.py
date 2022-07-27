from cProfile import label
from code import interact
import json
import random
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import config
import time
from calculator.main import calculate_
import important_bot_files.views

class Commands_executor(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        about_embed=discord.Embed(title="Help", color=0x6f2da8)
        about_embed.add_field(name="About this bot", value="This bot was made for a bot competition on a unpopular server wich he won.", inline=True)
        commands_embed=discord.Embed(title="Help", color=0x6f2da8)
        commands_embed.add_field(name="Commands", value="1. **store/load** - stores or load a data that you give with an argument (note : You can use -h on $load to make it hide the \"value : \")\n2. **rules** - Prints out the rules of the server\n3. **echo** - makes the bot say what you give it (note : if you add delete to the end of \"echo\" it auto deletes your message\n4. **mimic** - mimics a user (note : you can disable/enable it for you with $mimicset))\n5. **message** - sends a message that the next user that uses the command sees\n6. **betterrickroll** - Rick rolls someone (please don't spam)\n7. **calculate** - calculates what you give it (supports +, -, *, /, ^ and paranthesis, uses correct mathematical operation order)", inline=False)

        view = important_bot_files.views.HelpView(about_embed, commands_embed)

        message = await ctx.send(embed=about_embed, view=view)
        await view.init(message)

    @commands.command(brief="shows the stored value", category="storage")
    async def load(self, ctx, parameter=None):
        with open('storage.json', "r") as f:
            data = json.load(f)
            if parameter == "-h":
                await ctx.channel.send(f"{data['stored_value']}")
            else:
                await ctx.channel.send(f"value : {data['stored_value']}")


    @commands.command(brief="stores a value", category="storage")
    async def store(self, ctx, *, value):
        with open('storage.json', "w") as f:
            data = {}
            data['stored_value'] = value

            json.dump(data, f)

            await ctx.channel.send(f"stored the value : {value}")


    @commands.command(brief="shows the rules")
    async def rules(self, ctx):
        await ctx.channel.send(
            "1. No spamming\n2. Dont say a slur/swear\n3. Bee nice to the bots\n4. Bee nice to people, too\n5. No advertising\n6. No personal info\n7. Make sure your brain is in your head beefore typing\n8. Follow the rules\n9. No excessive use of emojis\n10. If you have a question, dm a moderator"
        )


    @commands.command(brief="make the bot say something")
    async def echo(self, ctx, *, message):
        await ctx.channel.send(message)


    @commands.command(brief="the echo command but the bot deletes your message")
    async def echodelete(self, ctx, *, message):
        await ctx.channel.send(message)
        await ctx.message.delete()


    @commands.command(brief="mimic a user")
    async def mimic(self, ctx, user: discord.Member, *, message):
        webhook = await ctx.channel.create_webhook(name=user.display_name)
        data = {}
        with open('mimic_table.json', 'r') as f:
            data = json.load(f)
        if f"{user.id}" in data:
            if data[f"{user.id}"] == "True":
                wrong = False
                for w in config.swear_words:
                    if w in str.lower(message):
                        await ctx.channel.send("don't even think about that")
                        wrong = True
                if not wrong:
                    await webhook.send(content=message)
                    await ctx.message.delete()
            else:
                await ctx.channel.send("This user disabled mimicing")
        else:
            wrong = False
            webhook = await ctx.channel.create_webhook(name=user.display_name)
            for w in config.swear_words:
                if w in str.lower(message):
                    await ctx.channel.send("don't even think about that")
                    wrong = True
            if not wrong:
                await webhook.send(content=message)
                await ctx.message.delete()
        await webhook.delete()


    #@mimic.error
    async def on_mimic_error(self, ctx, error):
        await ctx.channel.send(f"error : {error}")


    @commands.command(brief="send a message for the next user to see")
    async def message(self, ctx, *, message):
        with open('message_command.json', 'r') as f:
            data = json.load(f)
            await ctx.channel.send(data['message'])
        with open('message_command.json', 'w') as f:
            data = {}
            data['message'] = message
            json.dump(data, f)
        await ctx.message.delete()


    @commands.command(brief="disable or enable mimicing")
    async def mimicset(self, ctx, parameter):
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


    @commands.command(brief="rick roll someone (removed)")
    async def betterrickroll(self, ctx, user: discord.Member, parameter="none"):
        await user.send("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")
        answer = await ctx.channel.send("user rick rolled succesfully!")
        if not parameter == "-i":
            time.sleep(3)
            await answer.delete()
            await ctx.message.delete()
            await user.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        #await ctx.channel.send("command removed")


    @betterrickroll.error
    async def on_rickroll_error(self, ctx, error):
        await ctx.channel.send(error)

    @commands.command(brief="do calculations")
    async def calculate(self, ctx, *, calculation):
        value = calculate_(calculation)
        await ctx.channel.send(value)

    @calculate.error
    async def on_caculate_error(self, ctx, error):
        await ctx.channel.send(error)

    @commands.command(brief="testing the buttons")
    async def buttonTest(self, ctx):
        respond_button = Button(label="respond to this message", style=discord.ButtonStyle.primary)
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_message("I am responding")
        respond_button.callback = button_callback

        DM_button = Button(label="Send me a DM", style=discord.ButtonStyle.secondary)
        async def button_callback(interaction: discord.Interaction):
            await interaction.user.send("You have been sent a dm")
        DM_button.callback = button_callback

        view = View()
        view.add_item(respond_button)
        view.add_item(DM_button)

        await ctx.send("Testing buttons lol", view=view)

    @commands.command(brief="make a new ticket")
    async def createTicket(self, ctx: discord.Message):
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel: discord.TextChannel = await guild.create_text_channel(name=f"ticket-{ctx.author.name}", overwrites=overwrites, reason="new ticket", topic=ctx.author.id)

        ticket_embed = discord.Embed(title=f"{ctx.author.name}'s ticket", description=f"This is a ticket to help {ctx.author.name}")

        view = View(timeout=None)

        closeButton = Button(label="Close", style=discord.ButtonStyle.danger)
        async def button_callback(interaction: discord.Interaction):
            pass
        closeButton.callback = button_callback()

        await channel.send(embed=ticket_embed)