import asyncio
from os import getenv
from config import OWNER_ID
from dotenv import load_dotenv
from pyrogram import Client
import config


class Userbot(Client):
    def __init__(self):
        # ایجاد یک نمونه از کلاینت تلگرام
        self.one = Client(
            name="VIPAss1",  # نام ربات
            api_id=config.API_ID,  # شناسه API تلگرام
            api_hash=config.API_HASH,  # هش API تلگرام 
            session_string=str(config.STRING1),  # رشته نشست
            no_updates=False,  # دریافت آپدیت‌ها فعال است
            plugins=dict(root="nexichat.idchatbot"),  # مسیر پلاگین‌ها
        )
        

    async def start(self):
        print("در حال راه‌اندازی ربات چت آیدی...")

        if config.STRING1:  # اگر رشته نشست موجود باشد
            await self.one.start()  # شروع کلاینت
            try:
                # عضویت در کانال‌های تلگرام
                await self.one.join_chat("TG_NAME_STYLE")
                await self.one.join_chat("TG_NAME_STYLE") 
                await self.one.join_chat("TG_NAME_STYLE")
                await self.one.join_chat("TG_NAME_STYLE")

            except:
                pass
            
            # ذخیره اطلاعات کاربر
            self.one.id = self.one.me.id  # شناسه کاربر
            self.one.name = self.one.me.mention  # نام کاربر 
            self.one.username = self.one.me.username  # نام کاربری
     
            print(f"ربات چت آیدی با نام {self.one.me.first_name} شروع به کار کرد")
            
    async def stop(self):
        LOGGER(__name__).info("در حال متوقف کردن ربات چت آیدی...")
        try:
            if config.STRING1:
                await self.one.stop()  # توقف کلاینت
        except:
            pass
