# Telegram Functions Bot (Full categories + toggles)

- Shows *all* categories with functions.
- Each function displays ✅/❌ and toggles on press.
- Posts a formatted update to your group **-4930039742**.

## Setup
1. Unzip.
2. Copy `.env.example` to `.env`, set `BOT_TOKEN` (keep `GROUP_CHAT_ID=-4930039742` or change).
3. `pip install -r requirements.txt`
4. `python bot.py`
5. Add the bot to your group and grant send permissions.

## Customize
- Edit `config.json` to rename categories or add/remove functions.
- Initial ON/OFF for each function is stored in `state.json`. Update it or just toggle from the UI.
