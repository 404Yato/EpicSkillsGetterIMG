import csv
import requests
from bs4 import BeautifulSoup
import os

# Variables
path_script = os.path.dirname(os.path.abspath(__file__))  # Script path

csv_name = 'e7HeroData.csv'

path_csv_file = os.path.join(path_script, csv_name)

column_name = 'name'    # Name of the column you want to extract

column_values = []  # List to store column values

main_page_url = "https://epic7x.com/character/" # Main page URL with images




# The following block of code executes all necessary processes with the csv file.
with open(path_csv_file, 'r', newline='', encoding='utf-8') as csv_file:    # Open CSV file in read mode

    csv_reader = csv.DictReader(csv_file)   # Create a CSV reader object interpreting the first row as headers

    for row in csv_reader:  # Iterate over CSV file rows
        
        if column_name in row:  # Check if column exists in row before attempting to access
            
            column_values.append(row[column_name])  # Add column value to list




parse_list = [name.lower().replace(" ", "-") for name in column_values] # Format the list extracted from the csv file




for name in parse_list: # Iterate through the list with all character names
    
    folder_name = name.replace("-", " ").title()    #Folder name to save the images

    directory = os.path.join(path_script, folder_name)
   
    url_character = main_page_url + name + "/"   # Save character direct URL
       
    character_response = requests.get(url_character)  # Perform HTTP request to get HTML content of character page
    
    
    
    
    print(f"NAME CHARACTER: {name}")
    



    if character_response.status_code == 200:
        
        soup = BeautifulSoup(character_response.text, 'html.parser')  # Parse HTML of page containing images with BeautifulSoup

        image = soup.find_all('img', class_='skill-img pure-u-1-3')  # Find in soup all HTML tags that meet the given parameters 

        links_img = []  # List to store all obtained links
        



        for index, string in enumerate(image):
  
            if index >= 3:  # Execute loop only 3 times per character as each one has 3 skills
                break

            src_value = string.get('src') # Store the value containing 'src', in this case the image link
            
            print(f"{name} - {src_value}")
            
            if src_value:
                
                links_img.append(src_value) # If 'src' value is found, add it to the results list




        if not os.path.exists(directory):

            os.makedirs(directory) # Create directory if it doesn't exist
            
        count = 0 # Counter to name and order obtained images




        for img in links_img:

            count += 1

            image_response = requests.get(img) # Get complete URL of the image

            with open(f'{directory}/skill_{name}_{count}.png', 'wb') as f: f.write(image_response.content) # Save the image in the indicated directory


    else:

        print(f"It couldn't retrieve the image links. Code {character_response.status_code}") # If this is printed in the console, the get request to the page returned a code different from 200.
