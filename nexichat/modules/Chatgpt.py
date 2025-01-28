import requests
from pyrogram import filters, Client
from pyrogram.enums import ChatAction
from nexichat import nexichat as app
# استفاده از API رایگان و معتبر
GEMINI_API = "https://api.itsrose.life/gemini/free"

@Client.on_message(filters.command(["جمینی", "پرسش", "سوال", "ربات"]))
async def gemini_handler(client, message):
    # دریافت متن سوال
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    elif len(message.command) > 1:
        user_input = " ".join(message.command[1:])
    else:
        await message.reply_text("مثال: `/پرسش سلام چطوری؟`")
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        # درخواست به API اصلی
        response = requests.get(
            GEMINI_API,
            params={
                "text": user_input,
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json().get("result", "")
            if result:
                await message.reply_text(result, quote=True)
                return
            
        # استفاده از API پشتیبان اگر API اصلی کار نکرد
        backup_url = "https://chatwithai.codesearch.workers.dev/?chat="
        backup_response = requests.get(backup_url + user_input, timeout=30)
        
        if backup_response.text.strip():
            await message.reply_text(backup_response.text.strip(), quote=True)
        else:
            # اگر هیچ کدام کار نکرد، از API سوم استفاده کن
            third_api = "https://api.betabotz.eu.org/api/ai/gemini"
            final_response = requests.get(
                third_api,
                params={"text": user_input},
                timeout=30
            )
            
            if final_response.status_code == 200:
                final_result = final_response.json().get("result", "")
                if final_result:
                    await message.reply_text(final_result, quote=True)
                    return
                    
            await message.reply_text("**متأسفانه در حال حاضر سیستم پاسخگویی در دسترس نیست. لطفا کمی بعد دوباره تلاش کنید**")
            
    except Exception as e:
        await message.reply_text("**خطا در دریافت پاسخ. لطفاً دوباره تلاش کنید یا کمی صبر کنید**")
