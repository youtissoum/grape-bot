import discord
from discord.ui import Button, View

class HelpView(View):
    async def about_me_button_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.about_embed, view=self)

    def __init__(self):
        super().__init__(timeout=10.0)
        self.message: discord.Message = None

        self.about_embed = discord.Embed(title="Help", color=0x6f2da8)
        self.about_embed.add_field(name='About this bot', value='This is a bot I have created for a bot competition in a server called "The bot boat". I have won the competition and I am now actively working on this bot.', inline=True)
        self.about_button = Button(label='About me', style=discord.ButtonStyle.primary, custom_id="about_button")

    async def init(self, message: discord.Message):
        self.message = message
        self.about_button.callback = self.about_me_button_callback
        self.add_item(self.about_button)
        await self.message.edit(content="", view=self, embed=self.about_embed)

    async def on_timeout(self):
        self.about_button.disabled = True
        
        await self.message.edit(view=self)