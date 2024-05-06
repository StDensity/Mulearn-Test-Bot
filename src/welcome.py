import discord
from discord.ext import commands
import configparser
from discord import app_commands




class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.welcome_channel_id = None

        self.load_config()

    @commands.command()
    async def test(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await self.send_welcome_message_channel(member)
            await self.send_welcome_message_dm(member)
        except Exception as e:
            print(f"Exception {e} occurred in on_member_join")

    async def send_welcome_message_channel(self, member: discord.Member):
        channel = self.client.get_channel(self.welcome_channel_id)
        await channel.send(f"Welcome {member.mention} to the server")

    @staticmethod
    async def send_welcome_message_dm(member: discord.Member):
        await member.send(f"Welcome {member.mention} to the server. Head to the server an have a time of your life.")

    def load_config(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.welcome_channel_id = int(config['channel_id']['WELCOME_CHANNEL_ID'])
        except Exception as e:
            print(f"Exception {e} occurred while loading configfile")

    def update_config(self, category, key, new_value):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if category in config:
            config[category][key] = str(new_value)
        else:
            config[category] = {key: str(new_value)}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    @app_commands.command(name='set_welcome_channel', description="Returns the 10 most used words")
    @app_commands.describe(channel="Word status of the user.")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            self.update_config(category='channel_id', key='WELCOME_CHANNEL_ID', new_value=channel.id)
            await interaction.response.send_message(f'Welcome messages set to {channel.mention}', ephemeral=True)
            self.load_config()
        except Exception as e:
            await interaction.response.send_message(f"An Error {e} occurred.", ephemeral=True)
            print(f"Error {e} occurred!")


async def setup(client: commands.Bot):
    await client.add_cog(Welcome(client))
