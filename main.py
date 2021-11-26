import scrap
import funs
import graf
from threading import Thread
import pickle
from config import hosts
from itertools import product
from math import inf
from time import time
# import time
from datetime import datetime

order_list = funs.get_order_list("order.txt")


def thread(order_list, host):
    for item in order_list:
        args = (item['author'], item['title'], host)
        price_info[item['id']][host] = scrap.get_price(*args)
    delivery_info[host] = scrap.get_delivery(host)



start_time = datetime.now()
sta

price_info = {key: {} for key in range(len(order_list))}
delivery_info = {key: None for key in hosts.keys()}

threads = [Thread(target=thread, args=(order_list, host)) for host in hosts]
for item in threads:
    item.start()
for item in threads:
    item.join()




seconds = time.time() - start_time

end_time = datetime.now()
print('Час виконання Web-скрапінгу за допомогою потоків: {}'.format(end_time - start_time))

with open('data.pickle', 'wb') as f:
    pickle.dump(price_info, f)

with open('data.pickle', 'rb') as f:
    price_info = pickle.load(f)
print(price_info)

delivery_info = {'bookclub.ua': (69.0, 390.0), 'bambook.com': (40.0, inf),
                 'yakaboo.ua': (40.0, inf), 'starylev.com.ua': (45, 500)}

markets = list(hosts.keys())  # індексом магазину є його індекс у списку

start_time = datetime.now()


orders = product(range(len(markets)), repeat=len(order_list))  # генерує список розміщень з повтореннями
print(orders)
min_price, order = inf, None
for tpl in orders:
    p = funs.price(price_info, delivery_info, tpl)
    if p and p[0] < min_price:
        min_price, order = p



end_time = datetime.now()
print('Витрачений час на знаходження мінімального замовлення за допомогою розміщень: {}'.format(end_time - start_time))


print(f'Order: {order} - {min_price} грн.')


def dfs_find_routes(tree, start, end):
    global min_price, order
    if start == end:
        p = funs.price(price_info, delivery_info, graf.route_to_order(route))

        if p and p[0] < min_price:
            min_price, order = p
    else:
        for node in tree[start]:
            if not visited.get(node, False):
                visited[node] = True
                route.append(node)
                dfs_find_routes(tree, node, end)
                visited[node] = False
                route.remove(node)



start_time = datetime.now()
start = time()

adj = graf.build_adj_list(price_info, markets)

visited, route = {}, []
min_price, order = inf, None
dfs_find_routes(adj, 0, max(adj.keys()))


finish = time()


end_time = datetime.now()



print(f'Order: {order} - {min_price} грн.')




def display():
    total_price = 0
    print("-" * 50)
    for market_id in range(len(order)):
        if not order[market_id]:
            continue
        print(f"{markets[market_id]}:")
        market_total = 0
        for item in order[market_id]:
            title = order_list[item]["title"]
            author = order_list[item]["author"]
            amount = order_list[item]["amount"]
            price = price_info[item][markets[market_id]][0]
            total = price * amount
            market_total += total
            print(f"\t<<{title}>> {author}: {amount} * {price} = {total} грн.")
            print(f"\t  - Кількість екземплярів книги : {amount}")
            print(f"\t  - Ціна за один кеземпляр книги : {price}")
            if price_info[item][markets[market_id]][1].strip('https:https:'):
                print(f"URL: https:{price_info[item][markets[market_id]][1].strip('https:')}")
        if market_total < delivery_info[markets[market_id]][1]:
            delivery = delivery_info[markets[market_id]][0]
        else:
            delivery = 0.
        print(f"\tДоставка: {delivery} грн.")
        print("-" * 50)
        total_price += market_total + delivery
    print(f"Загальна вартість замовлення: {total_price} грн.")


display()
