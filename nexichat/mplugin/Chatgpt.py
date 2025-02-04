import requests
from MukeshAPI import api
from pyrogram import filters, Client
from pyrogram.enums import ChatAction
from nexichat import nexichat as app

# Define both English and Persian commands
COMMANDS = ["gemini", "ai", "ask", "chatgpt", "هوش_مصنوعی", "جمینی", "بپرس"]

@Client.on_message(filters.command(COMMANDS) | filters.regex(r'^(جمینی|بپرس|هوش مصنوعی)'))
async def gemini_handler(client, message):
    # Handle command with bot username
    if message.text and message.text.startswith(f"/gemini@{client.me.username}"):
        if len(message.text.split(" ", 1)) > 1:
            user_input = message.text.split(" ", 1)[1]
        else:
            await message.reply_text("مثال: `بپرس نارندرا مودی کیست؟` یا `/ask who is Narendra Modi`")
            return
    # Handle reply to message
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    # Handle direct command
    else:
        if message.text.startswith('/'):
            if len(message.command) > 1:
                user_input = " ".join(message.command[1:])
            else:
                await message.reply_text("مثال: `بپرس نارندرا مودی کیست؟` یا `/ask who is Narendra Modi`")
                return
        else:
            # Handle Persian text without slash
            text_parts = message.text.split(maxsplit=1)
            if len(text_parts) > 1:
                user_input = text_parts[1]
            else:
                await message.reply_text("لطفا سوال خود را بعد از دستور وارد کنید")
                return

    # Try Gemini API first
    try:
        response = api.gemini(user_input)
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        result = response.get("results")
        if result:
            await message.reply_text(result, quote=True)
            return
    except:
        pass

    # If Gemini fails, try the alternative API
    try:
        base_url = "https://open.wiki-api.ir/apis-2/ChatGPT4/?chat="
        response = requests.get(base_url + user_input)
        if response and response.text.strip():
            await message.reply_text(response.text.strip(), quote=True)
        else:
            await message.reply_text("**در حال حاضر هر دو سرویس Gemini و Chat با AI در دسترس نیستند**\n\n**Both Gemini and Chat with AI are currently unavailable**")
    except:
        await message.reply_text("**چت جی‌پی‌تی در حال حاضر در دسترس نیست. لطفا بعدا دوباره امتحان کنید**\n\n**Chatgpt is currently dead. Try again later.**")
