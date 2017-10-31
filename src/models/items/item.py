import uuid

import requests
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
import re

from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, url, name, price=None, _id=None):
        self.url = url
        store = Store.find_by_url(url)
        title_tag_name = store.title_tag_name
        title_query = store.title_query
        self.name = self.load_title(title_tag_name, title_query) if name is "" else name
        self.price_tag_name = store.price_tag_name
        self.price_query = store.price_query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with url {}".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.price_tag_name, self.price_query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)

        self.price = float(match.group())
        return self.price

    def load_title(self, tag_name, query):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name, query)
        string_name = element.text.strip()

        pattern = re.compile("([\w]+)")
        match = pattern.search(string_name)

        return match.group()

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
