import os
import random
import discord
import schedule
import json
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("token")

intents = discord.Intents.all()
bot = discord.Client(intents=intents)


class Channel:
    def __init__(self, config_path):
        self.channel_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "channel_list.json"
        )


def load_adjectives(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            adjectives = [line.strip() for line in file]
        return adjectives
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name="tasty gohan!"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # メンションがある際にチャンネル登録の有無を切り替える
    if bot.user.mention in message.content:
        await message.channel.send("Hello! I'm GohanBot, how can I assist you today?")


if __name__ == "__main__":
    adjective_path = os.path.join(
        os.path.dirname(__file__), "..", "resources", "adjective.txt"
    )
    adjectives = load_adjectives(adjective_path)
    adjective = random.choice(adjectives)

bot.run(discord_token)
