from config import OWNER_USERNAME, SUPPORT_GRP
from nexichat import nexichat
from pyrogram import Client, filters

START = """**
{} 🐺 ربات چت هوشمند و سریع ᴀʟᴏɴᴇ ᴡᴏʟғ

◈ پشتیبانی از متن، استیکر، عکس، ویدیو...
◈ چند زبانه برای هر چت /setlang
◈ فعال/غیرفعال کردن ربات با /chatbot
◈ هوش مصنوعی پیشرفته و سریع
◈ پشتیبانی 24 ساعته

❯ تعداد کاربران: {}
❯ تعداد چت‌ها: {}
❯ زمان کارکرد: {}

╔══════════════════╗
║ ⟫ سازنده: [𝙍𝘼𝙉𝙂𝙀𝙍 ™](https://t.me/beblnn)
╚══════════════════╝
**"""

HELP_READ = f"""**
━━━━━━━━━━━━━━━━━━━━━
برای اطلاعات بیشتر روی دکمه‌های زیر کلیک کنید.
اگر با مشکلی مواجه شدید می‌توانید در [گروه پشتیبانی](https://t.me/atrinmusic_tm1) سوال کنید.
━━━━━━━━━━━━━━━━━━━━━

همه دستورات با / قابل استفاده هستند:**
"""

TOOLS_DATA_READ = f"""**
◈ دستورات ابزارها:
━━━━━━━━━━━━━━━━━━━━━

❯ /start 
• شروع کار با ربات و دریافت پیام خوش‌آمدگویی
━━━━━━━━━━━━━━━━━━━━━

❯ /help 
• دریافت راهنمای کامل دستورات و امکانات
━━━━━━━━━━━━━━━━━━━━━

❯ /ping 
• بررسی آنلاین بودن ربات
━━━━━━━━━━━━━━━━━━━━━

❯ /speedtest 
• بررسی سرعت سرور
━━━━━━━━━━━━━━━━━━━━━

❯ /id 
• دریافت شناسه کاربری، گروه و پیام
━━━━━━━━━━━━━━━━━━━━━

❯ /broadcast 
• ارسال پیام به همه کاربران
• مثال: `/broadcast -user -pin سلام دوستان`
━━━━━━━━━━━━━━━━━━━━━

❯ /shayri 
• دریافت شعر تصادفی عاشقانه
━━━━━━━━━━━━━━━━━━━━━

❯ /link 
• دریافت لینک گروه با شناسه
━━━━━━━━━━━━━━━━━━━━━

❯ /givelink 
• دریافت لینک گروه فعلی
━━━━━━━━━━━━━━━━━━━━━

◈ ساخته شده توسط ⟫ [𝙍𝘼𝙉𝙂𝙀𝙍 ™](https://t.me/beblnn ) 🐺**
"""

CHATBOT_READ = f"""**
◈ دستورات ربات چت:
━━━━━━━━━━━━━━━━━━━━━

❯ /chatbot 
• گزینه‌های فعال/غیرفعال کردن ربات
━━━━━━━━━━━━━━━━━━━━━

❯ /ask 
• پرسیدن هر سوالی از ChatGPT
━━━━━━━━━━━━━━━━━━━━━

❯ /setlang 
• منوی انتخاب زبان چت
━━━━━━━━━━━━━━━━━━━━━

❯ /resetlang 
• بازنشانی زبان ربات به حالت ترکیبی
━━━━━━━━━━━━━━━━━━━━━

❯ /chatlang 
• مشاهده زبان فعلی چت
━━━━━━━━━━━━━━━━━━━━━

❯ /status 
• بررسی وضعیت فعال بودن ربات
━━━━━━━━━━━━━━━━━━━━━

❯ /stats 
• دریافت آمار ربات
━━━━━━━━━━━━━━━━━━━━━

◈ ساخته شده توسط ⟫ [𝙍𝘼𝙉𝙂𝙀𝙍 ™](https://t.me/beblnn) 🐺**
"""

SOURCE_READ = f"""**
━━━━━━━━━━━━━━━━━━━━━
سلام، به ربات [{nexichat.name}](https://t.me/{nexichat.username}) خوش آمدید

◈ برای راهنمایی بیشتر با سازنده تماس بگیرید
━━━━━━━━━━━━━━━━━━━━━

❯ سازنده: [𝙍𝘼𝙉𝙂𝙀𝙍 ™](https://t.me/beblnn)
━━━━━━━━━━━━━━━━━━━━━

❯ گروه پشتیبانی: [کلیک کنید](https://t.me/atrinmusic_tm1)
━━━━━━━━━━━━━━━━━━━━━

◈ ساخته شده توسط ⟫ [𝙍𝘼𝙉𝙂𝙀𝙍 ™](https://t.me/beblnn) 🐺**
"""

ADMIN_READ = "به زودی"

ABOUT_READ = f"""**
━━━━━━━━━━━━━━━━━━━━━
◈ [{nexichat.name}](https://t.me/{nexichat.username}) یک ربات چت مبتنی بر هوش مصنوعی است

❯ پاسخگویی خودکار به کاربران
❯ کمک به فعال‌سازی گروه‌ها 
❯ پشتیبانی از چندین زبان
❯ امکانات پیشرفته مدیریتی
━━━━━━━━━━━━━━━━━━━━━

◈ برای دریافت راهنما و اطلاعات بیشتر روی دکمه‌های زیر کلیک کنید
━━━━━━━━━━━━━━━━━━━━━

◈ ساخته شده توسط ⟫ [ 𝙍𝘼𝙉𝙂𝙀𝙍 ™𝙖(https://t.me/beblnn) 🐺**
"""
