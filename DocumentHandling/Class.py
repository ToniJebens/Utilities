from DocumentHandling.Helpers import *

class DocumentManager:
    
    #------- FOLDERS --------#

    @classmethod
    def create_folder(cls, folder_location, folder_name):
        """
        Creates folder within a specified directory.
        """
        folder_path = os.path.join(folder_location, folder_name)
        
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            return folder_path
        else:
            return folder_path
        
    @classmethod
    def create_subfolder(cls, parent_folder, subfolder_name):
        """
        Creates sub-folder within parent-folder.
        """
        if not os.path.exists(parent_folder):
            os.mkdir(parent_folder)
            
        subfolder_path = os.path.join(parent_folder, subfolder_name)
        
        if not os.path.exists(subfolder_path):
            os.mkdir(subfolder_path)
            return subfolder_path
        else:
            return subfolder_path

    @classmethod
    def delete_folder(cls, folder_path: str) -> bool:
        """
        Deletes the specified folder and its contents.
        """
        try:
            shutil.rmtree(folder_path)
            return True
        except Exception as e:
            print(f"Failed to delete folder: {folder_path}. Error: {e}")
            return False


    #------- DOCUMENTS --------#

    @classmethod
    def create_document(cls, file_path, content):
        """
        Create or overwrite a document with the given content.
        """
        doc_type = get_doc_type(file_path)
        file_path = create_doc(doc_type, file_path, content)
        return file_path


    @classmethod
    def read_document(cls, file_path):
        """
        Load content from a file based on its extension.
        Currently supports: .pdf, .txt, .doc, and .docx files.
        """
        doc = ""
        fileExtension = get_doc_type(file_path)
        doc = load_document(fileExtension, file_path)
        return doc

        
    @classmethod
    def update_document(cls, file_path, new_content):
        """
        Update the content of the document at the given file path.
        """
        cls.delete_document(file_path)
        cls.create_document(file_path, new_content)


    @classmethod
    def delete_document(cls, file_path):
        """
        Delete the document at the given file path.
        """
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete document: {file_path}. Error: {e}")

