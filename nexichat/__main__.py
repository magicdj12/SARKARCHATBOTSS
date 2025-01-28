import sys
import asyncio
import importlib
from flask import Flask
import threading
import config
from nexichat import ID_CHATBOT
from pyrogram import idle
from pyrogram.types import BotCommand
from config import OWNER_ID
from nexichat import LOGGER, nexichat, userbot, load_clone_owners
from nexichat.modules import ALL_MODULES
from nexichat.modules.Clone import restart_bots
from nexichat.modules.Id_Clone import restart_idchatbots

async def anony_boot():
    """راه‌اندازی اصلی ربات و تنظیمات اولیه"""
    try:
        # شروع ربات اصلی
        await nexichat.start()
        try:
            # ارسال پیام شروع به مالک
            await nexichat.send_message(int(OWNER_ID), f"**{nexichat.mention} با موفقیت شروع شد✅**")
        except Exception as ex:
            LOGGER.info(f"@{nexichat.username} شروع شد، لطفاً ربات را از آیدی مالک راه‌اندازی کنید.")
    
        # راه‌اندازی ربات‌های کلون شده
        asyncio.create_task(restart_bots())
        asyncio.create_task(restart_idchatbots())
        await load_clone_owners()

        # راه‌اندازی ربات کاربر اگر تنظیم شده باشد
        if config.STRING1:
            try:
                await userbot.start()
                try:
                    await nexichat.send_message(int(OWNER_ID), f"**ربات چت آیدی نیز راه‌اندازی شد✅**")
                except Exception as ex:
                    LOGGER.info(f"@{nexichat.username} شروع شد، لطفاً ربات را از آیدی مالک راه‌اندازی کنید.")
    
            except Exception as ex:
                print(f"خطا در راه‌اندازی ربات چت آیدی: {ex}")
                pass
    except Exception as ex:
        LOGGER.error(ex)

    # بارگذاری تمام ماژول‌ها
    for all_module in ALL_MODULES:
        importlib.import_module("nexichat.modules." + all_module)
        LOGGER.info(f"ماژول با موفقیت بارگذاری شد: {all_module}")

    # تنظیم دستورات ربات
    try:
        await nexichat.set_bot_commands(
            commands=[
                BotCommand("start", "شروع کار با ربات"),
                BotCommand("help", "دریافت منوی راهنما"),
                BotCommand("clone", "ساخت ربات چت شخصی"),
                BotCommand("idclone", "ساخت ربات چت آیدی"),
                BotCommand("cloned", "دریافت لیست ربات‌های کلون شده"),
                BotCommand("ping", "بررسی وضعیت فعال بودن ربات"),
                BotCommand("lang", "انتخاب زبان پاسخ ربات"),
                BotCommand("chatlang", "مشاهده زبان فعلی چت"),
                BotCommand("resetlang", "بازنشانی به زبان پیش‌فرض"),
                BotCommand("id", "دریافت شناسه کاربری"),
                BotCommand("stats", "مشاهده آمار ربات"),
                BotCommand("gcast", "ارسال پیام به گروه‌ها/کاربران"),
                BotCommand("chatbot", "فعال/غیرفعال کردن ربات چت"),
                BotCommand("status", "بررسی وضعیت ربات در چت"),
                BotCommand("shayri", "دریافت شعر تصادفی عاشقانه"),
                BotCommand("ask", "پرسیدن سوال از ChatGPT"),
            ]
        )
        LOGGER.info("دستورات ربات با موفقیت تنظیم شدند.")
    except Exception as ex:
        LOGGER.error(f"خطا در تنظیم دستورات ربات: {ex}")
    
    LOGGER.info(f"@{nexichat.username} شروع به کار کرد.")
    
    await idle()

# راه‌اندازی سرور فلاسک
app = Flask(__name__)
@app.route('/')
def home():
    return "ربات در حال اجراست"

def run_flask():
    """اجرای سرور فلاسک در پورت 8000"""
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # راه‌اندازی سرور فلاسک در یک thread جداگانه
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    # راه‌اندازی ربات
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("در حال متوقف کردن ربات...")
