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
                property_type = prop_value.get('type')

                if property_type == 'multi_select':
                    page_detail[prop_key] = ', '.join([item.get('name', '') for item in prop_value.get('multi_select', [])])
                elif property_type == 'checkbox':
                    page_detail[prop_key] = prop_value.get('checkbox')
                elif property_type == 'created_by':
                    page_detail[prop_key] = prop_value.get('created_by', {}).get('id')
                elif property_type == 'created_time':
                    page_detail[prop_key] = prop_value.get('created_time')
                elif property_type == 'date':
                    page_detail[prop_key] = prop_value.get('date', {}).get('start')
                elif property_type == 'email':
                    page_detail[prop_key] = prop_value.get('email')
                elif property_type == 'number':
                    page_detail[prop_key] = prop_value.get('number')
                elif property_type == 'phone_number':
                    page_detail[prop_key] = prop_value.get('phone_number')
                elif property_type == 'rich_text':
                    page_detail[prop_key] = ' '.join([item.get('text', {}).get('content', '') for item in prop_value.get('rich_text', [])])
                elif property_type == 'text':
                    page_detail[prop_key] = prop_value.get('text', {}).get('content', '')
                else:
                    # Handle other unknown types here
                    page_detail[prop_key] = str(prop_value)

            page_details_list.append(page_detail)

    return pd.DataFrame(page_details_list)





def basic_page_structure(page_parent, page_title):
    new_page = {
        "parent": page_parent,
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
