# 可搜尋指定定址附近的餐廳，暫時沒用到
import requests
import re
import os

places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

def get_location(pattern:str, input_string:str)->str:
    match = re.search(pattern, input_string)
    return f"{match.group(1)}, {match.group(2)}"

def get_nearby_food(location:str)->dict:
    params = {
        "location": location,
        "radius": 1000,
        "type": "restaurant",
        "key": os.getenv('MAP_API'),
    }
    response = requests.get(places_url, params=params).json()

    return response

def top_20_food(data:dict)->None:
    searched_data = data['results']
    result = ""
    for i in range(0, len(searched_data)):
        name = searched_data[i]['name']
        rating = searched_data[i]['rating']
        result += f"{name} {rating}\n"
    return result

if __name__ == "__main__":
    food_pattern = r"(\d+\.\d+), (\d+\.\d+)"
    received_message = "35.681236, 139.767125"
    if re.match(food_pattern, received_message):
        location = get_location(food_pattern, received_message)
        data = get_nearby_food(location)
        result = top_20_food(data)
        print(location)