# وارد کردن کتابخانه‌های مورد نیاز
import random  # برای انتخاب تصادفی پاسخ‌ها
from pymongo import MongoClient  # برای اتصال به دیتابیس
from pyrogram import Client, filters  # برای ساخت ربات تلگرام
from pyrogram.errors import MessageEmpty  # برای مدیریت خطای پیام خالی
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS  # برای وضعیت‌های چت
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery  # برای ساخت دکمه و پیام
from deep_translator import GoogleTranslator  # برای ترجمه متن‌ها
# وارد کردن توابع دیتابیس
from nexichat.database.chats import add_served_chat
from nexichat.database.users import add_served_user
from nexichat.database import add_served_cchat, add_served_cuser
from config import MONGO_URL  # آدرس دیتابیس
from nexichat import nexichat, mongo, LOGGER, db  # ابزارهای ربات
from nexichat.mplugin.helpers import chatai, languages  # زبان‌ها و هوش مصنوعی
import asyncio  # برای برنامه‌نویسی ناهمزمان

# راه‌اندازی مترجم گوگل
translator = GoogleTranslator()

# تنظیم دیتابیس‌های زبان و وضعیت
lang_db = db.ChatLangDb.LangCollection  # دیتابیس زبان‌ها
status_db = db.chatbot_status_db.status  # دیتابیس وضعیت ربات

# لیست کش برای ذخیره پاسخ‌ها
replies_cache = []

# تابع بارگذاری پاسخ‌ها در کش
async def load_replies_cache():
    """بارگذاری تمام پاسخ‌ها از دیتابیس به حافظه"""
    global replies_cache
    replies_cache = await chatai.find().to_list(length=None)

# تابع ذخیره پاسخ جدید
async def save_reply(original_message: Message, reply_message: Message):
    """ذخیره پیام و پاسخ در دیتابیس و کش"""
    global replies_cache
    try:
        # ساخت دیکشنری پاسخ
        reply_data = {
            "word": original_message.text,  # متن اصلی پیام
            "text": None,  # متن یا شناسه فایل پاسخ
            "check": "none",  # نوع پاسخ
        }

        # تشخیص نوع پیام و ذخیره شناسه فایل
        if reply_message.sticker:  # استیکر
            reply_data["text"] = reply_message.sticker.file_id
            reply_data["check"] = "sticker"
        elif reply_message.photo:  # عکس
            reply_data["text"] = reply_message.photo.file_id
            reply_data["check"] = "photo"
        elif reply_message.video:  # ویدیو
            reply_data["text"] = reply_message.video.file_id
            reply_data["check"] = "video"
        elif reply_message.audio:  # فایل صوتی
            reply_data["text"] = reply_message.audio.file_id
            reply_data["check"] = "audio"
        elif reply_message.animation:  # گیف
            reply_data["text"] = reply_message.animation.file_id
            reply_data["check"] = "gif"
        elif reply_message.voice:  # پیام صوتی
            reply_data["text"] = reply_message.voice.file_id
            reply_data["check"] = "voice"
        elif reply_message.text:  # متن
            reply_data["text"] = reply_message.text
            reply_data["check"] = "none"

        # اگر پاسخ تکراری نبود، ذخیره کن
        is_chat = await chatai.find_one(reply_data)
        if not is_chat:
            await chatai.insert_one(reply_data)
            replies_cache.append(reply_data)

    except Exception as e:
        print(f"خطا در ذخیره پاسخ: {e}")

# تابع دریافت پاسخ مناسب
async def get_reply(word: str):
    """یافتن پاسخ مناسب برای یک کلمه"""
    global replies_cache
    if not replies_cache:  # اگر کش خالی است، بارگذاری کن
        await load_replies_cache()
        
    # یافتن پاسخ‌های مرتبط
    relevant_replies = [reply for reply in replies_cache if reply['word'] == word]
    if not relevant_replies:  # اگر پاسخ مرتبط نبود، از همه پاسخ‌ها استفاده کن
        relevant_replies = replies_cache
    return random.choice(relevant_replies) if relevant_replies else None

# تابع دریافت زبان چت
async def get_chat_language(chat_id, bot_id):
    """دریافت زبان تنظیم شده برای یک چت"""
    chat_lang = await lang_db.find_one({"chat_id": chat_id, "bot_id": bot_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None
    
# مدیریت پیام‌های ورودی
@Client.on_message(filters.incoming)
async def chatbot_response(client: Client, message: Message):
    """پردازش پیام‌های ورودی و ارسال پاسخ"""
    try:
        chat_id = message.chat.id
        bot_id = client.me.id
        
        # بررسی وضعیت فعال/غیرفعال بودن ربات
        chat_status = await status_db.find_one({"chat_id": chat_id, "bot_id": bot_id})
        if chat_status and chat_status.get("status") == "disabled":
            return

        # بررسی دستورات
        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            if message.chat.type in ["group", "supergroup"]:  # اگر گروه است
                await add_served_cchat(bot_user_id, message.chat.id)
                return await add_served_chat(message.chat.id)      
            else:  # اگر چت خصوصی است
                await add_served_cuser(bot_user_id, message.chat.id)
                return await add_served_user(message.chat.id)

        # پردازش پیام و ارسال پاسخ
        if ((message.reply_to_message and message.reply_to_message.from_user.id == client.me.id) or 
            not message.reply_to_message) and not message.from_user.is_bot:
            
            # دریافت پاسخ مناسب
            reply_data = await get_reply(message.text)

            if reply_data:
                response_text = reply_data["text"]
                chat_lang = await get_chat_language(chat_id, bot_id)

                # ترجمه پاسخ به زبان چت
                if not chat_lang or chat_lang == "nolang":
                    translated_text = response_text
                else:
                    translated_text = GoogleTranslator(source='auto', target=chat_lang).translate(response_text)
                    if not translated_text:
                        translated_text = response_text

                # ارسال پاسخ بر اساس نوع
                if reply_data["check"] == "sticker":  # استیکر
                    try:
                        await message.reply_sticker(reply_data["text"])
                    except:
                        pass
                elif reply_data["check"] == "photo":  # عکس
                    try:
                        await message.reply_photo(reply_data["text"])
                    except:
                        pass
                elif reply_data["check"] == "video":  # ویدیو
                    try:
                        await message.reply_video(reply_data["text"])
                    except:
                        pass
                elif reply_data["check"] == "audio":  # فایل صوتی
                    try:
                        await message.reply_audio(reply_data["text"])
                    except:
                        pass
                elif reply_data["check"] == "gif":  # گیف
                    try:
                        await message.reply_animation(reply_data["text"])
                    except:
                        pass
                elif reply_data["check"] == "voice":  # پیام صوتی
                    try:
                        await message.reply_voice(reply_data["text"])
                    except:
                        pass
                else:  # متن
                    try:
                        await message.reply_text(translated_text)
                    except:
                        pass
            else:  # اگر پاسخی پیدا نشد
                try:
                    await message.reply_text("**متوجه نشدم. چه می‌گویید؟**")
                except:
                    pass

        # ذخیره پیام و پاسخ برای یادگیری
        if message.reply_to_message:
            await save_reply(message.reply_to_message, message)

    except MessageEmpty:  # خطای پیام خالی
        try:
            await message.reply_text("🙄🙄")
        except:
            pass
    except Exception as e:
        return
