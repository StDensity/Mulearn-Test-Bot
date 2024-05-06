import time
import discord
from discord.ext import commands
from utils.sql import Sql
from discord import app_commands
import configparser


class RoleSelector(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='select_role', description="Allows you to select roles.")
    async def select_role(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=DropdownView(guild=interaction.guild))


class DropdownView(discord.ui.View):
    def __init__(self, guild):
        super().__init__()
        self.add_item(Dropdown(guild=guild))


class Dropdown(discord.ui.Select):

    def __init__(self, guild):
        self.drop_down_roles = []  # Stored as role object
        self.load_config(guild)
        self.sql = Sql('user_role', 'discord_id', 'role')


        options = []
        for index, role in enumerate(self.drop_down_roles):
            options.append(discord.SelectOption(label=f"{role.name}", value=str(index)))
        super().__init__(placeholder='Choose a role', min_values=0, max_values=len(self.drop_down_roles), options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            await self.remove_all_drop_down_roles(interaction)
            await self.add_selected_role(interaction)
        except Exception as e:
            await interaction.response.send_message(f'An error occurred')
            print(f'An error {e} occurred in dropdown callback')

    async def add_selected_role(self, interaction: discord.Interaction):
        role_name_list = []
        if len(self.values) == 0:
            await interaction.response.send_message(f'Your roles have been removed.', ephemeral=True)
            return
        for index in self.values:
            role = self.drop_down_roles[int(index)]
            await interaction.user.add_roles(role)
            role_name_list.append(role.name)
        role_names_string = ', '.join(role_name_list)
        await interaction.response.send_message(f'You have been granted {role_names_string} role.', ephemeral=True)
        self.sql.add_role(user_id=interaction.user.id, roles=role_name_list)

    async def remove_all_drop_down_roles(self, interaction: discord.Interaction):
        for role in self.drop_down_roles:
            await interaction.user.remove_roles(role)


    def load_config(self, guild):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            drop_down_role_ids = config['role_id']['drop_down_role_id'].split(',')
            for role_id in drop_down_role_ids:
                self.drop_down_roles.append(guild.get_role(int(role_id)))
        except Exception as e:
            print(f"Exception {e} occurred while loading configfile")


async def setup(client: commands.Bot):
    await client.add_cog(RoleSelector(client))