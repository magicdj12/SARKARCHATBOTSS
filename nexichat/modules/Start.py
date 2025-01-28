import asyncio
import logging
import random
import time
import psutil
import config
from nexichat import _boot_
from nexichat import get_readable_time
from nexichat import nexichat, mongo
from datetime import datetime
from pymongo import MongoClient
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from config import OWNER_ID, MONGO_URL, OWNER_USERNAME
from pyrogram.errors import FloodWait, ChatAdminRequired
from nexichat.database.chats import get_served_chats, add_served_chat
from nexichat.database.users import get_served_users, add_served_user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from nexichat.modules.helpers import (
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
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



from nexichat import db

chatai = db.Word.WordDb
lang_db = db.ChatLangDb.LangCollection
status_db = db.ChatBotStatusDb.StatusCollection


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


@nexichat.on_message(filters.new_chat_members)
async def خوش_آمدگویی(client, message: Message):
    چت = message.chat
    await add_served_chat(message.chat.id)
    await set_default_status(message.chat.id)
    تعداد_کاربران = len(await get_served_users())
    تعداد_چت‌ها = len(await get_served_chats())
    try:
        for عضو in message.new_chat_members:
            if عضو.id == nexichat.id:
                try:
                    دکمه‌ها = InlineKeyboardMarkup([[InlineKeyboardButton("انتخاب زبان", callback_data="choose_lang")]])    
                    await message.reply_text(
                        text="**ممنون که من رو به این گروه اضافه کردید.**\n\n**لطفاً زبان ربات را برای این گروه با دستور ☞ /lang انتخاب کنید**",
                        reply_markup=دکمه‌ها
                    )
                except Exception as خطا:
                    print(f"{خطا}")
                    pass
                try:
                    لینک_دعوت = await nexichat.export_chat_invite_link(message.chat.id)
                    لینک = f"[دریافت لینک]({لینک_دعوت})"
                except ChatAdminRequired:
                    لینک = "بدون لینک"
                    
                try:
                    عکس_گروه = await nexichat.download_media(
                        چت.photo.big_file_id, file_name=f"chatpp{چت.id}.png"
                    )
                    عکس_چت = عکس_گروه if عکس_گروه else "https://envs.sh/IL_.jpg"
                except AttributeError:
                    عکس_چت = "https://envs.sh/IL_.jpg"
                except Exception as خطا:
                    pass

                تعداد_اعضا = await nexichat.get_chat_members_count(چت.id)
                تعداد_چت‌ها = len(await get_served_chats())
                نام_کاربری = چت.username if چت.username else "گروه خصوصی"
                پیام = (
                    f"**📝ربات موزیک به یک #گروه_جدید اضافه شد**\n\n"
                    f"**📌نام گروه:** {چت.title}\n"
                    f"**🍂شناسه گروه:** `{چت.id}`\n"
                    f"**🔐نام کاربری گروه:** @{نام_کاربری}\n"
                    f"**🖇️لینک گروه:** {لینک}\n"
                    f"**📈تعداد اعضای گروه:** {تعداد_اعضا}\n"
                    f"**🤔اضافه شده توسط:** {message.from_user.mention}\n\n"
                    f"**تعداد کل چت‌ها:** {تعداد_چت‌ها}"
                )

                try:
                    مالک = config.OWNER_ID
                    if مالک:
                        await nexichat.send_photo(
                            int(OWNER_ID),
                            photo=عکس_چت,
                            caption=پیام,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{message.from_user.first_name}", user_id=message.from_user.id)]])
                        )
                except Exception as خطا:
                    print("لطفاً شناسه مالک صحیح را برای ارسال گزارش‌ها وارد کنید")
                    await nexichat.send_photo(
                        int(OWNER_ID),
                        photo=عکس_چت,
                        caption=پیام,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{message.from_user.first_name}", user_id=message.from_user.id)]])
                    )
    except Exception as خطا:
        print(f"خطا: {خطا}")

@nexichat.on_cmd(["ls"])
async def لیست_فایل‌ها(_, m: Message):
    "نمایش تمام فایل‌ها و پوشه‌ها."

    مسیر_ورودی = "".join(m.text.split(maxsplit=1)[1:])
    مسیر = مسیر_ورودی or os.getcwd()
    if not os.path.exists(مسیر):
        await m.reply_text(
            f"هیچ پوشه یا فایلی با نام `{مسیر_ورودی}` وجود ندارد. لطفا دوباره بررسی کنید."
        )
        return

    مسیر = Path(مسیر_ورودی) if مسیر_ورودی else os.getcwd()
    if os.path.isdir(مسیر):
        if مسیر_ورودی:
            پیام = f"پوشه‌ها و فایل‌های موجود در `{مسیر}`:\n"
        else:
            پیام = "پوشه‌ها و فایل‌های موجود در مسیر فعلی:\n"
            
        لیست_محتوا = os.listdir(مسیر)
        فایل‌ها = ""
        پوشه‌ها = ""
        
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
    else:
        حجم = os.stat(مسیر).st_size
        پیام = "جزئیات فایل انتخاب شده:\n"
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

    if len(پیام) > 4096:
        with io.BytesIO(str.encode(پیام)) as خروجی:
            خروجی.name = "ls.txt"
            await m.reply_document(
                خروجی,
                caption=مسیر,
            )
    else:
        await m.reply_text(پیام)


@nexichat.on_cmd(["start", "starts"])
async def شروع(_, m: Message):
    تعداد_کاربران = len(await get_served_users())
    تعداد_چت‌ها = len(await get_served_chats())
    if m.chat.type == ChatType.PRIVATE:
        پیام = await m.reply_text(
            text=random.choice(EMOJIOS),
        )
        await asyncio.sleep(0.5)
        
        # انیمیشن شروع
        مراحل_انیمیشن = [
            "**__ꨄ︎ ش__**", "**__ꨄ شر__**", "**__ꨄ︎ شرو__**",
            "**__ꨄ︎ شروع__**", "**__ꨄ شروع .__**",
            "**__ꨄ︎ شروع ..__**", "**__ꨄ︎ شروع ...__**",
            "**__ꨄ شروع ....__**", "**__ꨄ︎ در حال شروع.__**",
            "**__ꨄ در حال شروع.....__**"
        ]
        
        for متن in مراحل_انیمیشن:
            await پیام.edit(متن)
            await asyncio.sleep(0.1)
            
        await پیام.delete()
        
        استیکر = await m.reply_sticker(sticker=random.choice(STICKER))
        عکس_چت = BOT  
        if m.chat.photo:
            try:
                عکس_کاربر = await nexichat.download_media(m.chat.photo.big_file_id)
                await استیکر.delete()
                if عکس_کاربر:
                    عکس_چت = عکس_کاربر
            except AttributeError:
                عکس_چت = BOT  

        تعداد_کاربران = len(await get_served_users())
        تعداد_چت‌ها = len(await get_served_chats())
        آپتایم, سی_پی_یو, رم, دیسک = await bot_sys_stats()
        
        await m.reply_photo(
            photo=عکس_چت,
            caption=START.format(nexichat.mention or "غیرقابل منشن", تعداد_کاربران, تعداد_چت‌ها, آپتایم),
            reply_markup=InlineKeyboardMarkup(START_BOT)
        )
        
        await add_served_user(m.chat.id)
        
        دکمه_کاربر = InlineKeyboardMarkup([[InlineKeyboardButton(f"{m.chat.first_name}", user_id=m.chat.id)]])
        await nexichat.send_photo(
            int(OWNER_ID),
            photo=عکس_چت,
            caption=f"{m.from_user.mention} ربات را شروع کرد.\n\n**نام:** {m.chat.first_name}\n**نام کاربری:** @{m.chat.username}\n**شناسه:** {m.chat.id}\n\n**تعداد کل کاربران:** {تعداد_کاربران}",
            reply_markup=دکمه_کاربر
        )
        
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=GSTART.format(m.from_user.mention or "غیرقابل منشن"),
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)


@nexichat.on_cmd("help")
async def راهنما(client: nexichat, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption="**سلام، برای دریافت راهنما به من پیام خصوصی بدهید!**",
            reply_markup=InlineKeyboardMarkup(HELP_BUTN),
        )
        await add_served_chat(m.chat.id)


@nexichat.on_cmd("rreepo")
async def مخزن(_, m: Message):
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )


@nexichat.on_cmd("ping")
async def پینگ(_, message: Message):
    شروع = datetime.now()
    آپتایم, سی_پی_یو, رم, دیسک = await bot_sys_stats()
    پیام = await message.reply_photo(
        photo=random.choice(IMG),
        caption="در حال بررسی پینگ...",
    )

    زمان = (datetime.now() - شروع).microseconds / 1000
    await پیام.edit_text(
        text=f"""سلام عزیزم!!
{nexichat.name} ربات چت فعال است 🥀 و با پینگ زیر کار می‌کند:

**➥** `{زمان}` میلی‌ثانیه
**➲ پردازنده:** {سی_پی_یو}
**➲ حافظه:** {رم}
**➲ دیسک:** {دیسک}
**➲ زمان کارکرد »** {آپتایم}

<b>||**๏ ساخته شده با ❣️ توسط [موزیک سیدی ✯](https://t.me/{OWNER_USERNAME}) **||</b>""",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )
    
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)


@nexichat.on_message(filters.command("statsts"))
async def آمار(cli: Client, message: Message):
    تعداد_کاربران = len(await get_served_users())
    تعداد_چت‌ها = len(await get_served_chats())
    await message.reply_text(
        f"""{(await cli.get_me()).mention} آمار ربات چت:

➻ **چت‌ها:** {تعداد_چت‌ها}
➻ **کاربران:** {تعداد_کاربران}"""
    )


from pyrogram.enums import ParseMode

from nexichat import nexichat


@nexichat.on_cmd("id")
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTO_SLEEP = 5
IS_BROADCASTING = False
broadcast_lock = asyncio.Lock()


@nexichat.on_message(
    filters.command(["broadcast", "gcast"]) & filters.user(int(OWNER_ID))
)
async def broadcast_message(client, message):
    global IS_BROADCASTING
    async with broadcast_lock:
        if IS_BROADCASTING:
            return await message.reply_text(
                "A broadcast is already in progress. Please wait for it to complete."
            )

        IS_BROADCASTING = True
        try:
            query = message.text.split(None, 1)[1].strip()
        except IndexError:
            query = message.text.strip()
        except Exception as eff:
            return await message.reply_text(
                f"**Error**: {eff}"
            )
        try:
            if message.reply_to_message:
                broadcast_content = message.reply_to_message
                broadcast_type = "reply"
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }
            else:
                if len(message.command) < 2:
                    return await message.reply_text(
                        "**Please provide text after the command or reply to a message for broadcasting.**"
                    )
                
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }

                for flag in flags:
                    query = query.replace(flag, "").strip()

                if not query:
                    return await message.reply_text(
                        "Please provide a valid text message or a flag: -pin, -nogroup, -pinloud, -user"
                    )

                
                broadcast_content = query
                broadcast_type = "text"
            

            await message.reply_text("**Started broadcasting...**")

            if not flags.get("-nogroup", False):
                sent = 0
                pin_count = 0
                chats = await get_served_chats()

                for chat in chats:
                    chat_id = int(chat["chat_id"])
                    if chat_id == message.chat.id:
                        continue
                    try:
                        if broadcast_type == "reply":
                            m = await nexichat.forward_messages(
                                chat_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await nexichat.send_message(
                                chat_id, text=broadcast_content
                            )
                        sent += 1

                        if flags.get("-pin", False) or flags.get("-pinloud", False):
                            try:
                                await m.pin(
                                    disable_notification=flags.get("-pin", False)
                                )
                                pin_count += 1
                            except Exception as e:
                                continue

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for chat {chat_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping chat {chat_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(
                    f"**Broadcasted to {sent} chats and pinned in {pin_count} chats.**"
                )

            if flags.get("-user", False):
                susr = 0
                users = await get_served_users()

                for user in users:
                    user_id = int(user["user_id"])
                    try:
                        if broadcast_type == "reply":
                            m = await nexichat.forward_messages(
                                user_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await nexichat.send_message(
                                user_id, text=broadcast_content
                            )
                        susr += 1

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for user {user_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping user {user_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(f"**Broadcasted to {susr} users.**")

        finally:
            IS_BROADCASTING = False


    
