from Notion.Notion_Helpers import *
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class NotionAPI:

    integration_token = os.getenv("integration_token")
    headers = { 
        "Authorization": f"Bearer {integration_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    @staticmethod
    def HTTP_STATUS(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.status_code == 200:
                print('Request successful.')
            else:
                print(f"Error. Status code: {response.status_code}")
                print(response.json())
            return response
        return wrapper
    
    @classmethod
    @HTTP_STATUS
    def post_request(cls, url, json=None):
        res = requests.request("POST", url, json=json, headers=cls.headers, timeout=15)
        return res
    
    @classmethod
    @HTTP_STATUS
    def patch_request(cls, url, json=None):
        res = requests.request("PATCH", url, json=json, headers=cls.headers, timeout=15)
        return res
    
    @classmethod
    @HTTP_STATUS
    def get_request(cls, url, json=None):
        res = requests.request("GET", url, json=json, headers=cls.headers, timeout=15)
        return res
    

    ############################################################################
    ###############################   DATABASE  ################################
    ############################################################################

    @classmethod
    def database_read(cls, database_id):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        res = cls.post_request(url)
        data = res.json()
        return data 
    
    @classmethod
    def database_extract_page_details(cls, database_id):
        data = cls.database_read(database_id)
        db_pages = f'put helper function link here{data}'
        return db_pages
    

    @classmethod
    def database_extract_property_details(cls, database_id):
        data = cls.database_read(database_id)
        db_properties = f'put helper function link here{data}'
        return db_properties
    

    ############################################################################
    #################################   PAGES  #################################
    ############################################################################


    @classmethod
    def page_create(cls, database_id, page_structure=None, page_title=None, page_content=None, page_properties=None):
        """
        Creates and publishes a Notion page. If a pre-populated page structure (JSON) is provided, 
        that page will get published. Else, a basic page using only the title is published and updated 
        with content and/or properties as provided.

        Inputs:
            - database_id (str): The ID of the database where the page will be created.
            - page_structure (dict, optional): The pre-populated page structure to be published. 
            - page_title (str, optional): The title of the new page to be created.
            - page_content (DataFrame, optional): The content to be added to the page.
            - page_properties (dict, optional): The properties to be added to the page.

        Returns: 
            - The ID of the newly created or published page.

        Note: Either page_structure or page_title should be provided, not both.
        """
        url = "https://api.notion.com/v1/pages"

        if (page_structure is None and page_title is None) or (page_structure is not None and page_title is not None):
            raise ValueError("Either page_structure or page_title must be provided, but not both")

        if page_structure is None:
            page_structure = cls.page_structure(database_id, page_title)

        response = cls.post_request(url, json=page_structure)
        page_id = response.json().get("id")

        # update page with content and properties if provided
        if page_content is not None:
            cls.process_content(page_content, page_id=page_id)
        if page_properties is not None:
            cls.process_properties(database_id, page_properties, page_id=page_id)

        return page_id


    @classmethod
    def add_property(cls, property_name, property_values, property_type, page_id=None, page_structure=None):
            """
            Adds or updates properties of a Notion page or page structure.
            
            If a page_id is specified, updates the properties of an existing page.
            If a page_structure is specified, adds the properties to the page structure.
            
            Inputs:
            - property_name (str): The name of the property to add or update.
            - property_values (any): The values of the property to add or update.
            - property_type (str): The type of the property to add or update.
            - page_id (str, optional): The ID of the page to update. If specified, page_structure should be None.
            - page_structure (dict, optional): The structure of the page to update. If specified, page_id should be None.

            Returns:
            - If page_structure is specified, returns the updated page structure (JSON).
            - If page_id is specified, returns the response from the PATCH request.
            
            Note: Either page_id or page_structure should be specified, not both.
            """
            property_object = create_properties(property_values, property_type)

            if page_id is not None and page_structure is not None:
                raise ValueError("Only one of page_id or page_structure should be specified")

            if page_structure is not None:
                page_structure.setdefault('properties', {}).update({property_name: property_object})
                return page_structure
            elif page_id is not None:
                updated_property = {"properties": {property_name: property_object}}
                url = f"https://api.notion.com/v1/pages/{page_id}"
                res = cls.patch_request(url, json=updated_property)
                return res
            else:
                raise ValueError("Either page_id or page_structure must be specified")

    @classmethod
    def add_content_block(cls, content_type, content, page_id=None, page_structure=None):
        """
        Adds a new content block to a Notion page or page structure.
        
        If a page_id is specified, adds the content block to an existing page.
        If a page_structure is specified, adds the content block to the page structure.
        
        Inputs:
        - content_type (str): The type of content to add.
        - content (str): The content to add.
        - page_id (str, optional): The ID of the page to update. If specified, page_structure should be None.
        - page_structure (dict, optional): The structure of the page to update. If specified, page_id should be None.

        Returns:
        - If page_structure is specified, returns the updated page structure (JSON).
        - If page_id is specified, returns the response from the PATCH request.
        
        Note: Either page_id or page_structure should be specified, not both.
        """
        if page_id is not None and page_structure is not None:
            raise ValueError("Only one of page_id or page_structure should be specified")

        if page_structure is not None:
            page_structure = create_and_append_new_block_to_page_structure(page_structure, content_type, content)
            return page_structure
        elif page_id is not None:
            url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            new_content = create_and_append_new_block_to_existing_page(content_type, content)
            res = cls.patch_request(url, json=new_content)
            return res
        else:
            raise ValueError("Either page_id or page_structure must be specified")



    @classmethod
    def process_properties(cls, database_id, property_dict, page_id=None, page_structure=None):
        """
        Updates page property values in either an existing Notion page or a page structure (not published yet).

        Inputs:
        - database_id (str): ID of the database, needed to extract property details.
        - property_dict (dict): Dictionary containing property name (key) and value pairs.
        - page_id (str): ID of the page to be updated, if updating an existing page.
        - page_structure (dict): JSON structure to which properties will be added, if creating a new page structure.

        Returns:
        - If page_structure is specified, returns the updated page structure (JSON).
        - If page_id is specified, updates the specified page with new properties and returns None.

        Note: Either page_structure or page_id should be specified, not both.
        """
        if page_structure is None and page_id is None:
            raise ValueError("Either page_structure or page_id must be provided")
        if page_structure is not None and page_id is not None:
            raise ValueError("Only one of page_structure or page_id should be provided")

        # get properties of this database
        db_properties = cls.database_extract_property_details(database_id)

        # translate the input dict into an iterable table
        property_table = make_property_table(db_properties, property_dict)

        # add each property name, value pair to the page or page structure
        for property_name, property_values, property_type in iterate_property_table(property_table):
            if page_structure is not None:
                page_structure = cls.page_add_properties(page_structure, property_name, property_values, property_type)
            else:
                cls.page_update_properties(page_id, property_name, property_values, property_type)

        print('All Properties Added')

        if page_structure is not None:
            return page_structure



    @classmethod
    def process_content(cls, df, page_structure=None, page_id=None):
        """
        Translates content dataframe into Notion blocks (JSON) and either appends blocks to a 
        page structure (not published yet) or updates an existing Notion page with this content.

        Inputs:
        - df (DataFrame): content types, content 
        - page_structure (dict): JSON structure to which content will be added, if specified.
        - page_id (str): ID of the page to be updated, if specified.

        Returns:
        - If page_structure is specified, returns the populated page structure (JSON).
        - If page_id is specified, returns None but updates the specified page with new content.
        
        Note: Either page_structure or page_id should be specified, not both.
        """
        if page_structure is None and page_id is None:
            raise ValueError("Either page_structure or page_id must be provided")
        if page_structure is not None and page_id is not None:
            raise ValueError("Only one of page_structure or page_id should be provided")

        for _, row in df.iterrows():
            content_type = row['content_type']
            content = row['content']
            
            if page_structure is not None:
                page_structure = cls.page_add_content(page_structure, content_type, content)
            else:
                cls.page_update_content(page_id, content_type, content)

        print('All Content Added')
        
        if page_structure is not None:
            return page_structure


    @classmethod
    def page_read(cls, page_id, details=False):
        """
        Retrieves Notion Page Properties & Content. 
        If include_details is True, processes the response data dictionary further.
        Returns response data dictionary or a tuple containing two data frames depending on the include_details parameter.
        """
        # retrieve page properties
        url = f"https://api.notion.com/v1/pages/{page_id}"
        res = cls.get_request(url)
        properties = res.json()

        # retrieve page contents 
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        res = cls.get_request(url)
        content = res.json()

        # merge response data dictionaries
        page = {**properties, **content}

        if details:
            page_info, page_content = extract_page_details(page)
            return page_info, page_content
        else:
            return page