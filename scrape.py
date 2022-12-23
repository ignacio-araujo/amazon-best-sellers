# Amazon's Best Sellers web scrapper

from bs4 import BeautifulSoup
import requests
import xlsxwriter
from datetime import date
from timeit import default_timer as timer

start = timer() #Get the start time to measure execution time
items = 0 #Scrapped items counter

NUMBER_OF_ITEMS = 50 #Number of items to scrap from each category (max: 50)
main_url = 'https://www.amazon.com/Best-Sellers/zgbs'

def scrape_url(url):
    response = requests.get(url).text
    response_soup = BeautifulSoup(response, 'lxml')
    return response_soup


soup = scrape_url(main_url)

#Scrape the URL of the best selling item in each category
categories_url = []
for category in soup.find('ul', {'id': 'zg_browseRoot'}).find('ul').find_all('li'):
    if 'music' in category.a['href'] : continue
    categories_url.append(category.a['href'])

file_name = f"Amazon's Best Sellers {date.today()}.xlsx"
workbook = xlsxwriter.Workbook(file_name)


for url in categories_url:
    soup = scrape_url(url)
    title = soup.find('span', class_='category').text
    print('Processing '+title)

    worksheet = workbook.add_worksheet(title)
    bold = workbook.add_format({'bold': True})
    worksheet.write(0, 0, title, bold)
    worksheet.write(1, 0, 'Item name', bold)
    worksheet.write(1, 1, 'URL', bold)
    worksheet.write(1, 2, 'Image', bold)
    row = 2
    col = 0

    index = 1
    for i in soup.find_all('li', class_='zg-item-immersion'):
        if index > NUMBER_OF_ITEMS : break
        if i.find('span', class_='zg-item-unavailable') : continue
        worksheet.write(row, col, i.find('img')['alt'])
        worksheet.write(row, col+1, 'https://amazon.com'+i.find('a', class_='a-link-normal')['href'])
        worksheet.write(row, col+2, i.find('img')['src'])

        row += 1
        index += 1
        items += 1

workbook.close()

end = timer()
print(f'Done! It took {end - start} seconds to scrape {items} items from Amazon.com')