import json
from bs4 import BeautifulSoup
import requests
from ..database.models import RecipeModel, UrlVisited
import time
from ..utils.logger import Logger
import math


class Scrapper:
    """Scraps the data from allrecipes.com"""

    sleep_for = 2

    data = []

    source_name = "allrecipes.com"  # source of the data

    total_pages = 37

    base_url = "https://www.allrecipes.com/element-api/content-proxy/aggregate-load-more?sourceFilter[]=alrcom&id=cms%2Fonecms_posts_alrcom_2007692&excludeIds[]=cms%2Fallrecipes_recipe_alrcom_142967&excludeIds[]=cms%2Fonecms_posts_alrcom_231026&excludeIds[]=cms%2Fonecms_posts_alrcom_247233&excludeIds[]=cms%2Fonecms_posts_alrcom_246179&excludeIds[]=cms%2Fonecms_posts_alrcom_256599&excludeIds[]=cms%2Fonecms_posts_alrcom_247204&excludeIds[]=cms%2Fonecms_posts_alrcom_34591&excludeIds[]=cms%2Fonecms_posts_alrcom_245131&excludeIds[]=cms%2Fonecms_posts_alrcom_220560&excludeIds[]=cms%2Fonecms_posts_alrcom_212721&excludeIds[]=cms%2Fonecms_posts_alrcom_236563&excludeIds[]=cms%2Fallrecipes_recipe_alrcom_14565&excludeIds[]=cms%2Fonecms_posts_alrcom_8189766&excludeIds[]=cms%2Fonecms_posts_alrcom_8188886&excludeIds[]=cms%2Fonecms_posts_alrcom_8189135&excludeIds[]=cms%2Fonecms_posts_alrcom_2052087&excludeIds[]=cms%2Fonecms_posts_alrcom_7986932&excludeIds[]=cms%2Fonecms_posts_alrcom_2040338&excludeIds[]=cms%2Fonecms_posts_alrcom_142967&excludeIds[]=cms%2Fonecms_posts_alrcom_174543&excludeIds[]=cms%2Fonecms_posts_alrcom_14565&excludeIds[]=cms%2Fonecms_posts_alrcom_72349&excludeIds[]=cms%2Fonecms_posts_alrcom_13087&excludeIds[]=cms%2Fonecms_posts_alrcom_141169&page={}&orderBy=Popularity30Days&docTypeFilter[]=content-type-recipe&docTypeFilter[]=content-type-gallery&size=24&pagesize=24&x-ssst=iTv629LHnNxfbQ1iVslBTZJTH69zVWEa&variant=food"

    
    def __init__(self):
        self.model = RecipeModel()
        self.url_visted = UrlVisited()
        self.logger = Logger(__name__, std_out=True)

    def get_html_document(self, url):
        # request for HTML document of given url
        response = requests.get(url)
        # response will be provided in JSON format
        return response.text

    def extract_recipe(self, url):
        page = self.get_html_document(url)

        soup = BeautifulSoup(page, 'lxml')

        title = None

        summary = None

        recipe_steps = {}

        image_url = None

        ingredients = []

        nutritions = None

        prep_cook_timings = None

        # scrapping starts
        try:
            title = soup.find('h1', class_='headline').text

            recipe_info_ele = soup.find('section',class_="recipeInstructions").find_all('li')

            for step,li in enumerate(recipe_info_ele,1):
                recipe_steps[f'step_{step}'] = li.text.strip()

            image_ele = soup.find('div', class_='lazy-image')
        
            if image_ele.attrs.get('data-src'):
                image_url = image_ele.attrs['data-src']

            ingredients_ele = soup.find('ul',class_='ingredients-section').find_all('li')

            for li in ingredients_ele:
                ingredients.append(li.text.strip())

            nutritions = soup.find('div', class_='recipe-nutrition-section').text

            summary = soup.find("div", class_="recipe-summary").text

            # prep and cook timings
            prep_cook_summary_ele = soup.find_all("div", class_="recipe-meta-item")

            prep_cook_timings_list = []
            for ele in prep_cook_summary_ele:
                prep_cook_timings_list.append(ele.text.strip())

            prep_cook_timings = ",".join(prep_cook_timings_list)
        except Exception:
            return

        data = {
            "url": url,
            "recipe": json.dumps(recipe_steps),
            "title": title.strip(),
            "summary": summary.strip(),
            "ingredients": ",".join(ingredients),
            "nutritions": nutritions,
            "prep_cook_timings": prep_cook_timings,
            "image_url": image_url
        }
        # print(ingredients)
        self.model.save(data)
        self.logger.info(f"Saving {title} recipe to the database...")

       

    def extract(self, url):
        response = requests.get(url)

        data = response.json()

        soup = BeautifulSoup(data['html'], 'lxml')

        reciepe_cards = soup.find_all('div',class_="recipeCard")
       
        for card in reciepe_cards:
            anchor_tag = card.find('a',class_='recipeCard__titleLink')

            self.extract_recipe(anchor_tag['href'])
            time.sleep(self.sleep_for)
           


    def start(self):

        self.logger.info(f'Started scrapping data from {self.source_name}')

        for i in range(self.total_pages):
            self.logger.info(f'Processing page no. {i+1}')

            url = self.base_url.format(i+1)

            if self.url_visted.find(url):
                return
            

            self.extract(url)

            self.url_visted.save({'link': url})

            self.logger.info(f'Processed page no. {i+1}')

            time.sleep(self.sleep_for)


def start_scrapper():
    Scrapper().start()


if __name__ == '__main__':
    start_scrapper()
