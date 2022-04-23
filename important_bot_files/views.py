import discord
from discord.ext import commands, tasks
from discord.ui import Button, View

class HelpView(View):
    ctx = None
    message = None

    about_embed = None
    commands_embed = None

    def __init__(self, about_embed, commands_embed, timeout=10.0):
        super().__init__(timeout=timeout)
        self.about_embed = about_embed
        self.commands_embed = commands_embed

    async def init(self, message):
        self.message = message
        self.abt_btn.callback = self.about_me_button_callback
        self.commands_btn.callback = self.commands_button_call_back
        self.add_item(self.abt_btn)
        self.add_item(self.commands_btn)
        await message.edit(view=self)

    abt_btn = Button(label="About me !", style=discord.ButtonStyle.primary, custom_id="abt_btn")
    async def about_me_button_callback(self, interaction: discord.Interaction):
        await interaction.message.edit(embed=self.about_embed, view=self)

    commands_btn = Button(label="My commands!", style=discord.ButtonStyle.primary, custom_id="cmd_btn")
    async def commands_button_call_back(self, interaction: discord.Interaction):
        await interaction.message.edit(embed=self.commands_embed, view=self)

    async def on_timeout(self):
        self.abt_btn.disabled = True
        self.commands_btn.disabled = True
        await self.message.edit(view=self)