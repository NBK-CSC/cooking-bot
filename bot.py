import random

import telebot
from telebot import types
import config
import os
import json
from pprint import pprint
import parsing

bot = telebot.TeleBot(config.TOKEN, parse_mode=None)

LIST_OF_POPULAR_COUNTRIES = ['🇹🇭 Тайланд', '🇹🇷 Турция', '🇮🇳 Индия', '🇯🇵 Япония', '🇫🇷 Франция', '🇪🇸 Испания', '🇮🇹 Италия',
                             '🇨🇳 Китай', '🇲🇽 Мексика', '🇮🇩 Индонезия']

DICT_OF_POPULAR_COUNTRIES = {'Тайланд': 'Тайская', 'Турция': 'Турецкая', 'Индия': 'Индийская', 'Япония': 'Японская',
                             'Франция': 'Французская', 'Испания': 'Испанская', 'Италия': 'Итальянская',
                             'Китай': 'Китайская', 'Мексика': 'Мексиканская', 'Индонезия': 'Индонезийская'}

CURRENT_COUNTRY = ''

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
                                      'калорий</b> 📝\n\t\t➡\tТут вы можете узнать свою норму потребления калорий, '
                                      'либо узнать калорийность блюда',
                     reply_markup=markup_for_help, parse_mode="html")


@bot.message_handler(content_types=['text'])
def bot_message(message):
    global CURRENT_COUNTRY
    if message.text == '🥘 Готовка блюд':
        markup_for_cooking_dishes = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton('🍴 Поиск блюда')
        item2 = types.KeyboardButton('🗺 Кухни мира')
        item3 = types.KeyboardButton('🍳 Категории блюд')
        item4 = types.KeyboardButton('🧄 Поиск по ингредиентам')
        item5 = types.KeyboardButton('🔙 Назад')

        markup_for_cooking_dishes.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id,
                         'Готовка блюд имеет следущие функции:\n\n\t<b>1. Поиск блюда</b> 🍴\n\t\t➡\tТут вы можете '
                         'найти любое блюдо, которое захотите.\n\n\t<b>2. Кухни мира</b> '
                         '🗺\n\t\t➡\tТут будут представлены 10 '
                         'популярных кухонь мира. Если не нашли нужную, то введите: \n"Кухня: '
                         '✏ Русская ✏"\n\n\t<b>3. Категории блюд</b> 🍳\n\t\t➡\tТут вы можете '
                         'найти блюда по категориям. Например, завтрак\n\n\t<b>4. Поиск по '
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

        bot.send_message(message.chat.id, '10 популярных кухонь мира 🗺', reply_markup=markup_for_world_kitchens,
                         parse_mode='html')

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

    elif message.text == '🍴 Поиск блюда':
        bot.send_message(message.chat.id, 'Введите блюдо, которое хотите найти. Например: блины')

    elif message.text == '🔙 Назад':
        markup_for_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('🥘 Готовка блюд')
        item2 = types.KeyboardButton('📝 Подсчет калорий')

        markup_for_help.add(item1, item2)

        bot.send_message(message.chat.id, "Вы вернулись к выбору категории", reply_markup=markup_for_help,
                         parse_mode='html')

    elif message.text == '🔙 Нaзад':
        markup_for_cooking_dishes = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton('🍴 Поиск блюда')
        item2 = types.KeyboardButton('🗺 Кухни мира')
        item3 = types.KeyboardButton('🍳 Категории блюд')
        item4 = types.KeyboardButton('🧄 Поиск по ингредиентам')
        item5 = types.KeyboardButton('🔙 Назад')

        markup_for_cooking_dishes.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "Вы вернулись к выбору подкатегории", reply_markup=markup_for_cooking_dishes,
                         parse_mode='html')

    elif message.text[:5].lower() == 'кухня':
        markup_dishes_of_the_selected_country_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                                 resize_keyboard=True)

        country = message.text.lower()[7:]
        country = country[0].upper() + country[1:]
        CURRENT_COUNTRY = country
        list_of_countries = os.listdir('country_cuisine')
        top_ten = 0
        find_it = False

        for country_couisine in list_of_countries:
            if country == country_couisine[0:len(country)]:
                find_it = True
                with open(f'country_cuisine/{country}.json', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)-1):
                    top_ten += 1
                    random_dish = random.randint(0, len(text_json)-1)
                    markup_dishes_of_the_selected_country_dishes.add(
                        types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                    if top_ten > 19:
                        break
            if find_it == True:
                break

        bot.send_message(message.chat.id, 'По выбранной кухне предоставляю следующие двадцать блюд:',
                         reply_markup=markup_dishes_of_the_selected_country_dishes)
        bot.send_message(message.chat.id, 'Если вы не нашли нужное вам блюдо, то найдите его через поиск блюда')


    elif message.text[:2] == '🍽 ':
        dish = message.text[2:]
        dir_name = 'country_cuisine'
        countries = os.listdir(dir_name)
        found_dish = False
        print(CURRENT_COUNTRY)
        if CURRENT_COUNTRY != '':
            with open(f'country_cuisine/{CURRENT_COUNTRY}.json', 'r', encoding='utf-8') as f:
                text_json = json.load(f)

            for count_of_dishes in range(len(text_json)):
                if text_json[count_of_dishes]['name'] == dish:
                    url = text_json[count_of_dishes]['url']
                    about_dish = parsing.get_data_about_dish(url)
                    break
        else:
            for country in countries:
                with open(f'country_cuisine/{country}', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)):
                    if text_json[count_of_dishes]['name'] == dish:
                        url = text_json[count_of_dishes]['url']
                        about_dish = parsing.get_data_about_dish(url)
                        found_dish = True
                        break
                if found_dish:
                    break

        ingredients = about_dish['ingredients']
        list_of_cooking_instuction = about_dish['cooking_instructions']
        calories = about_dish['calories']
        protein = about_dish['protein']
        fat = about_dish['fat']
        carbohydrate = about_dish['carbohydrate']
        text_for_cooking_instruction = ''
        text_for_ingredients = ''

        for steps in list_of_cooking_instuction:
            text_for_cooking_instruction += steps
            text_for_cooking_instruction += '\n'

        for step, ingredient in enumerate(ingredients):
            text_for_ingredients += str(step + 1) + '. ' + ingredient[0] + ': ' + ingredient[1] + '\n'

        text_about_calories = 'Энергетическая ценность на порцию:\n\t' + str(calories) + ' ккал\n\t' + str(protein) + ' белков\n' \
                                                                                                            '\t' + \
                              str(fat) + ' жиров\n\t' + str(carbohydrate) + ' углеводов\n\t '

        markup_for_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('🥘 Готовка блюд')
        item2 = types.KeyboardButton('📝 Подсчет калорий')

        markup_for_help.add(item1, item2)
        bot.send_message(message.chat.id, text_for_ingredients)
        bot.send_message(message.chat.id, text_for_cooking_instruction)
        bot.send_message(message.chat.id, text_about_calories, reply_markup=markup_for_help)


    elif message.text in LIST_OF_POPULAR_COUNTRIES:
        country_for_dict = message.text[3:]
        country = DICT_OF_POPULAR_COUNTRIES.get(country_for_dict)
        markup_dishes_of_the_selected_country_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                                 resize_keyboard=True)
        list_of_countries = os.listdir('country_cuisine')
        top_ten = 0
        find_it = False
        CURRENT_COUNTRY = country
        for country_couisine in list_of_countries:
            if country == country_couisine[0:len(country)]:
                find_it = True
                with open(f'country_cuisine/{country}.json', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)-1):
                    top_ten += 1
                    random_dish = random.randint(0, len(text_json)-1)
                    markup_dishes_of_the_selected_country_dishes.add(
                        types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                    if top_ten > 19:
                        break
            if find_it == True:
                break

        bot.send_message(message.chat.id, 'По выбранной кухне предоставляю следующие двадцать блюд:',
                         reply_markup=markup_dishes_of_the_selected_country_dishes)
        bot.send_message(message.chat.id, 'Если вы не нашли нужное вам блюдо, то найдите его через команду "Блюдо: ✏ название блюда ✏ "')


    elif message.text == '📝 Подсчет калорий':
        markup_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_gender.add(types.KeyboardButton('Мужской'), types.KeyboardButton('Женский'))

        msg = bot.send_message(message.chat.id, 'Для того, чтобы вычислить вашу норму калорий, мне нужны некоторые '
                                          'данные.\nВаш пол:', reply_markup=markup_gender)

        bot.register_next_step_handler(msg, user_weight)

    else:
        markup_for_similar_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        CURRENT_COUNTRY = ''
        dish = message.text
        dish = dish[0].upper() + dish[1:]
        dir_name = 'country_cuisine'
        countries = os.listdir(dir_name)
        find_anything = False
        limit = 0

        for country in countries:
            with open(f'country_cuisine/{country}', 'r', encoding='utf-8') as f:
                text_json = json.load(f)

            for count_of_dishes in range(len(text_json)):
                if text_json[count_of_dishes]['name'].find(dish) != -1:
                    if limit > 120:
                        break
                    markup_for_similar_dishes.add(types.KeyboardButton("🍽 " + text_json[count_of_dishes]['name']))
                    find_anything = True
                    limit += 1
            if limit > 120:
                break

        if find_anything == True:
            bot.send_message(message.chat.id, 'По запросу нашел следующие блюда:',
                             reply_markup=markup_for_similar_dishes)
        else:
            bot.send_message(message.chat.id, 'Извините, я вас не понимаю')


def user_weight(message):
    if message.text == "Мужской" or message.text == "Женский":
        msg = bot.send_message(message.chat.id, 'Впишите свой вес:')




bot.infinity_polling()
