# وارد کردن کتابخانه‌های مورد نیاز
from pyrogram import Client, filters
import requests
from pyrogram.types import Message
from nexichat import nexichat as app, mongo, db
from MukeshAPI import api
import asyncio
from nexichat.mplugin.helpers import chatai, languages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

# تنظیم دیتابیس زبان و حافظه موقت پیام‌ها
lang_db = db.ChatLangDb.LangCollection
message_cache = {}

# تابع دریافت زبان چت
async def get_chat_language(chat_id, bot_id):
    """دریافت زبان تنظیم شده برای یک چت"""
    chat_lang = await lang_db.find_one({"chat_id": chat_id, "bot_id": bot_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None

# دستور نمایش زبان فعلی چت
@Client.on_message(filters.command("chatlang", prefixes=["/"]))
async def fetch_chat_lang(client, message):
    """نمایش کد زبان فعلی چت"""
    chat_id = message.chat.id
    bot_id = client.me.id
    chat_lang = await get_chat_language(chat_id, bot_id)
    await message.reply_text(f"کد زبان مورد استفاده در این چت: {chat_lang}")

# ذخیره و تحلیل پیام‌ها
@Client.on_message(filters.text, group=2)
async def store_messages(client, message: Message):
    """ذخیره و تحلیل پیام‌ها برای تشخیص زبان"""
    global message_cache

    chat_id = message.chat.id
    bot_id = client.me.id
    chat_lang = await get_chat_language(chat_id, bot_id)

    # اگر زبان تنظیم نشده باشد
    if not chat_lang or chat_lang == "nolang":
        # پیام‌های ربات‌ها را نادیده بگیر
        if message.from_user and message.from_user.is_bot:
            return

        # ایجاد لیست برای ذخیره پیام‌های چت
        if chat_id not in message_cache:
            message_cache[chat_id] = []

        # اضافه کردن پیام به حافظه موقت
        message_cache[chat_id].append(message)

        # وقتی تعداد پیام‌ها به 30 رسید
        if len(message_cache[chat_id]) >= 30:
            # ساخت تاریخچه پیام‌ها
            history = "\n\n".join(
                [f"Text: {msg.text}..." for msg in message_cache[chat_id]]
            )
            
            # ساخت درخواست برای تحلیل زبان
            user_input = f"""
            لیست جملات:-
            [
            {history}
            ]

            این لیستی از جملات است. هر جمله می‌تواند به زبان‌های مختلف باشد. 
            زبان هر جمله را جداگانه تحلیل کنید و زبان غالب را مشخص کنید. 
            دستورات (مثل جملات شروع شده با /) را نادیده بگیرید.
            
            فقط نام رسمی زبان و کد آن را در این قالب ارائه دهید:
            نام زبان :- ""
            کد زبان :- ""
            فقط [نام زبان و کد زبان] کلی را در قالب بالا ارائه دهید. چیز دیگری ارائه ندهید.
            """
            
            # ارسال درخواست به API تشخیص زبان
            base_url = "https://chatwithai.codesearch.workers.dev/?chat="
            response = requests.get(base_url + user_input)

            # ساخت دکمه انتخاب زبان
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("انتخاب زبان", callback_data="choose_lang")
            ]])    

            # ارسال نتیجه تشخیص زبان
            await message.reply_text(
                f"**زبان تشخیص داده شده برای این چت:**\n\n"
                f"{response.text}\n\n"
                f"**می‌توانید با دستور /lang زبان من را تنظیم کنید**", 
                reply_markup=reply_markup
            )

            # پاک کردن حافظه موقت
            message_cache[chat_id].clear()
