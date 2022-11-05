import time

import telebot
from shop_parser import *
from decouple import config
from telebot import types


bot = telebot.TeleBot(config("TOKEN_BOT"))


@bot.message_handler(commands=["start"])
def greet_user_and_show_brands(message):
    greetings_phrase = f"Привет, {message.from_user.first_name}, здесь собирается актуальная информация по" \
                       f"ценам смартфонов в магазинах Бишкека"
    bot.reply_to(message, greetings_phrase)
    smartphone_brand_mark_up = types.InlineKeyboardMarkup(row_width=2)

    xiaomi_button = types.InlineKeyboardButton("Xiaomi", callback_data="brand_xiaomi")
    samsung_button = types.InlineKeyboardButton("Samsung", callback_data="brand_samsung")
    realme_button = types.InlineKeyboardButton("Realme", callback_data="brand_realme")
    google_button = types.InlineKeyboardButton("Google", callback_data="brand_google")
    apple_button = types.InlineKeyboardButton("Apple", callback_data="brand_apple")
    one_plus_button = types.InlineKeyboardButton("OnePlus", callback_data="brand_oneplus")

    smartphone_brand_mark_up.add(xiaomi_button,
                                 samsung_button,
                                 realme_button,
                                 google_button,
                                 apple_button,
                                 one_plus_button)

    bot.reply_to(message, "Выберите интересующий вас бренд", reply_markup=smartphone_brand_mark_up)


@bot.callback_query_handler(func=lambda call: True)
def get_brand_data_and_return_info(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    continue_button = types.InlineKeyboardButton("Далее", callback_data="continue_render")
    stop_button = types.InlineKeyboardButton("Стоп", callback_data="stop_render")
    markup.add(continue_button, stop_button)
    if call.data == "brand_xiaomi":
        xiaomi_smartphones = get_smartphones_info_telefon_kg(get_smartphones_list_html(shop_url, HEADERS))
        for each_smartphone in xiaomi_smartphones:
            bot.send_message(call.message.chat.id, f"{each_smartphone}")
    elif call.data == "brand_samsung":
        bot.send_message(call.message.chat.id, "Смартфоны Samsung")
    elif call.data == "brand_realme":
        bot.send_message(call.message.chat.id, "Смартфоны Realme")
    elif call.data == "brand_google":
        bot.send_message(call.message.chat.id, "Смартфоны Google")
    elif call.data == "brand_apple":
        bot.send_message(call.message.chat.id, "Смартфоны Apple")
    elif call.data == "brand_oneplus":
        bot.send_message(call.message.chat.id, "Смартфоны OnePlus")


bot.polling()