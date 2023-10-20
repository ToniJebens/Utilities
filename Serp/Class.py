from Serp.Helpers import *

class SERP:

    api_key = os.getenv("SERP_API_KEY")

    @classmethod
    def google_search(cls, query, tbs=None, extract_components=['Titles', 'Snippets', 'Dates', 'Links']):
        """
        Search for a query using the Google SERP API and extract specified components.

        :param query: The search query.
        :param tbs: Timeframe for the search, if any.
        :param extract_components: List of components to extract. Default is all components.
        :return: DataFrame with the extracted information.
        """
        output_dictionary = {key: [] for key in extract_components}
        params = build_params_for_google_search(query, tbs, api_key)
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results.get('organic_results', [])
            
            # Extract specified components
            for result in organic_results:
                extracted_data = extract_components_from_organic_result(result, extract_components)
                for key, value in extracted_data.items():
                    output_dictionary[key].append(value)
        except Exception as e:
            print(e)

        return pd.DataFrame(output_dictionary)


    @classmethod
    def google_search_bulk(cls, queries, tbs=None, extract_components=['Titles', 'Snippets', 'Dates', 'Links']):
        """
        Search for a list of queries using the Google SERP API and extract specified components.

        :param queries: List of search queries. Minumum 1 query.
        :param tbs: Timeframe for the searches, if any.
        :param extract_components: List of components to extract. Default is all components.
        :return: DataFrame with queries as index and each extracted component as columns.
        """
        all_data = []
        
        for query in queries:
            result = cls.google_search(query, tbs, extract_components)
            all_data.append(result)

        # Concatenate all individual DataFrames
        return pd.concat(all_data, keys=queries, names=['Query'])


    @classmethod
    def google_maps_search(cls, query, latitude, longitude, 
                           extract_components=['Position', 'Title', 'Rating', 'Reviews']):
        
        params = build_params_for_google_maps_search(query, latitude, longitude, api_key)
        search = GoogleSearch(params)
        results = search.get_dict()
        local_results_data = results["local_results"]

        output_results = []
        for result in local_results_data:
            extracted_data = extract_components_from_local_result(result, extract_components)
            output_results.append(extracted_data)

        return pd.DataFrame(output_results)


    @classmethod
    def google_maps_search_bulk(cls, queries, extract_components=['Position', 'Title', 'Rating', 'Reviews']):
        """
        :param queries: List of dictionaries, where each dictionary contains 'query', 'latitude', and 'longitude'
        :return: DataFrame with each query details as index and extracted components as columns.
        """
        all_data = []

        for query_obj in queries:
            df = cls.google_maps_search(
                query_obj['query'], 
                query_obj['latitude'], 
                query_obj['longitude'], 
                extract_components
            )
            all_data.append(df)

        # Concatenate all individual DataFrames
        return pd.concat(all_data, keys=[(q['query'], q['latitude'], q['longitude']) for q in queries], names=['Query', 'Latitude', 'Longitude'])

    # To Come: Ebay Search, YouTube Search ....
