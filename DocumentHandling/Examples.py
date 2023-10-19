from DocumentHandling.Class import *

#------ FOLDERS ------#

# Create a new folder
folder_path = DocumentManager.create_folder(
   # folder_location='C:/Users/Owner/Desktop/...', 
    folder_location = os.getcwd(),
    folder_name='test_folder'
)

# Create a new sub-folder
subfolder_path = DocumentManager.create_subfolder(
    parent_folder=folder_path, 
    subfolder_name='test_subfolder'
)

# Delete the sub-folder & folder
DocumentManager.delete_folder(subfolder_path)
DocumentManager.delete_folder(folder_path)


#------ DOCUMENTS ------#

# Create a new document
file_path = DocumentManager.create_document(
    file_path = os.path.join(os.getcwd(), 'Test_File.txt'),
    content = 'bla bla bla'
)

# Read the document 
content = DocumentManager.read_document(file_path)
print(content)


# Update the document
DocumentManager.update_document(file_path, 'This is an updated test document.')

# Read the document again
content = DocumentManager.read_document(file_path)
print(content)

# Delete the document
DocumentManager.delete_document(file_path)
