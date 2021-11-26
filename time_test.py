import scrap
from threading import Thread
import pickle
from config import hosts
from itertools import product
from math import inf
from time import time

from main import visited, route


def build_adj_list():
	books = 9
	shops = 7
	adj = {node: [] for  node in range(books*shops+2)}
	for i in range(shops):
		adj[0].append(i+1)
	for j in range(books-1):
		for i in range(shops):
			for k in range(shops):
				adj[j*shops+i+1].append((j+1)*shops+k+1)
	for i in range(shops):
		adj[(books-1)*shops+i+1].append(books*shops+1)
	return adj
	
def dfs_find_routes(tree, start, end):
	if start == end:
		#routes.append(tuple(route))
		pass
	else:
		for node in tree[start]:
			if not visited.get(node, False):
				visited[node] = True
				route.append(node)
				dfs_find_routes(tree, node, end)
				visited[node] = False
				route.remove(node)
	
	
start=time()
#adj=build_adj_list()
#print(adj)
#visited, route, routes = {}, [], []
#dfs_find_routes(adj, 0, max(adj.keys()))
for _ in product(range(10),repeat=9):
	pass
finish = time()
print(finish-start)



	

	
#adj = build_adj_list(price_info, markets)
#print(adj)


