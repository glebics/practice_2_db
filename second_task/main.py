import re
import os
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from database import get_db
from sqlalchemy.orm import Session
import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

BASE_URL = "https://spimex.com/markets/oil_products/trades/results/"


def calculate_months_limit():
    start_date = datetime(2023, 1, 1)
    current_date = datetime.now()
    months_diff = (current_date.year - start_date.year) * \
        12 + current_date.month - start_date.month
    return months_diff


def fetch_report_links():
    session = requests.Session()
    page_number = 1
    months_limit = calculate_months_limit()
    collected_links = []

    while len(collected_links) < months_limit:
        url = f"{BASE_URL}?page={page_number}"
        response = session.get(url)

        if response.status_code != 200:
            logging.info(
                f"Ошибка загрузки страницы {page_number}. Код ответа: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select("a.accordeon-inner__item-title.link.xls")

        for link in links:
            if "Бюллетень по итогам торгов в Секции «Нефтепродукты»" in link.text:
                href = link.get("href")
                full_link = f"https://spimex.com{href}"
                collected_links.append(full_link)
                print(f"Ссылка на файл: {full_link}")

                if len(collected_links) >= months_limit:
                    break

        page_number += 1

    return collected_links[:10]


def extract_trade_date(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        for row in df.itertuples(index=False):
            for cell in row:
                if isinstance(cell, str) and "Дата торгов:" in cell:
                    date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", cell)
                    if date_match:
                        trade_date = datetime.strptime(
                            date_match.group(), "%d.%m.%Y")
                        logging.info(
                            f"Дата торгов успешно извлечена: {trade_date.date()}")
                        return trade_date.date()
        logging.error(f"Дата не найдена в файле {file_path}")
        return None
    except Exception as e:
        logging.error(f"Ошибка извлечения даты из файла {file_path}: {e}")
        return None


def download_report(url, index):
    response = requests.get(url)
    if response.status_code == 200:
        temp_file_path = os.path.join(REPORTS_DIR, f"temp_report_{index}.xls")
        with open(temp_file_path, "wb") as file:
            file.write(response.content)

        report_date = extract_trade_date(temp_file_path)

        if report_date:
            final_file_path = os.path.join(REPORTS_DIR, f"{report_date}.xls")
            os.rename(temp_file_path, final_file_path)
            logging.info(f"Файл сохранен: {final_file_path}")
        else:
            os.remove(temp_file_path)
            logging.warning(
                f"Файл {temp_file_path} удален из-за отсутствия даты.")
    else:
        logging.error(
            f"Ошибка скачивания файла по ссылке {url}. Код ответа: {response.status_code}")


def main():
    logging.info("Начало работы программы.")
    report_links = fetch_report_links()

    for i, url in enumerate(report_links, start=1):
        logging.info(f"Скачивание отчета {i} из {len(report_links)}")
        download_report(url, i)

    logging.info("Завершение работы программы.")


if __name__ == "__main__":
    main()
