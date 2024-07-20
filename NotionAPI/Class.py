from Notion.Helpers import *
import os
import requests
from dotenv import load_dotenv
load_dotenv()


def http_status(func):
    def wrapper(cls, *args, **kwargs):  # Notice the 'cls' parameter here
        response = func(cls, *args, **kwargs)
        if response.status_code == 200:
            print('Request successful.')
        else:
            print(f"Error. Status code: {response.status_code}")
            print(response.json())
        return response
    return wrapper


class NotionAPI:

    integration_token = os.getenv("integration_token")
    headers = { 
        "Authorization": f"Bearer {integration_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    @classmethod
    @http_status
    def post_request(cls, url, json=None):
        res = requests.request("POST", url, json=json, headers=cls.headers, timeout=15)
        return res
    
    @classmethod
    @http_status
    def patch_request(cls, url, json=None):
        res = requests.request("PATCH", url, json=json, headers=cls.headers, timeout=15)
        return res
    
    @classmethod
    @http_status
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
        """
        Extracts the page ID, title, and URL from the database.
        """
        data = cls.database_read(database_id)
        page_details = create_table_with_page_details(data)
        return page_details
    

    @classmethod
    def database_extract_property_details(cls, database_id):
        """
        Extracts the property ID, name, and type from the database.
        """
        data = cls.database_read(database_id)
        property_details = create_table_with_property_details(data)
        return property_details
    

    ############################################################################
    #################################   PAGES  #################################
    ############################################################################

    #--------- CREATE ----------

    @classmethod
    def page_structure(cls, database_id, page_title, page_content=None, page_properties=None):
        """ Creates and returns basic Notion page structure (JSON)."""
        page_structure = basic_page_structure(database_id, page_title)
        if page_content is not None:
            page_structure = cls.process_content(page_content, page_structure=page_structure)
        if page_properties is not None:
            page_structure = cls.process_properties(database_id, page_properties, page_structure=page_structure)
        return page_structure
    

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


    #--------- READ ----------
   
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
        
    
    
    #--------- UPDATE ----------

    @classmethod
    def add_content_block(cls, content_type, content, header = None, sub_header = None, page_id=None, page_structure=None):
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

        # Appending to Page Structure 
        if page_structure is not None:
            
            # add content title and/or subtitle if specified
            if header is not None:
                page_structure = cls.add_content_block('heading_2', header, page_structure=page_structure)
            if sub_header is not None:  
                page_structure = cls.add_content_block('heading_3', sub_header, page_structure=page_structure)
            
            # add new content
            page_structure = create_and_append_new_block_to_page_structure(content_type, content, page_structure)
            return page_structure
        
        # Appending to Existing Page
        elif page_id is not None:
            url = f"https://api.notion.com/v1/blocks/{page_id}/children"

            # Helper function to wrap block data within 'children' array and send the PATCH request
            def send_block_to_notion(block_data):
                data = {"children": [block_data]}  # wrap block in 'children' array
                return cls.patch_request(url, json=data)

            # add content title and/or subtitle if specified
            if header is not None:
                content_title = create_and_append_new_block_to_existing_page('heading_2', header, page_id)
                res1 = send_block_to_notion(content_title)

            if sub_header is not None:
                content_subtitle = create_and_append_new_block_to_existing_page('heading_3', sub_header, page_id)
                res2 = send_block_to_notion(content_subtitle)

            # add new content
            new_content = create_and_append_new_block_to_existing_page(content_type, content, page_id)
            res3 = send_block_to_notion(new_content)
            return res3

        else:
            raise ValueError("Either page_id or page_structure must be specified")



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

        if page_id is not None and page_structure is not None:
            raise ValueError("Only one of page_id or page_structure should be specified")

        property_object = create_properties(property_values, property_type)

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
        
    #--------- DELETE ----------

    @classmethod
    def page_delete(cls, page_id):
        """ Deletes Notion page. """
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"archived": True}
        res = cls.patch_request(url, json=payload)
        return res

    @classmethod
    def page_refresh(cls, database_id, page_id, new_page_title, new_page_content=None, new_page_properties=None):
        """
        Deletes & creates a new Notion page with new page_title, content, and property values.
        
        Inputs:
            - database Id (str)
            - page Id (str): Id of the page to be refreshed
            - new page_title (str)
            - new content (str, optional): FILE PATH TO CONTENT INPUT FLAT FILE
            - new property values (dict) - Optional 
        
        Returns: page Id of new page version. 
        """
        cls.page_delete(page_id)  # delete old version
        new_page_id = cls.page_create(database_id,
                                      page_title=new_page_title,
                                      page_content=new_page_content,
                                      page_properties=new_page_properties
                                      )
        print('Page Refreshed with new Content.')
        return new_page_id


    ############################################################################
    ################################   BLOCKS  #################################
    ############################################################################

    @classmethod
    def block_read(cls, block_id):
        """ Retrieves Notion block. """
        url = f"https://api.notion.com/v1/blocks/{block_id}"
        res = cls.get_request(url)
        data = res.json()
        return data
    
    @classmethod
    def block_update(cls, block_id, content_type, content):
        """ Updates existing Notion block with new block. """
        updated_block = create_block(content_type, content)
        url = f"https://api.notion.com/v1/blocks/{block_id}"
        res = cls.patch_request(url, json=updated_block)
        return res
    
    @classmethod
    def block_delete(cls, block_id):
        """ Deletes Notion block. """
        url = f"https://api.notion.com/v1/blocks/{block_id}"
        data = {"archived": True}
        res = cls.patch_request(url, json=data)
        return res
    

    ############################################################################
    #######################   DATA PROCESSING  #################################
    ############################################################################

    @classmethod
    def process_content(cls, file_path, page_structure=None, page_id=None):
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

        # check params
        if page_structure is None and page_id is None:
            raise ValueError("Either page_structure or page_id must be provided")
        if page_structure is not None and page_id is not None:
            raise ValueError("Only one of page_structure or page_id should be provided")

        # load flat file 
        df = pd.read_csv(file_path)

        # iterate over flat file rows
        for _, row in df.iterrows():
            title = row['title']
            subtitle = row['subtitle']
            content_type = row['content_type']
            content = row['content']
            
            # add title 
            if pd.notnull(title):
                if page_structure is not None:
                    page_structure = cls.add_content_block('heading_2', title, page_structure=page_structure)
                else:
                    cls.add_content_block('heading_3', title, page_id = page_id)
            
            # add subtitle 
            if pd.notnull(subtitle):
                if page_structure is not None:
                    page_structure = cls.add_content_block('heading_2', subtitle, page_structure=page_structure)
                else:
                    cls.add_content_block('heading_3', subtitle, page_id = page_id)

            # add content 
            if pd.notnull(content):
                if page_structure is not None:
                    page_structure = cls.add_content_block(content_type, content, page_structure=page_structure)
                else:
                    cls.add_content_block(content_type, content, page_id = page_id)

        print('All Content Added')

        if page_structure is not None:
            return page_structure
        


    @classmethod
    def process_properties(cls, database_id, property_dict, page_structure=None, page_id=None):
        # check params
        if page_structure is None and page_id is None:
            raise ValueError("Either page_structure or page_id must be provided")
        if page_structure is not None and page_id is not None:
            raise ValueError("Only one of page_structure or page_id should be provided")

        # get properties of this database
        db_properties = cls.database_extract_property_details(database_id)

        # translate the input dict into an iterable table
        property_table = make_property_table(db_properties, property_dict)

        # placeholder for properties
        data = { "properties": {}}

        # add each property name, value pair to the page or page structure
        for property_name, property_values, property_type in iterate_property_table(property_table):
            property_object = create_properties(property_values, property_type)
            if page_structure is not None:
                if 'properties' not in page_structure:
                    page_structure['properties'] = {}
                page_structure['properties'][property_name] = property_object
            else:
                data['properties'][property_name] = property_object

        
        # update page with all properties values if page id not None
        if page_id is not None:
            url = f"https://api.notion.com/v1/pages/{page_id}"
            cls.patch_request(url, json=data)

        print('All Properties Added')

        if page_structure is not None:
            return page_structure