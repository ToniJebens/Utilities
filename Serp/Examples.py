from Serp.Class import * 

# Initialize the class
my_serp = SERP()

### Google Search ###

# Single Query
query = 'Best neighbourhood to live in London'
tbs = 'qdr:m' # Past month
extract_components = ['Titles', 'Snippets', 'Dates', 'Links'] # all components
result = my_serp.google_search(query, tbs, extract_components)
print(result)

# Bulk Query
queries = ['Best neighbourhood to live in London', 'Best neighbourhood to live in New York']
result = SERP.google_search_bulk(queries, tbs, extract_components)
print(result) 


### Google Maps Search ###

# Single Query
query = "Coffee Shops"
latitude = 40.7455096
longitude = -74.0083012
map_results = my_serp.google_maps_search(query, latitude, longitude)
print(map_results)


# Bulk Query
map_queries = [
    {'query': 'restaurant', 'latitude': 40.7455096, 'longitude': -74.0083012},
    {'query': 'cafe', 'latitude': 40.7255096, 'longitude': -74.0083012}
]
bulk_map_results = my_serp.google_maps_search_bulk(map_queries)
print(bulk_map_results)


