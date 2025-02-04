import random
import os
import shutil
from MukeshAPI import api
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from nexichat.database.chats import add_served_chat
from nexichat.database.users import add_served_user
from config import MONGO_URL, OWNER_ID
from nexichat import nexichat, mongo, LOGGER, db
from nexichat.modules.helpers import chatai, storeai, languages, CHATBOT_ON
from nexichat.modules.helpers import (
    ABOUT_BTN,
    ABOUT_READ,
    ADMIN_READ,
    BACK,
    CHATBOT_BACK,
    CHATBOT_READ,
    DEV_OP,
    HELP_BTN,
    HELP_READ,
    MUSIC_BACK_BTN,
    SOURCE_READ,
    START,
    TOOLS_DATA_READ,
)
import asyncio

translator = GoogleTranslator()

lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status

# دکمه‌های هوشمند برای انتخاب زبان
LANG_BUTTONS = [
    [
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="setlang_fa"),
        InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en")
    ],
    [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
]

# دکمه‌های وضعیت ربات
STATUS_BUTTONS = [
    [
        InlineKeyboardButton("✅ فعال", callback_data="chatbot_on"),
        InlineKeyboardButton("❌ غیرفعال", callback_data="chatbot_off")
    ],
    [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
]

@nexichat.on_message(filters.command("راه‌اندازی‌مجدد") & filters.user(int(OWNER_ID)))
async def restart(client: Client, message: Message):
    reply = await message.reply_text("🔄 در حال راه‌اندازی مجدد...")
    await message.delete()
    await reply.edit_text("✅ ربات با موفقیت راه‌اندازی مجدد شد\n⏳ لطفاً 5 ثانیه صبر کنید...")
    os.system(f"kill -9 {os.getpid()} && bash start")

@nexichat.on_message(filters.command(["زبان", "تنظیم‌زبان"]))
async def set_language(client: Client, message: Message):
    await message.reply_text(
        "🌍 لطفاً زبان مورد نظر خود را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(LANG_BUTTONS)
    )

@nexichat.on_message(filters.command("وضعیت"))
async def check_status(client: Client, message: Message):
    chat_id = message.chat.id
    status = await status_db.find_one({"chat_id": chat_id})
    if status:
        current = status.get("status", "نامشخص")
        await message.reply(f"💬 وضعیت فعلی ربات: {current}")
    else:
        await message.reply("❌ وضعیتی برای این گفتگو یافت نشد.")

@nexichat.on_message(filters.command("حذف‌زبان"))
async def reset_language(client: Client, message: Message):
    chat_id = message.chat.id
    lang_db.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"language": "nolang"}}, 
        upsert=True
    )
    await message.reply_text("✅ زبان ربات به حالت پیش‌فرض بازگشت.")

@nexichat.on_message(filters.command("ربات"))
async def chatbot_settings(client: Client, message: Message):
    await message.reply_text(
        f"💭 گفتگو: {message.chat.title}\n📋 لطفاً یک گزینه را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(STATUS_BUTTONS)
    )

# پردازش کال‌بک‌های دکمه‌ها
@nexichat.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):
    data = callback.data
    
    if data.startswith("setlang_"):
        lang = data.split("_")[1]
        chat_id = callback.message.chat.id
        lang_db.update_one(
            {"chat_id": chat_id},
            {"$set": {"language": lang}},
            upsert=True
        )
        await callback.message.edit_text(
            f"✅ زبان ربات به {'فارسی' if lang == 'fa' else 'English'} تغییر کرد."
        )
    
    elif data == "chatbot_on":

chat_id = callback.message.chat.id
        status_db.update_one(
            {"chat_id": chat_id},
            {"$set": {"status": "فعال"}},
            upsert=True
        )
        await callback.message.edit_text("✅ ربات فعال شد.")
    
    elif data == "chatbot_off":
        chat_id = callback.message.chat.id
        status_db.update_one(
            {"chat_id": chat_id},
            {"$set": {"status": "غیرفعال"}},
            upsert=True
        )
        await callback.message.edit_text("❌ ربات غیرفعال شد.")
    
    elif data == "back":
        await callback.message.edit_text(
            "🏠 به منوی اصلی بازگشتید.",
            reply_markup=InlineKeyboardMarkup(HELP_BTN)
)
