import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CONTROL_CHANNEL_ID = int(os.getenv("CONTROL_CHANNEL_ID"))  # Must match your desired channel

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=None, self_bot=True, intents=intents)

processed_messages = set()
cooldown_seconds = 20

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    # Only react in the control channel
    if message.channel.id != CONTROL_CHANNEL_ID:
        return

    # Don't process the same message twice
    if message.id in processed_messages:
        return

    print(f"🔍 Watching message {message.id} in control channel...")

    await asyncio.sleep(cooldown_seconds)  # ⏳ Wait cooldown

    # Process all users who reacted to the message
    if message.reactions:
        user_ids = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.id != bot.user.id:
                    user_ids.add(user.id)

        # Send P <user_id> for each unique user
        for uid in user_ids:
            await message.channel.send(f"P {uid}")
            await asyncio.sleep(0.5)  # Small delay to avoid spam

        processed_messages.add(message.id)
    else:
        print("⚠️ No reactions found.")

bot.run(TOKEN)
