import requests, re, os
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium import webdriver


driver = webdriver.Firefox()

Base_URL = 'https://novelsbin.novelmagic.org/book/' 
URL = None

while True:
    novel_title = input('Input title of novel, in this format (eg. the-great-hero): ')
    match = re.search(r'([a-z]+(-[a-z]+)+)', novel_title)
    if match:
        # Tab page of desired book
        URL = Base_URL + novel_title + '#tab-chapters-title/'
        break
    else:
        continue

# New folder in books with title name

path = './books/' + novel_title
os.mkdir(path)

# Navigate main book page to get to first chapter
page = requests.get(URL)
soup = bs(page.content, "html.parser")
panel = soup.find('div',class_='panel-body')
# Access first chapter page
first_chapter = panel.find('a')
chapter_URl = first_chapter.get('href')
chapter_page = requests.get(chapter_URl)
# Do not consent to cookies
driver.get(chapter_URl)
driver.find_element(By.CSS_SELECTOR, 'button.fc-button.fc-cta-do-not-consent.fc-secondary-button').click()

for chapter in range(5):
    # Scrape chapter content
    title = driver.find_element(By.CSS_SELECTOR, 'span.chr-text').text
    content = driver.find_element(By.ID, 'chr-content').text
    # So doesn't try to make more than one file
    title = title.replace('/', '-')
    # Write to a new file in correct folder
    file_path = path +'/' + title +'.txt'
    file = open(file_path, 'wt')
    file.write(content)
    file.close()
    # Next chapter
    driver.find_element(By.ID, 'next_chap').click()

driver.quit()
