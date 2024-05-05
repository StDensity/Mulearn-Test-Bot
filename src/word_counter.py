import discord
from discord.ext import commands
from utils.sql import Sql
from discord import app_commands
from collections import Counter

class WordCounter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sql = Sql()

    @commands.Cog.listener()
    async def on_message(self, ctx: discord.Message):
        # To make sure the bot is not responding to itself.
        if ctx.author.id == self.client.user.id:
            return
        print(ctx.author.id)
        self.sql.add_message(ctx.author.id, ctx.content)
        await ctx.channel.send(f"```{self.sql.get_table()}```")

    @app_commands.command(name='word_status', description="Returns the 10 most used words")
    async def word_status(self, interaction: discord.Interaction):
        table = self.sql.get_table()
        word_counts = Counter()
        for item in table:
            words = item['message'].split()
            word_counts.update(words)

        top_10_words = word_counts.most_common(10)
        embed = discord.Embed(title="Top 10 Most Common Words", color=discord.Color.blue())

        # '\u200b' is a placeholder for an empty value
        for word, count in top_10_words:
            embed.add_field(name=f"{word} : {count}", value="\u200b", inline=False)
        await interaction.response.send_message(embed=embed)



async def setup(client: commands.Bot):
    await client.add_cog(WordCounter(client))
