import telebot
from telebot import types
import config
bot = telebot.TeleBot(config.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    stic = open('stic/hello.webp', 'rb')
    bot.send_message(message.chat.id, "{0.first_name}, вас приветствует бот Шеф-Повар 👨‍🍳".format(message.from_user))
    bot.send_sticker(message.chat.id, stic)
    bot.send_message(message.chat.id, "Для ознакомления с функционалом бота, пропишите команду /help")


@bot.message_handler(commands=['help'])
def help(message):
    markup_for_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🥘 Готовка блюд')
    item2 = types.KeyboardButton('📝 Подсчет калорий')

    markup_for_help.add(item1, item2)

    bot.send_message(message.chat.id, 'У бота есть две категории:\n\n\t<b>1.Готовка блюд</b> 🥘\n\t\t➡\tТут вы можете '
                                      'найти '
                                      'рецепты для блюд и способы их приготовления\n\n\t<b>2.Подсчет '
                                      'калорий</b> 📝\n\t\t➡\tТут вы можете узнать свою норму потребления калорий, либо узнать калорийность блюда',
                     reply_markup=markup_for_help, parse_mode="html")


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == '🥘 Готовка блюд':
        markup_for_cooking_dishes = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton('🗺 Кухни мира')
        item2 = types.KeyboardButton('🍳 Категории блюд')
        item3 = types.KeyboardButton('🧄 Поиск по ингредиентам')
        item4 = types.KeyboardButton('🔙 Назад')

        markup_for_cooking_dishes.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id, 'Готовка блюд имеет следущие функции:\n\n\t<b>1. Кухни мира</b> 🗺\n\t\t➡\tТут будут представлены 10 '
                                          'популярных кухонь мира. Если не нашли нужную, то введите: \n"Страна: '
                                          '✏ название страны ✏"\n\n\t<b>2. Категории блюд</b> 🍳\n\t\t➡\tТут вы можете '
                                          'найти блюда по категориям. Например, завтрак\n\n\t<b>3. Поиск по '
                                          'ингредиентам</b> 🧄\n\t\t➡\tТут вы можете ввести ингредиенты, и бот подберет '
                                          'для вас блюдо состоящее из них',
                         reply_markup=markup_for_cooking_dishes,
                         parse_mode='html')

    elif message.text == '🗺 Кухни мира':
        markup_for_world_kitchens = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton('🇹🇭 Тайланд')
        item2 = types.KeyboardButton('🇹🇷 Турция')
        item3 = types.KeyboardButton('🇮🇳 Индия')
        item4 = types.KeyboardButton('🇯🇵 Япония')
        item5 = types.KeyboardButton('🇫🇷 Франция')
        item6 = types.KeyboardButton('🇪🇸 Испания')
        item7 = types.KeyboardButton('🇮🇹 Италия')
        item8 = types.KeyboardButton('🇨🇳 Китай')
        item9 = types.KeyboardButton('🇲🇽 Мексика')
        item10 = types.KeyboardButton('🇮🇩 Индонезия')
        item11 = types.KeyboardButton('🔙 Нaзад')


        markup_for_world_kitchens.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)

        bot.send_message(message.chat.id, '10 популярных кухонь мира 🗺', reply_markup=markup_for_world_kitchens, parse_mode='html')

    elif message.text == '🍳 Категории блюд':
        markup_for_categories = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton('🥐 Выпечка и десерты')
        item2 = types.KeyboardButton('🍲 Основные блюда')
        item3 = types.KeyboardButton('🍳 Завтраки')
        item4 = types.KeyboardButton('🥗 Салаты')
        item5 = types.KeyboardButton('🥣 Супы')
        item6 = types.KeyboardButton('🍝 Паста и пицца')
        item7 = types.KeyboardButton('🥪 Сэндвичи')
        item8 = types.KeyboardButton('🥤 Напитки')
        item9 = types.KeyboardButton('🔙 Назад')


        markup_for_categories.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)

        bot.send_message(message.chat.id, '8 категорий блюд 🍳', reply_markup=markup_for_categories, parse_mode='html')

    elif message.text == '🔙 Назад':
        markup_for_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('🥘 Готовка блюд')
        item2 = types.KeyboardButton('📝 Подсчет калорий')

        markup_for_help.add(item1, item2)

        bot.send_message(message.chat.id, "Вы вернулись к выбору категории", reply_markup=markup_for_help, parse_mode='html')

    elif message.text == '🔙 Нaзад':
        markup_for_cooking_dishes = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton('🗺 Кухни мира')
        item2 = types.KeyboardButton('🍳 Категории блюд')
        item3 = types.KeyboardButton('🧄 Поиск по ингредиентам')
        item4 = types.KeyboardButton('🔙 Назад')

        markup_for_cooking_dishes.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id, "Вы вернулись к выбору подкатегории", reply_markup=markup_for_cooking_dishes, parse_mode='html')

    # elif message.text == '📝 Подсчет калорий':
    #     bot.send_message(message.text.id, )

    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю')

bot.infinity_polling()
