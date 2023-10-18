import os
import json
import requests
import pandas as pd
import shutil
from PyPDF2 import PdfFileReader
import docx


def get_doc_type(file_path):
    """
    Determine the type of a document based on its file extension.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension in ['.txt']:
        return 'txt'
    elif file_extension in ['.pdf']:
        return 'pdf'
    elif file_extension in ['.docx']:
        return 'docx'
    else:
        print(f'Unsupported file extension: {file_extension}')
        return None



