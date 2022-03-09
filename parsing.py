from bs4 import BeautifulSoup
import requests
import json
import os

URL = 'https://eda.ru'
str_recipes = "/recepty/"


def get_list_data(data):
    return [c.text.strip() for c in data]


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
        "calories": soup.find('span', itemprop="calories").text.strip(),
        "protein": soup.find('span', itemprop="proteinContent").text.strip(),
        "fat": soup.find('span', itemprop="fatContent").text.strip(),
        "carbohydrate": soup.find('span', itemprop="carbohydrateContent").text.strip(),
        "cooking instructions": [str(i + 1) + '.' + c.text.strip().replace("\xa0", " ").replace("­", "") for i, c in
                                 enumerate(parse_cooking_instructions)]
    }

    return dish


def main():
    soup = get_soup(URL)

    recipe_selection_categories = soup('ul', class_="select-suggest__result js-select-suggest__result")
    country = recipe_selection_categories[2]('li')

    if not os.path.isdir("parce_data"):
        os.mkdir("parce_data")

    # count=len(country)#количество кухней
    count = 10

    try:
        data_dict = []
        for index in range(2, count):
            print(country[index].text.strip())
            dishes = []
            new_soup = get_soup(URL + str_recipes + country[index]["data-select-suggest-value"])
            name_dishes = new_soup('span', class_="emotion-1j2opmb")
            for name_dish in name_dishes:
                dish_url = name_dish.findParent()["href"]
                print(name_dish.text.strip())
                print(URL + dish_url)
                dishes.append(get_data_about_dish(URL + dish_url))

            data = {
                "country": country[index].text.strip(),
                "dishes": dishes
            }
            data_dict.append(data)

        with open('data.json', 'w+', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)


    except IndexError:
        print("index out of range")


if __name__ == "__main__":
    main()
