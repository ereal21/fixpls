
import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / "state.json"
CONF_FILE = ROOT / "config.json"

# ---------- load config/state ----------
def load_json(p: Path, default):
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

CONF = load_json(CONF_FILE, {})
STATE = load_json(STATE_FILE, {"functions": {}})

def save_state():
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(STATE, f, indent=2, ensure_ascii=False)
    tmp.replace(STATE_FILE)

def get_flag(key: str) -> bool:
    return bool(STATE["functions"].get(key, False))

def set_flag(key: str, val: bool):
    STATE["functions"][key] = bool(val)
    save_state()

# ---------- env ----------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "").strip()
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID", "-4930039742"))
if not TOKEN:
    raise SystemExit("Please set BOT_TOKEN in .env (see .env.example).")

# ---------- ui helpers ----------
def onoff(v: bool) -> str:
    return "✅" if v else "❌"

def btn(label, data):
    return InlineKeyboardButton(label, callback_data=data)

def main_menu():
    kb = [
        [btn("🛒 Purchase", "noop"), btn("⚙️ Config", "cfg")],
        [btn("➕ Top up", "noop"), btn("🆘 Support", "noop")],
        [btn("🌐 Language", "noop")],
        [btn("🛡 Admin Panel", "noop")]
    ]
    return InlineKeyboardMarkup(kb)

def config_menu():
    kb = [
        [btn("🖥 RDP", "noop")],
        [btn("🧩 Functions", "cfg:functions")],
        [btn("🆘 Support ↗️", "noop")],
        [btn("⬅️ Back", "back:home")]
    ]
    return InlineKeyboardMarkup(kb)

def categories_menu():
    kb = []
    for cat_key, cat in CONF.items():
        kb.append([btn(cat["title"], f"cat:{cat_key}")])
    kb.append([btn("⬅️ Back", "back:cfg")])
    return InlineKeyboardMarkup(kb)

def category_items_menu(cat_key: str):
    cat = CONF[cat_key]
    rows = []
    for fn_key, label in cat["items"].items():
        rows.append([btn(f"{label} {onoff(get_flag(fn_key))}", f"toggle:{fn_key}:{cat_key}")])
    rows.append([btn("⬅️ Back", "back:cats")])
    return InlineKeyboardMarkup(rows)

# ---------- handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    txt = (f"✨ Welcome {user.mention_html()} 👋\n\n"
           f"🧾 Status: Middle Tier\n"
           f"🤖 Bots owned: 0\n"
           f"💰 Balance: €101.0")
    if update.message:
        await update.message.reply_html(txt, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(txt, reply_markup=main_menu())

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data
    await q.answer()

    if data == "cfg":
        await q.edit_message_text("⚙️ Bot settings:", reply_markup=config_menu())

    elif data == "cfg:functions" or data == "back:cats":
        await q.edit_message_text("🧩 Choose a function category:", reply_markup=categories_menu())

    elif data.startswith("cat:"):
        cat_key = data.split(":",1)[1]
        cat = CONF[cat_key]
        await q.edit_message_text(f"{cat['title']}\nPick a tool below to see what it covers.",
                                  reply_markup=category_items_menu(cat_key))

    elif data.startswith("toggle:"):
        # format: toggle:<fn_key>:<cat_key>
        _, fn_key, cat_key = data.split(":")
        new_state = not get_flag(fn_key)
        set_flag(fn_key, new_state)
        state_label = "ON" if new_state else "OFF"

        # Update the menu in place (stay in the same category view)
        await q.edit_message_reply_markup(reply_markup=category_items_menu(cat_key))

        # Announce to group
        user = update.effective_user
        label = None
        for k, v in CONF.items():
            if fn_key in v["items"]:
                label = v["items"][fn_key]
                break
        if not label:
            label = fn_key.replace("_", " ").title()

        msg = (f"🔧 Function changed\n"
               f"• Name: <b>{label}</b>\n"
               f"• State: <b>{state_label}</b>\n"
               f"• By: {user.mention_html()}")
        try:
            await context.bot.send_message(GROUP_CHAT_ID, msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            await q.message.reply_text(f"Couldn't post to group ({GROUP_CHAT_ID}): {e}")

    elif data == "back:cfg":
        await q.edit_message_text("⚙️ Bot settings:", reply_markup=config_menu())

    elif data == "back:home":
        await q.edit_message_text("Back to home:", reply_markup=main_menu())

    else:
        await q.answer("Coming soon…")

# ---------- bootstrap ----------
def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    app.run_polling()

if __name__ == "__main__":
    main()
