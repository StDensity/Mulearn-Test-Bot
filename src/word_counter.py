import discord
from discord.ext import commands
from utils.sql import Sql
from discord import app_commands
from collections import Counter


class WordCounter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sql = Sql('user_words', 'discord_id', 'message')

    @commands.Cog.listener()
    async def on_message(self, ctx: discord.Message):
        try:
            # To make sure the bot is not responding to itself.
            if ctx.author.id == self.client.user.id:
                return
            self.sql.add_message(ctx.author.id, ctx.content)
            await ctx.channel.send(f"```{self.sql.get_table()}```")
        except Exception as e:
            print(f"An error occurred {e}")

    @app_commands.command(name='word_status', description="Returns the 10 most used words")
    @app_commands.describe(user="Word status of the user.")
    async def word_status(self, interaction: discord.Interaction, user: discord.Member = None):
        try:
            word_counts = Counter()
            if user:
                user_message = self.sql.get_message(user.id)
                word_counts.update(user_message.split())
                embed_title_name = f"By {user.name}"
            else:
                table = self.sql.get_table()
                embed_title_name = "From the server"
                for item in table:
                    words = item['message'].split()
                    word_counts.update(words)

            top_10_words = word_counts.most_common(10)
            embed = discord.Embed(title=f"Top 10 Most Common Words {embed_title_name}", color=discord.Color.blue())

            # '\u200b' is a placeholder for an empty value
            for word, count in top_10_words:
                embed.add_field(name=f"{word} : {count}", value="\u200b", inline=False)
            await interaction.response.send_message(embed=embed)
        except IndexError as e:
            await interaction.response.send_message(f"No records found for the user {user.name}")
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred.")


async def setup(client: commands.Bot):
    await client.add_cog(WordCounter(client))
