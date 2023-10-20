# Imports
import requests
import time 
import pandas as pd 

from trafilatura import fetch_url, extract
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def evaluate_output(output):
    """
    Evaluates the content of the scraped output.
    
    Parameters:
    - output (str or None): The scraped content from a webpage.
    
    Returns:
    - str: 
        - "None" if the output is None.
        - "Error" if the output indicates an error.
        - "Success" if the output contains more than 10 words.
        - "Other" otherwise.
    """
    
    if output is None:
        return "None"
    elif output == "Error":
        return "Error"
    elif len(output.split()) > 10:
        return "Success"
    else:
        return "Other"

