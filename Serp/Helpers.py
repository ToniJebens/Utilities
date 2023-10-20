from serpapi import GoogleSearch
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("SERP_API_KEY")


### GOOGLE SEARCH ###

def build_params_for_google_search(query, tbs, api_key):
    return {
        "engine": "google",
        "q": query,
        "tbs": tbs,
        "api_key": api_key
    }

def extract_components_from_organic_result(result, components):
    data = {}
    if 'Titles' in components:
        data['Titles'] = result.get('title', '')
    if 'Snippets' in components:
        data['Snippets'] = result.get('snippet', 'NA')
    if 'Dates' in components:
        data['Dates'] = result.get('date', '')
    if 'Links' in components:
        data['Links'] = result.get('link', '')
    return data


### GOOGLE MAPS SEARCH ###

def build_params_for_google_maps_search(query, latitude, longitude, api_key):
    ll_formatted = f"@{latitude},{longitude},15.1z"
    
    return {
        "engine": "google_maps",
        "q": query,
        "ll": ll_formatted,
        "type": "search",
        "api_key": api_key
    }


def extract_components_from_local_result(result, components):
    data = {}
    if 'Position' in components:
        data['Position'] = result.get('position')
    if 'Title' in components:
        data['Title'] = result.get('title')
    if 'Rating' in components:
        data['Rating'] = result.get('rating')
    if 'Reviews' in components:
        data['Reviews'] = result.get('reviews')
    if 'Price' in components:
        data['Price'] = result.get('price')
    if 'Type' in components:
        data['Type'] = result.get('type')
    if 'Address' in components:
        data['Address'] = result.get('address')
    if 'Phone' in components:
        data['Phone'] = result.get('phone')
    if 'Website' in components:
        data['Website'] = result.get('website')
    if 'Description' in components:
        data['Description'] = result.get('description')
    if 'ServiceOptions' in components:
        data['ServiceOptions'] = result.get('service_options')
    return data
