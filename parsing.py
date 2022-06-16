from multiprocessing import Process, current_process, Semaphore
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import asyncio
import aiohttp
import requests
import re
import json
import time
import os
import math

MAIN_URL = 'https://eda.ru'
CATEGORIES_CUISINE = "categories_cuisine"
COUNTRIES_CUISINE = "countries_cuisine"
RECIPES = "/recepty/"

headers = {
    "user-agent": UserAgent().random,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

def write_logs(data):
    global NOW
    NOW = datetime.now().strftime("%d-%m-%Y")
    create_folder('logs')
    with open(f"logs\\{NOW}.txt", 'a+') as file:
        file.write(data)
        file.write("\n")


async def get_data_about_dish(url, session, dishes, retry=5):
    try:
        async with session.get(url=url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            name = soup.find(class_="emotion-gl52ge")
            url_image=soup.find("img", class_="emotion-hsr74c")
            cook_time = soup.find('div', class_='emotion-my9yfq')
            servings_count = soup.find('span', itemprop='recipeYield')
            calories = soup.find('span', itemprop="calories")
            protein = soup.find('span', itemprop="proteinContent")
            fat = soup.find('span', itemprop="fatContent")
            carbohydrate = soup.find('span', itemprop="carbohydrateContent")
            count_ingredients = soup("span", class_='emotion-15im4d2')
            cooking_instructions = soup("span", itemprop="text")
            additional_information = soup("span", class_="emotion-yq9yyo")
            category = None
            country = None
            if additional_information:
                if len(additional_information) >= 1:
                    category = additional_information[0]
                if len(additional_information) >= 2:
                    if "кухня" in additional_information[1].text.strip():
                        country = additional_information[1]

            ingredients = []
            parse_ingredients = soup("span", itemprop='recipeIngredient')
            for i in range(len(parse_ingredients)):
                ingredients.append([parse_ingredients[i].text.strip(), count_ingredients[i].text.strip()])

            dishes.append({
                "name": name.text.strip().replace("\xa0", " "),
                "url": url,
                "url_image": url_image["src"] if url_image is not None else 0,
                "category": category.text.strip() if category is not None else 0,
                "country": country.text.strip() if country is not None else 0,
                "cook_time": cook_time.text.strip() if cook_time is not None else 0,
                "servings_count": int(servings_count.text.strip()) if servings_count is not None else 0,
                "count_ingredient": len(parse_ingredients),
                "ingredients": ingredients,
                "calories": int(calories.text.strip()) if calories is not None else 0,
                "protein": int(protein.text.strip()) if protein is not None else 0,
                "fat": int(fat.text.strip()) if fat is not None else 0,
                "carbohydrate": int(carbohydrate.text.strip()) if carbohydrate is not None else 0,
                "cooking_instructions": [c.text.strip().replace("\xa0", " ").replace("­", "") for c in
                                         cooking_instructions]
            })
    except Exception:
        time.sleep(3)
        if retry:
            await get_data_about_dish(url, session, dishes, retry=retry - 1)
        else:
            write_logs(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Exception: attempts are over; url = {url}")


async def parse_pages(url, page, session, dishes, retry=5):  # парсинг страницы
    pages_url = url + f"?page={page}"
    try:
        async with session.get(url=pages_url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            urls_dishes = soup('span', class_="emotion-1j2opmb")
            tasks = []
            for url_dish in urls_dishes:
                tasks.append(
                    asyncio.create_task(get_data_about_dish(MAIN_URL + url_dish.findParent()["href"], session, dishes)))
            await asyncio.gather(*tasks)
    except Exception:
        time.sleep(3)
        if retry:
            await parse_pages(url, page, session, dishes, retry=retry - 1)
        else:
            write_logs(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Exception: attempts are over; url = {url}")
        return


async def parse_catalog(main_catalog, category_name, url):  # парсинг канкретного каталога
    dishes = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        dishes_count = soup.find('span', class_="emotion-1ad0u8b")
        if not dishes_count:
            return
        pages_count = math.ceil(int(re.findall(r'\d+', dishes_count.text.strip())[0]) / 14) + 2

        limit_pages = 10
        start = time.time()
        for l_pages in range(pages_count // limit_pages + 1):
            tasks = []
            for page in range(l_pages * limit_pages + 1,
                              l_pages * limit_pages + limit_pages + 1 if l_pages * limit_pages + limit_pages + 1 < pages_count else pages_count):
                tasks.append(asyncio.create_task(parse_pages(url, page, session, dishes)))
            await asyncio.gather(*tasks)

        if len(dishes) == 0:
            write_logs(
                f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Exception: information not recorded: dishes={len(dishes)} => \"{category_name}\"; url = {url}; time={time.time() - start}c")
            return
        write_logs(
            f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] end => \"{category_name}\"; dishes={len(dishes)}; url = {url}; time={time.time() - start}c")
        writing_to_json(f'{main_catalog}\\{category_name}', dishes)


def writing_to_json(path, dishes):
    with open(f'{path}.json', 'w', encoding='utf-8') as json_file:
        json.dump(dishes, json_file, indent=4, ensure_ascii=False)
    json_file.close()


def create_folder(folder):
    if os.path.isdir(folder):
        return
    os.mkdir(folder)


def bridge_async_threading(sem, main_catalog, category_name, url):
    with sem:
        write_logs(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] start => \"{category_name}\"; url = {url}")
        asyncio.get_event_loop().run_until_complete(parse_catalog(main_catalog, category_name, url))


def parse_recipe_catalogs(url):  # парсинг каталогов с блюдами
    global NOW
    NOW = datetime.now().strftime("%d-%m-%Y")
    create_folder(CATEGORIES_CUISINE)

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    recipe_selection_categories = soup('ul', class_="select-suggest__result js-select-suggest__result")
    categories = recipe_selection_categories[0]('li')

    sem = Semaphore(5)
    for i in range(1, len(categories) - 1):
        url_category = MAIN_URL + RECIPES + categories[i]['data-select-suggest-value']
        Process(target=bridge_async_threading,
                args=(sem, CATEGORIES_CUISINE, categories[i].text.strip(), url_category)).start()


def parse_country_catalogs(url):  # парсинг каталогов с странами
    global NOW
    NOW = datetime.now().strftime("%d-%m-%Y")
    create_folder(COUNTRIES_CUISINE)

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    recipe_selection_categories = soup('ul', class_="select-suggest__result js-select-suggest__result")
    countries = recipe_selection_categories[2]('li')

    sem = Semaphore(5)
    for i in range(44, len(countries)):
        url_country = MAIN_URL + RECIPES + countries[i]['data-select-suggest-value']
        Process(target=bridge_async_threading,
                args=(sem, COUNTRIES_CUISINE, countries[i].text.strip(), url_country)).start()


def main():
    parse_recipe_catalogs(MAIN_URL)
    parse_country_catalogs(MAIN_URL)


if __name__ == "__main__":
    main()