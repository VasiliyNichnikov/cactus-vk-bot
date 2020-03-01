import bs4
from selenium import webdriver


class SchoolDiary:
    def __init__(self, vk_api, chatId, parent=None):
        self.parent = parent
        self.vk_api = vk_api
        self.chatId = chatId

    def Command(self):
        chromeDriver = r'C:\Users\vnich\AppData\Local\Temp\Rar$EXa17188.32852\chromedriver.exe'
        options = webdriver.ChromeOptions()

        #options.add_argument()
        browser = webdriver.Chrome(executable_path=chromeDriver, chrome_options=options)

        # Переход на страницу
        browser.get('https://dnevnik.mos.ru/')
        browser.find_element_by_xpath('/html/body/ui-view/div/div[1]/div/div[2]/div[1]/a').click()

        login = browser.find_element_by_name('login')
        password = browser.find_element_by_name('password')
        btn = browser.find_element_by_class_name('btn-primary')

        login.send_keys('89990993136')
        password.send_keys('R973ff578')
        btn.click()

        # Переход на страницу после ввода пароля
        browser.get('https://dnevnik.mos.ru/desktop')
        state = browser.execute_script("return document.readyState")
        print(state)
        requiredHtml = browser.page_source

        soup = bs4.BeautifulSoup(requiredHtml, 'html.parser')
        #blocksSchedule = soup.find('div', class_='lessons-wrapper')
        print(soup.prettify())



school = SchoolDiary(1, 2, 3)
school.Command()