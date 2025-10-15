
import os
from typing import Optional

from dotenv import load_dotenv

# Load .env files
load_dotenv()
load_dotenv("steps.env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "Inereal").lstrip("@")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "EUR")
DB_PATH = os.getenv("DB_PATH", "bot.db")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
FUNCTION_ALERT_CHAT_ID = int(os.getenv("FUNCTION_ALERT_CHAT_ID", "-4930039742"))

# NowPayments configuration
NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY", "").strip()
NOWPAYMENTS_IPN_URL = os.getenv("NOWPAYMENTS_IPN_URL", "").strip()
NOWPAYMENTS_API_URL = os.getenv("NOWPAYMENTS_API_URL", "https://api.nowpayments.io/v1").rstrip("/")

# Setup step media files (images or videos)
STEP1_IMAGE = os.getenv("STEP1_IMAGE", "").strip()
STEP2_IMAGE = os.getenv("STEP2_IMAGE", "").strip()
STEP3_IMAGE = os.getenv("STEP3_IMAGE", "").strip()
STEP4_IMAGE = os.getenv("STEP4_IMAGE", "").strip()
STEP5_IMAGE = os.getenv("STEP5_IMAGE", "").strip()
STEP6_IMAGE = os.getenv("STEP6_IMAGE", "").strip()
STEP7_IMAGE = os.getenv("STEP7_IMAGE", "").strip()

# Package prices in DEFAULT_CURRENCY
PACKAGE_PRICING = {
    "nova": {"monthly": 109, "lifetime": 349},
    "supernova": {"monthly": 189, "lifetime": 479},
    "hypernova": {"monthly": 249, "lifetime": 699},
    "bigbang": {"monthly": 400, "lifetime": 899},
}

# Package ordering and status mapping
PACKAGE_ORDER = ["nova", "supernova", "hypernova", "bigbang"]
PACKAGE_STATUSES = {
    "nova": "Nova",
    "supernova": "Supernova",
    "hypernova": "Hypernova",
    "bigbang": "Big Bang",
}
STATUS_TO_PACKAGE = {status: package for package, status in PACKAGE_STATUSES.items()}

PLAN_TYPES = ("monthly", "lifetime")

def get_plan_price(
    package: str,
    plan_type: str,
    current_package: Optional[str] = None,
    current_plan: Optional[str] = None,
) -> float:
    """Return payable amount for a package plan considering current ownership."""

    if package not in PACKAGE_PRICING:
        raise KeyError(f"Unknown package: {package}")
    if plan_type not in PLAN_TYPES:
        raise KeyError(f"Unknown plan type: {plan_type}")

    base_price = PACKAGE_PRICING[package][plan_type]

    if not current_package:
        return base_price

    # normalize values to known keys
    if current_package not in PACKAGE_PRICING:
        current_package = None

    if not current_package:
        return base_price

    try:
        current_index = PACKAGE_ORDER.index(current_package)
        target_index = PACKAGE_ORDER.index(package)
    except ValueError:
        return base_price

    if plan_type == "monthly":
        if (
            package == "bigbang"
            and current_package == "bigbang"
            and current_plan == "monthly"
        ):
            # Loyalty renewal for Big Bang after the onboarding month.
            return 249
        # Monthly plans are charged at base price (used for renewals).
        return base_price

    # Lifetime plan logic
    if current_plan == "lifetime":
        if target_index <= current_index:
            raise ValueError("Lifetime upgrade not available for this tier")
        current_price = PACKAGE_PRICING[current_package]["lifetime"]
        return max(base_price - current_price, 0)

    if current_plan == "monthly" and current_package == package:
        # Allow converting monthly to lifetime by deducting the first month payment.
        monthly_price = PACKAGE_PRICING[current_package]["monthly"]
        return max(base_price - monthly_price, 0)

    return base_price

# RDP package prices in DEFAULT_CURRENCY
RDP_PACKAGES = {
    "rdp1": 10,
    "rdp2": 20,
    "rdp3": 30,
}

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Put it in your .env file.")

# Bot tag used in control messages
BOT_TAG = os.getenv('BOT_TAG', '@ParduotuveBot')
