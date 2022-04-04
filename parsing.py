import math
from multiprocessing import Process, current_process, Semaphore
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
import requests
import re
import json
import time
import os

MAIN_URL = 'https://eda.ru'
CATEGORIES_CUISINE = "categories_cuisine"
COUNTRIES_CUISINE = "countries_cuisine"
RECIPES = "/recepty/"

headers = {
    "user-agent": UserAgent().random,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

async def get_data_about_dish(url, session, dishes, retry=5):
    try:
        async with session.get(url=url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            name = soup.find(class_="emotion-gl52ge").text.strip().replace("\xa0", " ")
            cook_time = soup.find('div',class_='emotion-my9yfq')
            servings_count = soup.find('span',class_='recipeYield')
            calories = soup.find('span', itemprop="calories")
            protein = soup.find('span', itemprop="proteinContent")
            fat = soup.find('span', itemprop="fatContent")
            carbohydrate = soup.find('span', itemprop="fatContent")
            parse_count_ingredients = soup("span", class_='emotion-15im4d2')
            parse_cooking_instructions = soup("span", itemprop="text")

            ingredients = []
            parse_ingredients = soup("span", itemprop='recipeIngredient')
            for i in range(len(parse_ingredients)):
                ingredients.append([parse_ingredients[i].text.strip(), parse_count_ingredients[i].text.strip()])

            dishes.append({
                "name": name,
                "url": url,
                "cook_time": cook_time.text.strip() if cook_time is not None else 0,
                "servings_count": servings_count.text.strip() if servings_count is not None else 0,
                "count_ingredient": len(parse_ingredients),
                "ingredients": ingredients,
                "calories": calories.text.strip() if calories is not None else 0,
                "protein": protein.text.strip() if protein is not None else 0,
                "fat":fat.text.strip() if fat is not None else 0,
                "carbohydrate": carbohydrate.text.strip() if carbohydrate is not None else 0,
                "cooking_instructions": [c.text.strip().replace("\xa0", " ").replace("­", "") for c in
                                         parse_cooking_instructions]
            })
    except Exception as e:
        time.sleep(3)
        # if retry < 3:
            # print(f"{current_process().name} [INFO]dish = retry:{retry} => url {url}")
        if retry:
            await get_data_about_dish(url, session, dishes, retry=retry - 1)
        else:
            print(f"[INFO]dish = ПОПЫТКИ ЗАКОНЧИЛИСЬ => url {url}")


async def parse_pages(url, page, session, dishes, retry=5):  # парсинг страницы
    pages_url = url + f"?page={page}"
    # print(f"{current_process().name}; PAGE {page}")
    try:
        async with session.get(url=pages_url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

            urls_dishes = soup('span', class_="emotion-1j2opmb")
            tasks = []
            for url_dish in urls_dishes:
                task = asyncio.create_task(get_data_about_dish(MAIN_URL + url_dish.findParent()["href"], session, dishes))
                tasks.append(task)
            await asyncio.gather(*tasks)
    except Exception as e:
        time.sleep(3)
        # print(f"[INFO]page:{page} retry:{retry} => url {pages_url}")
        if retry:
            await parse_pages(url, page, session, dishes, retry=retry - 1)
        return


async def parse_catalog(main_catalog, category_name, url):  # парсинг канкретного каталога
    dishes = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')

        dishes_count = int(re.findall(r'\d+', soup.find('span', class_="emotion-1ad0u8b").text.strip())[0])
        pages_count = math.ceil(dishes_count / 14) + 2

        limit_pages = 10
        # start = time.time()
        for l_pages in range(pages_count // limit_pages + 1):
            tasks = []
            for page in range(l_pages * limit_pages + 1,
                              l_pages * limit_pages + limit_pages + 1 if l_pages * limit_pages + limit_pages + 1 < pages_count else pages_count):
                task = asyncio.create_task(parse_pages(url, page, session, dishes))
                tasks.append(task)
            await asyncio.gather(*tasks)

        # print(f"{current_process().name} close pars. Catalog {category_name}; URL {url}; dishes {len(dishes)}",
        #       time.time() - start, 'c')
        writing_to_json(f'{main_catalog}\\{category_name}', dishes)


def writing_to_json(path, dishes):
    with open(f'{path}.json', 'w+', encoding='utf-8') as json_file:
        json.dump(dishes, json_file, indent=4, ensure_ascii=False)
    json_file.close()


def create_folder(folder):
    if os.path.isdir(folder):
        return
    os.mkdir(folder)


def bridge_async_threading(sem, main_catalog, category_name, url):
    with sem:
        # print(f"{current_process().name} started. URL {url}")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([loop.create_task(parse_catalog(main_catalog,category_name, url))]))
        loop.close()


def parse_recipe_catalogs(url):  # парсинг каталогов с блюдами
    create_folder(CATEGORIES_CUISINE)

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    recipe_selection_categories = soup('ul', class_="select-suggest__result js-select-suggest__result")
    categories = recipe_selection_categories[0]('li')

    sem = Semaphore(5)
    for i in range(1, len(categories)-1):
        Process(target=bridge_async_threading, args=(sem, CATEGORIES_CUISINE, categories[i].text.strip(),MAIN_URL + RECIPES + categories[i]['data-select-suggest-value'])).start()


def parse_country_catalogs(url):  # парсинг каталогов с странами
    create_folder(COUNTRIES_CUISINE)

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    recipe_selection_categories = soup('ul', class_="select-suggest__result js-select-suggest__result")
    countries = recipe_selection_categories[2]('li')

    sem = Semaphore(5)
    for i in range(44, len(countries)):
        Process(target=bridge_async_threading,
                args=(sem, COUNTRIES_CUISINE, countries[i].text.strip(),MAIN_URL + RECIPES + countries[i]['data-select-suggest-value'])).start()


def main():
    parse_recipe_catalogs(MAIN_URL)
    parse_country_catalogs(MAIN_URL)


if __name__ == "__main__":
    main()
