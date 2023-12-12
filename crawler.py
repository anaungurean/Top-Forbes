from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup

class ForbesScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.profile_billionaire_urls = []

    def scrape_page_top_billionaires(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'TableRow_row__L-0Km'))
            )
            html_source = self.driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            divs = soup.find_all('div', class_='TableRow_row__L-0Km')

            for div in divs:
                div_id = div['id']
                url = f'https://www.forbes.com/profile/{div_id}'
                if len(self.profile_billionaire_urls) >= 3:
                   break
                self.profile_billionaire_urls.append(url)

        except Exception as e:
            print(f"An error occurred: {e}")

    def click_next_page_button(self):
        try:
            button_locator = (By.CSS_SELECTOR, 'button.Pagination_gotoPageBtn__een24[aria-label="go to page 1"]')
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(button_locator)
            ).click()
        except Exception as e:
            print(f"An error occurred while clicking the next page button: {e}")

    def scrap_profile_page(self, url):
        try:
            profile_keys = [
                'Name', 'Net Worth', 'Age', 'Source of Wealth', 'Self-Made Score',
                'Philanthropy Score', 'Residence', 'Citizenship', 'Marital Status',
                'Children', 'Education'
            ]
            profile_dict = {key: None for key in profile_keys}

            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'listuser-block__item'))
            )

            html_source = self.driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            h1_element = soup.find('h1', class_='listuser-header__name')
            h1_text = h1_element.get_text(strip=True) if h1_element else None
            profile_dict['Name'] = h1_text

            div_element = soup.find('div', class_='profile-info__item-value')
            div_text = div_element.get_text(strip=True) if div_element else None
            profile_dict['Net Worth'] = div_text

            dl_elements = soup.find_all('dl', class_='listuser-block__item')
            for dl_element in dl_elements:
                dt_element = dl_element.find('dt', class_='profile-stats__title')
                dd_element = dl_element.find('dd', class_='profile-stats__text')

                dt_text = dt_element.get_text(strip=True) if dt_element else None
                dd_text = dd_element.get_text(strip=True) if dd_element else None
                profile_dict[dt_text] = dd_text

            print(profile_dict)

        except Exception as e:
            print(f"An error occurred while scraping the profile page: {e}")

    def scrap_profile_pages(self):
        for url in self.profile_billionaire_urls:
            self.scrap_profile_page(url)


    def run_scraper(self):
        try:
            self.driver.get('https://www.forbes.com/billionaires/')
            self.scrape_page_top_billionaires()
            # print(len(self.profile_billionaire_urls))
            self.click_next_page_button()
            self.scrape_page_top_billionaires()
            # print(self.profile_billionaire_urls)
            # print(len(self.profile_billionaire_urls))
            self.scrap_profile_pages()

        finally:
            self.driver.quit()




