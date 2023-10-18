import pandas as pd


def create_table_with_page_details(data):
    page_details_list = []

    for result in data.get('results', []):
        if result.get('object') == 'page':
            page_detail = {}
            page_detail['pageName'] = result.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', '')
            page_detail['pageId'] = result.get('id', '')
            page_detail['url'] = result.get('url', '')

            properties = result.get('properties', {})
            for prop_key, prop_value in properties.items():
                if prop_value.get('type') == 'multi_select':
                    page_detail[prop_key] = ', '.join([item.get('name', '') for item in prop_value.get('multi_select', [])])
                elif prop_value.get('type') in ('text', 'created_time', 'number'):
                    if prop_value.get('type') == 'created_time':
                        page_detail[prop_key] = prop_value.get('created_time', '')
                    else:
                        page_detail[prop_key] = prop_value.get(prop_value.get('type'), '')
                # Add additional property types as needed

            page_details_list.append(page_detail)

    return pd.DataFrame(page_details_list)



def create_table_with_property_details(data):
    # Initialize dictionaries to hold property details
    property_details_dict = {}

    for result in data.get('results', []):
        if result.get('object') == 'page':
            properties = result.get('properties', {})
            for property_name, property_details in properties.items():
                if property_name in {'Created', 'Name'}:
                    continue

                property_type = property_details.get('type', '')

                if property_name not in property_details_dict:
                    property_details_dict[property_name] = {
                        'Property Type': property_type,
                        'Possible Values': set()
                    }

                if property_type == 'multi_select' and 'multi_select' in property_details:
                    values = {item.get('name', '') for item in property_details.get('multi_select', [])}
                    property_details_dict[property_name]['Possible Values'].update(values)

    # Create lists to hold property details
    property_names = []
    property_types = []
    possible_values = []

    for property_name, details in property_details_dict.items():
        property_names.append(property_name)
        property_types.append(details['Property Type'])
        possible_values.append(list(details['Possible Values']))

    # Create a data frame
    df = pd.DataFrame({
        'Property Name': property_names,
        'Property Type': property_types,
        'Possible Values': possible_values
    })

    return df






def basic_page_structure(database_id, page_title):
    new_page = {
        "parent": {
            "database_id": database_id
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": page_title
                        }
                    }
                ]
            }
        },
        "children": []  
    }
    return new_page






def create_block(block_type, block_content):
    if block_type == 'paragraph':
        block_object = {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": block_content
                        }
                    }
                ]
            }
        }
    elif block_type.startswith('heading'):
        block_object = {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{"type": "text", "text": {"content": block_content}}]
            }
        }
    elif block_type == 'image':
        block_object = {
            "object": "block",
            "type": block_type,
            block_type: {
                "type": "external",
                "external": {
                    "url": block_content  # image url 
                }
            }
        }
    elif block_type == 'bulleted_list':
        block_object = {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": block_content,
                            "link": None
                        }
                    }
                ],
                "color": "default"
            }
        }
    elif block_type == 'numbered_list':
        block_object = {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": block_content,
                            "link": None
                        }
                    }
                ],
                "color": "default"
            }
        }
    elif block_type == 'to_do':
        block_object = {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{"type": "text", "text": {"content": block_content}}],
                "checked": False
            }
        }
    else:
        block_object = {}
    return block_object



def create_and_append_new_block_to_page_structure(content_type, content, page_structure):
    new_block = create_block(content_type, content)
    page_structure['children'].append(new_block)
    return page_structure
    

def create_and_append_new_block_to_existing_page(content_type, content, page_id):
    new_block = create_block(content_type, content)
    new_block['parent'] = {'page_id': page_id}
    return new_block





def create_properties(property_values, property_type):

    # Extract the first value from the list if the list is not empty
    property_value = property_values[0] if property_values else None

    if property_type == "multi_select":
        property_object = {
            "multi_select": [{"name": tag} for tag in property_values]
        }
    elif property_type == "checkbox":
        # Example for checkbox property
        property_object = {
            "checkbox": property_value  # Assuming property_value is a boolean value
        }
    elif property_type == "created_by":
        # Example for created_by property
        property_object = {
            "created_by": {
                "object": "user",
                "id": property_value  # Assuming property_value is a user ID
            }
        }
    elif property_type == "created_time":
        # Example for created_time property
        property_object = {
            "created_time": property_value  # Assuming property_value is a timestamp
        }
    elif property_type == "date":
        property_object = {
            "date": {
                "start": property_value  # Assuming property_value is a date string
            }
        }
    elif property_type == "email":
        # Example for email property
        property_object = {
            "email": property_value  # Assuming property_value is an email address
        }
    elif property_type == "number":
        # Example for number property
        property_object = {
            "number": property_value  # Assuming property_value is a numeric value
        }
    elif property_type == "phone_number":
        # Example for phone_number property
        property_object = {
            "phone_number": property_value  # Assuming property_value is a phone number
        }
    else:
        # Default to rich_text for unknown property types
        property_object = {
            "rich_text": [{"text": {"content": tag}} for tag in property_values]
        }

    return property_object




def extract_page_details(data):
    """
    Extracts page and block details from a Notion API response data dictionary.

    Args:
    data (dict): The data dictionary from the Notion API response.

    Returns:
    tuple: A tuple containing two data frames: one for the page details and one for the blocks.
    """
    
    # Extract page properties
    page_properties = {
        "Page ID": data.get('id', ''),
        "Created Time": data.get('created_time', ''),
        "Page URL": data.get('url', ''),
        "Page Title": data['properties']['Name']['title'][0]['plain_text'] if data.get('properties') and data['properties'].get('Name') and data['properties']['Name'].get('title') else '',
    }

    # Extract block details
    blocks_data = []
    for block in data.get('results', []):
        block_type = block.get('type')
        block_content = block[block_type]['rich_text'][0]['text']['content'] if block.get(block_type) and block[block_type].get('rich_text') else ''
        block_details = {
            "Block ID": block.get('id', ''),
            "Block Type": block_type,
            "Block Content": block_content,
        }
        blocks_data.append(block_details)

    # Create DataFrames
    page_df = pd.DataFrame([page_properties])
    blocks_df = pd.DataFrame(blocks_data)

    return page_df, blocks_df





def most_recent_page_version(db_pages, page_name):
    """Checks for page duplicates and returns ID of most recent version"""
    
    # Convert 'Created' column to datetime
    db_pages['Created'] = pd.to_datetime(db_pages['Created'])

    # Filter the dataframe to only include rows with the specified string value
    filtered_df = db_pages[db_pages['pageName'] == page_name]

    # If there are one or more entries with that string value
    if len(filtered_df) >= 1:
        # Find the row with the most recent date
        most_recent_entry = filtered_df.sort_values(by='Created', ascending=False).iloc[0]

        # Get the 'PageId' of the most recent entry (adjust 'PageId' to your actual column name)
        most_recent_page_id = most_recent_entry['pageId']
        return most_recent_page_id
    else:
        return None



def make_property_table(db_properties, property_values):
    properties = db_properties[['Property Name', 'Property Type']]  # Extract necessary columns
    properties['Property Values'] = None

    for index, row in properties.iterrows():
        property_name = row['Property Name']
        if property_name in property_values:
            properties.at[index, 'Property Values'] = property_values[property_name]

    return properties


def iterate_property_table(property_table):
    for _, row in property_table.iterrows():
        property_type = row['Property Type']
        property_values = row['Property Values']
        property_name = row['Property Name']
        
        yield property_name, property_values, property_type
