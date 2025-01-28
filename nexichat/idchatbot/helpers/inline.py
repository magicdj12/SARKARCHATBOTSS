from pyrogram.types import InlineKeyboardButton
from config import SUPPORT_GRP, UPDATE_CHNL
from nexichat import OWNER, nexichat

# دکمه‌های شروع
START_BOT = [
    [
        InlineKeyboardButton(text="🛠️ دستورات ربات ⚙️", callback_data="HELP"),
    ],
]

# دکمه‌های اصلی
DEV_OP = [
    [
        InlineKeyboardButton(
            text="✦ افزودن به گروه ✦",
            url=f"https://t.me/{nexichat.username}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="« راهنما »", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="☁️ درباره ما ☁️", callback_data="ABOUT"),
    ],
]

# دکمه‌های منوی اصلی
PNG_BTN = [
    [
        InlineKeyboardButton(text="🛠️ مشاهده دستورات ⚙️", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(
            text="⦿ بستن ⦿",
            callback_data="CLOSE",
        ),
    ],
]

# دکمه برگشت
BACK = [
    [
        InlineKeyboardButton(text="⦿ برگشت ⦿", callback_data="BACK"),
    ],
]

# دکمه‌های راهنما
HELP_BTN = [
    [
        InlineKeyboardButton(text="🐳 ربات چت 🐳", callback_data="CHATBOT_CMD"),
        InlineKeyboardButton(text="🎄 ابزارها 🎄", callback_data="TOOLS_DATA"),
    ],
    [
        InlineKeyboardButton(text="⦿ بستن ⦿", callback_data="CLOSE"),
    ],
]

# دکمه بستن
CLOSE_BTN = [
    [
        InlineKeyboardButton(text="⦿ بستن ⦿", callback_data="CLOSE"),
    ],
]

# دکمه‌های فعال/غیرفعال کردن ربات
CHATBOT_ON = [
    [
        InlineKeyboardButton(text="فعال کردن", callback_data="enable_chatbot"),
        InlineKeyboardButton(text="غیرفعال کردن", callback_data="disable_chatbot"),
    ],
]

# دکمه‌های موزیک (به زودی)
MUSIC_BACK_BTN = [
    [
        InlineKeyboardButton(text="به زودی", callback_data=f"soom"),
    ],
]

# دکمه‌های برگشت و بستن
S_BACK = [
    [
        InlineKeyboardButton(text="⦿ برگشت ⦿", callback_data="SBACK"),
        InlineKeyboardButton(text="⦿ بستن ⦿", callback_data="CLOSE"),
    ],
]

# دکمه‌های برگشت ربات چت
CHATBOT_BACK = [
    [
        InlineKeyboardButton(text="⦿ برگشت ⦿", callback_data="CHATBOT_BACK"),
        InlineKeyboardButton(text="⦿ بستن ⦿", callback_data="CLOSE"),
    ],
]

# دکمه‌های شروع راهنما
HELP_START = [
    [
        InlineKeyboardButton(text="« راهنما »", callback_data="HELP"),
        InlineKeyboardButton(text="🐳 بستن 🐳", callback_data="CLOSE"),
    ],
]

# دکمه‌های راهنمای اصلی
HELP_BUTN = [
    [
        InlineKeyboardButton(text="« امکانات »", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="⦿ بستن ⦿", callback_data="CLOSE"),
    ],
]

# دکمه‌های درباره ما
ABOUT_BTN = [
    [
        InlineKeyboardButton(text="🎄 پشتیبانی 🎄", url=f"https://t.me/{SUPPORT_GRP}"),
        InlineKeyboardButton(text="« راهنما »", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="🍾 سازنده 🍾", user_id=OWNER),
    ],
    [
        InlineKeyboardButton(text="🐳 کانال اخبار 🐳", url=f"https://t.me/{UPDATE_CHNL}"),
        InlineKeyboardButton(text="⦿ برگشت ⦿", callback_data="BACK"),
    ],
]
