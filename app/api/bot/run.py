import telebot
from app.core.config import BOT_MINI_APP_URL, BOT_TOKEN
from telebot import types
from telebot.types import WebAppInfo

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    markup = types.InlineKeyboardMarkup()

    button = types.InlineKeyboardButton(
        "Add spending",
        web_app=WebAppInfo(url=BOT_MINI_APP_URL),
    )

    markup.add(button)
    bot.reply_to(message, 'Please tap the button below to add your spending!', reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
