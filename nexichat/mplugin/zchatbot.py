# اضافه کردن کتابخانه‌های مورد نیاز
import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from nexichat.database.chats import add_served_chat
from nexichat.database.users import add_served_user
from nexichat.database import add_served_cchat, add_served_cuser
from config import MONGO_URL
from nexichat import nexichat, mongo, LOGGER, db
from nexichat.mplugin.helpers import chatai, languages
import asyncio

# تنظیم دیتابیس‌ها
lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status
bad_words_db = db.bad_words_db.words  # دیتابیس جدید برای کلمات نامناسب

# لیست کش‌ها
replies_cache = []
bad_words_cache = {}  # کش کلمات نامناسب برای هر گروه

# لیست پیش‌فرض کلمات نامناسب
DEFAULT_BAD_WORDS = [
    "کلمه1", "کلمه2", "کلمه3"  # کلمات نامناسب پیش‌فرض را اینجا اضافه کنید
]

# تابع بررسی کلمات نامناسب
async def check_bad_words(text: str, chat_id: int) -> tuple[bool, str]:
    """بررسی متن برای کلمات نامناسب و جایگزینی آنها"""
    if not text:
        return False, text
        
    # دریافت کلمات فیلتر شده از کش یا دیتابیس
    if chat_id not in bad_words_cache:
        chat_filters = await bad_words_db.find_one({"chat_id": chat_id})
        bad_words_cache[chat_id] = set(chat_filters["words"] if chat_filters else DEFAULT_BAD_WORDS)
    
    bad_words = bad_words_cache[chat_id]
    has_bad_word = False
    words = text.split()
    
    for i, word in enumerate(words):
        if word.lower() in bad_words:
            words[i] = "❌" * len(word)
            has_bad_word = True
            
    return has_bad_word, " ".join(words)

# دستورات مدیریت کلمات نامناسب
@nexichat.on_message(filters.command(["addbadword", "badword"]) & filters.group)
async def add_bad_word(client, message: Message):
    """اضافه کردن کلمه به لیست فیلتر"""
    try:
        # بررسی دسترسی ادمین
        user_status = await message.chat.get_member(message.from_user.id)
        if user_status.status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await message.reply_text("❌ فقط ادمین‌ها می‌توانند کلمات نامناسب را مدیریت کنند!")

        if len(message.command) < 2:
            return await message.reply_text("❌ لطفاً کلمه مورد نظر را وارد کنید!\n\nمثال: /badword کلمه")

        word = message.command[1].lower()
        chat_id = message.chat.id

        # اضافه کردن به دیتابیس
        await bad_words_db.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"words": word}},
            upsert=True
        )
        
        # به‌روزرسانی کش
        if chat_id in bad_words_cache:
            bad_words_cache[chat_id].add(word)
        
        await message.reply_text(f"✅ کلمه '{word}' به لیست فیلتر اضافه شد.")
        
    except Exception as e:
        await message.reply_text(f"❌ خطا: {str(e)}")

@nexichat.on_message(filters.command(["rmbadword", "unbadword"]) & filters.group)
async def remove_bad_word(client, message: Message):
    """حذف کلمه از لیست فیلتر"""
    try:
        # بررسی دسترسی ادمین
        user_status = await message.chat.get_member(message.from_user.id)
        if user_status.status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await message.reply_text("❌ فقط ادمین‌ها می‌توانند کلمات نامناسب را مدیریت کنند!")

        if len(message.command) < 2:
            return await message.reply_text("❌ لطفاً کلمه مورد نظر را وارد کنید!\n\nمثال: /unbadword کلمه")

        word = message.command[1].lower()
        chat_id = message.chat.id

        # حذف از دیتابیس
        result = await bad_words_db.update_one(
            {"chat_id": chat_id},
            {"$pull": {"words": word}}
        )
        
        # به‌روزرسانی کش
        if chat_id in bad_words_cache and word in bad_words_cache[chat_id]:
            bad_words_cache[chat_id].remove(word)
        
        if result.modified_count > 0:
            await message.reply_text(f"✅ کلمه '{word}' از لیست فیلتر حذف شد.")
        else:
            await message.reply_text("❌ این کلمه در لیست فیلتر وجود ندارد!")
            
    except Exception as e:
        await message.reply_text(f"❌ خطا: {str(e)}")

@nexichat.on_message(filters.command(["badwords", "listbadwords"]) & filters.group)
async def list_bad_words(client, message: Message):
    """نمایش لیست کلمات فیلتر شده"""
    try:
        chat_id = message.chat.id
        
        # دریافت لیست از دیتابیس
        chat_filters = await bad_words_db.find_one({"chat_id": chat_id})
        words = list(chat_filters["words"]) if chat_filters else DEFAULT_BAD_WORDS
        
        if not words:
            return await message.reply_text("❌ لیست کلمات فیلتر شده خالی است!")
            
        text = "📋 لیست کلمات فیلتر شده:\n\n"
        for i, word in enumerate(words, 1):
            text += f"{i}. {word}\n"
            
        await message.reply_text(text)
        
    except Exception as e:
        await message.reply_text(f"❌ خطا: {str(e)}")
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

        # بررسی و فیلتر کلمات نامناسب
        if message.text:
            has_bad_word, filtered_text = await check_bad_words(message.text, chat_id)
            if has_bad_word:
                try:
                    await message.delete()  # حذف پیام حاوی کلمه نامناسب
                    warning_msg = await message.reply_text(
                        f"⚠️ {message.from_user.mention} لطفاً از کلمات نامناسب استفاده نکنید!"
                    )
                    await asyncio.sleep(5)  # 5 ثانیه صبر
                    await warning_msg.delete()  # حذف پیام هشدار
                    return
                except:
                    pass
            message.text = filtered_text

        # بررسی دستورات
        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            if message.chat.type in ["group", "supergroup"]:
                await add_served_cchat(bot_user_id, message.chat.id)
                return await add_served_chat(message.chat.id)      
            else:
                await add_served_cuser(bot_user_id, message.chat.id)
                return await add_served_user(message.chat.id)

        # پردازش پیام و ارسال پاسخ
        if ((message.reply_to_message and message.reply_to_message.from_user.id == client.me.id) or 
            not message.reply_to_message) and not message.from_user.is_bot:
            
            reply_data = await get_reply(message.text)

            if reply_data:
                response_text = reply_data["text"]
                chat_lang = await get_chat_language(chat_id, bot_id)

                if not chat_lang or chat_lang == "nolang":
                    translated_text = response_text
                else:
                    translated_text = GoogleTranslator(source='auto', target=chat_lang).translate(response_text)
                    if not translated_text:
                        translated_text = response_text

                # ارسال پاسخ بر اساس نوع
                try:
                    if reply_data["check"] == "sticker":
                        await message.reply_sticker(reply_data["text"])
                    elif reply_data["check"] == "photo":
                        await message.reply_photo(reply_data["text"])
                    elif reply_data["check"] == "video":
                        await message.reply_video(reply_data["text"])
                    elif reply_data["check"] == "audio":
                        await message.reply_audio(reply_data["text"])
                    elif reply_data["check"] == "gif":
                        await message.reply_animation(reply_data["text"])
                    elif reply_data["check"] == "voice":
                        await message.reply_voice(reply_data["text"])
                    else:
                        await message.reply_text(translated_text)
                except:
                    pass
            else:
                try:
                    await message.reply_text("**متوجه نشدم. چه می‌گویید؟**")
                except:
                    pass

        # ذخیره پیام و پاسخ برای یادگیری
        if message.reply_to_message:
            await save_reply(message.reply_to_message, message)

    except MessageEmpty:
        try:
            await message.reply_text("🙄🙄")
        except:
            pass
    except Exception as e:
        LOGGER.error(f"خطا در پردازش پیام: {e}")
        return        
