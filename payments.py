import aiohttp
from aiohttp import web
from typing import Dict, Optional
from config import (
    NOWPAYMENTS_API_KEY,
    NOWPAYMENTS_API_URL,
    NOWPAYMENTS_IPN_URL,
    DEFAULT_CURRENCY,
    ADMIN_ID,
    PACKAGE_STATUSES,
    PACKAGE_PRICING,
)
from texts import T
from database import Database
from aiogram import Bot
from datetime import datetime, timedelta

bot: Optional[Bot] = None
db: Optional[Database] = None
qr_messages: Dict[int, int] = {}

def init_payments(bot_obj: Bot, db_obj: Database, qr_dict: Dict[int, int]):
    global bot, db, qr_messages
    bot = bot_obj
    db = db_obj
    qr_messages = qr_dict

async def create_invoice(
    price: float, pay_currency: str, order_id: str, description: str
) -> Dict:
    """Create a payment via NowPayments and return API response."""

    headers = {
        "x-api-key": NOWPAYMENTS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "price_amount": price,
        "price_currency": DEFAULT_CURRENCY,
        "pay_currency": pay_currency,
        "order_id": order_id,
        "order_description": description,
        "ipn_callback_url": NOWPAYMENTS_IPN_URL,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"{NOWPAYMENTS_API_URL}/payment", json=payload) as resp:
            return await resp.json()

async def ipn_handler(request: web.Request):
    data = await request.json()
    status = data.get("payment_status")
    order_id = data.get("order_id", "")
    if status not in {"confirmed", "finished"}:
        return web.Response(text="OK")

    parts = order_id.split("-")
    if len(parts) < 2:
        return web.Response(text="OK")
    item = parts[0]
    try:
        user_id = int(parts[1])
    except ValueError:
        return web.Response(text="OK")

    rdp_map = {"rdp1": "1 month", "rdp2": "2 months", "rdp3": "3 months"}
    package = None
    plan = None
    if "_" in item:
        package, plan = item.split("_", 1)
    elif item in PACKAGE_PRICING:
        package = item
        plan = "lifetime"

    # remove invoice message
    if user_id in qr_messages:
        try:
            await bot.delete_message(user_id, qr_messages.pop(user_id))
        except Exception:
            qr_messages.pop(user_id, None)

    lang = db.get_language(user_id)
    if package in PACKAGE_PRICING:
        plan = plan or "lifetime"
        status_name = PACKAGE_STATUSES.get(package)
        if status_name:
            db.set_status(user_id, status_name)
            db.set_config_seen(user_id, False)
        expires_at = None
        if plan == "monthly":
            expires_at = (datetime.utcnow() + timedelta(days=30)).replace(microsecond=0)
            expires_at = expires_at.isoformat()
        db.set_subscription(user_id, package, plan, expires_at)

        name_key = f"package_name_{package}"
        package_name = T[lang].get(name_key, PACKAGE_STATUSES.get(package, package.title()))
        if plan == "monthly" and expires_at:
            try:
                expiry_dt = datetime.fromisoformat(expires_at)
                expiry_str = expiry_dt.strftime("%Y-%m-%d")
            except ValueError:
                expiry_str = expires_at
            message = T[lang]["purchase_success_monthly"].format(
                package=package_name, expires=expiry_str
            )
        else:
            message = T[lang]["purchase_success_lifetime"].format(
                package=package_name
            )
        await bot.send_message(user_id, message)
    elif item in rdp_map:
        await bot.send_message(user_id, T[lang]["rdp_payment_success"])
    else:
        return web.Response(text="OK")

    if ADMIN_ID:
        user = db.get_user(user_id)
        uname = user[1] if user and user[1] else str(user_id)
        if package in PACKAGE_PRICING:
            await bot.send_message(
                ADMIN_ID,
                f"{uname} (ID {user_id}) purchased {package} ({plan}) package",
            )
        elif item in rdp_map:
            amount = data.get("price_amount", "")
            months = rdp_map[item]
            await bot.send_message(
                ADMIN_ID,
                f"{uname} (ID {user_id}) purchased RDP {months} for {amount} {DEFAULT_CURRENCY}",
            )

    return web.Response(text="OK")
