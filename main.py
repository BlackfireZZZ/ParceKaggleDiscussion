from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
import os

# === Настройка Selenium-драйвера ===
def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# === Функция для извлечения текста и сохранения в JSON ===
def extract_text_to_json(url, name: str, output_filename='output.json'):
    driver = create_driver()
    driver.get(url)

    time.sleep(5)  # Ждём загрузку сайта

    try:
        div_container = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="discussions-topic-header"]')
        text = div_container.text.strip()

        if os.path.exists(output_filename):
            with open(output_filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {}

        data[name] = text

        with open(output_filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"[✔] Данные успешно добавлены в '{output_filename}' под ключом '{name}'.")

    except NoSuchElementException:
        print("[!] Контейнер с data-testid='discussions-topic-header' не найден.")

    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.kaggle.com/competitions/playground-series-s5e3/discussion/571176"
    discussion_prefix = url.split("competitions/")[-1]
    extract_text_to_json(url, name=discussion_prefix)
