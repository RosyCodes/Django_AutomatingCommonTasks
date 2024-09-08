from bs4 import BeautifulSoup
import requests

# our target website to extract data
# url = "https://webscraper.io/test-sites/tables"
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
response = requests.get(url)

# returns the website's html code but in readable format
soup = BeautifulSoup(response.content, 'html.parser')
# extracts the table using the class
datatype_table = soup.find(class_='wikitable')
body = datatype_table.find('tbody')
rows = body.find_all('tr')[1:]  # extracts all tr's starting at position 1

mutable_types = []
immutable_types = []


for row in rows:
    data = row.find_all('td')
    if data[1].get_text() == 'mutable\n':  # gets the table column # 2
        mutable_types.append(data[0].get_text().strip())  # adds the data type
    else:
        immutable_types.append(data[0].get_text().strip())

print('Mutatable data types:', mutable_types)
print('================')
print('Immutatable data types:', immutable_types)


# THIS BLOCK IS FOR WEBSCRAPER WEBSITE:  https://webscraper.io/test-sites/tables
# # extracts only the headings i.e h1
# headings1 = soup.find_all('h1')
# headings2 = soup.find_all('h2')
# images = soup.find_all('img'[0])  # gets the first image

# # extracts the tables
# table = soup.find_all('table')[1]  # gets the 2nd table
# # returns everything starting at index 1 (excludes 'th')
# rows = table.find_all('tr')[1:]

# last_names = []
# for row in rows:
#     # adds the value only w/o tags
#     last_names.append(row.find_all('td')[2].get_text())
# print(last_names)
