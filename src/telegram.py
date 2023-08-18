import telegram
import src.settings as settings

bot = telegram.Bot(token=settings.BOT_TOKEN)
chat_id = settings.CHAT_ID

async def send_telegram_message(chat_id, message):
  await bot.sendMessage(chat_id=chat_id, text=message, parse_mode='Markdown')

async def send_notification(
    message,
):
  await send_telegram_message(chat_id, message)
  
