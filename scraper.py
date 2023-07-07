'''Gets quotes from the website and saves them to a file.'''
from logging import getLogger

from seleniumwire import webdriver
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from base64 import b64encode

from output import BaseOutput

logger = getLogger(__name__)
getLogger('selenium').setLevel('INFO')

class Scraper():
    def __init__(self, PROXY: str, INPUT_URL: str, output: BaseOutput) -> None:
        self.input_url = INPUT_URL
        self.output = output
        self.driver = self.create_driver(PROXY, PROXY != '')
        self.proxy_auth = b64encode(PROXY.split('@')[0].encode('utf-8'))
        
        if PROXY != '':
            self.__test_proxy()


    def __del__(self) -> None:
        self.driver.quit()


    def request_interceptor(self, request) -> None:
        '''Sets proxy auth headers on each request.'''
        request.headers['Proxy-Authorization'] = f'Basic {self.proxy_auth}'


    @staticmethod
    def create_driver(proxy: str, use_proxy) -> webdriver.Chrome:
        '''Creates a Chrome webdriver with proxy settings.'''

        proxy_server = proxy.split('@')[1]

        options = Options()
        options.add_argument('--window-size=1420,1080')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        if use_proxy:
            options.add_argument(f'--proxy-server={proxy_server}')
        
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
        #                           options=options)

        # for local testing if you have chromedriver.exe in root directory
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

        return driver


    def __test_proxy(self) -> None:
        '''Tests the proxy by getting the IP address from a website.'''
        self.driver.get('https://api.ipify.org')
        logger.info('IP: %s', self.driver.page_source)
        print(self.driver.page_source)
        if self.driver.page_source != '':
            self.driver.request_interceptor = self.request_interceptor
        else:
            self.driver = self.create_driver('', False)


    def __extract_data(self, quote) -> dict:
        return {
            'text': quote.find_element(By.XPATH, './/span[@class="text"]').text,
            'by': quote.find_element(By.XPATH, './/small[@class="author"]').text,
            'tags': [tag.text for tag in quote.find_elements(By.XPATH, './/a[@class="tag"]')]
        }


    def scrape(self) -> None:
        '''Scrapes the website and saves the data to passed output.'''
        wait = WebDriverWait(self.driver, 30)

        self.driver.get(self.input_url)
        logger.info('Opened %s', self.input_url)
        
        more_pages = True
        scrape_count = 0

        while more_pages:
            try:
                quotes = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="quote"]'))
                )
            except common.exceptions.TimeoutException:
                logger.error('Timed out waiting for quotes to load')
                pass

            scrape_count += 1
            logger.info('Scraping page %s', scrape_count)

            for quote in quotes:
                logger.info('Scraping quote: %s', quote.find_element(By.XPATH, './/span[@class="text"]').text)

                try:
                    data = self.__extract_data(quote)
                    self.output.write(data)
                except Exception as e:
                    logger.error('Error scraping quote: %s', e)
                    continue

            try:
                next_page = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//li[@class="next"]/a'))
                )
                logger.info('Found next page button, clicking it')
            except common.exceptions.TimeoutException:
                logger.info('No next page button found, exiting')
                more_pages = False
                break
            
            next_page.click()
            logger.info('Clicked next page button')
        
        logger.info('Scraping complete')
