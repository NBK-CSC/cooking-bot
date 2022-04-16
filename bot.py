import random
import telebot
from telebot import types
import config
import os
import json
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN, parse_mode=None)

LIST_OF_POPULAR_COUNTRIES = ['🇹🇭 Тайланд', '🇹🇷 Турция', '🇮🇳 Индия', '🇯🇵 Япония', '🇫🇷 Франция', '🇪🇸 Испания',
                             '🇮🇹 Италия',
                             '🇨🇳 Китай', '🇲🇽 Мексика', '🇮🇩 Индонезия']

DICT_OF_POPULAR_COUNTRIES = {'Тайланд': 'Тайская', 'Турция': 'Турецкая', 'Индия': 'Индийская', 'Япония': 'Японская',
                             'Франция': 'Французская', 'Испания': 'Испанская', 'Италия': 'Итальянская',
                             'Китай': 'Китайская', 'Мексика': 'Мексиканская', 'Индонезия': 'Индонезийская'}

LIST_OF_CATEGORIES = ['🥐 Выпечка и десерты', '🍲 Основные блюда', '🍳 Завтраки', '🥗 Салаты', '🥣 Супы',
                      '🍝 Паста и пицца', '🥪 Сэндвичи', '🥤 Напитки']

ACTIVITY_LEVELS = {'Минимальный уровень': 1.2, 'Низкий уровень': 1.375, 'Средний уровень': 1.55,
                   'Высокий уровень': 1.725, 'Очень высокий': 1.9}

now = datetime.now()
dict_of_users_category = {}
dict_of_users_kitchen = {}
dict_of_last_dish_users = {}
dict_users_last_list_of_dishes = {}
dict_of_users_ingredients = {}


def main():
    global dict_of_users_param
    dict_of_users_param = {}
    if os.path.exists('users_param.json'):
        with open('users_param.json', 'r', encoding='utf-8') as file:
            if os.stat('users_param.json').st_size:
                dict_of_users_param = json.load(file)
                for k, v in dict_of_users_param.items():
                    print(k)
                    print(v)


if __name__ == "__main__":
    main()


@bot.message_handler(commands=['start'])
def start(message):
    check_users_activity(message.chat.id)
    stic = open('stic/hello.webp', 'rb')
    bot.send_message(message.chat.id, "{0.first_name}, вас приветствует бот Шеф-Повар 👨‍🍳".format(message.from_user))
    bot.send_sticker(message.chat.id, stic)
    bot.send_message(message.chat.id, "Для ознакомления с функционалом бота, пропишите команду /help")


@bot.message_handler(commands=['help'])
def help(message):
    check_users_activity(message.chat.id)
    bot.send_message(message.chat.id, 'У бота есть две категории:\n\n\t<b>1. Готовка блюд</b> 🥘\n➔\tТут вы можете '
                                      'найти различные '
                                      'рецепты блюд и способы их приготовления.\n\n\t<b>2. Дневник калорий</b> '
                                      '📖\n➔\tТут вы можете узнать свою норму потребления калорий. После ввода ваших '
                                      'параметров, бот запомнит вашу норму потребления калорий.\n\n\t<b>3. Обновление '
                                      'дневника</b> 📝\n➔\tТут вы можете '
                                      'обновить ваш дневник калорий, изменив информацию о параметрах вашего тела.',
                     reply_markup=return_markup_for_help(), parse_mode="html")


@bot.message_handler(content_types=['text'])
def bot_message(message):
    check_users_activity(message.chat.id)
    if message.text == '🥘 Готовка блюд':
        bot.send_message(message.chat.id,
                         'Готовка блюд имеет следущие функции:\n\n\t<b>1. Поиск блюда</b> 🍴\n➔\tТут вы можете '
                         'найти любое блюдо, которое захотите.\n\n\t<b>2. Кухни мира</b> '
                         '🗺\n➔\tТут будут представлены 10 '
                         'популярных кухонь мира. Если не нашли нужную, то введите название кухни: \nНапример: '
                         '"Русская"\n\n\t<b>3. Категории блюд</b> 🍳\n➔\tТут вы можете '
                         'найти блюда по категориям. Например, завтрак\n\n\t<b>4. Поиск по '
                         'ингредиентам</b> 🧄\n➔\tТут вы можете ввести ингредиенты, и бот подберет '
                         'для вас блюдо состоящее из них',
                         reply_markup=return_markup_for_cooking(),
                         parse_mode='html')

    elif message.text == '🗺 Кухни мира':
        bot.send_message(message.chat.id, '❗ Если не нашли нужную кухню, то просто введите название.\nНапример: Русская')
        bot.send_message(message.chat.id, '🗺 10 популярных кухонь мира',
                         reply_markup=return_markup_for_kitchens_wolrd(),
                         parse_mode='html')
        dict_of_users_category[str(message.chat.id)] = ''

    elif message.text == '🍳 Категории блюд':
        bot.send_message(message.chat.id, '🍳 Список категорий блюд', reply_markup=return_markup_for_categories(),
                         parse_mode='html')
        dict_of_users_kitchen[str(message.chat.id)] = ''

    elif message.text == '🍴 Поиск блюда':
        bot.send_message(message.chat.id, '🔍 Введите блюдо, которое хотите найти. Например: блины')

    elif message.text == '🧄 Поиск по ингредиентам':
        msg = bot.send_message(message.chat.id, '🖊 Введите названия ингредиентов через запятую.\nНапример: курица, чеснок, соль')

        dict_of_users_ingredients[str(message.chat.id)] = []
        bot.register_next_step_handler(msg, add_ingredient)

    elif message.text == '🔙 Назад':
        bot.send_message(message.chat.id, text='Вы вернулись к главному меню', reply_markup=return_markup_for_help())

    elif message.text == '🔙 Нaзaд':
        bot.send_message(message.chat.id, text='Вы вернулись к меню категорий',
                         reply_markup=return_markup_for_cooking())

    elif message.text == '🔙 К выбору категорий':
        dict_of_users_kitchen[str(message.chat.id)] = ''
        dict_of_users_category[str(message.chat.id)] = ''
        bot.send_message(message.chat.id, '🍳 Список категорий блюд', reply_markup=return_markup_for_categories(),
                         parse_mode='html')

    elif message.text == '🔙 К выбору кухонь':
        dict_of_users_category[str(message.chat.id)] = ''
        dict_of_users_kitchen[str(message.chat.id)] = ''
        bot.send_message(message.chat.id, '🗺 10 популярных кухонь мира',
                         reply_markup=return_markup_for_kitchens_wolrd(),
                         parse_mode='html')


    elif message.text in LIST_OF_CATEGORIES:
        category = message.text[2:]
        markup_dishes_of_the_selected_country_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                                 resize_keyboard=True)
        markup_for_copy = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔄 Обновить список блюд'))

        dict_of_users_category[str(message.chat.id)] = category
        dict_of_users_kitchen[str(message.chat.id)] = ''
        list_of_categories = os.listdir('categories_cuisine')
        limit = 0
        find_it = False

        for category_cuisine in list_of_categories:
            if category == category_cuisine[0:len(category_cuisine) - 5]:
                find_it = True
                with open(f'categories_cuisine/{category}.json', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json) - 1):
                    limit += 1
                    random_dish = random.randint(0, len(text_json) - 1)
                    markup_dishes_of_the_selected_country_dishes.add(
                        types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                    markup_for_copy.add(
                        types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                    if limit > 120:
                        break
            if find_it == True:
                break

        markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔙 К выбору категорий'))
        markup_for_copy.add(types.KeyboardButton('🔙 К выбору категорий'))
        dict_users_last_list_of_dishes[str(message.chat.id)] = markup_for_copy
        bot.send_message(message.chat.id, '🥘 По выбранной категории предоставляю следующие блюда',
                         reply_markup=markup_dishes_of_the_selected_country_dishes)

    elif message.text in LIST_OF_POPULAR_COUNTRIES:
        country_for_dict = message.text[3:]
        country = DICT_OF_POPULAR_COUNTRIES.get(country_for_dict)
        markup_dishes_of_the_selected_country_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                                 resize_keyboard=True)
        markup_for_copy = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔄 Обновить список блюд'))
        list_of_countries = os.listdir('countries_cuisine')
        limit = 0
        find_it = False
        dict_of_users_kitchen[str(message.chat.id)] = country
        for country_couisine in list_of_countries:
            if country == country_couisine[0:len(country_couisine) - 5]:
                find_it = True
                with open(f'countries_cuisine/{country}.json', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json) - 1):
                    limit += 1
                    random_dish = random.randint(0, len(text_json) - 1)
                    markup_dishes_of_the_selected_country_dishes.add(
                        types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                    markup_for_copy.add(
                        types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                    if limit > 120:
                        break
            if find_it == True:
                break

        markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔙 К выбору кухонь'))
        markup_for_copy.add(types.KeyboardButton('🔙 К выбору кухонь'))

        dict_users_last_list_of_dishes[str(message.chat.id)] = markup_for_copy
        bot.send_message(message.chat.id, '🥘 По выбранной категории предоставляю следующие блюда',
                         reply_markup=markup_dishes_of_the_selected_country_dishes)
        dict_of_users_category[str(message.chat.id)] = ''

    elif message.text == '🔄 Обновить список блюд':
        markup_dishes_of_the_selected_country_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                                 resize_keyboard=True)
        markup_for_copy = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔄 Обновить список блюд'))
        if dict_of_users_kitchen[str(message.chat.id)] != '':
            list_of_countries = os.listdir('countries_cuisine')
            limit = 0
            find_it = False
            for country_couisine in list_of_countries:
                if dict_of_users_kitchen[str(message.chat.id)] == country_couisine[0:len(country_couisine) - 5]:
                    find_it = True
                    with open(f'countries_cuisine/{dict_of_users_kitchen.get(str(message.chat.id))}.json', 'r',
                              encoding='utf-8') as f:
                        text_json = json.load(f)

                    for count_of_dishes in range(len(text_json) - 1):
                        limit += 1
                        random_dish = random.randint(0, len(text_json) - 1)
                        markup_dishes_of_the_selected_country_dishes.add(
                            types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                        markup_for_copy.add(
                            types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                        if limit > 120:
                            break
                if find_it == True:
                    break

            markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔙 К выбору кухонь'))
            markup_for_copy.add(types.KeyboardButton('🔙 К выбору кухонь'))
            dict_users_last_list_of_dishes[str(message.chat.id)] = markup_for_copy

            bot.send_message(message.chat.id, '🔄 Обновляю список блюд...',
                             reply_markup=markup_dishes_of_the_selected_country_dishes)

        elif dict_of_users_category[str(message.chat.id)] != '':
            list_of_categories = os.listdir('categories_cuisine')
            limit = 0
            find_it = False
            for categori_couisine in list_of_categories:
                if dict_of_users_category[str(message.chat.id)] == categori_couisine[0:len(categori_couisine) - 5]:
                    find_it = True
                    with open(f'categories_cuisine/{dict_of_users_category.get(str(message.chat.id))}.json', 'r',
                              encoding='utf-8') as f:
                        text_json = json.load(f)

                    for count_of_dishes in range(len(text_json) - 1):
                        limit += 1
                        random_dish = random.randint(0, len(text_json) - 1)
                        markup_dishes_of_the_selected_country_dishes.add(
                            types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                        markup_for_copy.add(
                            types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                        if limit > 120:
                            break
                if find_it == True:
                    break

            markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔙 К выбору категорий'))
            markup_for_copy.add(types.KeyboardButton('🔙 К выбору категорий'))
            dict_users_last_list_of_dishes[str(message.chat.id)] = markup_for_copy
            bot.send_message(message.chat.id, '🔄 Обновляю список блюд...',
                             reply_markup=markup_dishes_of_the_selected_country_dishes)

    elif message.text == '🔙 Вернуться к списку блюд':
        markup = dict_users_last_list_of_dishes[str(message.chat.id)]
        bot.send_message(message.chat.id, '📃 Список блюд:', reply_markup=markup)

    elif message.text[:2] == '🍽 ':
        if message.chat.id in dict_of_last_dish_users:
            pass
        else:
            dict_of_last_dish_users[message.chat.id] = 0

        dish = message.text[2:]
        dir_name = 'countries_cuisine'
        countries = os.listdir(dir_name)
        categories = os.listdir('categories_cuisine')
        found_dish = False
        if (message.chat.id in dict_of_users_kitchen) or (message.chat.id in dict_of_users_category):
            if dict_of_users_kitchen[str(message.chat.id)] != '':
                with open(f'countries_cuisine/{dict_of_users_kitchen.get(str(message.chat.id))}.json', 'r',
                          encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)):
                    if text_json[count_of_dishes]['name'] == dish:
                        break
            if dict_of_users_category[str(message.chat.id)] != '':
                with open(f'categories_cuisine/{dict_of_users_category.get(str(message.chat.id))}.json', 'r',
                          encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)):
                    if text_json[count_of_dishes]['name'] == dish:
                        break
        else:
            for country in countries:
                with open(f'countries_cuisine/{country}', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)):
                    if text_json[count_of_dishes]['name'] == dish:
                        found_dish = True
                        break
                if found_dish:
                    break
            if found_dish == False:
                for category in categories:
                    with open(f'categories_cuisine/{category}', 'r', encoding='utf-8') as f:
                        text_json = json.load(f)

                    for count_of_dishes in range(len(text_json)):
                        if text_json[count_of_dishes]['name'] == dish:
                            found_dish = True
                            break
                    if found_dish:
                        break

        if text_json[count_of_dishes]['cook_time'] != 0:
            cook_time = "<b>2. Время приготовления и кол-во порций</b> 🕖\n➔ " + text_json[count_of_dishes][
                'cook_time'] + "\n➔ " + str(text_json[count_of_dishes]['servings_count']) + " порции"
        ingredients = text_json[count_of_dishes]['ingredients']
        list_of_cooking_instuction = text_json[count_of_dishes]['cooking_instructions']
        calories = text_json[count_of_dishes]['calories']
        protein = text_json[count_of_dishes]['protein']
        fat = text_json[count_of_dishes]['fat']
        carbohydrate = text_json[count_of_dishes]['carbohydrate']
        text_for_cooking_instruction = '<b>3. Шаги приготовления</b> 👣\n'
        text_for_ingredients = '<b>1. Ингредиенты</b> 🧂\n'

        dict_of_last_dish_users[message.chat.id] = int(calories)

        for steps in list_of_cooking_instuction:
            text_for_cooking_instruction += '➔\t' + steps
            text_for_cooking_instruction += '\n'

        for step, ingredient in enumerate(ingredients):
            text_for_ingredients += '➔\t' + ingredient[0] + ': ' + ingredient[1] + '\n'

        text_about_calories = '<b>4. Энергетическая ценность</b> 📄\n➔\t' + str(calories) + ' ккал\n➔\t' + \
                              str(protein) + ' белков\n➔' \
                                             '\t' + \
                              str(fat) + ' жиров\n➔\t' + str(carbohydrate) + ' углеводов'

        markup_for_add_at_diary = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_for_add_at_diary.add(types.KeyboardButton('🔙 Вернуться к списку блюд'))
        bot.send_message(message.chat.id, text_for_ingredients, parse_mode='html')
        bot.send_message(message.chat.id, cook_time, parse_mode='html')
        bot.send_message(message.chat.id, text_for_cooking_instruction, parse_mode='html')
        bot.send_message(message.chat.id, text_about_calories, parse_mode='html', reply_markup=markup_for_add_at_diary)
        dict_of_users_category[str(message.chat.id)] = ''
        dict_of_users_kitchen[str(message.chat.id)] = ''

    elif message.text == '📖 Дневник калорий':
        if str(message.chat.id) in dict_of_users_param:
            markup_for_add_calories = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup_for_add_calories.add(types.KeyboardButton('Добавить калории'),
                                        types.KeyboardButton('Обнулить калории'), types.KeyboardButton('🔙 Назад'))
            basal_metabolism_for_send = f'<b>{dict_of_users_param.get(str(message.chat.id))[5]} ккал/сутки</b>. Это ваш <b>базовый метаболизм</b> (основной обмен). Это калории, которые сжигаются, когда вы находитесь в покое, и энергия тратится на обеспечение процессов дыхания, кровообращения, поддержание температуры тела и т.д.'
            normal_calories_for_send = f'<b>{dict_of_users_param.get(str(message.chat.id))[6]} ккал/сутки</b>. Ваша <b>норма калорий</b> для поддержания веса с текущей физической активностью (вы не худеете и не набираете вес)'
            bot.send_message(message.chat.id, basal_metabolism_for_send, parse_mode='html')
            bot.send_message(message.chat.id, normal_calories_for_send, parse_mode='html')
        else:
            markup_gender = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup_gender.add(types.KeyboardButton('🙋‍♂️ Мужской'), types.KeyboardButton('🙋‍♀️ Женский'))

            msg = bot.send_message(message.chat.id, 'Для того, чтобы вычислить вашу норму калорий, мне нужны некоторые '
                                                    'данные.\nВаш пол:', reply_markup=markup_gender)
            bot.register_next_step_handler(msg, user_gender)

    elif message.text == '📝 Обновление дневника':
        markup_gender = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_gender.add(types.KeyboardButton('🙋‍♂️ Мужской'), types.KeyboardButton('🙋‍♀️ Женский'))

        msg = bot.send_message(message.chat.id, 'Для того, чтобы вычислить вашу норму калорий, мне нужны некоторые '
                                                'данные.\nВаш пол:', reply_markup=markup_gender)
        bot.register_next_step_handler(msg, user_gender)

    else:
        #TODO Сделать нормальный рандом блюд
        list_of_countries = os.listdir('countries_cuisine')
        find_it = False
        user_input = message.text.lower()
        user_input = user_input[0].upper() + user_input[1:]
        for country_couisine in list_of_countries:
            if user_input == country_couisine[0:len(country_couisine) - 5]:
                find_it = True

        if find_it == True:
            markup_dishes_of_the_selected_country_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                                     resize_keyboard=True)
            markup_for_copy = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔄 Обновить список блюд'))
            dict_of_users_kitchen[str(message.chat.id)] = user_input
            dict_of_users_category[str(message.chat.id)] = ''
            limit = 0

            with open(f'countries_cuisine/{user_input}.json', 'r', encoding='utf-8') as f:
                text_json = json.load(f)

            for count_of_dishes in range(len(text_json) - 1):
                limit += 1
                random_dish = random.randint(0, len(text_json) - 1)
                markup_dishes_of_the_selected_country_dishes.add(
                    types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                markup_for_copy.add(
                    types.KeyboardButton("🍽 " + text_json[random_dish]['name']))
                if limit > 120:
                    break
            markup_dishes_of_the_selected_country_dishes.add(types.KeyboardButton('🔙 Нaзaд'))
            markup_for_copy.add(types.KeyboardButton('🔙 Нaзaд'))
            dict_users_last_list_of_dishes[str(message.chat.id)] = markup_for_copy
            bot.send_message(message.chat.id,
                             f'🥘 По запросу "Кухня: {message.text}" предоставляю следующие двадцать блюд',
                             reply_markup=markup_dishes_of_the_selected_country_dishes)

        else:
            markup_for_similar_dishes = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            dish = message.text
            dish = dish[0].upper() + dish[1:]
            dir_name = 'countries_cuisine'
            countries = os.listdir(dir_name)
            categories = os.listdir('categories_cuisine')
            find_anything = False
            limit = 0

            for country in countries:
                with open(f'countries_cuisine/{country}', 'r', encoding='utf-8') as f:
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

            for category in categories:
                with open(f'categories_cuisine/{category}', 'r', encoding='utf-8') as f:
                    text_json = json.load(f)

                for count_of_dishes in range(len(text_json)):
                    if text_json[count_of_dishes]['name'].find(dish) != -1:
                        if limit > 120:
                            break
                        markup_for_similar_dishes.add(
                            types.KeyboardButton("🍽 " + text_json[count_of_dishes]['name']))
                        find_anything = True
                        limit += 1
                if limit > 120:
                    break

            if find_anything == True:
                markup_for_similar_dishes.add(types.KeyboardButton('🔙 Нaзaд'))
                dict_users_last_list_of_dishes[str(message.chat.id)] = markup_for_similar_dishes
                bot.send_message(message.chat.id, '✅ По запросу нашел следующие блюда:',
                                 reply_markup=markup_for_similar_dishes)
            else:
                bot.send_message(message.chat.id, '❌ Извините, я вас не понимаю')


def user_gender(message):
    if message.text == "🙋‍♂️ Мужской" or message.text == "🙋‍♀️ Женский":
        msg = bot.send_message(message.chat.id, 'Введити свой рост в сантиметрах')
        mass = []
        mass.append(message.text[5:])
        dict_of_users_param[str(message.chat.id)] = mass
        del mass
        bot.register_next_step_handler(msg, user_height)
    elif message.text == "/help":
        del dict_of_users_param[str(message.chat.id)]
        bot.send_message(message.chat.id, 'Вы вернулись к главному меню', reply_markup=return_markup_for_help())
    else:
        msg = bot.send_message(message.chat.id, '❌ Некорректно введен пол')
        bot.register_next_step_handler(msg, user_gender)


def user_height(message):
    if message.text.isdigit():
        if int(message.text) > 66 and int(message.text) < 273:
            msg = bot.send_message(message.chat.id, 'Введите свой вес')
            dict_of_users_param.get(str(message.chat.id)).append(int(message.text))
            bot.register_next_step_handler(msg, user_weight)
        else:
            msg = bot.send_message(message.chat.id, '❌ Не думаю, что вы такого роста 😉\n Введите еще раз')
            bot.register_next_step_handler(msg, user_height)
    elif message.text == "/help":
        del dict_of_users_param[message.chat.id]
        bot.send_message(message.chat.id, 'Вы вернулись к главному меню', reply_markup=return_markup_for_help())
    else:
        msg = bot.send_message(message.chat.id, '❌ Некорректно введен рост, введите еще раз')
        bot.register_next_step_handler(msg, user_height)


def user_weight(message):
    if message.text.isdigit():
        if int(message.text) > 1 and int(message.text) < 545:
            msg = bot.send_message(message.chat.id, "Введите свой возраст")
            dict_of_users_param.get(str(message.chat.id)).append(int(message.text))
            bot.register_next_step_handler(msg, user_age)
        else:
            msg = bot.send_message(message.chat.id, '❌ Не думаю, что вы столько весите 😉\n Введите еще раз')
            bot.register_next_step_handler(msg, user_weight())
    elif message.text == "/help":
        del dict_of_users_param[str(message.chat.id)]
        bot.send_message(message.chat.id, 'Вы вернулись к главному меню', reply_markup=return_markup_for_help())
    else:
        msg = bot.send_message(message.chat.id, '❌ Некорректно введен вес, введите еще раз')
        bot.register_next_step_handler(msg, user_weight)


def user_age(message):
    if message.text.isdigit():
        if int(message.text) > 0 and int(message.text) < 100:
            markup_activity = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup_activity.add(types.KeyboardButton('Минимальный уровень'), types.KeyboardButton('Низкий уровень'),
                                types.KeyboardButton('Средний уровень'), types.KeyboardButton('Высокий уровень'),
                                types.KeyboardButton('Очень высокий'))
            msg = bot.send_message(message.chat.id,
                                   '<b>Степень физической активности</b>: \n\t\t<b>1. Минимальный уровень</b>: Для '
                                   'малоподвижных людей, тренировок мало или они отсутствуют\n\t\t '
                                   '<b>2. Низкий уровень</b>: Для людей с низкой активностью, легкие тренировки 1-3 '
                                   'раза в неделю или в виде эквивалента другой активности.\n\t\t '
                                   '<b>3. Средний уровень</b>: Для умеренно активных людей: физическая работа средней '
                                   'тяжести или регулярные тренировки 3-5 дней в неделю.\n\t\t '
                                   '<b>4. Высокий уровень</b>: Для очень активных людей: физическая работа полный '
                                   'день или интенсивные тренировки 6-7 раз в неделю.\n\t\t '
                                   '<b>5. Очень высокий</b>: Для предельно активных людей: тяжелая физическая работа '
                                   'и интенсивные тренировки/занятия спортом.',
                                   reply_markup=markup_activity, parse_mode='html')
            dict_of_users_param.get(str(message.chat.id)).append(int(message.text))
            bot.register_next_step_handler(msg, activity_level)
        else:
            msg = bot.send_message(message.chat.id, '❌ Не думаю, что вам столько лет 😉\n Введите еще раз')
            bot.register_next_step_handler(msg, user_age)
    elif message.text == "/help":
        del dict_of_users_param[str(message.chat.id)]
        bot.send_message(message.chat.id, 'Вы вернулись к главному меню', reply_markup=return_markup_for_help())
    else:
        msg = bot.send_message(message.chat.id, '❌ Некорректно введен возраст, введите еще раз')
        bot.register_next_step_handler(msg, user_age)


def activity_level(message):
    if message.text in ACTIVITY_LEVELS:
        dict_of_users_param.get(str(message.chat.id)).append(ACTIVITY_LEVELS.get(message.text))
        print(dict_of_users_param.get(str(message.chat.id)))
        if dict_of_users_param.get(str(message.chat.id))[0] == "Мужской":
            basal_metabolism = dict_of_users_param.get(str(message.chat.id))[4] * (
                    9.99 * dict_of_users_param.get(str(message.chat.id))[2] + 6.25 *
                    dict_of_users_param.get(str(message.chat.id))[1] - 4.92 *
                    dict_of_users_param.get(str(message.chat.id))[3] + 5)
        else:
            basal_metabolism = dict_of_users_param.get(str(message.chat.id))[4] * (
                    9.99 * dict_of_users_param.get(str(message.chat.id))[2] + 6.25 *
                    dict_of_users_param.get(str(message.chat.id))[1] - 4.92 *
                    dict_of_users_param.get(str(message.chat.id))[3] - 161)
        basal_metabolism = round(basal_metabolism)
        basal_metabolism_for_send = f'<b>{round(basal_metabolism / (dict_of_users_param.get(str(message.chat.id))[4]))} ккал/сутки</b>. Это ваш <b>базовый метаболизм</b> (основной обмен). Это калории, которые сжигаются, когда вы находитесь в покое, и энергия тратится на обеспечение процессов дыхания, кровообращения, поддержание температуры тела и т.д. '
        normal_calories_for_send = f'<b>{basal_metabolism} ккал/сутки</b>. Ваша <b>норма калорий</b> для поддержания веса с текущей физической активностью (вы не худеете и не набираете вес)'
        dict_of_users_param.get(str(message.chat.id)).append(
            round(basal_metabolism / (dict_of_users_param.get(str(message.chat.id))[4])))
        dict_of_users_param.get(str(message.chat.id)).append(basal_metabolism)
        add_paramaters_at_json(dict_of_users_param)
        bot.send_message(message.chat.id, basal_metabolism_for_send, parse_mode='html')
        bot.send_message(message.chat.id, normal_calories_for_send, parse_mode='html',
                         reply_markup=return_markup_for_help())


    elif message.text == "/help":
        del dict_of_users_param[str(message.chat.id)]
        bot.send_message(message.chat.id, 'Вы вернулись к главному меню', reply_markup=return_markup_for_help())
    else:
        msg = bot.send_message(message.chat.id, '❌ Некорректно введена активность, введите еще раз')
        bot.register_next_step_handler(msg, activity_level)


def add_paramaters_at_json(dict):
    with open('users_param.json', 'w+', encoding='utf-8') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)


def add_ingredient(message):
    markup_find_dishes = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    list_of_dishes = []
    ingredients = message.text.split(",")
    for i in range(0, len(ingredients)):
        if ingredients[i][0] == " ":
            ingredients[i] = ingredients[i][1:]
        elif ingredients[i][len(ingredients[i]) - 1] == " ":
            ingredients[i] = ingredients[i][0:len(ingredients[i]) - 1]
        ingredients[i] = ingredients[i].lower()
    dict_of_users_ingredients[str(message.chat.id)] = ingredients
    countries = os.listdir('countries_cuisine')
    categories = os.listdir('categories_cuisine')
    mass_of_ingredients = []
    find_it = False
    print(ingredients)

    for country in countries:
        with open(f'countries_cuisine/{country}', 'r', encoding='utf-8') as f:
            text_json = json.load(f)

        for dishes in text_json:
            for all_ingredients in dishes['ingredients']:
                mass_of_ingredients.append(all_ingredients[0].lower())
            coincidence = 0
            for ingredient in dict_of_users_ingredients.get(str(message.chat.id)):
                if find_it:
                    find_it = False
                    break
                for ingredient_of_dishes in mass_of_ingredients:
                    if ingredient.lower() in ingredient_of_dishes.lower():
                        coincidence += 1
                        if coincidence == len(dict_of_users_ingredients.get(str(message.chat.id))):
                            list_of_dishes.append("🍽 " + dishes['name'])
                            find_it = True
                        break
            mass_of_ingredients = []

    mass_of_ingredients = []
    find_it = False

    for category in categories:
        with open(f'categories_cuisine/{category}', 'r', encoding='utf-8') as f:
            text_json = json.load(f)

        for dishes in text_json:
            for all_ingredients in dishes['ingredients']:
                mass_of_ingredients.append(all_ingredients[0].lower())
            coincidence = 0
            for ingredient in dict_of_users_ingredients.get(str(message.chat.id)):
                if find_it:
                    find_it = False
                    break
                for ingredient_of_dishes in mass_of_ingredients:
                    if ingredient.lower() in ingredient_of_dishes.lower():
                        coincidence += 1
                        if coincidence == len(dict_of_users_ingredients.get(str(message.chat.id))):
                            list_of_dishes.append("🍽 " + dishes['name'])
                            find_it = True
                        break
            mass_of_ingredients = []

    list_of_dishes = list(set(list_of_dishes))
    print(list_of_dishes)

    if list_of_dishes != []:
        for _ in range(0, 115):
            if list_of_dishes == []:
                break
            random_dish = random.choice(list_of_dishes)
            markup_find_dishes.add(types.KeyboardButton(random_dish))
            list_of_dishes.remove(random_dish)

        markup_find_dishes.add(types.KeyboardButton("🔙 Нaзaд"))
        dict_users_last_list_of_dishes[str(message.chat.id)] = markup_find_dishes
        bot.send_message(message.chat.id, '✅ Нашел следующие блюда', reply_markup=markup_find_dishes)
    else:
        bot.send_message(message.chat.id, '❌ По вашему запросу ничего не нашел')


def return_markup_for_help():
    markup_for_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🥘 Готовка блюд')
    item2 = types.KeyboardButton('📖 Дневник калорий')
    item3 = types.KeyboardButton('📝 Обновление дневника')
    markup_for_help.add(item1, item2, item3)
    return markup_for_help


def return_markup_for_cooking():
    markup_for_cooking_dishes = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🍴 Поиск блюда')
    item2 = types.KeyboardButton('🗺 Кухни мира')
    item3 = types.KeyboardButton('🍳 Категории блюд')
    item4 = types.KeyboardButton('🧄 Поиск по ингредиентам')
    item5 = types.KeyboardButton('🔙 Назад')
    markup_for_cooking_dishes.add(item1, item2, item3, item4, item5)
    return markup_for_cooking_dishes


def return_markup_for_kitchens_wolrd():
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
    item11 = types.KeyboardButton('🔙 Нaзaд')
    markup_for_world_kitchens.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)
    return markup_for_world_kitchens


def return_markup_for_categories():
    markup_for_categories = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🥐 Выпечка и десерты')
    item2 = types.KeyboardButton('🍲 Основные блюда')
    item3 = types.KeyboardButton('🍳 Завтраки')
    item4 = types.KeyboardButton('🥗 Салаты')
    item5 = types.KeyboardButton('🥣 Супы')
    item6 = types.KeyboardButton('🍝 Паста и пицца')
    item7 = types.KeyboardButton('🥪 Сэндвичи')
    item8 = types.KeyboardButton('🥤 Напитки')
    item9 = types.KeyboardButton('🔙 Нaзaд')
    markup_for_categories.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    return markup_for_categories


def check_users_activity(id):
    if not os.path.isdir('activity'):
        os.mkdir('activity')
    if not os.path.exists(f'activity/{now.date()}.txt'):
        f = open(f'activity/{now.date()}.txt', 'x')
        f.close()
    with open(f'activity/{now.date()}.txt', 'r+', encoding='utf-8') as file:
        info = file.read()
        if not (str(id) in info):
            file.write(f"{id}\n")


bot.infinity_polling()
