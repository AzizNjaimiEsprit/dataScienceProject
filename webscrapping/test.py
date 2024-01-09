from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv

def remove_chars_between_brackets(input_string):
    # Define a regular expression pattern for matching text between square brackets
    pattern = re.compile(r'\[.*?\]')

    # Use the sub() function to replace the matched pattern with an empty string
    result_string = re.sub(pattern, '', input_string)

    return result_string

csv_file_path = 'matrix_data.csv'

url = "https://apps.who.int/gho/athena/data/GHO/RS_196,RS_198?profile=xtab&format=html&x-topaxis=GHO;SEX&x-sideaxis=COUNTRY;YEAR&x-title=table&filter=COUNTRY:*&ead="  # Replace with the actual URL of the website

# Use a web driver (make sure to have the appropriate driver installed, e.g., chromedriver)
driver = webdriver.Chrome()

# Open the website
driver.get(url)

# Wait for the dynamic content to load (you may need to adjust the waiting time)
#driver.implicitly_wait(2)

# Get the updated page source after dynamic content is loaded
updated_page_source = driver.page_source

# Parse the updated page source with BeautifulSoup
soup = BeautifulSoup(updated_page_source, 'html.parser')



# Find the table containing the data with the class "crosstable"
table = soup.find('table', class_='crosstable')


# Check if the table was found
if table:
    # Extract data from the table
    rows = table.find_all('tr')
    contryName = ""
    matrix = []
    headers = ['Country']
    # Remove first row
    print(rows[2])
    for header in rows[1].find_all(['th', 'td'])[1:]:
        headers.append(header.text.strip())
    rows = rows[2:]
    matrix.append(headers)
    # Iterate through rows
    for row in rows:
        # Extract individual cells from each row
        columns = row.find_all(['th', 'td'])

        row = []
        # Print the data (modify as needed)
        for column in columns:
            columnValue = column.text.strip()
            if (columnValue.isalpha()):
                contryName = column.text.strip()
            else:
                row.append(remove_chars_between_brackets(columnValue))
        row.insert(0,contryName)
        matrix.append(row)
    ###################################################
    # for row in matrix:
    #     for element in row:
    #         print(element, end=' ')
    #     print()
    with open(csv_file_path, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write each row of the matrix to the CSV file
        for row in matrix:
            csv_writer.writerow(row)

    print(f'Matrix has been exported to {csv_file_path}.')
else:
    print("Table with class 'crosstable' not found on the page.")

# Close the browser
driver.quit()

