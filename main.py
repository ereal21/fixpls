import logging
import io
import os
import html
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiohttp import web

import qrcode
from config import (
    BOT_TOKEN,
    RDP_PACKAGES,
    ADMIN_ID,
    STEP1_IMAGE,
    STEP2_IMAGE,
    STEP3_IMAGE,
    STEP4_IMAGE,
    STEP5_IMAGE,
    STEP6_IMAGE,
    STEP7_IMAGE,
    PACKAGE_STATUSES,
    STATUS_TO_PACKAGE,
    get_plan_price,
    PACKAGE_PRICING,
    FUNCTION_ALERT_CHAT_ID,
    PACKAGE_ORDER,
)
from database import Database
from keyboards import (
    language_keyboard,
    role_selection_keyboard,
    buyer_menu_keyboard,
    dealer_main_menu_keyboard,
    purchase_keyboard,
    back_to_menu,
    purchase_item_keyboard,
    payment_method_keyboard,
    cancel_payment,
    admin_panel_keyboard,
    user_profile_keyboard,
    config_keyboard,
    functions_menu_keyboard,
    functions_engagement_keyboard,
    functions_operations_keyboard,
    functions_commerce_keyboard,
    functions_catalog_keyboard,
    manage_keyboard,
    extend_keyboard,
    purchase_functions_keyboard,
    rdp_keyboard,
    setup_next_keyboard,
    setup_cancel_keyboard,
    setup_complete_keyboard,
    topup_amount_keyboard,
    rdp_details_keyboard,
    manage_rdps_keyboard,
    admin_rdp_cancel_keyboard,
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from texts import T
from payments import create_invoice, ipn_handler, init_payments

logging.basicConfig(level=logging.INFO)
db = Database()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=MemoryStorage())
history = defaultdict(list)
qr_messages = {}
init_payments(bot, db, qr_messages)

# === Feature toggle via Telegram group (staged + confirm) ===
import asyncio
import json
import re
import os
import html
from aiogram import types
from config import ADMIN_ID, FUNCTION_ALERT_CHAT_ID, BOT_TAG

_STATE_FILE = "state.json"
PENDING_CONFIRM: dict = {}

LINE_RE = re.compile(r'function\s+"(?P<feature>[\w_]+)"\s+turn\s+(?P<state>ON|OFF)', re.IGNORECASE)

def _load_state():
    try:
        with open(_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"functions": {}}

def _save_state(data):
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _list_features():
    return list(_load_state().get("functions", {}).keys())

def _apply_pending():
    state = _load_state()
    state.setdefault("functions", {})
    for feat, enabled in PENDING_CONFIRM.items():
        state["functions"][feat] = bool(enabled)
    _save_state(state)

def _is_allowed(message: types.Message) -> bool:
    return bool(message.from_user and message.from_user.id == ADMIN_ID)

@dp.message_handler(lambda m: m.chat and m.chat.id == FUNCTION_ALERT_CHAT_ID and m.text and 'function' in m.text.lower())
async def group_toggle_listener(message: types.Message):
    if not _is_allowed(message):
        return
    text = message.text.strip()
    if BOT_TAG not in text:
        return  # must address this bot explicitly
    m = LINE_RE.search(text)
    if not m:
        return

    feature = m.group("feature")
    state_str = m.group("state").upper()
    desired_state = (state_str == "ON")

    valid = _list_features()
    if feature not in valid:
        await message.reply(
            f"❌ Unknown feature: `{feature}`. Available: {', '.join(valid)}",
            parse_mode="Markdown",
        )
        return

    PENDING_CONFIRM[feature] = desired_state
    await message.reply(
        f"""📝 Received request for {BOT_TAG}: `{feature}` → {'ON' if desired_state else 'OFF'}
Please confirm by sending *exactly*: `Confirm function changes for {BOT_TAG}`""",
        parse_mode="Markdown",
    )

@dp.message_handler(lambda m: m.chat and m.chat.id == FUNCTION_ALERT_CHAT_ID and m.text and m.text.strip() == f"Confirm function changes for {BOT_TAG}")
async def confirm_and_restart(message: types.Message):
    if not _is_allowed(message):
        return

    if not PENDING_CONFIRM:
        await message.reply("ℹ️ No pending changes to confirm.")
        return

    lines = [f"- {k}: {'ON' if v else 'OFF'}" for k, v in PENDING_CONFIRM.items()]
    await message.reply(
        f"""✅ Confirmation received. Applying feature changes for {BOT_TAG}
{os.linesep.join(lines)}
♻️ Restarting bot to apply feature changes…""",
        parse_mode="Markdown",
    )

    _apply_pending()
    PENDING_CONFIRM.clear()

    async def _delayed_restart():
        await asyncio.sleep(1)
        os._exit(0)

    asyncio.create_task(_delayed_restart())
# === /Feature toggle via group ===

FULL_STATUS = PACKAGE_STATUSES["bigbang"]

FEATURES = {
    "blackjack": {"text_key": "feature_blackjack", "category": "engagement"},
    "coinflip": {"text_key": "feature_coinflip", "category": "engagement"},
    "achievements": {"text_key": "feature_achievements", "category": "engagement"},
    "quests": {"text_key": "feature_quests", "category": "engagement"},
    "gift": {"text_key": "feature_gift", "category": "engagement"},
    "lottery": {"text_key": "feature_lottery", "category": "engagement"},
    "leaderboard": {"text_key": "feature_leaderboard", "category": "engagement"},
    "assistant": {"text_key": "feature_assistant", "category": "operations"},
    "broadcast": {"text_key": "feature_broadcast", "category": "operations"},
    "analytics": {"text_key": "feature_analytics", "category": "operations"},
    "stock_alerts": {"text_key": "feature_stock_alerts", "category": "commerce"},
    "promocodes": {"text_key": "feature_promocodes", "category": "commerce"},
    "reservations": {"text_key": "feature_reservations", "category": "commerce"},
    "product_types": {"text_key": "feature_product_types", "category": "commerce"},
    "manual_payments": {"text_key": "feature_manual_payments", "category": "commerce"},
    "crypto_payments": {"text_key": "feature_crypto_payments", "category": "commerce"},
    "locations": {"text_key": "feature_locations", "category": "catalog"},
    "reviews": {"text_key": "feature_reviews", "category": "catalog"},
    "media_library": {"text_key": "feature_media_library", "category": "catalog"},
}

CATEGORY_KEYBOARDS = {
    "engagement": functions_engagement_keyboard,
    "operations": functions_operations_keyboard,
    "commerce": functions_commerce_keyboard,
    "catalog": functions_catalog_keyboard,
}

PACKAGE_NAME_KEYS = {
    "nova": "package_name_nova",
    "supernova": "package_name_supernova",
    "hypernova": "package_name_hypernova",
    "bigbang": "package_name_bigbang",
}

def _package_localized_name(lang: str, package: str) -> str:
    key = PACKAGE_NAME_KEYS.get(package)
    if key and key in T[lang]:
        return T[lang][key]
    return PACKAGE_STATUSES.get(package, package.title())

def _current_subscription(user_id: int):
    sub = db.get_subscription(user_id)
    if sub:
        return (
            sub.get("package"),
            sub.get("plan_type"),
            sub.get("expires_at"),
            sub.get("reminder_sent", False),
        )
    status = db.get_status(user_id)
    package = STATUS_TO_PACKAGE.get(status)
    return package, None, None, False

def _build_dealer_main(user: types.User, lang: str):
    balance = db.get_balance(user.id)
    status = db.get_status(user.id)
    package, plan, _, _ = _current_subscription(user.id)
    show_purchase = True
    if status == FULL_STATUS and (plan in {None, "lifetime"}):
        show_purchase = False
    text = T[lang]["main_title"].format(
        name=_display_name(user), status=status, balance=balance
    )
    markup = dealer_main_menu_keyboard(
        lang,
        is_admin=user.id == ADMIN_ID,
        show_purchase=show_purchase,
    )
    return text, markup

def _build_buyer_main(user_id: int, lang: str):
    text = T[lang]["buyer_main_title"]
    return text, buyer_menu_keyboard(lang)

async def _maybe_send_subscription_reminder(user_id: int, lang: str):
    package, plan, expires_at, reminder_sent = _current_subscription(user_id)
    if plan != "monthly" or not expires_at:
        if reminder_sent:
            db.set_subscription_reminder(user_id, False)
        return
    try:
        expiry = datetime.fromisoformat(expires_at)
    except ValueError:
        return

    delta = expiry - datetime.utcnow()
    if delta <= timedelta(days=3) and delta > timedelta():
        if not reminder_sent:
            expiry_str = expiry.strftime("%Y-%m-%d")
            package_name = _package_localized_name(lang, package or "")
            await bot.send_message(
                user_id,
                T[lang]["subscription_reminder"].format(
                    package=package_name, expires=expiry_str
                ),
            )
            db.set_subscription_reminder(user_id, True)
    elif delta > timedelta(days=3) and reminder_sent:
        db.set_subscription_reminder(user_id, False)

def _apply_package_purchase(user_id: int, package: str, plan: str) -> Optional[str]:
    status_name = PACKAGE_STATUSES.get(package)
    if status_name:
        db.set_status(user_id, status_name)
        db.set_config_seen(user_id, False)
    expires_at = None
    if plan == "monthly":
        expires_at = (datetime.utcnow() + timedelta(days=30)).replace(microsecond=0)
        expires_at = expires_at.isoformat()
    db.set_subscription(user_id, package, plan, expires_at)
    return expires_at

def _get_feature_states(user_id: int):
    states = db.get_user_feature_states(user_id)
    for key in FEATURES:
        states.setdefault(key, False)
    return states

class AdminStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_balance = State()
    waiting_for_bot_username = State()

class TopUpStates(StatesGroup):
    waiting_for_amount = State()

class SetupStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_ngrok = State()
    waiting_for_crypto = State()
    waiting_for_api_key = State()
    waiting_for_ipn_key = State()
    waiting_for_user_id = State()
    waiting_for_botfather = State()
    waiting_for_bot_token = State()

class ManageRDPStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()
    waiting_for_ip = State()
    waiting_for_name = State()
    waiting_for_rdp_password = State()
    waiting_for_expiry = State()

def _display_name(user: types.User) -> str:
    if user.username:
        return f"@{user.username}"
    if user.full_name:
        return user.full_name
    return str(user.id)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user = message.from_user
    history[user.id].clear()
    db.upsert_user(user.id, user.username)
    lang = db.get_language(user.id)
    prompt_lang = lang if "role_prompt" in T.get(lang, {}) else "en"
    await message.answer(
        T[prompt_lang]["role_prompt"], reply_markup=role_selection_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("lang:"))
async def cb_set_language(call: types.CallbackQuery):
    lang = call.data.split(":")[1]
    user = call.from_user
    db.upsert_user(user.id, user.username, language=lang)

    role = db.get_role(user.id)
    if role.upper() == "BUYER":
        text, markup = _build_buyer_main(user.id, lang)
    else:
        await _maybe_send_subscription_reminder(user.id, lang)
        text, markup = _build_dealer_main(user, lang)
    await call.message.edit_text(text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("role:"))
async def cb_choose_role(call: types.CallbackQuery):
    role = call.data.split(":")[1]
    user = call.from_user
    history[user.id].clear()
    db.set_role(user.id, role.upper())
    lang = db.get_language(user.id)
    if role == "buyer":
        text, markup = _build_buyer_main(user.id, lang)
    else:
        await _maybe_send_subscription_reminder(user.id, lang)
        text, markup = _build_dealer_main(user, lang)
    await call.message.edit_text(text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "menu:lang")
async def cb_language_menu(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(T[lang]["choose_language"], reply_markup=language_keyboard(lang))

@dp.callback_query_handler(lambda c: c.data == "buyer:search")
async def cb_buyer_search(call: types.CallbackQuery):
    if db.get_role(call.from_user.id).upper() != "BUYER":
        return
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["buyer_search_desc"], reply_markup=back_to_menu(lang)
    )

@dp.callback_query_handler(lambda c: c.data == "menu:purchase")
async def cb_purchase(call: types.CallbackQuery):
    user_id = call.from_user.id
    if db.get_role(user_id).upper() == "BUYER":
        lang = db.get_language(user_id)
        await call.answer(T[lang]["buyer_no_access"], show_alert=True)
        return
    lang = db.get_language(user_id)
    history[user_id].append((call.message.text or "", call.message.reply_markup))
    status = db.get_status(user_id)
    current_package, current_plan, _, _ = _current_subscription(user_id)
    highest_package = PACKAGE_ORDER[-1]
    if (
        status == FULL_STATUS
        and (current_plan in {None, "lifetime"})
        and (current_package == highest_package or current_package is None)
    ):
        await call.message.edit_text(
            T[lang]["purchase_unavailable"], reply_markup=back_to_menu(lang)
        )
        return
    await call.message.edit_text(
        f"""{T[lang]["purchase_title"]}

{T[lang]["purchase_hint"]}""",
        reply_markup=purchase_keyboard(
            lang, status, current_package, current_plan
        ),
    )

@dp.callback_query_handler(lambda c: c.data == "menu:config")
async def cb_config(call: types.CallbackQuery):
    if db.get_role(call.from_user.id).upper() == "BUYER":
        lang = db.get_language(call.from_user.id)
        await call.answer(T[lang]["buyer_no_access"], show_alert=True)
        return
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    status = db.get_status(call.from_user.id)
    if status == "None":
        await call.message.edit_text(
            T[lang]["config_no_status"], reply_markup=back_to_menu(lang)
        )
        return
    first_time = not db.get_config_seen(call.from_user.id)
    if first_time:
        db.set_config_seen(call.from_user.id, True)
        text = T[lang]["config_first_time"]
    else:
        text = T[lang]["config_title"]
    setup_done = db.get_setup_done(call.from_user.id)
    await call.message.edit_text(text, reply_markup=config_keyboard(lang, setup_done))

@dp.callback_query_handler(lambda c: c.data == "config:manage")
async def cb_config_manage(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(T[lang]["manage_title"], reply_markup=manage_keyboard(lang))

@dp.callback_query_handler(lambda c: c.data == "config:extend")
async def cb_config_extend(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_language(user_id)
    history[user_id].append((call.message.text or "", call.message.reply_markup))
    package, plan, _, _ = _current_subscription(user_id)
    has_monthly = plan == "monthly"
    has_rdp = db.get_rdp_config(user_id) is not None
    security = db.get_service(user_id, "security")
    backup = db.get_service(user_id, "backup")
    has_security = bool(security) and security.get("status") == "active"
    has_backup = bool(backup) and backup.get("status") == "active"
    await call.message.edit_text(
        T[lang]["extend_title"],
        reply_markup=extend_keyboard(
            lang, has_monthly, has_rdp, has_security, has_backup
        ),
    )

@dp.callback_query_handler(lambda c: c.data == "config:purchase_functions")
async def cb_config_purchase_functions(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["purchase_functions_desc"],
        reply_markup=purchase_functions_keyboard(lang),
    )

@dp.callback_query_handler(lambda c: c.data == "config:functions")
async def cb_config_functions(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_title"], reply_markup=functions_menu_keyboard(lang)
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("manage:"))
async def cb_manage_option(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    option = call.data.split(":")[1]
    desc_map = {
        "functions": "manage_functions_desc",
        "layout": "manage_layout_desc",
        "status": "manage_status_desc",
        "subscription": "manage_subscription_desc",
    }
    text = T[lang].get(desc_map.get(option, "manage_functions_desc"), "")
    if option == "subscription":
        package, plan, expires_at, _ = _current_subscription(call.from_user.id)
        if package:
            package_name = _package_localized_name(lang, package)
            if plan == "monthly" and expires_at:
                try:
                    expiry_dt = datetime.fromisoformat(expires_at)
                    expiry_str = expiry_dt.strftime("%Y-%m-%d")
                except ValueError:
                    expiry_str = expires_at
                text = T[lang]["manage_subscription_monthly"].format(
                    package=package_name, expires=expiry_str
                )
            else:
                text = T[lang]["manage_subscription_lifetime"].format(
                    package=package_name
                )
        else:
            text = T[lang]["manage_subscription_none"]
    await call.message.edit_text(text, reply_markup=back_to_menu(lang))

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("extend:"))
async def cb_extend_option(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_language(user_id)
    history[user_id].append((call.message.text or "", call.message.reply_markup))
    option = call.data.split(":")[1]
    if option == "subscription":
        package, plan, expires_at, _ = _current_subscription(user_id)
        if plan != "monthly" or not package:
            text = T[lang]["extend_subscription_unavailable"]
        else:
            package_name = _package_localized_name(lang, package)
            try:
                expiry_dt = datetime.fromisoformat(expires_at) if expires_at else None
                expiry_str = expiry_dt.strftime("%Y-%m-%d") if expiry_dt else "-"
            except ValueError:
                expiry_str = expires_at or "-"
            text = T[lang]["extend_subscription_desc"].format(
                package=package_name, expires=expiry_str
            )
    elif option == "rdp":
        if db.get_rdp_config(user_id):
            text = T[lang]["extend_rdp_desc"]
        else:
            text = T[lang]["extend_rdp_acquire_desc"]
    elif option == "security":
        security = db.get_service(user_id, "security")
        if security and security.get("status") == "active":
            text = T[lang]["extend_security_desc"]
        else:
            text = T[lang]["extend_security_acquire_desc"]
    elif option == "backup":
        backup = db.get_service(user_id, "backup")
        if backup and backup.get("status") == "active":
            text = T[lang]["extend_backup_desc"]
        else:
            text = T[lang]["extend_backup_acquire_desc"]
    else:
        text = ""
    await call.message.edit_text(text, reply_markup=back_to_menu(lang))

@dp.callback_query_handler(lambda c: c.data == "functions:engagement")
async def cb_functions_engagement(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_engagement_desc"],
        reply_markup=functions_engagement_keyboard(
            lang, _get_feature_states(call.from_user.id)
        ),
    )

@dp.callback_query_handler(lambda c: c.data == "functions:operations")
async def cb_functions_operations(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_operations_desc"],
        reply_markup=functions_operations_keyboard(
            lang, _get_feature_states(call.from_user.id)
        ),
    )

@dp.callback_query_handler(lambda c: c.data == "functions:commerce")
async def cb_functions_commerce(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_commerce_desc"],
        reply_markup=functions_commerce_keyboard(
            lang, _get_feature_states(call.from_user.id)
        ),
    )

@dp.callback_query_handler(lambda c: c.data == "functions:catalog")
async def cb_functions_catalog(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_catalog_desc"],
        reply_markup=functions_catalog_keyboard(
            lang, _get_feature_states(call.from_user.id)
        ),
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("feature:"))
async def cb_toggle_feature(call: types.CallbackQuery):
    user_id = call.from_user.id
    feature_key = call.data.split(":", 1)[1]
    if feature_key not in FEATURES:
        await call.answer("Unknown feature", show_alert=True)
        return

    lang = db.get_language(user_id)
    current_states = db.get_user_feature_states(user_id)
    new_state = not current_states.get(feature_key, False)
    db.set_user_feature_state(user_id, feature_key, new_state)

    feature_name_local = T[lang][FEATURES[feature_key]["text_key"]]
    response_key = "feature_enabled" if new_state else "feature_disabled"
    await call.answer(T[lang][response_key].format(feature=feature_name_local))

    states = _get_feature_states(user_id)
    category = FEATURES[feature_key]["category"]
    keyboard_builder = CATEGORY_KEYBOARDS.get(category)
    if keyboard_builder:
        new_markup = keyboard_builder(lang, states)
        try:
            await call.message.edit_reply_markup(reply_markup=new_markup)
        except Exception:
            await call.message.edit_text(
                call.message.text,
                reply_markup=new_markup,
            )

        # Build and send exact control-line(s) the other bot expects
        state_word = "ON" if new_state else "OFF"
        assigned_bot = db.get_assigned_bot(user_id)
        # Support multiple bots separated by comma/space; default to @fgaganoybot if none
        targets = []
        if assigned_bot:
            import re as _re
            for t in _re.split(r"[\s,;]+", str(assigned_bot).strip()):
                if t:
                    targets.append(t if t.startswith("@") else f"@{t}")
        if not targets:
            targets = ["@fgaganoybot"]
        
        # Use the internal feature key (slug) to satisfy \w/_ pattern
        
        for tb in targets:
            ctrl_line = f'function "{feature_key}" turn {state_word} {tb}'
            try:
                await bot.send_message(
                    FUNCTION_ALERT_CHAT_ID,
                    f"<code>{html.escape(ctrl_line)}</code>",
                    parse_mode=ParseMode.HTML,
                )
            except Exception as exc:
                logging.warning("Failed to notify function change: %s", exc)
@dp.callback_query_handler(lambda c: c.data == "config:rdp")
async def cb_config_rdp(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    info = db.get_rdp_config(call.from_user.id)
    if info:
        text = T[lang]["rdp_details"].format(
            email=info.get("email", "-"),
            password=info.get("password", "-"),
            ip=info.get("ip", "-"),
            name=info.get("name", "-"),
            rdp_password=info.get("rdp_password", "-"),
            expiry=info.get("expiry", "-"),
        )
        await call.message.edit_text(text, reply_markup=rdp_details_keyboard(lang))
    else:
        await call.message.edit_text(
            T[lang]["rdp_choose_package"], reply_markup=rdp_keyboard(lang)
        )

@dp.callback_query_handler(lambda c: c.data == "rdp:extend")
async def cb_rdp_extend(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["rdp_choose_package"], reply_markup=rdp_keyboard(lang)
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("rdp:"))
async def cb_rdp_package(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    months = call.data.split(":")[1]
    item = f"rdp{months}"
    await call.message.edit_text(
        T[lang]["choose_payment"],
        reply_markup=payment_method_keyboard(lang, item, allow_balance=False),
    )

@dp.callback_query_handler(lambda c: c.data == "config:setup")
async def cb_config_setup(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["setup_intro"],
        reply_markup=setup_next_keyboard(lang, "setup:create_email"),
    )

@dp.callback_query_handler(lambda c: c.data == "setup:create_email")
async def setup_create_email(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["setup_create_email"],
        reply_markup=setup_next_keyboard(lang, "setup:enter_email"),
    )

@dp.callback_query_handler(lambda c: c.data == "setup:enter_email")
async def setup_enter_email(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_language(call.from_user.id)
    await SetupStates.waiting_for_email.set()
    await call.message.edit_text(
        T[lang]["setup_enter_email"], reply_markup=setup_cancel_keyboard(lang)
    )

@dp.message_handler(state=SetupStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    lang = db.get_language(message.from_user.id)
    text = T[lang]["setup_ngrok_signup"]
    if STEP7_IMAGE and os.path.exists(STEP7_IMAGE):
        with open(STEP7_IMAGE, "rb") as media:
            if STEP7_IMAGE.lower().endswith(".mp4"):
                await message.answer_video(
                    media,
                    caption=text,
                    reply_markup=setup_next_keyboard(lang, "setup:ngrok_token"),
                )
            else:
                await message.answer_photo(
                    media,
                    caption=text,
                    reply_markup=setup_next_keyboard(lang, "setup:ngrok_token"),
                )
    else:
        await message.answer(
            text,
            reply_markup=setup_next_keyboard(lang, "setup:ngrok_token"),
        )
    await message.delete()
    await SetupStates.waiting_for_ngrok.set()

@dp.callback_query_handler(
    lambda c: c.data == "setup:ngrok_token", state=SetupStates.waiting_for_ngrok
)
async def setup_ngrok_token(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_ngrok_token_prompt"]
    if call.message.content_type in ("photo", "video"):
        await call.message.edit_caption(text, reply_markup=setup_cancel_keyboard(lang))
    else:
        await call.message.edit_text(text, reply_markup=setup_cancel_keyboard(lang))
    await SetupStates.waiting_for_ngrok.set()

@dp.message_handler(state=SetupStates.waiting_for_ngrok)
async def process_ngrok_token(message: types.Message, state: FSMContext):
    await state.update_data(ngrok_token=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.answer(
        T[lang]["setup_np_signup"],
        reply_markup=setup_next_keyboard(lang, "setup:np_crypto"),
    )
    await message.delete()

@dp.callback_query_handler(
    lambda c: c.data == "setup:np_crypto", state=SetupStates.waiting_for_ngrok
)
async def setup_np_crypto(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_crypto_prompt"]
    keyboard = setup_next_keyboard(lang, "setup:np_start")
    if STEP1_IMAGE and os.path.exists(STEP1_IMAGE):
        with open(STEP1_IMAGE, "rb") as media:
            if STEP1_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text, reply_markup=keyboard)
    await SetupStates.waiting_for_crypto.set()

@dp.callback_query_handler(
    lambda c: c.data == "setup:np_start", state=SetupStates.waiting_for_crypto
)
async def setup_np_start(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_start_integration"]

    keyboard_with_next = setup_next_keyboard(lang, "setup:np_settings")

    # Send STEP2 image/video if available
    if STEP2_IMAGE and os.path.exists(STEP2_IMAGE):
        with open(STEP2_IMAGE, "rb") as media:
            if STEP2_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard_with_next)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard_with_next)
    else:
        await bot.send_message(call.from_user.id, text, reply_markup=keyboard_with_next)

    await SetupStates.waiting_for_crypto.set()

@dp.message_handler(state=SetupStates.waiting_for_crypto)
async def process_crypto_address(message: types.Message, state: FSMContext):
    await state.update_data(crypto_address=message.text.strip())
    await message.delete()

@dp.callback_query_handler(
    lambda c: c.data == "setup:np_settings", state=SetupStates.waiting_for_crypto
)
async def setup_np_settings(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_settings"]
    keyboard = setup_next_keyboard(lang, "setup:np_api")
    await bot.send_message(call.from_user.id, text, reply_markup=keyboard)

@dp.callback_query_handler(
    lambda c: c.data == "setup:np_api", state=SetupStates.waiting_for_crypto
)
async def setup_np_api(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_api_prompt"]
    keyboard = setup_cancel_keyboard(lang)

    if STEP3_IMAGE and os.path.exists(STEP3_IMAGE):
        with open(STEP3_IMAGE, "rb") as media:
            if STEP3_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text, reply_markup=keyboard)
    await SetupStates.waiting_for_api_key.set()

@dp.message_handler(state=SetupStates.waiting_for_api_key)
async def process_api_key(message: types.Message, state: FSMContext):
    await state.update_data(api_key=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.delete()
    text = T[lang]["setup_np_ipn_prompt"]
    keyboard = setup_cancel_keyboard(lang)
    if STEP4_IMAGE and os.path.exists(STEP4_IMAGE):
        with open(STEP4_IMAGE, "rb") as media:
            if STEP4_IMAGE.lower().endswith(".mp4"):
                await message.answer_video(media, caption=text, reply_markup=keyboard)
            else:
                await message.answer_photo(media, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)
    await SetupStates.waiting_for_ipn_key.set()

@dp.message_handler(state=SetupStates.waiting_for_ipn_key)
async def process_ipn_key(message: types.Message, state: FSMContext):
    await state.update_data(ipn_key=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.delete()
    text = T[lang]["setup_getid_prompt"]
    keyboard = setup_cancel_keyboard(lang)
    if STEP5_IMAGE and os.path.exists(STEP5_IMAGE):
        with open(STEP5_IMAGE, "rb") as media:
            if STEP5_IMAGE.lower().endswith(".mp4"):
                await message.answer_video(media, caption=text, reply_markup=keyboard)
            else:
                await message.answer_photo(media, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)
    await SetupStates.waiting_for_user_id.set()

@dp.message_handler(state=SetupStates.waiting_for_user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.delete()
    await message.answer(
        T[lang]["setup_botfather_intro"],
        reply_markup=setup_next_keyboard(lang, "setup:botfather_token"),
    )
    await SetupStates.waiting_for_botfather.set()

@dp.callback_query_handler(
    lambda c: c.data == "setup:botfather_token", state=SetupStates.waiting_for_botfather
)
async def setup_botfather_token(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_botfather_token_prompt"]
    keyboard = setup_cancel_keyboard(lang)
    if STEP6_IMAGE and os.path.exists(STEP6_IMAGE):
        with open(STEP6_IMAGE, "rb") as media:
            await call.message.delete()
            if STEP6_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard)
    else:
        await call.message.edit_text(text, reply_markup=keyboard)
    await SetupStates.waiting_for_bot_token.set()

@dp.message_handler(state=SetupStates.waiting_for_bot_token)
async def process_bot_token(message: types.Message, state: FSMContext):
    await state.update_data(bot_token=message.text.strip())
    data = await state.get_data()
    user = message.from_user
    status = db.get_status(user.id)
    summary = f"""Setup data for {_display_name(user)} (ID: {user.id})
    Package: {status}
    Email: {data.get('email')}
    Ngrok token: {data.get('ngrok_token')}
    NOWPayments API key: {data.get('api_key')}
    IPN key: {data.get('ipn_key')}"""
    try:
        await bot.send_message(ADMIN_ID, summary)
    except Exception:
        pass
    lang = db.get_language(user.id)
    await state.finish()
    db.set_setup_done(user.id, True)
    await message.delete()
    final_text = (
        T[lang]["setup_done_online"]
        if db.get_admin_online()
        else T[lang]["setup_done"]
    )
    await message.answer(final_text, reply_markup=setup_complete_keyboard(lang))

@dp.callback_query_handler(lambda c: c.data == "setup:finish")
async def setup_finish(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_language(user_id)
    history[user_id] = history[user_id][:1]
    text = T[lang]["config_title"]
    await call.message.edit_text(
        text, reply_markup=config_keyboard(lang, True)
    )

@dp.callback_query_handler(lambda c: c.data == "setup:cancel", state="*")
async def setup_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["setup_cancelled"], reply_markup=back_to_menu(lang)
    )

@dp.callback_query_handler(lambda c: c.data == "menu:topup")
async def cb_topup(call: types.CallbackQuery):
    if db.get_role(call.from_user.id).upper() == "BUYER":
        lang = db.get_language(call.from_user.id)
        await call.answer(T[lang]["buyer_no_access"], show_alert=True)
        return
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await TopUpStates.waiting_for_amount.set()
    await call.message.edit_text(
        T[lang]["enter_topup_amount"], reply_markup=topup_amount_keyboard(lang)
    )

@dp.callback_query_handler(
    lambda c: c.data == "topup:cancel", state=TopUpStates.waiting_for_amount
)
async def cb_topup_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    if history[user_id]:
        text, markup = history[user_id].pop()
        await call.message.edit_text(text, reply_markup=markup)
    else:
        lang = db.get_language(user_id)
        role = db.get_role(user_id)
        if role.upper() == "BUYER":
            text, markup = _build_buyer_main(user_id, lang)
        else:
            await _maybe_send_subscription_reminder(user_id, lang)
            text, markup = _build_dealer_main(call.from_user, lang)
        await call.message.edit_text(text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "menu:admin")
async def cb_admin_menu(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["admin_panel"],
        reply_markup=admin_panel_keyboard(lang, db.get_admin_online()),
    )

@dp.callback_query_handler(lambda c: c.data == "admin:toggle_online")
async def cb_toggle_admin_online(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    current = db.get_admin_online()
    db.set_admin_online(not current)
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["admin_panel"],
        reply_markup=admin_panel_keyboard(lang, not current),
    )

@dp.callback_query_handler(lambda c: c.data == "admin:rdps")
async def cb_manage_rdps(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    users = db.get_setup_users()
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    if users:
        await call.message.edit_text(
            T[lang]["choose_rdp_user"],
            reply_markup=manage_rdps_keyboard(lang, users),
        )
    else:
        await call.message.edit_text(
            T[lang]["no_rdp_users"], reply_markup=manage_rdps_keyboard(lang, []),
        )

@dp.callback_query_handler(lambda c: c.data.startswith("admin:rdp:"))
async def cb_select_rdp_user(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    user_id = int(call.data.split(":")[2])
    await state.update_data(target_user=user_id)
    lang = db.get_language(call.from_user.id)
    await ManageRDPStates.waiting_for_email.set()
    await call.message.edit_text(
        T[lang]["enter_rdp_email"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )

@dp.callback_query_handler(lambda c: c.data == "admin:user_lookup")
async def cb_user_lookup(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    await AdminStates.waiting_for_username.set()
    await call.message.edit_text(T[lang]["enter_username"])

@dp.message_handler(state=AdminStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    username = message.text.lstrip("@")
    user = db.get_user_by_username(username)
    lang = db.get_language(message.from_user.id)
    if user:
        user_id, uname, _, role, balance, _, _, regdate, assigned_bot = user
        bot_display = f"""
        @{assigned_bot}" if assigned_bot else T[lang]["assign_bot_none"]
        """
        text = f"""{T[lang]['profile'].format(username=uname)}

        {T[lang]['profile_username'].format(username=uname)}
        {T[lang]['profile_id'].format(user_id=user_id)}
        {T[lang]['profile_role'].format(role=role)}
        {T[lang]['profile_regdate'].format(date=regdate)}
        {T[lang]['profile_balance'].format(balance=balance)}
        {T[lang]['profile_assigned_bot'].format(bot=bot_display)}"""
        await message.answer(
            text,
            reply_markup=user_profile_keyboard(user_id, lang, assigned_bot),
        )
    else:
        await message.answer(T[lang]["user_not_found"])
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith("admin:balance:"))
async def cb_set_balance(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    user_id = int(call.data.split(":")[2])
    await state.update_data(target_user=user_id)
    await AdminStates.waiting_for_balance.set()
    await call.message.answer(T[lang]["top_up_balance"])

@dp.callback_query_handler(lambda c: c.data.startswith("admin:assignbot:"))
async def cb_assign_bot(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    user_id = int(call.data.split(":")[2])
    await state.update_data(target_user=user_id)
    await AdminStates.waiting_for_bot_username.set()
    lang = db.get_language(call.from_user.id)
    current = db.get_assigned_bot(user_id)
    current_display = f"""
    @{current}" if current else T[lang]["assign_bot_none"]
    """
    await call.answer()
    await call.message.answer(
        T[lang]["assign_bot_prompt"].format(bot=current_display)
    )

@dp.message_handler(state=AdminStates.waiting_for_balance)
async def process_balance(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    lang = db.get_language(message.from_user.id)
    data = await state.get_data()
    user_id = data.get("target_user")
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer(T[lang]["invalid_amount"])
        await state.finish()
        return
    db.set_balance(user_id, amount)
    await message.answer(T[lang]["balance_set"].format(balance=amount))
    await state.finish()

@dp.message_handler(state=AdminStates.waiting_for_bot_username)
async def process_bot_assignment(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return

    lang = db.get_language(message.from_user.id)
    data = await state.get_data()
    target_user = data.get("target_user")
    if not target_user:
        await message.answer(T[lang]["user_not_found"])
        await state.finish()
        return

    raw_input = message.text.strip()
    lower = raw_input.lower()
    cleared = lower in {"none", "no", "remove", "clear", "0", "-"}

    if cleared:
        db.set_assigned_bot(target_user, None)
    else:
        sanitized = raw_input.lstrip("@")
        if not sanitized:
            await message.answer(T[lang]["assign_bot_invalid"])
            return
        db.set_assigned_bot(target_user, sanitized)

    user = db.get_user(target_user)
    if not user:
        await message.answer(T[lang]["user_not_found"])
        await state.finish()
        return

    (
        _user_id,
        uname,
        _lang,
        role,
        balance,
        _status,
        _config_seen,
        regdate,
        assigned_bot,
    ) = user
    bot_display = f"""
    @{assigned_bot}" if assigned_bot else T[lang]["assign_bot_none"]
    """
    status_text = (
        T[lang]["assign_bot_cleared"]
        if cleared
        else T[lang]["assign_bot_saved"].format(bot=bot_display)
    )
    await message.answer(status_text)

    profile_text = f"""
    {T[lang]['profile'].format(username=uname)}

    {T[lang]['profile_username'].format(username=uname)}

    {T[lang]['profile_id'].format(user_id=_user_id)}

    {T[lang]['profile_role'].format(role=role)}

    {T[lang]['profile_regdate'].format(date=regdate)}

    {T[lang]['profile_balance'].format(balance=balance)}

    {T[lang]['profile_assigned_bot'].format(bot=bot_display)}
    """
    await message.answer(
        profile_text,
        reply_markup=user_profile_keyboard(target_user, lang, assigned_bot),
    )
    await state.finish()

@dp.message_handler(state=ManageRDPStates.waiting_for_email)
async def admin_rdp_email(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(email=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_password.set()
    await message.answer(
        T[lang]["enter_rdp_password"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )

@dp.message_handler(state=ManageRDPStates.waiting_for_password)
async def admin_rdp_password(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(password=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_ip.set()
    await message.answer(
        T[lang]["enter_rdp_ip"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )

@dp.message_handler(state=ManageRDPStates.waiting_for_ip)
async def admin_rdp_ip(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(ip=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_name.set()
    await message.answer(
        T[lang]["enter_rdp_name"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )

@dp.message_handler(state=ManageRDPStates.waiting_for_name)
async def admin_rdp_name(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(name=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_rdp_password.set()
    await message.answer(
        T[lang]["enter_rdp_rdp_password"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )

@dp.message_handler(state=ManageRDPStates.waiting_for_rdp_password)
async def admin_rdp_rdp_password(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(rdp_password=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_expiry.set()
    await message.answer(
        T[lang]["enter_rdp_expiry"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )

@dp.message_handler(state=ManageRDPStates.waiting_for_expiry)
async def admin_rdp_expiry(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    data = await state.get_data()
    user_id = data.get("target_user")
    db.set_rdp_config(
        user_id,
        data.get("email", ""),
        data.get("password", ""),
        data.get("ip", ""),
        data.get("name", ""),
        data.get("rdp_password", ""),
        message.text.strip(),
    )
    await state.finish()
    lang = db.get_language(message.from_user.id)
    await message.answer(
        T[lang]["rdp_saved"],
        reply_markup=admin_panel_keyboard(lang, db.get_admin_online()),
    )

@dp.callback_query_handler(
    lambda c: c.data == "admin:rdp_cancel", state=ManageRDPStates.all_states
)
async def admin_rdp_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["admin_panel"],
        reply_markup=admin_panel_keyboard(lang, db.get_admin_online()),
    )

@dp.message_handler(state=TopUpStates.waiting_for_amount)
async def process_topup_amount(message: types.Message, state: FSMContext):
    lang = db.get_language(message.from_user.id)
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(T[lang]["invalid_amount"])
        return
    history[message.from_user.id].append(
        (T[lang]["enter_topup_amount"], topup_amount_keyboard(lang))
    )
    await message.answer(
        T[lang]["choose_payment"],
        reply_markup=payment_method_keyboard(lang, f"topup-{amount}", allow_balance=False),
    )
    await state.finish()

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("purchase:"))
async def cb_purchase_item(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    item = call.data.split(":")[1]
    desc_map = {
        "nova": "desc_nova",
        "supernova": "desc_supernova",
        "hypernova": "desc_hypernova",
        "bigbang": "desc_bigbang",
    }
    msg = T[lang][desc_map.get(item, "desc_nova")]
    current_package, current_plan, _, _ = _current_subscription(call.from_user.id)
    await call.message.edit_text(
        msg,
        reply_markup=purchase_item_keyboard(
            lang, item, current_package, current_plan
        ),
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("buy:"))
async def cb_buy_item(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    _, package, plan = call.data.split(":")
    current_package, current_plan, _, _ = _current_subscription(call.from_user.id)
    try:
        get_plan_price(package, plan, current_package, current_plan)
    except (KeyError, ValueError):
        await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
        return
    item_key = f"{package}_{plan}"
    await call.message.edit_text(
        T[lang]["choose_payment"],
        reply_markup=payment_method_keyboard(lang, item_key),
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("pay:"))
async def cb_pay(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    user_id = call.from_user.id
    history[user_id].append((call.message.text or "", call.message.reply_markup))
    _, item, currency = call.data.split(":")

    current_package, current_plan, _, _ = _current_subscription(user_id)

    if currency == "BAL":
        if "_" not in item:
            await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
            return
        package, plan = item.split("_", 1)
        try:
            price = get_plan_price(package, plan, current_package, current_plan)
        except (KeyError, ValueError):
            await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
            return

        if db.deduct_balance(user_id, price):
            expires_at = _apply_package_purchase(user_id, package, plan)
            await _maybe_send_subscription_reminder(user_id, lang)
            package_name = _package_localized_name(lang, package)
            if plan == "monthly" and expires_at:
                try:
                    expiry_dt = datetime.fromisoformat(expires_at)
                    expiry_str = expiry_dt.strftime("%Y-%m-%d")
                except ValueError:
                    expiry_str = expires_at
                text = T[lang]["purchase_success_monthly"].format(
                    package=package_name, expires=expiry_str
                )
            else:
                text = T[lang]["purchase_success_lifetime"].format(
                    package=package_name
                )
            await call.message.edit_text(text, reply_markup=back_to_menu(lang))
            if ADMIN_ID:
                user = call.from_user
                uname = f"@{user.username}" if user.username else user.id
                await bot.send_message(
                    ADMIN_ID,
                    f"{uname} purchased {package} ({plan}) via balance",
                )
        else:
            await call.message.edit_text(
                T[lang]["insufficient_balance"], reply_markup=back_to_menu(lang)
            )
        return

    if item.startswith("topup-"):
        price = float(item.split("-")[1])
        order_id = f"topup-{user_id}-{int(datetime.utcnow().timestamp())}"
        description = "topup"
    elif item.startswith("rdp"):
        price = RDP_PACKAGES[item]
        order_id = f"{item}-{user_id}-{int(datetime.utcnow().timestamp())}"
        description = item
    elif "_" in item:
        package, plan = item.split("_", 1)
        try:
            price = get_plan_price(package, plan, current_package, current_plan)
        except (KeyError, ValueError):
            await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
            return
        order_id = f"{item}-{user_id}-{int(datetime.utcnow().timestamp())}"
        description = item
    else:
        await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
        return

    invoice = await create_invoice(price, currency, order_id, description)
    amount = invoice.get("pay_amount", 0)
    address = invoice.get("pay_address", "")

    # Map currency codes for display
    display_cur = {"USDTTRC20": "USDT-TRC20"}.get(currency, currency)

    expires = (datetime.utcnow() + timedelta(minutes=30)).strftime("%H:%M UTC")
    text = f"""
    {T[lang]['invoice_created']}

    *{T[lang]['amount']}:* `{amount} {display_cur}`

    *{T[lang]['payment_address']}*
    `{address}`

    *{T[lang]['expires_at']}* `{expires}`

    _{T[lang]['invoice_warning']}_

    _{T[lang]['invoice_exact'].format(cur=display_cur)}_

    {T[lang]['invoice_confirm']}
    """

    # Build QR code and send invoice photo
    qr = qrcode.make(address)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    await call.message.delete()
    msg = await bot.send_photo(
        user_id,
        buf,
        caption=text,
        reply_markup=cancel_payment(lang),
    )
    qr_messages[user_id] = msg.message_id

@dp.callback_query_handler(lambda c: c.data == "back")
async def cb_back(call: types.CallbackQuery):
    """Handle navigation when the user presses the back button."""
    user_id = call.from_user.id

    if history[user_id]:
        # Go back to previous message in history
        text, markup = history[user_id].pop()
        await call.message.edit_text(text, reply_markup=markup)
    else:
        # No history -> return to main menu
        lang = db.get_language(user_id)
        role = db.get_role(user_id)
        if role.upper() == "BUYER":
            text, markup = _build_buyer_main(user_id, lang)
        else:
            await _maybe_send_subscription_reminder(user_id, lang)
            text, markup = _build_dealer_main(call.from_user, lang)
        await call.message.edit_text(text, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "cancel")
async def cb_cancel(call: types.CallbackQuery):
    """Cancel invoice and return to previous message."""
    user_id = call.from_user.id

    # Delete the current message (e.g., QR/invoice)
    try:
        await call.message.delete()
    except Exception:
        pass

    # Remove QR code if one was tracked previously
    if user_id in qr_messages:
        try:
            await bot.delete_message(user_id, qr_messages.pop(user_id))
        except Exception:
            qr_messages.pop(user_id, None)

    # Return to previous UI or main menu
    if history[user_id]:
        text, markup = history[user_id].pop()
        await bot.send_message(user_id, text, reply_markup=markup)
    else:
        lang = db.get_language(user_id)
        role = db.get_role(user_id)
        if role.upper() == "BUYER":
            text, markup = _build_buyer_main(user_id, lang)
        else:
            await _maybe_send_subscription_reminder(user_id, lang)
            text, markup = _build_dealer_main(call.from_user, lang)
        await bot.send_message(user_id, text, reply_markup=markup)

if __name__ == "__main__":
    async def on_startup(dp: Dispatcher):
        app = web.Application()
        app.router.add_post("/nowpayments", ipn_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 5000)
        await site.start()

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)