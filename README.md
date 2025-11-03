# mc-bot

A Python Discord bot with prefix and slash command support for multiple guilds.

## Features

- **Dual Command Support**: Supports both prefix commands (e.g., `!command`) and slash commands
- **Multi-Guild Support**: Works seamlessly across multiple Discord servers
- **Modular Design**: Uses cogs for organized command management
- **Python 3.8 Compatible**: Built for Python 3.8

## Project Structure

```
mc-bot/
├── cogs/              # Command modules (cogs)
│   └── __init__.py
├── main.py            # Main bot file
├── requirements.txt   # Python dependencies
└── .env.example       # Environment variables template
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your bot token:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your Discord bot token:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   ```
5. Run the bot:
   ```bash
   python main.py
   ```

## Configuration

- **Default Prefix**: `!` (can be modified in `main.py`)
- **Bot Token**: Set in `.env` file

## Adding Cogs

Place new cog files in the `cogs/` directory. They will be automatically loaded on startup.

## Requirements

- Python 3.8+
- discord.py 2.3.2
- python-dotenv 1.0.0
