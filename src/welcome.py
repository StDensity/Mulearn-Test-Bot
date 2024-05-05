import discord
from discord.ext import commands
import configparser


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


async def setup(client: commands.Bot):
    await client.add_cog(Welcome(client))
