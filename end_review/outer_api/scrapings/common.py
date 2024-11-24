from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape_url(place_id):
    url = f'https://place.map.kakao.com/{place_id}'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행 (옵션)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    try:
        rating_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div.location_evaluation > a:nth-child(3) > span.color_b')
            )
        )
    except Exception as e:
        rating_element = None

    rating = rating_element.text if rating_element else None

    if rating_element is None:
        try:
            no_rating_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     '#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div.location_evaluation > span.txt_blind')
                )
            )
        except Exception as e:
            no_rating_element = None
        rating = no_rating_element.text if no_rating_element else None
    driver.quit()
    return place_id, rating


def run_scraping(id_list, workers=5):
    with Pool(workers) as pool:
        results = pool.map(scrape_url, id_list)

    dict_result = dict()
    for place_id, rating in results:
        dict_result[place_id] = rating
    return dict_result
