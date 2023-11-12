import random
from input.foodpanda_crawler import Nearby_restaurants, Target_restaurant
def make_menu(loc:list[float, float])->str:
    '''
    Accoring to the location, return the menu of a random restaurant nearbys.
    '''
    nb_res = Nearby_restaurants(loc)
    rand_ = random.randint(0, nb_res.num_restaurants-1)
    name_, code_ = nb_res.res_name_list[rand_], nb_res.res_code_list[rand_]
    tg_res = Target_restaurant(code_)
    return f'店名: {name_} \n {tg_res.food_menu_string}'

if __name__ == '__main__':
    chai_loc = [121.55514690369998, 25.001554450030582]
    print(make_menu(chai_loc))