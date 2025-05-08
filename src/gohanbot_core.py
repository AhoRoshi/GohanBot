import os
import random
import discord
import json
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("token")

intents = discord.Intents.all()
bot = discord.Client(intents=intents)


def toggle_channel(channel_id):
    channel_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "channel_list.json"
    )
    if not os.path.exists(channel_path):
        data = []
    else:
        with open(channel_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    if channel_id in data["channels"]:
        data["channels"].remove(channel_id)
        with open(channel_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    else:
        data["channels"].append(channel_id)
        with open(channel_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return False


def get_channel_list():
    channel_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "channel_list.json"
    )
    if not os.path.exists(channel_path):
        return []
    else:
        with open(channel_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["channels"]


def load_adjectives(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            adjectives = [line.strip() for line in file]
        return adjectives
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []


async def send_random_message():
    await bot.wait_until_ready()
    channel_list = get_channel_list()
    adjective_path = os.path.join(
        os.path.dirname(__file__), "..", "resources", "adjective.txt"
    )
    adjectives = load_adjectives(adjective_path)
    for channel_id in channel_list:
        adjective = random.choice(adjectives)
        channel = bot.get_channel(channel_id)
        channel.send(f"{adjective}ごはん")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name="tasty gohan!"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # メンションがある際にチャンネル登録の有無を切り替える
    if bot.user.mention in message.content:
        channel_id = message.channel.id
        if toggle_channel(channel_id):
            await message.channel.send("not tasty gohan...")
        else:
            await message.channel.send("tasty gohan!")


send_random_message.start()
bot.run(discord_token)
