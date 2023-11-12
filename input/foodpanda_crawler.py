import requests
from typing import Self
from functools import cached_property

class Nearby_restaurants:
    def __init__(self:Self, location_:list[int], ) -> None:
        self.lon = location_[0]
        self.lat = location_[1]
        self.url = 'https://disco.deliveryhero.io/listing/api/v1/pandora/vendors'
        self.query = {
            'longitude': self.lon,  # 經度
            'latitude': self.lat,  # 緯度
            'language_id': 6,
            'include': 'characteristics',
            'dynamic_pricing': 0,
            'configuration': 'Variant1',
            'country': 'tw',
            'budgets': '',
            'cuisine': '',
            'sort': '',
            'food_characteristic': '',
            'use_free_delivery_label': False,
            'vertical': 'restaurants',
            'limit': 48,
            'offset': 0,
            'customer_type': 'regular'
        }
        self.headers = {
            'x-disco-client-id': 'web',
        }

    @cached_property
    def restaurants_data(self:Self) -> None:
        r = requests.get(url=self.url, params=self.query, headers=self.headers)
        if r.status_code == requests.codes.ok:
            return r.json()['data']['items']

    @property
    def num_restaurants(self:Self) -> int:
        num = len(self.restaurants_data)
        num = 10 if num > 10 else num
        return num

    @property
    def res_name_list(self:Self) -> list[str]:
        name_list = []
        for store in self.restaurants_data[:self.num_restaurants]:
            name_list.append(store['name'])
        return name_list

    @property
    def res_code_list(self:Self) -> list[str]:
        code_list = []
        for store in self.restaurants_data[:self.num_restaurants]:
            code_list.append(store['code'])
        return code_list

class Target_restaurant:
    def __init__(self:Self, code:str) -> None:
        self.url = f'https://tw.fd-api.com/api/v5/vendors/{code}'
        self.query = {
            'include': 'menus',
            'language_id': '6',
            'dynamic_pricing': '0',
            'opening_type': 'delivery',
        }

    @cached_property
    def target_data(self:Self) -> None:
        r = requests.get(url=self.url, params=self.query)
        if r.status_code == requests.codes.ok:
            return r.json()['data']['menus'][0]['menu_categories']

    @property
    def num_categories(self:Self) -> int:
        return len(self.target_data)

    @property
    def food_menu_list(self:Self) -> list[dict]:
        list_ = []
        for i in range(self.num_categories):
            num_prod = len(self.target_data[i]['products'])
            for j in range(num_prod):
                name = self.target_data[i]['products'][j]['name']
                price = self.target_data[i]['products'][j]['product_variations'][0]['price']
                list_.append({'name': name, 'price': price})
        return list_

    @property
    def food_menu_string(self:Self) -> str:
        str_ = ''
        for i in self.food_menu_list:
            str_ += f'{i["name"]}, {i["price"]} \n'
        return str_


if __name__ == '__main__':
    test_loc = [127.55514690369998, 23.001554450030582]
    nb_res = Nearby_restaurants(test_loc)
    rand_ = 0
    name_, code_ = nb_res.res_name_list[rand_], nb_res.res_code_list[rand_]
    tg_res = Target_restaurant(code_)