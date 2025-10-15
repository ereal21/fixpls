
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    SUPPORT_USERNAME,
    DEFAULT_CURRENCY,
    RDP_PACKAGES,
    PACKAGE_ORDER,
    STATUS_TO_PACKAGE,
    PACKAGE_PRICING,
    get_plan_price,
)
from texts import T
from typing import Optional, List, Tuple, Dict

def language_keyboard(lang: Optional[str] = None):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("🇬🇧 EN", callback_data="lang:en"),
        InlineKeyboardButton("🇷🇺 RU", callback_data="lang:ru"),
        InlineKeyboardButton("🇱🇹 LT", callback_data="lang:lt"),
    )
    if lang:
        kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def role_selection_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(
            "🛍️ Buyer / Покупатель / Pirkėjas", callback_data="role:buyer"
        ),
        InlineKeyboardButton(
            "🛠️ Dealer / Продавец / Pardavėjas", callback_data="role:dealer"
        ),
    )
    return kb

def buyer_menu_keyboard(lang: str):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(T[lang]["buyer_search"], callback_data="buyer:search"))
    kb.add(InlineKeyboardButton(T[lang]["menu_language"], callback_data="menu:lang"))
    kb.add(
        InlineKeyboardButton(
            T[lang]["menu_support"], url=f"https://t.me/{SUPPORT_USERNAME}"
        )
    )
    return kb

def dealer_main_menu_keyboard(
    lang: str, is_admin: bool = False, show_purchase: bool = True
):
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    if show_purchase:
        buttons.append(
            InlineKeyboardButton(T[lang]["menu_purchase"], callback_data="menu:purchase")
        )
    buttons.extend(
        [
            InlineKeyboardButton(T[lang]["menu_config"], callback_data="menu:config"),
            InlineKeyboardButton(T[lang]["menu_topup"], callback_data="menu:topup"),
            InlineKeyboardButton(
                T[lang]["menu_support"], url=f"https://t.me/{SUPPORT_USERNAME}"
            ),
            InlineKeyboardButton(T[lang]["menu_language"], callback_data="menu:lang"),
        ]
    )
    kb.add(*buttons)
    if is_admin:
        kb.add(InlineKeyboardButton(T[lang]["menu_admin"], callback_data="menu:admin"))
    return kb

def config_keyboard(lang: str, setup_done: bool):
    kb = InlineKeyboardMarkup(row_width=1)
    if setup_done:
        kb.add(InlineKeyboardButton(T[lang]["config_rdp"], callback_data="config:rdp"))
    else:
        kb.add(InlineKeyboardButton(T[lang]["config_setup"], callback_data="config:setup"))
    kb.add(InlineKeyboardButton(T[lang]["config_manage"], callback_data="config:manage"))
    kb.add(InlineKeyboardButton(T[lang]["config_extend"], callback_data="config:extend"))
    kb.add(
        InlineKeyboardButton(
            T[lang]["config_purchase_functions"], callback_data="config:purchase_functions"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["config_functions"], callback_data="config:functions"))
    kb.add(
        InlineKeyboardButton(
            T[lang]["config_support"], url=f"https://t.me/{SUPPORT_USERNAME}"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def functions_menu_keyboard(lang: str):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            T[lang]["functions_engagement"], callback_data="functions:engagement"
        )
    )
    kb.add(
        InlineKeyboardButton(
            T[lang]["functions_operations"], callback_data="functions:operations"
        )
    )
    kb.add(
        InlineKeyboardButton(
            T[lang]["functions_commerce"], callback_data="functions:commerce"
        )
    )
    kb.add(
        InlineKeyboardButton(
            T[lang]["functions_catalog"], callback_data="functions:catalog"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def _indicator(enabled: bool) -> str:
    return "[V]" if enabled else "[X]"

def functions_engagement_keyboard(lang: str, feature_states: Dict[str, bool]):
    kb = InlineKeyboardMarkup(row_width=1)
    for feature in (
        "blackjack",
        "coinflip",
        "achievements",
        "quests",
        "gift",
        "lottery",
        "leaderboard",
    ):
        kb.add(
            InlineKeyboardButton(
                f"{_indicator(feature_states.get(feature, False))} "
                f"{T[lang][f'feature_{feature}']}",
                callback_data=f"feature:{feature}",
            )
        )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def functions_operations_keyboard(lang: str, feature_states: Dict[str, bool]):
    kb = InlineKeyboardMarkup(row_width=1)
    for feature in ("assistant", "broadcast", "analytics"):
        kb.add(
            InlineKeyboardButton(
                f"{_indicator(feature_states.get(feature, False))} "
                f"{T[lang][f'feature_{feature}']}",
                callback_data=f"feature:{feature}",
            )
        )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def functions_commerce_keyboard(lang: str, feature_states: Dict[str, bool]):
    kb = InlineKeyboardMarkup(row_width=1)
    for feature in (
        "stock_alerts",
        "promocodes",
        "reservations",
        "product_types",
        "manual_payments",
        "crypto_payments",
    ):
        kb.add(
            InlineKeyboardButton(
                f"{_indicator(feature_states.get(feature, False))} "
                f"{T[lang][f'feature_{feature}']}",
                callback_data=f"feature:{feature}",
            )
        )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def functions_catalog_keyboard(lang: str, feature_states: Dict[str, bool]):
    kb = InlineKeyboardMarkup(row_width=1)
    for feature in ("locations", "reviews", "media_library"):
        kb.add(
            InlineKeyboardButton(
                f"{_indicator(feature_states.get(feature, False))} "
                f"{T[lang][f'feature_{feature}']}",
                callback_data=f"feature:{feature}",
            )
        )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def manage_keyboard(lang: str):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            T[lang]["manage_functions"], callback_data="manage:functions"
        )
    )
    kb.add(
        InlineKeyboardButton(T[lang]["manage_layout"], callback_data="manage:layout")
    )
    kb.add(
        InlineKeyboardButton(T[lang]["manage_status"], callback_data="manage:status")
    )
    kb.add(
        InlineKeyboardButton(
            T[lang]["manage_subscription"], callback_data="manage:subscription"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def extend_keyboard(
    lang: str,
    has_monthly: bool,
    has_rdp: bool,
    has_security: bool,
    has_backup: bool,
):
    kb = InlineKeyboardMarkup(row_width=1)
    if has_monthly:
        kb.add(
            InlineKeyboardButton(
                T[lang]["extend_subscription"], callback_data="extend:subscription"
            )
        )

    rdp_key = "extend_rdp_have" if has_rdp else "extend_rdp_acquire"
    kb.add(InlineKeyboardButton(T[lang][rdp_key], callback_data="extend:rdp"))

    security_key = "extend_security_have" if has_security else "extend_security_acquire"
    kb.add(InlineKeyboardButton(T[lang][security_key], callback_data="extend:security"))

    backup_key = "extend_backup_have" if has_backup else "extend_backup_acquire"
    kb.add(InlineKeyboardButton(T[lang][backup_key], callback_data="extend:backup"))

    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def purchase_functions_keyboard(lang: str):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            T[lang]["config_support"], url=f"https://t.me/{SUPPORT_USERNAME}"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def setup_next_keyboard(lang: str, next_cb: str):
    return (
        InlineKeyboardMarkup(row_width=2)
        .add(
            InlineKeyboardButton(T[lang]["next"], callback_data=next_cb),
            InlineKeyboardButton(T[lang]["cancel"], callback_data="setup:cancel"),
        )
    )

def setup_cancel_keyboard(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="setup:cancel")
    )

def setup_complete_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(T[lang]["complete"], callback_data="setup:finish")
    )

def purchase_keyboard(
    lang: str,
    status: str,
    current_package: Optional[str],
    current_plan: Optional[str],
):
    cur = DEFAULT_CURRENCY
    kb = InlineKeyboardMarkup(row_width=1)

    skip_until_index = -1
    if current_plan == "lifetime" and current_package:
        try:
            skip_until_index = PACKAGE_ORDER.index(current_package)
        except ValueError:
            skip_until_index = -1

    label_map = {
        "nova": "purchase_nova",
        "supernova": "purchase_supernova",
        "hypernova": "purchase_hypernova",
        "bigbang": "purchase_bigbang",
    }

    for idx, package in enumerate(PACKAGE_ORDER):
        if skip_until_index != -1 and idx <= skip_until_index:
            continue
        pricing = PACKAGE_PRICING[package]
        kb.add(
            InlineKeyboardButton(
                T[lang][label_map[package]].format(
                    monthly=pricing["monthly"], lifetime=pricing["lifetime"], cur=cur
                ),
                callback_data=f"purchase:{package}",
            )
        )

    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def rdp_keyboard(lang: str):
    cur = DEFAULT_CURRENCY
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            T[lang]["rdp_1m"].format(price=RDP_PACKAGES["rdp1"], cur=cur),
            callback_data="rdp:1",
        ),
        InlineKeyboardButton(
            T[lang]["rdp_2m"].format(price=RDP_PACKAGES["rdp2"], cur=cur),
            callback_data="rdp:2",
        ),
        InlineKeyboardButton(
            T[lang]["rdp_3m"].format(price=RDP_PACKAGES["rdp3"], cur=cur),
            callback_data="rdp:3",
        ),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )

def purchase_item_keyboard(
    lang: str,
    package: str,
    current_package: Optional[str],
    current_plan: Optional[str],
):
    kb = InlineKeyboardMarkup(row_width=1)
    monthly_price = get_plan_price(package, "monthly", current_package, current_plan)
    kb.add(
        InlineKeyboardButton(
            T[lang]["plan_monthly"].format(price=monthly_price, cur=DEFAULT_CURRENCY),
            callback_data=f"buy:{package}:monthly",
        )
    )
    try:
        lifetime_price = get_plan_price(
            package, "lifetime", current_package, current_plan
        )
        if lifetime_price > 0:
            kb.add(
                InlineKeyboardButton(
                    T[lang]["plan_lifetime"].format(
                        price=lifetime_price, cur=DEFAULT_CURRENCY
                    ),
                    callback_data=f"buy:{package}:lifetime",
                )
            )
    except ValueError:
        pass

    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def payment_method_keyboard(lang: str, item: str, allow_balance: bool = True):
    """Return keyboard with available payment methods."""

    kb = InlineKeyboardMarkup(row_width=1)
    if allow_balance:
        kb.add(
            InlineKeyboardButton(
                T[lang]["pay_with_balance"], callback_data=f"pay:{item}:BAL"
            )
        )
    kb.add(
        InlineKeyboardButton("🪙 SOL", callback_data=f"pay:{item}:SOL"),
        InlineKeyboardButton("🪙 USDT-TRC20", callback_data=f"pay:{item}:USDTTRC20"),
        InlineKeyboardButton("🪙 XMR", callback_data=f"pay:{item}:XMR"),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )
    return kb

def back_to_menu(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["back"], callback_data="back")
    )

def cancel_payment(lang: str):
    """Keyboard with cancel button for invoice screen."""

    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="cancel")
    )

def admin_panel_keyboard(lang: str, online: bool):
    toggle = (
        T[lang]["admin_set_offline"]
        if online
        else T[lang]["admin_set_online"]
    )
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(toggle, callback_data="admin:toggle_online"))
    kb.add(InlineKeyboardButton(T[lang]["user_lookup"], callback_data="admin:user_lookup"))
    kb.add(InlineKeyboardButton(T[lang]["manage_rdps"], callback_data="admin:rdps"))
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def user_profile_keyboard(
    user_id: int, lang: str, assigned_bot: Optional[str] = None
):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            "💰 " + T[lang]["top_up_balance"], callback_data=f"admin:balance:{user_id}"
        )
    )
    current = (
        f"@{assigned_bot}" if assigned_bot else T[lang]["assign_bot_none"]
    )
    kb.add(
        InlineKeyboardButton(
            f"🤖 {T[lang]['assign_bot_button'].format(bot=current)}",
            callback_data=f"admin:assignbot:{user_id}",
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="menu:admin"))
    return kb

def topup_amount_keyboard(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="topup:cancel")
    )

def rdp_details_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(T[lang]["extend"], callback_data="rdp:extend"),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )

def manage_rdps_keyboard(lang: str, users: List[Tuple[int, Optional[str]]]):
    kb = InlineKeyboardMarkup(row_width=1)
    for user_id, username in users:
        name = f"@{username}" if username else str(user_id)
        kb.add(InlineKeyboardButton(name, callback_data=f"admin:rdp:{user_id}"))
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def admin_rdp_cancel_keyboard(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="admin:rdp_cancel")
    )
