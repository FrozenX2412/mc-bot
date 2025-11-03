import discord
from discord.ext import commands
import os

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_PREFIX = '!'

# Create bot instance with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=DEFAULT_PREFIX,
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_guild_join(guild):
    print(f'Joined guild: {guild.name} (ID: {guild.id})')

@bot.event
async def on_guild_remove(guild):
    print(f'Left guild: {guild.name} (ID: {guild.id})')

# Load cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

@bot.event
async def setup_hook():
    await load_cogs()

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
