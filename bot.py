import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def handle_start(message):
    stic = open('stic/hello.webp', 'rb')
    bot.send_message(message.chat.id, "{0.first_name}, вас приветствует бот Шеф-Повар 👨‍🍳".format(message.from_user))
    bot.send_sticker(message.chat.id, stic)
    bot.send_message(message.chat.id, "Для ознакомления с функционалом бота, пропишите команду /help")


@bot.message_handler(commands=['help'])
def handle_help(message):
    markup_for_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Готовка блюд')
    item2 = types.KeyboardButton('Подсчет калорий')

    markup_for_help.add(item1, item2)

    bot.send_message(message.chat.id, 'У бота есть две категории:\n\n\t<b>1.Готовка блюд</b> 🥘\n\t\t➡\tТут вы можете '
                                      'найти '
                                      'рецепты для блюд и способы их приготовления\n\n\t<b>2.Подсчет '
                                      'калорий</b>\n\t\t➡\t',
                     reply_markup=markup_for_help, parse_mode="html")


@bot.message_handler(func=lambda m: True)
def country_kitchen(message):
    if message.text.lower() == "кухни мира":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Итальянская🇮🇹')
        item2 = types.KeyboardButton('Русская🇷🇺')
        item3 = types.KeyboardButton('Японская🇯🇵')
        item4 = types.KeyboardButton('Французская🇫🇷')
        item5 = types.KeyboardButton('Вьетнамская🇻🇳')
        item6 = types.KeyboardButton('Китайская🇨🇳')
        item7 = types.KeyboardButton('Грузинская🇬🇪')
        item8 = types.KeyboardButton('Корейская🇰🇷')

        markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

        bot.send_message(message.chat.id,
                         "Если не нашли нужную вам страну, то напишите: Кухня %Название страны%".format(
                             message.from_user), reply_markup=markup)
    # elif message.text.lower() == "":

    else:
        bot.reply_to(message, "Извините, но я не понимаю о чем вы")


bot.infinity_polling()
