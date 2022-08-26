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

class DuelView(View):
    message = None
    battler: discord.User = None
    victim: discord.User = None

    battler_has_voted = False
    victim_has_voted = False

    battler_vote = None
    victim_vote = None

    def __init__(self, battler, victim, timeout=120):
        super().__init__(timeout=timeout)
        self.battler = battler
        self.victim = victim

    async def init(self, message: discord.Message):
        self.message = message
        self.rock_btn.callback = self.rock_btn_callback
        self.paper_btn.callback = self.paper_btn_callback
        self.scissors_btn.callback = self.scissors_btn_callback
        self.add_item(self.rock_btn)
        self.add_item(self.paper_btn)
        self.add_item(self.scissors_btn)
        await message.edit(view=self)

    async def on_vote(self, vote: str, interaction: discord.Interaction):
        if interaction.user == self.battler:
            self.battler_has_voted = True
            self.battler_vote = vote
            await interaction.channel.send(f"{interaction.user.display_name} has voted")

        if interaction.user == self.victim:
            self.victim_has_voted = True
            self.victim_vote = vote
            await interaction.channel.send(f"{interaction.user.display_name} has voted")

        if self.battler_has_voted == True and self.victim_has_voted == True:
            if self.battler_vote == self.victim_vote:
                await interaction.response.send_message(f"draw !")
            elif self.battler_vote == "rock" and self.victim_vote == "scissors" or \
                self.battler_vote == "paper" and self.victim_vote == "rock" or \
                self.battler_vote == "scissors" and self.victim_vote == "paper":
                await interaction.response.send_message(f"{self.battler_vote}({self.battler.display_name}) wins against {self.victim_vote}({self.victim.display_name})")
            elif self.victim_vote == "rock" and self.battler_vote == "scissors" or \
                self.victim_vote == "paper" and self.battler_vote == "rock" or \
                self.victim_vote == "scissors" and self.battler_vote == "paper":
                await interaction.response.send_message(f"{self.victim_vote}({self.victim.display_name}) wins against {self.battler_vote}({self.battler.display_name})")
            await self.message.delete()

    rock_btn = Button(label="Rock", style=discord.ButtonStyle.primary, custom_id="rock_btn")
    async def rock_btn_callback(self, interaction: discord.Interaction):
        await self.on_vote("rock", interaction)

    paper_btn = Button(label="Paper", style=discord.ButtonStyle.primary, custom_id="paper_btn")
    async def paper_btn_callback(self, interaction: discord.Interaction):
        await self.on_vote("paper", interaction)

    scissors_btn = Button(label="Scissors", style=discord.ButtonStyle.primary, custom_id="scissors_btn")
    async def scissors_btn_callback(self, interaction: discord.Interaction):
        await self.on_vote("scissors", interaction)