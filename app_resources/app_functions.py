import streamlit as st
import os
from bs4 import BeautifulSoup
import pathlib

# Get the Google Adds link from environment variables
google_adds_link = os.getenv("GOOGLE_ADDS_LINK")

def add_script_to_header():
    """
    Function to add script tag to the head tag of an HTML file
    """
    filename = pathlib.Path(st.__file__).parent / "static" / "index.html"
    # Open the HTML file and parse it into a BeautifulSoup object
    with open(filename, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Create a new script tag
    new_tag = soup.new_tag(  
        name='script',  
        attrs={  
            'async': '',
            'src': google_adds_link,  
            'crossorigin': 'anonymous',  
            }  
    )  

    # Add the new script tag to the head tag
    soup.head.append(new_tag)

    # Write the modified HTML back to the file
    with open(filename, 'w') as file:
        file.write(str(soup))