from selenium import webdriver
from bs4 import BeautifulSoup
import telebot 
import re
import os

bot = telebot.TeleBot(os.environ.get("TOKEN"))

@bot.message_handler(content_types=['text'])
def answer(message):
    t = '[A-Z]{2}[0-9]{9}[A-Z]{2}'
    if len(message.text) == 13 and re.match(t, message.text):  
        parsel_from_ali = parsel(message.text)
        bot.send_message(message.from_user.id, parsel_from_ali.run())  
    else:
        fault_masssage = 'Трек-номер не верный' + u"\xE2\x9D\x97" + 'Попробуйте еще раз' + u"\xF0\x9F\x93\xB2" + u"\xF0\x9F\x92\xBB"
        bot.send_message(message.from_user.id, fault_masssage)

class parsel:
    def __init__(self, item_num):
        self.item_num = item_num  
        self.result = ''

    def load_page(self):
        url = 'https://1track.ru/tracking/' + '{}'.format(self.item_num)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get(url)  
        requiredHtml = browser.page_source 
        return requiredHtml

    def exploring_page(self, page):  
        soup = BeautifulSoup(page, 'lxml')
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
                    self.result = self.result + time + ' ' + info_about_po + '\n'  
        return self.result

    def run(self):  
        page = self.load_page()
        finish = self.exploring_page(page=page)
        return finish


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)