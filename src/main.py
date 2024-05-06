import discord
from dotenv import load_dotenv
import os
from discord.ext import commands


def get_token():
    load_dotenv()
    return os.getenv('DISCORD_TOKEN')


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.cogs_list = ["word_counter", "welcome", "role_selector"]


    async def on_ready(self):
        print(f"{self.user} is online!")
        synced = await self.tree.sync()
        print(synced)


    async def setup_hook(self):
        for ext in self.cogs_list:
            await self.load_extension(ext)


if __name__ == '__main__':
    DISCORD_TOKEN = get_token()
    client = Client()
    client.run(token=DISCORD_TOKEN)
