from typing import Dict

T: Dict[str, Dict[str, str]] = {
    "en": {
        "choose_language": "🌐 *Choose your language:*",
        "main_title": (
            "✨ *Welcome {name}* 👋\n\n"
            "🪪 *Status:* _{status}_\n"
            "🤖 *Bots owned:* _0_\n"
            "💰 *Balance:* _€{balance}_"
        ),
        "role_prompt": (
            "🌌 *Welcome!*\n"
            "Choose whether you are buying or managing a shop."
        ),
        "menu_purchase": "🛒 Purchase",
        "menu_config": "⚙️ Config",
        "menu_topup": "➕ Top up",
        "menu_support": "🆘 Support",
        "menu_language": "🌐 Language",
        "buyer_main_title": (
            "🔍 *Buyer's menu*\n"
            "Use *Search* to browse offers or contact support for assistance."
        ),
        "buyer_search": "🔎 Search",
        "buyer_search_desc": (
            "🔎 *Search instructions*\n"
            "Send keywords to the dealer to receive the latest catalogs and prices."
        ),
        "buyer_no_access": "⚠️ Only dealers can open this section.",
        "purchase_title": "🛍️ *Choose your galaxy tier:*",
        "purchase_nova": "🌟 Nova — {monthly} {cur}/mo • {lifetime} {cur} lifetime",
        "purchase_supernova": "✨ Supernova — {monthly} {cur}/mo • {lifetime} {cur} lifetime",
        "purchase_hypernova": "🚀 Hypernova — {monthly} {cur}/mo • {lifetime} {cur} lifetime",
        "purchase_bigbang": "🌠 Big Bang — {monthly} {cur}/mo • {lifetime} {cur} lifetime",
        "desc_nova": (
            "🌟 *Nova*\n"
            "• Template storefront ready to launch with curated copy and visuals.\n"
            "• Automated catalog, order tracking, and instant customer notifications.\n"
            "• Includes starter analytics and anti-spam protection.\n"
            "• Monthly subscription: 109€ — extend anytime.\n"
            "• Lifetime buyout: 349€ — own the bot forever."
        ),
        "desc_supernova": (
            "✨ *Supernova*\n"
            "• Premium template plus the ability to enable six advanced features on demand.\n"
            "• Everything in Nova plus assistant management and advanced user levels.\n"
            "• Priority feature updates and custom onboarding.\n"
            "• Monthly subscription: 189€.\n"
            "• Lifetime buyout: 479€."
        ),
        "desc_hypernova": (
            "🚀 *Hypernova*\n"
            "• Unlock every feature, choose bespoke UI themes, and swap layouts anytime.\n"
            "• Premium automation, stock alerts, and hands-on optimization sessions.\n"
            "• Includes enhanced security stack and backup automations.\n"
            "• Monthly subscription: 249€.\n"
            "• Lifetime buyout: 699€."
        ),
        "desc_bigbang": (
            "🌠 *Big Bang*\n"
            "• Bespoke build — you co-design the bot and I craft it from scratch.\n"
            "• First month onboarding is 400€; that credit deducts from the lifetime fee, so upgrading later costs just 499€ (899€ − 400€).\n"
            "• After onboarding you can continue service for 249€/mo loyalty renewals instead of buying out.\n"
            "• Lifetime buyout: 899€."
        ),
        "purchase_hint": (
            "💡 *Tap a tier to explore details, then pick monthly or lifetime.*"
        ),
        "buy": "💳 Purchase",
        "choose_payment": "💰 *Choose payment method:*",
        "invoice_created": "🧾 *Payment Invoice Created*",
        "amount": "Amount",
        "payment_address": "🏦 Payment Address:",
        "expires_at": "⏳ Expires At:",
        "invoice_warning": "⚠️ Payment must be completed within 30 minutes of invoice creation.",
        "invoice_exact": "❗️ Important: Send exactly this amount of {cur}.",
        "invoice_confirm": "✅ Confirmation is automatic via webhook after network confirmation.",
        "enter_topup_amount": "💶 Enter the amount to top up:",
        "invalid_amount": "❌ Invalid amount",
        "pay_with_balance": "💳 Pay with balance",
        "insufficient_balance": "❌ Insufficient balance. Please top up.",
        "purchase_success": "✅ Payment received! Go to *Config* to set up your bot.",
        "purchase_success_monthly": "✅ {package} monthly plan activated! Next renewal on {expires}.",
        "purchase_success_lifetime": "✅ {package} lifetime unlocked! Enjoy permanent access.",
        "subscription_reminder": "⏳ Your {package} monthly plan expires on {expires}. Renew to stay online.",
        "purchase_unavailable": "✅ You already own this package or a higher tier.",
        "config_first_time": (
            "🎉 *Welcome to settings!*\n"
            "It's your first time here. Tap *Set Up* below to configure your bot or contact support."
        ),
        "config_title": "⚙️ *Bot settings:*",
        "config_no_status": "🛑 *Purchase a bot to access settings.*",
        "config_setup": "🛠 Set Up",
        "config_rdp": "🖥 RDP",
        "config_manage": "🧭 Manage",
        "config_extend": "🔁 Extend",
        "config_purchase_functions": "🛠 Purchase functions",
        "config_functions": "🧩 Functions",
        "config_support": "🆘 Support",
        "manage_title": "🧭 *Management hub:* Pick what you want to adjust.",
        "manage_functions": "🧩 Manage functions",
        "manage_layout": "🛍️ Manage shop layout",
        "manage_status": "📡 Manage bot status",
        "manage_subscription": "🧾 Manage subscription",
        "manage_functions_desc": (
            "🧩 *Manage functions*\n"
            "Toggle individual modules, request tweaks, and keep your automation sharp."
        ),
        "manage_layout_desc": (
            "🛍️ *Manage shop layout*\n"
            "Update categories, banners, and customer flows with guided checklists."
        ),
        "manage_status_desc": (
            "📡 *Manage bot status*\n"
            "Switch between online/offline modes, schedule maintenance, and set alerts."
        ),
        "manage_subscription_desc": (
            "🧾 *Manage subscription*\n"
            "Review your active plan, request upgrades, or message support for billing changes."
        ),
        "manage_subscription_monthly": (
            "🧾 *Subscription details*\n"
            "You are on the {package} monthly plan. Current cycle ends on {expires}."
        ),
        "manage_subscription_lifetime": (
            "🧾 *Subscription details*\n"
            "You own the {package} lifetime license. No renewals required."
        ),
        "manage_subscription_none": (
            "🧾 *Subscription details*\n"
            "No active subscription yet. Purchase a tier to unlock management tools."
        ),
        "extend_title": "🔁 *Extend or acquire services:*",
        "extend_subscription": "🧾 Extend subscription",
        "extend_rdp_have": "🖥 Extend RDP server",
        "extend_rdp_acquire": "🖥 Acquire RDP server",
        "extend_security_have": "🛡 Extend security features",
        "extend_security_acquire": "🛡 Acquire security features",
        "extend_backup_have": "💽 Extend backup",
        "extend_backup_acquire": "💽 Acquire backup",
        "extend_subscription_desc": (
            "🧾 *Extend subscription*\n"
            "Your {package} monthly plan renews on {expires}. Pay early to add 30 days instantly."
        ),
        "extend_subscription_unavailable": (
            "ℹ️ Monthly renewals are only available if you have an active monthly plan."
        ),
        "extend_rdp_desc": (
            "🖥 *Extend RDP server*\n"
            "Renew your remote desktop to keep the infrastructure running without downtime."
        ),
        "extend_rdp_acquire_desc": (
            "🖥 *Acquire RDP server*\n"
            "Get a dedicated RDP server with hardened security and preinstalled tools."
        ),
        "extend_security_desc": (
            "🛡 *Extend security features*\n"
            "Refresh your protection bundle to keep anti-fraud shields up to date."
        ),
        "extend_security_acquire_desc": (
            "🛡 *Acquire security features*\n"
            "Enable advanced filtering, 2FA, and leak monitoring for your shop."
        ),
        "extend_backup_desc": (
            "💽 *Extend backup*\n"
            "Ensure daily encrypted backups continue without interruption."
        ),
        "extend_backup_acquire_desc": (
            "💽 *Acquire backup*\n"
            "Activate automatic backups with rapid restore support."
        ),
        "purchase_functions_desc": (
            "🛠️ *Need extra features?*\n"
            "Contact support to order custom automations, integrations, and unique flows."
        ),
        "plan_monthly": "📆 Monthly — {price} {cur}",
        "plan_lifetime": "♾️ Lifetime — {price} {cur}",
        "package_name_nova": "Nova",
        "package_name_supernova": "Supernova",
        "package_name_hypernova": "Hypernova",
        "package_name_bigbang": "Big Bang",
        "functions_title": "🧩 *Choose a function category:*",
        "functions_engagement": "🎮 Engagement & games",
        "functions_operations": "🧑‍💼 Operations",
        "functions_commerce": "💼 Commerce & payments",
        "functions_catalog": "🗂 Catalog & presence",
        "functions_engagement_desc": "🎮 *Engagement & games*\nTurn on interactive experiences to boost retention.",
        "functions_operations_desc": "🧑‍💼 *Operations*\nAutomate your team's workflows and messaging.",
        "functions_commerce_desc": "💼 *Commerce & payments*\nManage sales flows, alerts, and payment handling.",
        "functions_catalog_desc": "🗂 *Catalog & presence*\nKeep listings, media, and locations organised.",
        "feature_blackjack": "🂡 Blackjack",
        "feature_coinflip": "🪙 Coinflip",
        "feature_achievements": "🏆 Achievements",
        "feature_quests": "🧭 Quests",
        "feature_gift": "🎁 Gift",
        "feature_lottery": "🎟 Lottery",
        "feature_leaderboard": "🏁 Leaderboard",
        "feature_assistant": "🤖 Assistant",
        "feature_broadcast": "📢 Broadcast",
        "feature_analytics": "📊 Analytics",
        "feature_stock_alerts": "📈 Stock alerts",
        "feature_promocodes": "🏷️ Promo codes",
        "feature_reservations": "🗓 Reservations",
        "feature_product_types": "🧩 Product types",
        "feature_manual_payments": "💵 Manual payments",
        "feature_crypto_payments": "🪙 Crypto payments",
        "feature_locations": "📍 Locations",
        "feature_reviews": "⭐ Reviews",
        "feature_media_library": "🗂 Media library",
        "feature_enabled": "✅ \"{feature}\" turned ON.",
        "feature_disabled": "❌ \"{feature}\" turned OFF.",
        "coming_soon": "🚧 *This feature is disabled for now.*",
        "rdp_choose_package": "🖥 *Choose your RDP package:*",
        "rdp_1m": "1️⃣ 1 Month ({price} {cur})",
        "rdp_2m": "2️⃣ 2 Months ({price} {cur})",
        "rdp_3m": "3️⃣ 3 Months ({price} {cur})",
        "rdp_payment_success": "✅ *Payment received!* RDP details will be sent to you soon.",
        "back": "⬅️ Back",
        "cancel": "❌ Cancel",
        "support_button": "💬 Contact Support",
        "lang_en": "English",
        "lang_ru": "Русский",
        "lang_lt": "Lietuvių",
        "language_changed": "✅ Language changed to *{lang}*.",
        "menu_admin": "🛡 Admin Panel",
        "admin_panel": "🛡 *Admin Panel*",
        "admin_set_online": "Online",
        "admin_set_offline": "Offline",
        "user_lookup": "🔍 User lookup",
        "enter_username": "👤 Enter the user username to view or edit their data",
        "profile": "👤 Profile — {username}",
        "profile_username": "👤 Username — @{username}",
        "profile_id": "🆔 ID — {user_id}",
        "profile_role": "🎛 Role — {role}",
        "profile_regdate": "🕢 Registration date — {date}",
        "profile_balance": "💰 Balance — {balance}",
        "profile_assigned_bot": "🤖 Assigned bot — {bot}",
        "assign_bot_none": "None",
        "assign_bot_button": "Assign bot (current: {bot})",
        "assign_bot_prompt": (
            "🤖 Send the bot username to assign to this user (e.g. @myshopbot).\n"
            "Send 'none' to clear the current assignment.\n"
            "Current: {bot}"
        ),
        "assign_bot_saved": "✅ Assigned bot {bot} to the user.",
        "assign_bot_cleared": "✅ Cleared the bot assignment.",
        "assign_bot_invalid": "❌ Please provide a valid bot username or 'none'.",
        "top_up_balance": "Top up user's balance",
        "balance_set": "✅ Balance set to {balance}",
        "user_not_found": "❌ User not found",
        "manage_rdps": "🖥 Manage RDPs",
        "choose_rdp_user": "👤 Choose a user:",
        "enter_rdp_email": "📧 Enter RDP email:",
        "enter_rdp_password": "🔑 Enter email password:",
        "enter_rdp_ip": "🌐 Enter RDP IP:",
        "enter_rdp_name": "👤 Enter RDP name:",
        "enter_rdp_rdp_password": "🔒 Enter RDP password:",
        "enter_rdp_expiry": "📅 Enter expiry date:",
        "rdp_saved": "✅ RDP info saved.",
        "rdp_details": (
            "🖥 *Your RDP:*\n"
            "📧 Email: {email}\n"
            "🔑 Password: {password}\n"
            "🌐 IP: {ip}\n"
            "👤 Name: {name}\n"
            "🔒 RDP Password: {rdp_password}\n"
            "⏳ Expires: {expiry}"
        ),
        "extend": "🔄 Extend",
        "no_rdp_users": "❌ No users available",
        "next": "➡️ Next",
        "complete": "✅ Complete",
        "setup_intro": (
            "ℹ️ *To set up the bot you must fill in some details.* "
            "Follow the instructions carefully, otherwise the bot might not work."
        ),
        "setup_create_email": (
            "📧 *Create a new email.* You can use [inbox.lv](https://login.inbox.lv/signup?redirect_url=https://www.inbox.lv/), "
            "[inbox.lt](https://login.inbox.lt/signup?redirect_url=https://www.inbox.lt/) or "
            "[gmail.com](https://support.google.com/mail/answer/56256?hl=en)."
        ),
        "setup_enter_email": "✉️ *Enter the email you created:*",
        "setup_ngrok_signup": "🌐 *Register at [ngrok](https://dashboard.ngrok.com/signup).* Once registered, go to *Your Authtoken* and press *Copy*. Then press *Next*.",
        "setup_ngrok_token_prompt": "🔐 *Paste the Auth-Token you copied here:*",
        "setup_np_signup": (
            "🧾 *Sign up at [NOWPayments](https://account.nowpayments.io/create-account) with your new email.* "
            "Use the email you created, set a password, then confirm with the code sent to that address."
        ),
        "setup_np_crypto_prompt": "💰 *Enter the crypto address where you want to receive funds:*",
        "setup_np_start_integration": "⚙️ Click *Start integration*, set currency to *EUR*, select *Sender*, then press *Skip for now*.",
        "setup_np_settings": "🛠️ Go to *Settings* → *Payments*, then press *Next*.",
        "setup_np_api_prompt": "🔑 Go to *API keys* and send your API key here.",
        "setup_np_ipn_prompt": "📨 Go to *Instant payment notifications*, generate an IPN secret key and send it here.",
        "setup_getid_prompt": "🆔 *Open @GetIDcnBot, press Start, copy your ID and send it here.*",
        "setup_botfather_intro": "🤖 *Go to @BotFather, type /newbot and follow the instructions.* Then press *Next*.",
        "setup_botfather_token_prompt": "📮 *Copy the API code that is sent.*",
        "setup_cancelled": "❌ *Setup cancelled.*",
        "setup_done": "🎉 *Setup data sent to admin. Thank you!*",
        "setup_done_online": "🎉 Set up is complete, the owner is online your information was sent, and the bot will be turned on soon",
            "feature_blackjack": "🂡 Blackjack",
        "feature_coinflip": "🪙 Coinflip",
        "feature_achievements": "🏆 Achievements",
        "feature_quests": "🧭 Quests",
        "feature_gift": "🎁 Gift",
        "feature_stock_alerts": "📈 Stock alerts",
        "feature_broadcast": "📢 Broadcast",
        "feature_lottery": "🎟 Lottery",
        "feature_leaderboard": "🏁 Leaderboard",
        "feature_promocodes": "🏷️ Promo codes",
        "feature_analytics": "📊 Analytics",
        "feature_locations": "📍 Locations",
        "feature_product_types": "🧩 Product types",
        "feature_reviews": "⭐ Reviews",
        "feature_reservations": "🗓 Reservations",
        "feature_manual_payments": "💵 Manual payments",
        "feature_media_library": "🗂 Media library",
        "feature_crypto_payments": "🪙 Crypto payments",
},
    "ru": {
        "choose_language": "🌐 *Выберите язык:*",
        "main_title": (
            "✨ *Добро пожаловать, {name}* 👋\n\n"
            "🪪 *Статус:* _{status}_\n"
            "🤖 *Ботов куплено:* _0_\n"
            "💰 *Баланс:* _€{balance}_"
        ),
        "role_prompt": (
            "🌌 *Добро пожаловать!*\n"
            "Выберите, покупаете вы или управляете магазином."
        ),
        "menu_purchase": "🛒 Покупка",
        "menu_config": "⚙️ Настройки",
        "menu_topup": "➕ Пополнить",
        "menu_support": "🆘 Поддержка",
        "menu_language": "🌐 Язык",
        "buyer_main_title": (
            "🔍 *Меню покупателя*\n"
            "Используйте *Поиск*, чтобы получить актуальные каталоги, или свяжитесь с поддержкой."
        ),
        "buyer_search": "🔎 Поиск",
        "buyer_search_desc": (
            "🔎 *Как искать*\n"
            "Отправьте дилеру ключевые слова, и он пришлёт свежие позиции и цены."
        ),
        "buyer_no_access": "⚠️ Этот раздел доступен только дилерам.",
        "purchase_title": "🛍️ *Выберите уровень:*",
        "purchase_nova": "🌟 Nova — {monthly} {cur}/мес • {lifetime} {cur} навсегда",
        "purchase_supernova": "✨ Supernova — {monthly} {cur}/мес • {lifetime} {cur} навсегда",
        "purchase_hypernova": "🚀 Hypernova — {monthly} {cur}/мес • {lifetime} {cur} навсегда",
        "purchase_bigbang": "🌠 Big Bang — {monthly} {cur}/мес • {lifetime} {cur} навсегда",
        "desc_nova": (
            "🌟 *Nova*\n"
            "• Готовый шаблон магазина с подобранными текстами и визуалом.\n"
            "• Автоматизированный каталог, отслеживание заказов и мгновенные уведомления.\n"
            "• Базовая аналитика и антиспам входят в комплект.\n"
            "• Подписка: 109€ в месяц.\n"
            "• Пожизненный доступ: 349€."
        ),
        "desc_supernova": (
            "✨ *Supernova*\n"
            "• Улучшенный шаблон и возможность включить шесть продвинутых функций по запросу.\n"
            "• Всё из Nova плюс управление ассистентами и уровни пользователей.\n"
            "• Приоритетные обновления и персональное подключение.\n"
            "• Подписка: 189€ в месяц.\n"
            "• Пожизненный доступ: 479€."
        ),
        "desc_hypernova": (
            "🚀 *Hypernova*\n"
            "• Доступ ко всем функциям, подбор уникальных UI-тем и возможность менять интерфейсы в любой момент.\n"
            "• Продвинутые автоматизации, оповещения по складу и сессии оптимизации.\n"
            "• Усиленный пакет безопасности и резервирования.\n"
            "• Подписка: 249€ в месяц.\n"
            "• Пожизненный доступ: 699€."
        ),
        "desc_bigbang": (
            "🌠 *Big Bang*\n"
            "• Полностью индивидуальная разработка: вы задаёте концепцию, а я собираю бота с нуля.\n"
            "• Первый месяц стоит 400€; эта сумма вычитается из цены выкупа, поэтому перейти на пожизненный доступ можно за 499€ (899€ − 400€).\n"
            "• После онбординга можно продлевать сервис по лояльной цене 249€/мес вместо покупки выкупа.\n"
            "• Пожизненный доступ: 899€."
        ),
        "purchase_hint": (
            "💡 *Нажмите на уровень, чтобы увидеть детали, затем выберите помесячно или навсегда.*"
        ),
        "buy": "💳 Купить",
        "choose_payment": "💰 *Выберите способ оплаты:*",
        "invoice_created": "🧾 *Счёт на оплату создан*",
        "amount": "Сумма",
        "payment_address": "🏦 Платёжный адрес:",
        "expires_at": "⏳ Истекает в:",
        "invoice_warning": "⚠️ Оплата должна быть завершена в течение 30 минут после создания счёта.",
        "invoice_exact": "❗️ Важно: Отправьте ровно эту сумму {cur}.",
        "invoice_confirm": "✅ Подтверждение происходит автоматически через вебхук после подтверждения сети.",
        "enter_topup_amount": "💶 Введите сумму пополнения:",
        "invalid_amount": "❌ Неверная сумма",
        "pay_with_balance": "💳 Оплатить с баланса",
        "insufficient_balance": "❌ Недостаточно средств. Пополните баланс.",
        "purchase_success": "✅ Оплата получена! Перейдите в *Настройки*, чтобы настроить бота.",
        "purchase_success_monthly": "✅ Тариф {package} оформлен на месяц! Следующее продление {expires}.",
        "purchase_success_lifetime": "✅ Пожизненный доступ {package} активирован!",
        "subscription_reminder": "⏳ Ваша подписка {package} заканчивается {expires}. Продлите заранее, чтобы избежать простоев.",
        "purchase_unavailable": "✅ Этот пакет уже приобретён или у вас есть более высокий уровень.",
        "config_first_time": (
            "🎉 *Добро пожаловать в настройки!*\n"
            "Вы здесь впервые. Нажмите *Настроить*, чтобы сконфигурировать бота или обратитесь в поддержку."
        ),
        "config_title": "⚙️ *Настройки бота:*",
        "config_no_status": "🛑 *Чтобы получить доступ к настройкам, сначала приобретите бота.*",
        "config_setup": "🛠 Настроить",
        "config_rdp": "🖥 RDP",
        "config_manage": "🧭 Управление",
        "config_extend": "🔁 Продлить",
        "config_purchase_functions": "🛠 Купить функции",
        "config_functions": "🧩 Функции",
        "config_support": "🆘 Поддержка",
        "manage_title": "🧭 *Центр управления:* выберите, что изменить.",
        "manage_functions": "🧩 Управление функциями",
        "manage_layout": "🛍️ Управление витриной",
        "manage_status": "📡 Статус бота",
        "manage_subscription": "🧾 Подписка",
        "manage_functions_desc": (
            "🧩 *Управление функциями*\n"
            "Включайте и отключайте модули, заказывайте доработки и держите автоматизацию в тонусе."
        ),
        "manage_layout_desc": (
            "🛍️ *Управление витриной*\n"
            "Меняйте категории, баннеры и пути клиента по готовым чек-листам."
        ),
        "manage_status_desc": (
            "📡 *Статус бота*\n"
            "Переключайте режим онлайн/оффлайн, планируйте обслуживание и уведомления."
        ),
        "manage_subscription_desc": (
            "🧾 *Подписка*\n"
            "Просматривайте детали плана, запрашивайте переходы или пишите в поддержку для изменения биллинга."
        ),
        "manage_subscription_monthly": (
            "🧾 *Подписка*\n"
            "Вы на месячном плане {package}. Текущий цикл завершается {expires}."
        ),
        "manage_subscription_lifetime": (
            "🧾 *Подписка*\n"
            "У вас пожизненный доступ {package}. Продление не требуется."
        ),
        "manage_subscription_none": (
            "🧾 *Подписка*\n"
            "Активной подписки нет. Приобретите уровень, чтобы открыть управление."
        ),
        "extend_title": "🔁 *Продлить или приобрести сервисы:*",
        "extend_subscription": "🧾 Продлить подписку",
        "extend_rdp_have": "🖥 Продлить RDP-сервер",
        "extend_rdp_acquire": "🖥 Получить RDP-сервер",
        "extend_security_have": "🛡 Продлить защиту",
        "extend_security_acquire": "🛡 Получить защиту",
        "extend_backup_have": "💽 Продлить резервное копирование",
        "extend_backup_acquire": "💽 Получить резервное копирование",
        "extend_subscription_desc": (
            "🧾 *Продлить подписку*\n"
            "Ваш план {package} продлевается {expires}. Оплатите заранее и получите +30 дней сразу."
        ),
        "extend_subscription_unavailable": (
            "ℹ️ Продление доступно только при активной месячной подписке."
        ),
        "extend_rdp_desc": (
            "🖥 *Продлить RDP-сервер*\n"
            "Обновите срок действия удалённого сервера, чтобы избежать простоя."
        ),
        "extend_rdp_acquire_desc": (
            "🖥 *Получить RDP-сервер*\n"
            "Выделенный RDP с усиленной безопасностью и нужными инструментами."
        ),
        "extend_security_desc": (
            "🛡 *Продлить защиту*\n"
            "Продлите пакет антифрода и мониторинга утечек."
        ),
        "extend_security_acquire_desc": (
            "🛡 *Получить защиту*\n"
            "Включите расширенную фильтрацию, 2FA и мониторинг для магазина."
        ),
        "extend_backup_desc": (
            "💽 *Продлить резервное копирование*\n"
            "Обеспечьте продолжение ежедневных зашифрованных бэкапов."
        ),
        "extend_backup_acquire_desc": (
            "💽 *Получить резервное копирование*\n"
            "Активируйте автоматические бэкапы с быстрым восстановлением."
        ),
        "purchase_functions_desc": (
            "🛠️ *Нужны дополнительные функции?*\n"
            "Свяжитесь с поддержкой и закажите индивидуальные автоматизации и интеграции."
        ),
        "plan_monthly": "📆 Помесячно — {price} {cur}",
        "plan_lifetime": "♾️ Навсегда — {price} {cur}",
        "package_name_nova": "Nova",
        "package_name_supernova": "Supernova",
        "package_name_hypernova": "Hypernova",
        "package_name_bigbang": "Big Bang",
        "functions_title": "🧩 *Выберите категорию функций:*",
        "functions_engagement": "🎮 Игры и вовлечение",
        "functions_operations": "🧑‍💼 Операции",
        "functions_commerce": "💼 Коммерция и платежи",
        "functions_catalog": "🗂 Каталог и присутствие",
        "functions_engagement_desc": "🎮 *Игры и вовлечение*\nВключайте интерактивы, чтобы удерживать аудиторию.",
        "functions_operations_desc": "🧑‍💼 *Операции*\nАвтоматизируйте работу команды и рассылки.",
        "functions_commerce_desc": "💼 *Коммерция и платежи*\nУправляйте продажами, уведомлениями и приёмом оплат.",
        "functions_catalog_desc": "🗂 *Каталог и присутствие*\nСледите за медиатекой, отзывами и адресами.",
        "feature_blackjack": "🂡 Блэкджек",
        "feature_coinflip": "🪙 Орёл или решка",
        "feature_achievements": "🏆 Достижения",
        "feature_quests": "🧭 Квесты",
        "feature_gift": "🎁 Подарки",
        "feature_lottery": "🎟 Лотерея",
        "feature_leaderboard": "🏁 Таблица лидеров",
        "feature_assistant": "🤖 Ассистент",
        "feature_broadcast": "📢 Рассылка",
        "feature_analytics": "📊 Аналитика",
        "feature_stock_alerts": "📈 Оповещения о наличии",
        "feature_promocodes": "🏷️ Промокоды",
        "feature_reservations": "🗓 Бронирования",
        "feature_product_types": "🧩 Типы товаров",
        "feature_manual_payments": "💵 Ручные платежи",
        "feature_crypto_payments": "🪙 Криптоплатежи",
        "feature_locations": "📍 Локации",
        "feature_reviews": "⭐ Отзывы",
        "feature_media_library": "🗂 Медиа-библиотека",
        "feature_enabled": "✅ \"{feature}\" включена.",
        "feature_disabled": "❌ \"{feature}\" выключена.",
        "coming_soon": "🚧 *Эта функция отключена.*",
        "rdp_choose_package": "🖥 *Выберите пакет RDP:*",
        "rdp_1m": "1️⃣ 1 месяц ({price} {cur})",
        "rdp_2m": "2️⃣ 2 месяца ({price} {cur})",
        "rdp_3m": "3️⃣ 3 месяца ({price} {cur})",
        "rdp_payment_success": "✅ *Оплата получена!* Данные RDP будут отправлены вам вскоре.",
        "back": "⬅️ Назад",
        "cancel": "❌ Отменить",
        "support_button": "💬 Связаться с поддержкой",
        "lang_en": "English",
        "lang_ru": "Русский",
        "lang_lt": "Lietuvių",
        "language_changed": "✅ Язык изменён на *{lang}*.",
        "menu_admin": "🛡 Панель админа",
        "admin_panel": "🛡 *Панель администратора*",
        "admin_set_online": "Онлайн",
        "admin_set_offline": "Оффлайн",
        "user_lookup": "🔍 Поиск пользователя",
        "enter_username": "👤 Введите имя пользователя для просмотра или редактирования данных",
        "profile": "👤 Профиль — {username}",
        "profile_username": "👤 Имя пользователя — @{username}",
        "profile_id": "🆔 ID — {user_id}",
        "profile_role": "🎛 Роль — {role}",
        "profile_regdate": "🕢 Дата регистрации — {date}",
        "profile_balance": "💰 Баланс — {balance}",
        "profile_assigned_bot": "🤖 Назначенный бот — {bot}",
        "assign_bot_none": "Нет",
        "assign_bot_button": "Назначить бота (сейчас: {bot})",
        "assign_bot_prompt": (
            "🤖 Отправьте юзернейм бота для назначения (например, @myshopbot).\n"
            "Отправьте 'none', чтобы убрать назначение.\n"
            "Текущий бот: {bot}"
        ),
        "assign_bot_saved": "✅ Бот {bot} назначен пользователю.",
        "assign_bot_cleared": "✅ Назначение бота удалено.",
        "assign_bot_invalid": "❌ Укажите корректное имя бота или 'none'.",
        "top_up_balance": "Пополнить баланс пользователя",
        "balance_set": "✅ Баланс установлен на {balance}",
        "user_not_found": "❌ Пользователь не найден",
        "manage_rdps": "🖥 Управление RDP",
        "choose_rdp_user": "👤 Выберите пользователя:",
        "enter_rdp_email": "📧 Введите RDP email:",
        "enter_rdp_password": "🔑 Введите пароль от email:",
        "enter_rdp_ip": "🌐 Введите IP RDP:",
        "enter_rdp_name": "👤 Введите имя RDP:",
        "enter_rdp_rdp_password": "🔒 Введите пароль RDP:",
        "enter_rdp_expiry": "📅 Введите дату окончания:",
        "rdp_saved": "✅ Данные RDP сохранены.",
        "rdp_details": (
            "🖥 *Ваш RDP:*\n"
            "📧 Email: {email}\n"
            "🔑 Пароль: {password}\n"
            "🌐 IP: {ip}\n"
            "👤 Имя: {name}\n"
            "🔒 Пароль RDP: {rdp_password}\n"
            "⏳ Истекает: {expiry}"
        ),
        "extend": "🔄 Продлить",
        "no_rdp_users": "❌ Пользователи отсутствуют",
        "next": "➡️ Далее",
        "complete": "✅ Готово",
        "setup_intro": (
            "ℹ️ *Для настройки бота необходимо заполнить данные.* "
            "Следуйте инструкциям тщательно, иначе бот может не работать."
        ),
        "setup_create_email": (
            "📧 *Создайте новый email.* Можно использовать [inbox.lv](https://login.inbox.lv/signup?redirect_url=https://www.inbox.lv/), "
            "[inbox.lt](https://login.inbox.lt/signup?redirect_url=https://www.inbox.lt/) или "
            "[gmail.com](https://support.google.com/mail/answer/56256?hl=en)."
        ),
        "setup_enter_email": "✉️ *Введите созданный email:*",
        "setup_ngrok_signup": "🌐 *Зарегистрируйтесь на [ngrok](https://dashboard.ngrok.com/signup).* После регистрации перейдите в *Your Authtoken* и нажмите *Copy*. Затем нажмите *Далее*.",
        "setup_ngrok_token_prompt": "🔐 *Вставьте скопированный Auth-Token сюда:*",
        "setup_np_signup": (
            "🧾 *Зарегистрируйтесь в [NOWPayments](https://account.nowpayments.io/create-account) с новым email.* "
            "Введите созданный адрес, придумайте пароль и подтвердите регистрацию кодом, отправленным на этот же email."
        ),
        "setup_np_crypto_prompt": "💰 *Введите крипто адрес, на который хотите получать средства:*",
        "setup_np_start_integration": "⚙️ Нажмите *Start integration*, установите валюту *EUR*, выберите *Sender* и нажмите *Skip for now*.",
        "setup_np_settings": "🛠️ Перейдите в *Settings* → *Payments*, затем нажмите *Далее*.",
        "setup_np_api_prompt": "🔑 Откройте *API keys* и отправьте сюда свой API ключ.",
        "setup_np_ipn_prompt": "📨 Перейдите в *Instant payment notifications*, сгенерируйте IPN secret key и отправьте его здесь.",
        "setup_getid_prompt": "🆔 *Откройте @GetIDcnBot, нажмите Start, скопируйте свой ID и отправьте здесь.*",
        "setup_botfather_intro": "🤖 *Откройте @BotFather, отправьте /newbot и следуйте инструкциям.* Затем нажмите *Далее*.",
        "setup_botfather_token_prompt": "📮 *Скопируйте отправленный API код.*",
        "setup_cancelled": "❌ *Настройка отменена.*",
        "setup_done": "🎉 *Данные отправлены администратору. Спасибо!*",
        "setup_done_online": "🎉 Настройка завершена, владелец в сети, ваша информация отправлена, бот скоро будет включён",
    },
    "lt": {
        "choose_language": "🌐 *Pasirinkite kalbą:*",
        "main_title": (
            "✨ *Sveikas, {name}* 👋\n\n"
            "🪪 *Statusas:* _{status}_\n"
            "🤖 *Turimų botų:* _0_\n"
            "💰 *Balansas:* _€{balance}_"
        ),
        "role_prompt": (
            "🌌 *Sveiki!*\n"
            "Pasirinkite, ar esate pirkėjas, ar tiekėjas."
        ),
        "menu_purchase": "🛒 Pirkti",
        "menu_config": "⚙️ Nustatymai",
        "menu_topup": "➕ Papildyti",
        "menu_support": "🆘 Pagalba",
        "menu_language": "🌐 Kalba",
        "buyer_main_title": (
            "🔍 *Pirkėjo meniu*\n"
            "Naudokite *Paieška*, kad peržiūrėtumėte pasiūlymus, arba susisiekite su pagalba."
        ),
        "buyer_search": "🔎 Paieška",
        "buyer_search_desc": (
            "🔎 *Kaip ieškoti*\n"
            "Nusiųskite tiekėjui raktinius žodžius ir gaukite naujausius katalogus bei kainas."
        ),
        "buyer_no_access": "⚠️ Ši sritis skirta tik tiekėjams.",
        "purchase_title": "🛍️ *Pasirinkite lygį:*",
        "purchase_nova": "🌟 Nova — {monthly} {cur}/mėn • {lifetime} {cur} visam laikui",
        "purchase_supernova": "✨ Supernova — {monthly} {cur}/mėn • {lifetime} {cur} visam laikui",
        "purchase_hypernova": "🚀 Hypernova — {monthly} {cur}/mėn • {lifetime} {cur} visam laikui",
        "purchase_bigbang": "🌠 Big Bang — {monthly} {cur}/mėn • {lifetime} {cur} visam laikui",
        "desc_nova": (
            "🌟 *Nova*\n"
            "• Paruoštas šabloninis parduotuvės dizainas su tekstais ir vizualais.\n"
            "• Automatizuotas katalogas, užsakymų sekimas ir momentiniai pranešimai.\n"
            "• Pagrindinė analitika ir anti-spamas įskaičiuoti.\n"
            "• Prenumerata: 109€ per mėnesį.\n"
            "• Vienkartinis išpirkimas: 349€."
        ),
        "desc_supernova": (
            "✨ *Supernova*\n"
            "• Premium šablonas ir galimybė įjungti šešias pažangias funkcijas pagal poreikį.\n"
            "• Visa, kas Nova, plius asistentų valdymas ir vartotojų lygiai.\n"
            "• Prioritetiniai atnaujinimai ir individualus įvedimas.\n"
            "• Prenumerata: 189€ per mėnesį.\n"
            "• Vienkartinis išpirkimas: 479€."
        ),
        "desc_hypernova": (
            "🚀 *Hypernova*\n"
            "• Visos funkcijos, pasirinktinės UI temos ir galimybė keisti išdėstymą bet kada.\n"
            "• Pažangios automatizacijos, atsargų pranešimai ir optimizavimo sesijos.\n"
            "• Sustiprintas saugumas ir atsarginių kopijų automatika.\n"
            "• Prenumerata: 249€ per mėnesį.\n"
            "• Vienkartinis išpirkimas: 699€."
        ),
        "desc_bigbang": (
            "🌠 *Big Bang*\n"
            "• Individualus projektas – kartu kuriame viziją, o botą sukuriu nuo nulio.\n"
            "• Pirmasis mėnuo kainuoja 400€; ši suma atimama iš išpirkimo kainos, todėl pereiti į visam laikui kainuoja 499€ (899€ − 400€).\n"
            "• Po įvedimo galite tęsti mėnesinę paslaugą už 249€/mėn lojalumo tarifą vietoje išpirkimo.\n"
            "• Vienkartinis išpirkimas: 899€."
        ),
        "purchase_hint": (
            "💡 *Bakstelėkite lygį, peržiūrėkite detales ir pasirinkite mėnesinį arba visam laikui.*"
        ),
        "buy": "💳 Pirkti",
        "choose_payment": "💰 *Pasirinkite mokėjimo metodą:*",
        "invoice_created": "🧾 *Sąskaita sukurta*",
        "amount": "Suma",
        "payment_address": "🏦 Mokėjimo adresas:",
        "expires_at": "⏳ Galioja iki:",
        "invoice_warning": "⚠️ Mokėjimą būtina atlikti per 30 minučių nuo sąskaitos sukūrimo.",
        "invoice_exact": "❗️ Svarbu: Siųskite tiksliai tokią {cur} sumą.",
        "invoice_confirm": "✅ Patvirtinimas automatinis per webhook'ą po tinklo patvirtinimo.",
        "enter_topup_amount": "💶 Įveskite papildymo sumą:",
        "invalid_amount": "❌ Neteisinga suma",
        "pay_with_balance": "💳 Mokėti iš balanso",
        "insufficient_balance": "❌ Nepakanka lėšų. Papildykite balansą.",
        "purchase_success": "✅ Mokėjimas gautas! Eikite į *Nustatymai* ir sukonfigūruokite botą.",
        "purchase_success_monthly": "✅ {package} mėnesio planas suaktyvintas! Kitas atnaujinimas {expires}.",
        "purchase_success_lifetime": "✅ {package} visam laikui aktyvuotas!",
        "subscription_reminder": "⏳ Jūsų {package} mėnesio planas baigsis {expires}. Pratęskite iš anksto, kad išvengtumėte pauzių.",
        "purchase_unavailable": "✅ Jūs jau turite šį paketą arba aukštesnį lygį.",
        "config_first_time": (
            "🎉 *Sveiki atvykę į nustatymus!*\n"
            "Jūs čia pirmą kartą. Paspauskite *Nustatyti*, kad sukonfigūruotumėte botą arba susisiekite su pagalba."
        ),
        "config_title": "⚙️ *Boto nustatymai:*",
        "config_no_status": "🛑 *Norėdami pasiekti nustatymus, pirmiausia įsigykite botą.*",
        "config_setup": "🛠 Nustatyti",
        "config_rdp": "🖥 RDP",
        "config_manage": "🧭 Valdymas",
        "config_extend": "🔁 Pratęsti",
        "config_purchase_functions": "🛠 Įsigyti funkcijas",
        "config_functions": "🧩 Funkcijos",
        "config_support": "🆘 Pagalba",
        "manage_title": "🧭 *Valdymo centras:* pasirinkite, ką keisti.",
        "manage_functions": "🧩 Funkcijų valdymas",
        "manage_layout": "🛍️ Parduotuvės išdėstymas",
        "manage_status": "📡 Boto būsena",
        "manage_subscription": "🧾 Prenumerata",
        "manage_functions_desc": (
            "🧩 *Funkcijų valdymas*\n"
            "Įjunkite ar išjunkite modulius, užsakykite patobulinimus ir palaikykite automatizaciją."
        ),
        "manage_layout_desc": (
            "🛍️ *Parduotuvės išdėstymas*\n"
            "Atnaujinkite kategorijas, banerius ir kliento kelią naudodami paruoštus kontrolinius sąrašus."
        ),
        "manage_status_desc": (
            "📡 *Boto būsena*\n"
            "Perjunkite online/offline režimus, suplanuokite priežiūrą ir perspėjimus."
        ),
        "manage_subscription_desc": (
            "🧾 *Prenumerata*\n"
            "Peržiūrėkite aktyvų planą, prašykite pakeitimų arba rašykite pagalbai dėl sąskaitų."
        ),
        "manage_subscription_monthly": (
            "🧾 *Prenumerata*\n"
            "Naudojate {package} mėnesio planą. Dabartinis ciklas baigiasi {expires}."
        ),
        "manage_subscription_lifetime": (
            "🧾 *Prenumerata*\n"
            "Turite {package} visam laikui. Pratęsti nereikia."
        ),
        "manage_subscription_none": (
            "🧾 *Prenumerata*\n"
            "Aktyvios prenumeratos nėra. Įsigykite lygį, kad atsirakintumėte valdymą."
        ),
        "extend_title": "🔁 *Pratęskite ar įsigykite paslaugas:*",
        "extend_subscription": "🧾 Pratęsti prenumeratą",
        "extend_rdp_have": "🖥 Pratęsti RDP serverį",
        "extend_rdp_acquire": "🖥 Įsigyti RDP serverį",
        "extend_security_have": "🛡 Pratęsti apsaugą",
        "extend_security_acquire": "🛡 Įsigyti apsaugą",
        "extend_backup_have": "💽 Pratęsti atsargines kopijas",
        "extend_backup_acquire": "💽 Įsigyti atsargines kopijas",
        "extend_subscription_desc": (
            "🧾 *Pratęsti prenumeratą*\n"
            "Jūsų planas {package} atsinaujins {expires}. Apmokėkite iš anksto ir pridėkite +30 dienų."
        ),
        "extend_subscription_unavailable": (
            "ℹ️ Pratęsti galima tik turint aktyvią mėnesio prenumeratą."
        ),
        "extend_rdp_desc": (
            "🖥 *Pratęsti RDP serverį*\n"
            "Atnaujinkite nuotolinio serverio galiojimą, kad išvengtumėte pertraukų."
        ),
        "extend_rdp_acquire_desc": (
            "🖥 *Įsigyti RDP serverį*\n"
            "Gaukite dedikuotą RDP su sustiprinta apsauga ir reikalingais įrankiais."
        ),
        "extend_security_desc": (
            "🛡 *Pratęsti apsaugą*\n"
            "Atnaujinkite apsaugos paketą, kad antifrodas išliktų aktualus."
        ),
        "extend_security_acquire_desc": (
            "🛡 *Įsigyti apsaugą*\n"
            "Įjunkite pažangią filtraciją, 2FA ir nutekėjimų stebėseną parduotuvei."
        ),
        "extend_backup_desc": (
            "💽 *Pratęsti atsargines kopijas*\n"
            "Užtikrinkite, kad kasdienės šifruotos atsarginės kopijos tęstųsi be pertraukų."
        ),
        "extend_backup_acquire_desc": (
            "💽 *Įsigyti atsargines kopijas*\n"
            "Aktyvuokite automatines kopijas su greitu atkūrimu."
        ),
        "purchase_functions_desc": (
            "🛠️ *Reikia papildomų funkcijų?*\n"
            "Susisiekite su pagalba ir užsakykite individualias integracijas bei automatizacijas."
        ),
        "plan_monthly": "📆 Mėnesinis — {price} {cur}",
        "plan_lifetime": "♾️ Visam laikui — {price} {cur}",
        "package_name_nova": "Nova",
        "package_name_supernova": "Supernova",
        "package_name_hypernova": "Hypernova",
        "package_name_bigbang": "Big Bang",
        "functions_title": "🧩 *Pasirinkite funkcijų kategoriją:*",
        "functions_engagement": "🎮 Įsitraukimas ir žaidimai",
        "functions_operations": "🧑‍💼 Operacijos",
        "functions_commerce": "💼 Komercija ir mokėjimai",
        "functions_catalog": "🗂 Katalogas ir vitrina",
        "functions_engagement_desc": "🎮 *Įsitraukimas ir žaidimai*\nĮjunkite interaktyvius žaidimus ir pramogas.",
        "functions_operations_desc": "🧑‍💼 *Operacijos*\nAutomatizuokite komandos darbą ir pranešimus.",
        "functions_commerce_desc": "💼 *Komercija ir mokėjimai*\nValdykite pardavimus, įspėjimus ir apmokėjimus.",
        "functions_catalog_desc": "🗂 *Katalogas ir vitrina*\nTvarkykite vietas, atsiliepimus ir mediją.",
        "feature_blackjack": "🂡 Blackjack",
        "feature_coinflip": "🪙 Monetos metimas",
        "feature_achievements": "🏆 Pasiekimai",
        "feature_quests": "🧭 Užduotys",
        "feature_gift": "🎁 Dovanų centras",
        "feature_lottery": "🎟 Loterija",
        "feature_leaderboard": "🏁 Lyderių lentelė",
        "feature_assistant": "🤖 Asistentas",
        "feature_broadcast": "📢 Transliacijos",
        "feature_analytics": "📊 Analitika",
        "feature_stock_alerts": "📈 Atsargų įspėjimai",
        "feature_promocodes": "🏷️ Nuolaidų kodai",
        "feature_reservations": "🗓 Rezervacijos",
        "feature_product_types": "🧩 Produktų tipai",
        "feature_manual_payments": "💵 Rankiniai mokėjimai",
        "feature_crypto_payments": "🪙 Kriptomokėjimai",
        "feature_locations": "📍 Lokacijos",
        "feature_reviews": "⭐ Atsiliepimai",
        "feature_media_library": "🗂 Mediateka",
        "feature_enabled": "✅ „{feature}“ įjungta.",
        "feature_disabled": "❌ „{feature}“ išjungta.",
        "coming_soon": "🚧 *Ši funkcija išjungta.*",
        "rdp_choose_package": "🖥 *Pasirinkite RDP paketą:*",
        "rdp_1m": "1️⃣ 1 mėn. ({price} {cur})",
        "rdp_2m": "2️⃣ 2 mėn. ({price} {cur})",
        "rdp_3m": "3️⃣ 3 mėn. ({price} {cur})",
        "rdp_payment_success": "✅ *Mokėjimas gautas!* RDP informacija bus atsiųsta netrukus.",
        "back": "⬅️ Atgal",
        "cancel": "❌ Atšaukti",
        "support_button": "💬 Susisiekti su pagalba",
        "lang_en": "English",
        "lang_ru": "Русский",
        "lang_lt": "Lietuvių",
        "language_changed": "✅ Kalba pakeista į *{lang}*.",
        "menu_admin": "🛡 Admin skydelis",
        "admin_panel": "🛡 *Administratoriaus skydelis*",
        "admin_set_online": "Prisijungęs",
        "admin_set_offline": "Atsijungęs",
        "user_lookup": "🔍 Vartotojo paieška",
        "enter_username": "👤 Įveskite vartotojo naudotojo vardą peržiūrėti ar redaguoti duomenis",
        "profile": "👤 Profilis — {username}",
        "profile_username": "👤 Naudotojo vardas — @{username}",
        "profile_id": "🆔 ID — {user_id}",
        "profile_role": "🎛 Rolė — {role}",
        "profile_regdate": "🕢 Registracijos data — {date}",
        "profile_balance": "💰 Balansas — {balance}",
        "profile_assigned_bot": "🤖 Priskirtas botas — {bot}",
        "assign_bot_none": "Nėra",
        "assign_bot_button": "Priskirti botą (dabar: {bot})",
        "assign_bot_prompt": (
            "🤖 Atsiųskite boto naudotojo vardą priskyrimui (pvz., @myshopbot).\n"
            "Siųskite 'none', jei norite nuimti priskyrimą.\n"
            "Dabartinis: {bot}"
        ),
        "assign_bot_saved": "✅ Botas {bot} priskirtas vartotojui.",
        "assign_bot_cleared": "✅ Boto priskyrimas pašalintas.",
        "assign_bot_invalid": "❌ Įrašykite teisingą boto naudotojo vardą arba 'none'.",
        "top_up_balance": "Papildyti naudotojo balansą",
        "balance_set": "✅ Balansas nustatytas į {balance}",
        "user_not_found": "❌ Vartotojas nerastas",
        "manage_rdps": "🖥 RDP valdymas",
        "choose_rdp_user": "👤 Pasirinkite vartotoją:",
        "enter_rdp_email": "📧 Įveskite RDP el. paštą:",
        "enter_rdp_password": "🔑 Įveskite el. pašto slaptažodį:",
        "enter_rdp_ip": "🌐 Įveskite RDP IP:",
        "enter_rdp_name": "👤 Įveskite RDP vardą:",
        "enter_rdp_rdp_password": "🔒 Įveskite RDP slaptažodį:",
        "enter_rdp_expiry": "📅 Įveskite galiojimo datą:",
        "rdp_saved": "✅ RDP informacija išsaugota.",
        "rdp_details": (
            "🖥 *Jūsų RDP:*\n"
            "📧 El. paštas: {email}\n"
            "🔑 Slaptažodis: {password}\n"
            "🌐 IP: {ip}\n"
            "👤 Vardas: {name}\n"
            "🔒 RDP slaptažodis: {rdp_password}\n"
            "⏳ Galioja iki: {expiry}"
        ),
        "extend": "🔄 Pratęsti",
        "no_rdp_users": "❌ Nėra vartotojų",
        "next": "➡️ Toliau",
        "complete": "✅ Baigti",
        "setup_intro": (
            "ℹ️ *Norint sukonfigūruoti botą, reikia užpildyti keletą duomenų.* "
            "Laikykitės instrukcijų, kitaip botas gali neveikti."
        ),
        "setup_create_email": (
            "📧 *Sukurkite naują el. paštą.* Galite naudoti [inbox.lv](https://login.inbox.lv/signup?redirect_url=https://www.inbox.lv/), "
            "[inbox.lt](https://login.inbox.lt/signup?redirect_url=https://www.inbox.lt/) arba "
            "[gmail.com](https://support.google.com/mail/answer/56256?hl=en)."
        ),
        "setup_enter_email": "✉️ *Įveskite sukurtą el. paštą:*",
        "setup_ngrok_signup": "🌐 *Užsiregistruokite [ngrok](https://dashboard.ngrok.com/signup).* Užsiregistravę eikite į *Your Authtoken* ir paspauskite *Copy*. Tada spauskite *Toliau*.",
        "setup_ngrok_token_prompt": "🔐 *Įklijuokite nukopijuotą Auth-Token čia:*",
        "setup_np_signup": (
            "🧾 *Užsiregistruokite [NOWPayments](https://account.nowpayments.io/create-account) su nauju el. paštu.* "
            "Įveskite sukurtą adresą, susikurkite slaptažodį ir registraciją patvirtinkite kodu, išsiųstu į tą patį el. paštą."
        ),
        "setup_np_crypto_prompt": "💰 *Įveskite kripto adresą, į kurį norite gauti lėšas:*",
        "setup_np_start_integration": "⚙️ Paspauskite *Start integration*, nustatykite valiutą į *EUR*, pasirinkite *Sender* ir spauskite *Skip for now*.",
        "setup_np_settings": "🛠️ Eikite į *Settings* → *Payments* ir spauskite *Toliau*.",
        "setup_np_api_prompt": "🔑 Atsidarykite *API keys* ir atsiųskite čia savo API raktą.",
        "setup_np_ipn_prompt": "📨 Eikite į *Instant payment notifications*, sugeneruokite IPN slaptą raktą ir atsiųskite jį čia.",
        "setup_getid_prompt": "🆔 *Atidarykite @GetIDcnBot, paspauskite Start, nukopijuokite savo ID ir atsiųskite čia.*",
        "setup_botfather_intro": "🤖 *Atidarykite @BotFather, įrašykite /newbot ir sekite instrukcijas.* Tada paspauskite *Next*.",
        "setup_botfather_token_prompt": "📮 *Nukopijuokite atsiųstą API kodą.*",
        "setup_cancelled": "❌ *Nustatymai atšaukti.*",
        "setup_done": "🎉 *Duomenys išsiųsti administratoriui. Ačiū!*",
        "setup_done_online": "🎉 Nustatymas baigtas, savininkas prisijungęs, jūsų informacija išsiųsta ir botas netrukus bus įjungtas",
            "feature_blackjack": "🂡 Blackjack",
        "feature_coinflip": "🪙 Coinflip",
        "feature_achievements": "🏆 Achievements",
        "feature_quests": "🧭 Quests",
        "feature_gift": "🎁 Gift",
        "feature_stock_alerts": "📈 Stock alerts",
        "feature_broadcast": "📢 Broadcast",
        "feature_lottery": "🎟 Lottery",
        "feature_leaderboard": "🏁 Leaderboard",
        "feature_promocodes": "🏷️ Promo codes",
        "feature_analytics": "📊 Analytics",
        "feature_locations": "📍 Locations",
        "feature_product_types": "🧩 Product types",
        "feature_reviews": "⭐ Reviews",
        "feature_reservations": "🗓 Reservations",
        "feature_manual_payments": "💵 Manual payments",
        "feature_media_library": "🗂 Media library",
        "feature_crypto_payments": "🪙 Crypto payments",
},
}
