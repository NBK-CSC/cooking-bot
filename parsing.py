from bs4 import BeautifulSoup
import requests
import re
import json
import os

URL = 'https://eda.ru'
str_recipes = "/recepty/"
y=0

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')


def get_data_about_dish(url):
    soup = get_soup(url)

    parse_ingredients = soup("span", itemprop='recipeIngredient')
    parse_count_ingredients = soup("span", class_='emotion-15im4d2')
    parse_cooking_instructions = soup("span", itemprop="text")
    ingredients = []

    for i in range(len(parse_ingredients)):
        ingredients.append([parse_ingredients[i].text.strip(), parse_count_ingredients[i].text.strip()])

    dish = {
        "name": soup.find(class_="emotion-gl52ge").text.strip().replace("\xa0", " "),
        "count_ingredient": len(parse_ingredients),
        "ingredients": ingredients,
        "calories": soup.find('span', itemprop="calories").text.strip() if soup.find('span', itemprop="calories") is not None else 0,
        "protein":soup.find('span', itemprop="proteinContent").text.strip() if soup.find('span', itemprop="proteinContent") is not None else 0,
        "fat": soup.find('span', itemprop="fatContent").text.strip() if soup.find('span', itemprop="fatContent") is not None else 0,
        "carbohydrate": soup.find('span', itemprop="carbohydrateContent").text.strip() if soup.find('span', itemprop="carbohydrateContent") is not None else 0,
        "cooking instructions": [str(i + 1) + '.' + c.text.strip().replace("\xa0", " ").replace("­", "") for i, c in
                                 enumerate(parse_cooking_instructions)]
    }

    return dish

def parse_dishes(country):
    count=len(country)#количество кухней
    for index in range(44, count):
        dishes = []

        new_soup = get_soup(URL + str_recipes + country[index]["data-select-suggest-value"])
        number_recipes = int(re.findall(r'\d+',new_soup.find('span', class_="emotion-1ad0u8b").text.strip())[0])

        print(country[index].text.strip()+" кухня",f"Найдено рецептов {number_recipes}",sep="; ")

        for page in range(1,number_recipes//14+2):
            try:
                new_soup= get_soup(URL + str_recipes + country[index]["data-select-suggest-value"]+"?page="+str(page))
            except Exception:
                break

            name_dishes = new_soup('span', class_="emotion-1j2opmb")

            for i,name_dish in enumerate(name_dishes):
                dish_url = name_dish.findParent()["href"]
                print(index, country[index].text.strip(), i+(page-1)*14+1, name_dish.text.strip(),sep="; ")
                print(URL + dish_url)
                dishes.append(get_data_about_dish(URL + dish_url))

            if not len(dishes):
                continue
            with open(f'country_cuisine\\{country[index].text.strip()}.json', 'w+', encoding='utf-8') as json_file:
                json.dump(dishes, json_file, indent=4, ensure_ascii=False)
            json_file.close()



def main():
    soup = get_soup(URL)

    recipe_selection_categories = soup('ul', class_="select-suggest__result js-select-suggest__result")
    country = recipe_selection_categories[2]('li')

    if not os.path.isdir("country_cuisine"):
        os.mkdir("country_cuisine")

    try:
        parse_dishes(country)
    except IndexError:
        print("index out of range")


if __name__ == "__main__":
    main()
