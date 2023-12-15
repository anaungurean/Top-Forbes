from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
from DatabaseConnector import DatabaseConnector


class ForbesScraper:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.profile_billionaire_urls = []
        self.db_connector = DatabaseConnector()

    def scrape_principal_page_top_billionaires(self):
        try:
            button_locator = (By.CSS_SELECTOR, '.root__mAWHD.s14__GnYh6.w600__HAzqX.lh1\\.43__yhVAV')
            button_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(button_locator)
            )
            button_element.click()

            WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'TableRow_row__L-0Km')) #TableRow_row__L-0Km este clasa care contine informatiile pentru fiecare billionaire
            )
            html_source = self.driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            divs = soup.find_all('div', class_='TableRow_row__L-0Km')

            for div in divs:
                div_id = div['id']
                url = f'https://www.forbes.com/profile/{div_id}'
                if len(self.profile_billionaire_urls) >= 200:
                   break
                self.profile_billionaire_urls.append(url)

        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_billionaire_profile_data(self, profile_dict, index):
        try:
            self.db_connector.insert_data(
                profile_dict['Name'], profile_dict['Net Worth'], profile_dict['Age'],
                profile_dict['Source of Wealth'], profile_dict['Self-Made Score'],
                profile_dict['Philanthropy Score'], profile_dict['Residence'],
                profile_dict['Citizenship'], profile_dict['Marital Status'],
                profile_dict['Children'], profile_dict['Education'])

            print(f"Inserted data for billionaire from {index} position")
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")

    def scrap_profile_billionaire_page(self, url):
        try:
            profile_keys_list = [
                'Name', 'Net Worth', 'Age', 'Source of Wealth', 'Self-Made Score',
                'Philanthropy Score', 'Residence', 'Citizenship', 'Marital Status',
                'Children', 'Education'
            ]

            profile_dict = {key: None for key in profile_keys_list}

            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'listuser-block__item')) #listuser-block__item este clasa care contine informatiile 'Pesonal Stats'
            )

            html_source = self.driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            h1_element = soup.find('h1', class_='listuser-header__name') #listuser-header__name este clasa care contine numele miliardarului
            if h1_element:
                h1_text = h1_element.get_text(strip=True, separator=' ')
            else:
                h1_text = None
            profile_dict['Name'] = h1_text

            div_element = soup.find('div', class_='profile-info__item-value') #profile-info__item-value este clasa care contine valoarea averii
            if div_element:
                div_text = div_element.get_text(strip=True, separator=' ')
            else:
                div_text = None
            profile_dict['Net Worth'] = div_text

            dl_elements = soup.find_all('dl', class_='listuser-block__item')
            for dl_element in dl_elements:
                dt_element = dl_element.find('dt', class_='profile-stats__title')
                dd_element = dl_element.find('dd', class_='profile-stats__text')

                if dt_element:
                    dt_text = dt_element.get_text(strip=True)
                else:
                    dt_text = None

                if dd_element:
                    dd_text = dd_element.get_text(strip=True)
                else:
                    dd_text = None

                profile_dict[dt_text] = dd_text

            index = self.profile_billionaire_urls.index(url) + 1
            self.insert_billionaire_profile_data(profile_dict, index)
            # print(f"Print data for billionaire from {index} position")
            # print(profile_dict)
        except Exception as e:
            print(f"An error occurred while scraping the profile page with the url: {url} {e} ")

    def scrap_profile_pages(self):
        for url in self.profile_billionaire_urls:
            self.scrap_profile_billionaire_page(url)

    def run_scraper(self):
        try:
            self.db_connector.delete_all_data()
            self.driver.get('https://www.forbes.com/billionaires/')
            self.scrape_principal_page_top_billionaires()
            print(len(self.profile_billionaire_urls))
            self.scrap_profile_pages()
        finally:
            self.driver.quit()




