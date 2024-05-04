import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from welcome import Welcome

def get_token() -> str:
    load_dotenv()
    return os.getenv('DISCORD_TOKEN')



def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is online!")

        await bot.load_extension("welcome")




    DISCORD_TOKEN = get_token()
    bot.run(token=DISCORD_TOKEN)


if __name__ == '__main__':
    main()
