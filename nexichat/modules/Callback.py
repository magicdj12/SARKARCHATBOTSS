# وارد کردن کتابخانه‌های مورد نیاز
import random  # برای توابع تصادفی
from pymongo import MongoClient  # برای اتصال به دیتابیس
from pyrogram import Client, filters  # کتابخانه اصلی ربات تلگرام
from pyrogram.errors import MessageEmpty  # مدیریت خطای پیام خالی
from pyrogram.enums import ChatAction  # برای نمایش وضعیت‌های چت (مثل در حال تایپ)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message  # برای ساخت دکمه‌های شیشه‌ای
from deep_translator import GoogleTranslator  # برای ترجمه متن‌ها
from nexichat.database.chats import add_served_chat  # افزودن چت به دیتابیس
from nexichat.database.users import add_served_user  # افزودن کاربر به دیتابیس
from config import MONGO_URL  # آدرس اتصال به دیتابیس
from nexichat import nexichat, mongo  # ماژول‌های اصلی ربات
from pyrogram.enums import ChatMemberStatus as CMS  # وضعیت‌های عضویت در گروه
from pyrogram.types import CallbackQuery  # برای مدیریت کالبک‌های دکمه‌ها
import asyncio  # برای برنامه‌نویسی ناهمزمان
import config  # تنظیمات ربات
from nexichat import LOGGER, nexichat, db  # ابزارهای لاگ و دیتابیس
from nexichat.mplugin.helpers import chatai  # ماژول هوش مصنوعی چت
from nexichat.mplugin.helpers import (  # متن‌ها و دکمه‌های آماده
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
    languages,
)

# تنظیم دیتابیس‌ها
lang_db = db.ChatLangDb.LangCollection  # کالکشن زبان‌ها
status_db = db.chatbot_status_db.status  # کالکشن وضعیت چت‌بات

# تابع ساخت دکمه‌های زبان
def generate_language_buttons(languages):
    """ساخت دکمه‌های زبان به صورت 4 ستونه"""
    buttons = []
    current_row = []
    for lang, code in languages.items():
        current_row.append(InlineKeyboardButton(lang.capitalize(), callback_data=f'setlang_{code}'))
        if len(current_row) == 4:  # هر 4 دکمه در یک ردیف
            buttons.append(current_row)
            current_row = []
    if current_row:  # اضافه کردن دکمه‌های باقیمانده
        buttons.append(current_row)
    return InlineKeyboardMarkup(buttons)

# مدیریت کالبک‌های دکمه‌ها
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    """پردازش تمام کالبک‌های دکمه‌ها"""
    bot_id = client.me.id

    # دکمه راهنما
    if query.data == "HELP":
        await query.message.edit_text(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
            disable_web_page_preview=True,
        )

    # دکمه بستن
    elif query.data == "CLOSE":
        await query.message.delete()
        await query.answer("منو بسته شد!", show_alert=True)

    # دکمه برگشت به منوی اصلی
    elif query.data == "BACK":
        await query.message.edit(
            text=START,
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )

    # دکمه منبع کد
    elif query.data == "SOURCE":
        await query.message.edit(
            text=SOURCE_READ,
            reply_markup=InlineKeyboardMarkup(BACK),
            disable_web_page_preview=True,
        )

    # دکمه درباره ما
    elif query.data == "ABOUT":
        await query.message.edit(
            text=ABOUT_READ,
            reply_markup=InlineKeyboardMarkup(ABOUT_BTN),
            disable_web_page_preview=True,
        )

    # دکمه ادمین‌ها
    elif query.data == "ADMINS":
        await query.message.edit(
            text=ADMIN_READ,
            reply_markup=InlineKeyboardMarkup(MUSIC_BACK_BTN),
        )

    # دکمه ابزارها
    elif query.data == "TOOLS_DATA":
        await query.message.edit(
            text=TOOLS_DATA_READ,
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )

    # دکمه برگشت به راهنما
    elif query.data == "BACK_HELP":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )

    # دکمه دستورات چت‌بات
    elif query.data == "CHATBOT_CMD":
        await query.message.edit(
            text=CHATBOT_READ,
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )

    # دکمه برگشت از چت‌بات
    elif query.data == "CHATBOT_BACK":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )

    # فعال کردن چت‌بات
    elif query.data == "enable_chatbot":
        chat_id = query.message.chat.id
        status_db.update_one(
            {"chat_id": chat_id, "bot_id": bot_id},
            {"$set": {"status": "enabled"}},
            upsert=True
        )
        await query.answer("چت‌بات فعال شد ✅", show_alert=True)
        await query.edit_message_text(
            f"گروه: {query.message.chat.title}\n**چت‌بات فعال شد.**"
        )

    # غیرفعال کردن چت‌بات
    elif query.data == "disable_chatbot":
        chat_id = query.message.chat.id
        status_db.update_one(
            {"chat_id": chat_id, "bot_id": bot_id},
            {"$set": {"status": "disabled"}},
            upsert=True
        )
        await query.answer("چت‌بات غیرفعال شد!", show_alert=True)
        await query.edit_message_text(
            f"گروه: {query.message.chat.title}\n**چت‌بات غیرفعال شد.**"
        )

    # تنظیم زبان
    elif query.data.startswith("setlang_"):
        lang_code = query.data.split("_")[1]
        chat_id = query.message.chat.id
        if lang_code in languages.values():
            lang_db.update_one(
                {"chat_id": chat_id, "bot_id": bot_id},
                {"$set": {"language": lang_code}},
                upsert=True
            )
            await query.answer(f"زبان چت به {lang_code.title()} تغییر کرد.", show_alert=True)
            await query.message.edit_text(f"زبان چت به {lang_code.title()} تغییر کرد.")
        else:
            await query.answer("انتخاب زبان نامعتبر است.", show_alert=True)

    # حذف زبان (استفاده از همه زبان‌ها)
    elif query.data == "nolang":
        chat_id = query.message.chat.id
        lang_db.update_one(
            {"chat_id": chat_id, "bot_id": bot_id},
            {"$set": {"language": "nolang"}},
            upsert=True
        )
        await query.answer("زبان ربات به حالت ترکیبی تغییر کرد.", show_alert=True)
        await query.message.edit_text("**زبان ربات به حالت ترکیبی تغییر کرد.**")

    # انتخاب زبان
    elif query.data == "choose_lang":
        await query.answer("زبان چت‌بات را برای این گروه انتخاب کنید.", show_alert=True)
        await query.message.edit_text(
            "**لطفاً زبان مورد نظر خود را برای چت‌بات انتخاب کنید.**",
            reply_markup=generate_language_buttons(languages)
        )
