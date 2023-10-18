from Notion.Class import *

# Ensure you replace 'your_database_id' with an actual database id
database_id = os.getenv('database_id')

NotionAPI = NotionAPI()

##### 1. Test the database read operation
print("\nReading from the database...")
data = NotionAPI.database_read(database_id)
print(data)

# page details
page_details = NotionAPI.database_extract_page_details(database_id)
page_details

# proeprty details
property_details = NotionAPI.database_extract_property_details(database_id)
property_details


##### 2. Test the page creation
print("\nCreating a new page...")
new_page_id = NotionAPI.page_create(database_id, page_title="Test Page 1")
print(f"New Page ID: {new_page_id}")

##### 3. Test adding a property to a page
print("\nAdding a property to the page...")

# Example Property
property_name = 'Tag 1'
property_type = 'multi_select'
property_values = ['Choice 1', 'Choice 2']

# Appending to Existing Page 
NotionAPI.add_property(property_name, property_values, property_type, page_id=new_page_id)

# Appending to Page Structure
page_structure = NotionAPI.page_structure(database_id, "Test Page 2")
page_structure = NotionAPI.add_property(property_name, property_values, property_type, page_structure=page_structure)
new_page_id = NotionAPI.page_create(database_id, page_structure=page_structure)


##### 4. Test adding a content block to a page
print("\nAdding a content block to the page...")

# Example Block
content_type = 'paragraph'
content = 'this is a paragraph'

# Appending to Page Structure 
page_structure = NotionAPI.page_structure(database_id, "Test Page 3")
page_structure = NotionAPI.add_content_block(content_type, content, page_structure = page_structure)
new_page_id_2 = NotionAPI.page_create(database_id, page_structure=page_structure)

# Appending to Existing Page 
response = NotionAPI.add_content_block(
    "paragraph", 
    "This is a test paragraph.", 
    "Test Header", 
    "Test Sub Header", 
    new_page_id_2
)

##### 5. Test the page deletion
print("\nDeleting the page...")
response = NotionAPI.page_delete(new_page_id)
print(response.json())

##### 6. Test block read operation
page_details = NotionAPI.database_extract_page_details(database_id, new_page_id)
block_id = page_details['block_id'][0]
print("\nReading a block...")
block_data = NotionAPI.block_read(block_id)
print(block_data)

##### 7. Test block update
print("\nUpdating a block...")
response = NotionAPI.block_update(block_id, 'paragraph', 'Updated content')
print(response.json())

##### 8. Test block deletion
print("\nDeleting a block...")
response = NotionAPI.block_delete(block_id)
print(response.json())


##### 9. Test processing of page property dict

# example property dict
property_dict_example = {
'property_name': [
    'Tag 1', # multi_select
    'Tag 2', # number
    'Tag 3', # select
    'Tag 4', # date
    'Tag 5' # phone number
],
'property_values': [
    ['Choice 1', 'Choice 2'],  # multi_select
    [12345],  # number
    ['Option1'],  # select
    ['2023-02-23'],  # date
    ['123-456-7890'],  # phone_number
]}

# add to a page structure 
page_structure = NotionAPI.page_structure_create('Title')
NotionAPI.process_properties(property_dict_example, page_structure=page_structure)

# add to existing page 
NotionAPI.process_properties(property_dict_example, page_id=new_page_id)


##### 10. Test processing of content flat file
content = pd.read_excel("/Users/toni/Desktop/Portfolio/Utilities/Utilities/Notion/Page_Content.xls")
content = pd.DataFrame(content)
NotionAPI.process_content(content, page_id=new_page_id)


##### 11. Test refreshing the page
print("\nRefreshing the page...")

# provide new page content as flat file 
new_content = pd.read_excel("/Users/toni/Desktop/Portfolio/Utilities/Utilities/Notion/Page_Content.xls")

# refresh page with new content
refreshed_page_id = NotionAPI.page_refresh(database_id, new_page_id_2, "Refreshed Page", new_page_content=new_content, 
new_page_properties={"name": "value"})
print(f"Refreshed Page ID: {refreshed_page_id}")

