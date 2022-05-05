# from urllib import response
# from os import sep
# from cgitb import html
from inspect import Attribute
import requests
import json
from bs4 import BeautifulSoup

product_id = (input("Enter product id: "))

url = "https://www.ceneo.pl/" + product_id + "#tab=reviews" #kod ma być pobierany od uzytkownika
all_opinions = []


while(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text, "html.parser")
    error = page.select("div.error-page")
    if not error:
        opinions = page.select("div.js_product-review")
        for opinion in opinions:
            opinion_id = opinion["data-entry-id"]
            author = opinion.select_one("span.user-post__author-name").get_text().strip()

            try:
                recommendation = opinion.select_one("span.user-post__author-recomendation > em").get_text().strip()
            except AttributeError:
                recommendation = None

            stars = opinion.select_one(
                "span.user-post__score-count").get_text().strip()
            content = opinion.select_one("div.user-post__text").get_text().strip()

            useful = opinion.select_one('span[id^="votes-yes"]').get_text().strip()
            useless = opinion.select_one('span[id^="votes-no"]').get_text().strip()
            publish_date = opinion.select_one(
                'span.user-post__published > time:nth-child(1)')["datetime"]

            try:
                purchase_date = opinion.select_one(
                    'span.user-post__published > time:nth-child(2)')["datetime"]
            except TypeError:
                purchase_date = None

            pros = opinion.select(
                "div[class$=\"positives\"]~ div.review-feature__item")
            pros = [item.get_text().strip() for item in pros]
            cons = opinion.select(
                "div[class$=\"negatives\"]~ div.review-feature__item")
            cons = [item.get_text().strip() for item in cons]

            single_opinion = {
                "opinion_id": opinion_id,
                "author": author,
                "stars": stars,
                "content": content,
                "useful": useful,
                "useless": useless,
                "publish_date": publish_date,
                "purchase_date": purchase_date,
                "pros": pros,
                "cons": cons,

            }

            all_opinions.append(single_opinion)
        
        next = page.select_one("a.pagination_next")
        if(next):
            url = "https://www.ceneo.pl"+next["href"]
        else:
            url = None
        # try:
        #     url = "https://www.ceneo.pl"+page.select_one("a.pagination_next")["href"]
        # except TypeError:
        #     url = None

    else:
        no_page = page.select_one("p.error-info").get_text()
        print(no_page)
        url = None
       
if not error and len(all_opinions) > 0:
    with open("opinions/"+ product_id + ".json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions, jf, indent=4, ensure_ascii=False)

if not error and len(all_opinions) == 0:
        print("There are no opinions")

    #print(json.dumps(all_opinions, indent=4, ensure_ascii=False))
