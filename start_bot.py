
import telebot
from telebot.types import ReplyKeyboardRemove
from shop_parser import *
from decouple import config
from telebot import types


bot = telebot.TeleBot(config("TOKEN_BOT"))
list_current_smartphones = []
continue_button_xiaomi = types.KeyboardButton("Далее")
stop_button_xiaomi = types.KeyboardButton("Стоп")
render_counter = 0


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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(continue_button_xiaomi, stop_button_xiaomi)
    global list_current_smartphones

    if call.data == "brand_xiaomi":
        list_current_smartphones = get_smartphones_info_telefon_kg(get_smartphones_list_html("https://telefon.kg/smartphone/xiaomi_smartphones", HEADERS))
        for i in range(0, 5):
            bot.send_message(call.message.chat.id, f"{list_current_smartphones[i]}")
        bot.send_message(call.message.chat.id, "Показать другие смартфоны?", reply_markup=markup)

    elif call.data == "brand_samsung":
        list_current_smartphones = get_smartphones_info_telefon_kg(
            get_smartphones_list_html("https://telefon.kg/smartphone/samsung_smartphones", HEADERS))
        for i in range(0, 5):
            bot.send_message(call.message.chat.id, f"{list_current_smartphones[i]}")
        bot.send_message(call.message.chat.id, "Показать другие смартфоны?", reply_markup=markup)

    elif call.data == "brand_realme":
        list_current_smartphones = get_smartphones_info_telefon_kg(
            get_smartphones_list_html("https://telefon.kg/smartphone/smartfony-oppo", HEADERS))
        for i in range(0, 5):
            bot.send_message(call.message.chat.id, f"{list_current_smartphones[i]}")
        bot.send_message(call.message.chat.id, "Показать другие смартфоны?", reply_markup=markup)

    elif call.data == "brand_google":
        list_current_smartphones = get_smartphones_info_telefon_kg(
            get_smartphones_list_html("https://telefon.kg/smartphone/google-pixel", HEADERS))
        for i in range(0, 5):
            bot.send_message(call.message.chat.id, f"{list_current_smartphones[i]}")
        bot.send_message(call.message.chat.id, "Показать другие смартфоны?", reply_markup=markup)

    elif call.data == "brand_apple":
        list_current_smartphones = get_smartphones_info_telefon_kg(
            get_smartphones_list_html("https://telefon.kg/smartphone/apple_smartphones", HEADERS))
        for i in range(0, 5):
            bot.send_message(call.message.chat.id, f"{list_current_smartphones[i]}")
        bot.send_message(call.message.chat.id, "Показать другие смартфоны?", reply_markup=markup)

    elif call.data == "brand_oneplus":
        list_current_smartphones = get_smartphones_info_telefon_kg(
            get_smartphones_list_html("https://telefon.kg/smartphone/oneplus_smartphones", HEADERS))
        for i in range(0, 5):
            bot.send_message(call.message.chat.id, f"{list_current_smartphones[i]}")
        bot.send_message(call.message.chat.id, "Показать другие смартфоны?", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def get_number_of_render_and_continue_render_or_break(message):
    global list_current_smartphones
    global render_counter
    if message.text.lower() == "далее":
        for i in range(render_counter, render_counter + 6):
            if render_counter >= len(list_current_smartphones):
                render_counter = 0
                list_current_smartphones.clear()
                bot.send_message(message.chat.id, "Все смартфоны были отображены", reply_markup=ReplyKeyboardRemove())
                break
            bot.send_message(message.chat.id, f"{list_current_smartphones[i]}")
            render_counter += 1
    elif message.text.lower() == "стоп":
        render_counter = 0
        list_current_smartphones.clear()
        bot.send_message(message.chat.id, "Показ смартфонов приостановлен", reply_markup=ReplyKeyboardRemove())


bot.polling()