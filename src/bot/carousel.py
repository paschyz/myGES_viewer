import discord
from discord import Interaction
from discord.ui import Button, View
from utils import *


class Carousel(View):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.current_index = 0

    @discord.ui.button(emoji="⬅️")
    async def button_left(self, interaction: Interaction, button: Button):
        self.current_index = (self.current_index - 1) % len(self.items)
        self.items[self.current_index].set_footer(
            text=f"{self.current_index + 1}/{len(self.items)}")
        await interaction.response.edit_message(embed=self.items[self.current_index])

    @discord.ui.button(emoji="➡️")
    async def button_right(self, interaction: Interaction, button: Button):
        self.current_index = (self.current_index + 1) % len(self.items)
        self.items[self.current_index].set_footer(
            text=f"{self.current_index + 1}/{len(self.items)}")
        await interaction.response.edit_message(embed=self.items[self.current_index])
