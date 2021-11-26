from config import hosts
from itertools import product


def repeat_placements(m, n):  # генерує список розміщень з повтореннями
    return [tpl for tpl in product(range(m), repeat=n)]


def get_order_list(filename, sep="---"):
    id_, list_ = 0, []
    with open(filename, encoding="utf-8") as order:
        for line in order:
            info = line.split(sep)
            list_.append({"id": id_, "author": info[0].strip(),
                          "title": info[1].strip(),
                          "amount": int(info[2].strip())})
            id_ += 1
    return list_


order_list_2 = get_order_list("order.txt")


def price(price_info, delivery_info, placement):  # повертає ціну і склад замовлення
    markets = list(hosts.keys())  # індексом магазину є його індекс у списку
    shop_numbers, book_numbers = len(price_info[0]), len(price_info)
    orders = [[] for _ in range(shop_numbers)]
    for i in range(len(placement)):  # формуємо склад замовлення
        orders[placement[i]].append(i)
    # обчислюємо вартість замовлення:
    prices = [0 for _ in range(shop_numbers)]
    for shop in range(shop_numbers):
        for book in orders[shop]:
            try:
                amount = order_list_2[book]['amount']
                prices[shop] += price_info[book][markets[shop]][0] * amount
            except:
                return False  # такий варіант замовлення неможливий
        # уточнюємо вартість замовлення з урахуванням доставки:
        if orders[shop]:
            if prices[shop] < delivery_info[markets[shop]][1]:
                prices[shop] += delivery_info[markets[shop]][0]
    return sum(prices), orders


