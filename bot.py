import discord
from discord.ext import commands
from discord import app_commands
import openai
import os
from dotenv import load_dotenv
from datetime import datetime 

# --- Load environment variables ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") # Replace with variable name for your Discord token in your .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Replace with variable name for your OpenAI API key in your .env file
MODEL_NAME = "gpt-4"

# --- Set OpenAI API Key ---
openai.api_key = OPENAI_API_KEY

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- On Ready: Sync Slash Commands ---
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} and slash commands synced.")

# --- Slash Command: /ask ---
@bot.tree.command(name="ask", description="Ask Akatosh (GPT-4) a question.")
@app_commands.describe(question="What do you want to ask Akatosh?")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)

    try:
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[ 
                {"role": "system", "content": "You are Akatosh, The Dragon God of Time from The Elder Scrolls."}, # Set personality of GPT-4 model
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await interaction.followup.send(reply)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

# --- Server Log System ---
LOG_CHANNEL_NAME = "bot-log"  # Can be changed to desired log channel name in server

async def get_log_channel(guild: discord.Guild):
    return discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)

# Get current timestamp
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@bot.event
async def on_member_join(member):
    channel = await get_log_channel(member.guild)
    if channel:
        timestamp = get_current_time()
        await channel.send(f"**[{timestamp}]** 📥 **{member}** joined the server.")

@bot.event
async def on_member_remove(member):
    channel = await get_log_channel(member.guild)
    if channel:
        timestamp = get_current_time()
        await channel.send(f"**[{timestamp}]** 📤 **{member}** left the server.")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    channel = await get_log_channel(message.guild)
    if channel:
        timestamp = get_current_time()
        await channel.send(f"**[{timestamp}]** 🗑️ **Message Deleted** by {message.author}: `{message.content}`")

@bot.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content:
        return
    channel = await get_log_channel(before.guild)
    if channel:
        timestamp = get_current_time()
        await channel.send(
            f"**[{timestamp}]** ✏️ **Message Edited** by {before.author}:\n"
            f"Before: `{before.content}`\nAfter: `{after.content}`"
        )

@bot.event
async def on_voice_state_update(member, before, after):
    channel = await get_log_channel(member.guild)
    if channel:
        timestamp = get_current_time()
        if not before.channel and after.channel:
            await channel.send(f"**[{timestamp}]** 🔊 **{member}** joined voice channel: `{after.channel.name}`")
        elif before.channel and not after.channel:
            await channel.send(f"**[{timestamp}]** 🔇 **{member}** left voice channel: `{before.channel.name}`")
        elif before.channel != after.channel:
            await channel.send(
                f"**[{timestamp}]** 🔄 **{member}** switched from `{before.channel.name}` to `{after.channel.name}`"
            )

# --- Run Bot ---
bot.run(DISCORD_TOKEN)
