import json
from bs4 import BeautifulSoup
import requests
from ..database.models import PlaceModel, UrlVisited
import time
from ..utils.logger import Logger
import math


class Scrapper:
    """Scraps the data from holidify.com"""

    sleep_for = 2

    data = []

    source_name = "holidify.com"  # source of the data

    total_pages = 37

    base_url = "https://www.allrecipes.com/element-api/content-proxy/aggregate-load-more?sourceFilter[]=alrcom&id=cms%2Fonecms_posts_alrcom_2007692&excludeIds[]=cms%2Fallrecipes_recipe_alrcom_142967&excludeIds[]=cms%2Fonecms_posts_alrcom_231026&excludeIds[]=cms%2Fonecms_posts_alrcom_247233&excludeIds[]=cms%2Fonecms_posts_alrcom_246179&excludeIds[]=cms%2Fonecms_posts_alrcom_256599&excludeIds[]=cms%2Fonecms_posts_alrcom_247204&excludeIds[]=cms%2Fonecms_posts_alrcom_34591&excludeIds[]=cms%2Fonecms_posts_alrcom_245131&excludeIds[]=cms%2Fonecms_posts_alrcom_220560&excludeIds[]=cms%2Fonecms_posts_alrcom_212721&excludeIds[]=cms%2Fonecms_posts_alrcom_236563&excludeIds[]=cms%2Fallrecipes_recipe_alrcom_14565&excludeIds[]=cms%2Fonecms_posts_alrcom_8189766&excludeIds[]=cms%2Fonecms_posts_alrcom_8188886&excludeIds[]=cms%2Fonecms_posts_alrcom_8189135&excludeIds[]=cms%2Fonecms_posts_alrcom_2052087&excludeIds[]=cms%2Fonecms_posts_alrcom_7986932&excludeIds[]=cms%2Fonecms_posts_alrcom_2040338&excludeIds[]=cms%2Fonecms_posts_alrcom_142967&excludeIds[]=cms%2Fonecms_posts_alrcom_174543&excludeIds[]=cms%2Fonecms_posts_alrcom_14565&excludeIds[]=cms%2Fonecms_posts_alrcom_72349&excludeIds[]=cms%2Fonecms_posts_alrcom_13087&excludeIds[]=cms%2Fonecms_posts_alrcom_141169&page={}&orderBy=Popularity30Days&docTypeFilter[]=content-type-recipe&docTypeFilter[]=content-type-gallery&size=24&pagesize=24&x-ssst=iTv629LHnNxfbQ1iVslBTZJTH69zVWEa&variant=food"

    countries = ["india", "bhutan", "sri-lanka", "nepal", "thailand", "oman",
                 "laos", "uae", "qatar", "singapore", "vietnam", "seychelles",
                 "mauritius", "cambodia", "indonesia", "philippines", "hong-kong"]

    top_places = ["manali", "ladakh", "coorg",
                  "andaman-nicobar-islands", "goa", "udaipur",
                  "srinagar", "gangtok", "munnar", "Varkala",
                  "mcleodganj", "rishikesh", "alleppey", "darjeeling",
                  "nainital", "shimla", "ooty", "jaipur", "lonavala",
                  "mussoorie", "kodaikanal", "dalhousie", "pachmarhi",
                  "varanasi", "mumbai", "agra", "kolkata", "jodhpur",
                  "bangalore", "amritsar", "delhi", "jaisalmer", "mount-abu",
                  "wayanad", "hyderabad", "pondicherry", "khajuraho", "chennai",
                  "vaishno-devi", "ajanta-and-ellora-caves", "haridwar", "kanyakumari",
                  "pune", "kochi", "ahmedabad", "kanha-national-park",
                  "mysore", "chandigarh", "hampi", "Gulmarg", "almora",
                  "shirdi", "auli", "madurai", "amarnath", "bodh-gaya",
                  "mahabaleshwar", "visakhapatnam", "Kasol", "nashik", "tirupati",
                  "ujjain", "corbett-national-park", "gwalior", "mathura", "jog-falls",
                  "alibaug", "rameshwaram", "vrindavan", "coimbatore", "lucknow", "digha",
                  "dharamshala", "kovalam", "kaziranga-national-park", "madikeri",
                  "matheran", "ranthambore", "agartala", "khandala", "kalimpong", "thanjavur",
                  "bhubaneswar", "ajmer", "aurangabad", "jammu", "dehradun", "puri", "cherrapunji",
                  "bikaner", "shimoga", "hogenakkal", "gir-national-park", "kasauli", "pushkar",
                  "chittorgarh", "nahan", "lavasa", "poovar", "honnemaradu"]

    def __init__(self):
        self.model = PlaceModel()
        self.url_visted = UrlVisited()
        self.logger = Logger(__name__, std_out=True)

    def get_html_document(self, url):
        # request for HTML document of given url
        response = requests.get(url)
        # response will be provided in JSON format
        return response.text

    def extract(self, url):
        response = requests.get(url)

        data = response.json()

        # print(data['html'])

        soup = BeautifulSoup(data['html'], 'lxml')

        desc = None
        state = None
        country = None
        ratings = None
        total_reviews = None
        tagline = None
        images = []

        reciepe_cards = soup.find_all('div',class_="recipeCard")

        for card in reciepe_cards:
            title = card.find('h3',class_='card__title')
            print(card.a,type(card))
            # print(title)

        # try:
        #     desc = soup.find("div", class_="readMoreText").text

        #     locations = soup.find(
        #         "div", class_="mb-2 font-smaller").find_all("b")

        #     if locations:
        #         try:
        #             state = locations[0].text
        #             country = locations[1].text
        #         except IndexError:
        #             state = None
        #             country = None

        #     rating_badge = soup.find("span", class_="rating-badge").text

        #     ratings = rating_badge.strip()

        #     total_reviews = soup.find("a", class_="num-reviews").text

        #     tagline = soup.find("h3", class_="tagline").text

        #     # get all images
        #     image_divs = soup.find_all("div", class_="swipe-image")

        #     for img in image_divs:
        #         images.append(img.attrs['data-original'])
        # except Exception:
        #     return

        # data = {}

        # data['url'] = url
        # data['desc'] = desc
        # data['tagline'] = tagline
        # data['ratings'] = ratings
        # data['state'] = state
        # data['country'] = country
        # data['total_reviews'] = total_reviews
        # data['images'] = ".".join(images)

        # self.model.save(data)

        self.logger.info(f'Saving data to database...')

    def start(self):

        self.logger.info(f'Started scrapping data from {self.source_name}')

        for i in range(self.total_pages):
            self.logger.info(f'Processing page no. {i+1}')

            url = self.base_url.format(i+1)

            # if self.url_visted.find(url):
            #     return
            

            self.extract(url)

            # self.url_visted.save({'link': url})

            self.logger.info(f'Processed page no. {i+1}')

            time.sleep(self.sleep_for)


def start_scrapper():
    Scrapper().start()


if __name__ == '__main__':
    start_scrapper()
