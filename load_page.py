import os
import re

from selenium import webdriver
from selenium.common.exceptions import WebDriverException as WDE
from bs4 import BeautifulSoup

from emoji import *


class Load:
    """Loading main page."""
    def load_page_on_local(self, url):
        path = os.path.abspath('bot_parcel_item.py')
        base_dir = os.path.dirname(path)
        path_chromedriver = os.path.join(base_dir, 'chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  
        browser = webdriver.Chrome(executable_path=path_chromedriver, options=options)
        browser.implicitly_wait(2)
        try:
            browser.get(url)
        except WDE:
            print(WDE)
        else:
            requiredHtml = browser.page_source 
            return requiredHtml

    def load_page_on_host(self, url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.implicitly_wait(2)
        try:
            driver.get(url)
        except WDE:
            print(WDE)
        else:
            requiredHtml = driver.page_source 
            return requiredHtml


class Parser:
    """Getting info about post item."""

    result_delivery = ''
    time_in_way = ''
    estimated_time = ''
    total_info = ''

    def get_info_from_track_ru(self, html):
        soup = BeautifulSoup(html, 'lxml')
        row_parsel = soup.select('div.show_nogroups')
        for point in row_parsel:  
            points_of_arrivel = point.find_all('div', attrs={'class': 'stage'})           
            for block in points_of_arrivel:  
                title = block.find('div', attrs={'class': 'col-12 col-md-8 statuses-block'})
                if title == None:  
                    pass
                else:
                    info_about_po = title.h4['data-lang-ru']  
                    getting_time = block.find('div', attrs={'class': 'col-12 col-md-2 stage-timing stage-transit'})
                    time = getting_time.select_one('p.date').text
                    self.result_delivery = self.result_delivery + time + ' ' + info_about_po + '\n'  
        return self.result_delivery

    def get_info_from_posylka(self, html):
        global item_does_not_tracking 
        soup = BeautifulSoup(html, 'lxml')
       
        if soup.find('div', attrs={'class':'package-info-container'}):
            header = soup.find('div', attrs={'class':'package-status-info-box'}).text.strip()
            self.total_info = header + chip + plane + station + '\n'

            delivery_info = soup.find('div', attrs={'class':'package-info-delivery'})
            if delivery_info:
                days = delivery_info.find('div', attrs={'class':'package-info-delivery-days-title'}).text.strip()
                num_days = delivery_info.find('div', attrs={'class':'package-info-delivery-days-value'}).text.strip()
                self.time_in_way = days + ' ' + num_days + hourglass + '\n'

            target_time_info = soup.find('div', attrs={'class':'package-info-delivery-target'})
            if target_time_info:
                estimated = target_time_info.find('div', attrs={'class':'package-info-delivery-target-title'}).text.strip()
                estimated_time = target_time_info.find('div', attrs={'class':'package-info-delivery-target-value'}).text.strip()
                self.estimated_time = estimated + ': '+ estimated_time + postbox + '\n' + '\n'

            msg_to_user = self.total_info + self.time_in_way + self.estimated_time

            row_parsel = soup.find('ul', attrs={'class':'package-route-list'})
            if row_parsel:
                points_of_arrivel = row_parsel.find_all('li')
                points_of_arrivel_without_advert = points_of_arrivel[1:]
                for point in points_of_arrivel_without_advert:
                    full_time = point.find('div', attrs='package-route-box-content').text.split()
                    month_time = full_time[1]
                    month = re.findall(r'[а-я]+', month_time)[0]
                    num_month = full_time[0]

                    route_info = point.find('div', attrs='package-route-info')
                    country = route_info.find('div', attrs='package-route-box-content').small.text
                    action = route_info.find('div', attrs='package-route-box-content').text.strip().strip(country)

                    post_service = point.find('div', attrs='package-route-post-service').text.strip()
                    
                    point = num_month + ' ' + month + ' - ' + action + ' - ' + country + ' - ' + post_service + '\n'

                    if len(msg_to_user + point) > 4000:
                        return msg_to_user
                    else:
                        msg_to_user = msg_to_user + point

            return msg_to_user

        else:
            try:
                header = soup.find('div', attrs={'class':'package-status-header s2'}).text.strip()
                additional = soup.find('div', attrs={'class':'package-status-info-box'}).text.strip()
                return header + warning + '\n' + additional + negative_cross_mark
            except AttributeError:
                return 'Не удалось определить службу доставки' + ' ' + no_post_info
