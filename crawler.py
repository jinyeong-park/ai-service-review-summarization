import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver

print(webdriver.Chrome().service.path)


URL = 'https://www.yanolja.com/reviews/domestic/1000102262?sort=created-at%3Adesc'


def crawl_hotel_reviews():
    review_lists = []
    driver = webdriver.Chrome()
    driver.get(URL)

    time.sleep(3)

    # scroll down
    scroll_count = 10
    for i in range(scroll_count):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    # now parsing with BeautifulSoup - review text, star rating, date
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    review_containers = soup.select(
        '#__next > section > div > div.css-1js0bc8 > div > div > div')

    review_date = soup.select(
        '#__next > section > div > div.css-1js0bc8 > div > div > div > div.css-1toaz2b > div > div.css-1ivchjf')

    # extract review text, star rating, date from review container
    for i in range(len(review_containers)):
        review_text = review_containers[i].find(
            'p', class_='content-text').text
        review_star = review_containers[i].find_all(
            'path', {'fill': '#FDBD00'})  # yellow star
        star_cnt = len(review_star)
        date = review_date[i].text

        # one person's review
        review_dict = {
            'review': review_text,
            'stars': star_cnt,
            'date': date
        }

        review_lists.append(review_dict)

        print(review_dict)

    # save it into file
    with open('./data/review.json', 'w') as f:
        # easy to read korean: ensure_ascii=False
        json.dump(review_lists, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    crawl_hotel_reviews()
