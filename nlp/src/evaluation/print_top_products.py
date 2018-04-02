import pickle

with open("../../../../results/top_products.pkl", "rb") as file:
	asin_buckets = pickle.load(file)
print(asin_buckets["51-100"])
