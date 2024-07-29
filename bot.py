import telebot

API_TOKEN = '7023902731:AAF2h-CaoxJUlIHCR8Vkk_cLnjOkEEJWHQc'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Это базовый Telegram-бот.")

bot.polling()
