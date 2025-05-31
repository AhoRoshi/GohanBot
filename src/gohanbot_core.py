import os
import random
import discord
import json
from discord.ext import tasks
from datetime import time, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("token")

intents = discord.Intents.default()
bot = discord.Client(intents=intents)


def is_channel_registered(channel_id):
    channel_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "channels.json"
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


def load_channels():
    channel_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "channels.json"
    )
    if not os.path.exists(channel_path):
        return []
    else:
        with open(channel_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["channels"]


def load_adjectives():
    adjectives_path = os.path.join(
        os.path.dirname(__file__), "..", "resources", "adjectives.txt"
    )
    try:
        with open(adjectives_path, "r", encoding="utf-8") as file:
            adjectives = [line.strip() for line in file]
        return adjectives
    except FileNotFoundError:
        print(f"Error: File not found at {adjectives_path}")
        return []


JST = timezone(timedelta(hours=+9), "JST")
times = [time(hour=0, minute=0, tzinfo=JST)]


@tasks.loop(time=times)
async def send_random_message():
    await bot.wait_until_ready()
    channels = load_channels()
    adjectives = load_adjectives()
    for channel_id in channels:
        adjective = random.choice(adjectives)
        try:
            channel = bot.get_channel(channel_id)
            await channel.send(f"{adjective}ごはん")
        except:
            is_channel_registered(channel_id)  # チャンネルが消えてる場合は登録解除


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name="神"))
    if not send_random_message.is_running():
        send_random_message.start()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # 管理者からメンションがある際にチャンネル登録の有無を切り替える
    if bot.user.mention in message.content and message.author.guild_permissions.administrator:
        channel_id = message.channel.id
        if is_channel_registered(channel_id):
            await message.channel.send("うどん")
        else:
            await message.channel.send("ごはん")


bot.run(discord_token)
