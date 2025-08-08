import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetMessagesRequest
from tqdm.asyncio import tqdm

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT = int(os.getenv("TARGET_CHAT"))

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern=r'https://t.me/([^/]+)/(\d+)'))
async def clone_handler(event):
    match = re.match(r'https://t.me/([^/]+)/(\d+)', event.raw_text)
    if not match:
        await event.reply("❌ Invalid link format")
        return

    channel = match.group(1)
    msg_id = int(match.group(2))

    await event.reply(f"🔄 Cloning from `{channel}`, starting at message {msg_id}...")
    
    try:
        messages = await bot.get_messages(channel, ids=msg_id)
        total = 1 if not isinstance(messages, list) else len(messages)

        # Simple progress bar
        for i in tqdm(range(total), desc="Cloning Progress"):
            msg = messages if total == 1 else messages[i]
            await bot.send_message(TARGET_CHAT, msg)
            await asyncio.sleep(0.5)

        await event.reply(f"✅ Cloning complete: {total} messages")
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")

print("Bot is running...")
bot.run_until_disconnected()
