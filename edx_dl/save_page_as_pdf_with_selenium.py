import chromedriver_binary
import sys
import os
from typing import List
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import pickle


#script_path = sys.path[0]
#download_path = os.path.join(script_path, 'PAGES_AS_PDFS_DIR')


'''
def create_download_dir(path: str = "PDFS_DOWNLOAD_DIR"):   
    script_path = sys.path[0]
    download_path = os.path.join(script_path, path)
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
    except IOError as e:
        exit()
    return download_path
'''
def login_to_edx(email:str, password:str) -> None:
    driver.get("https://courses.edx.org/login")
    driver.find_element_by_id('login-email').send_keys(email)
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="login"]/button').click()

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

def save_as_pdf_at_edx(urls: List[str]) -> None:

    for url in urls:
        driver.get(url)
        time.sleep(5)
        driver.execute_script('window.print();')

if __name__ == '__main__':
    
    options = webdriver.ChromeOptions()
    #options.add_argument("--user-data-dir=chrome-data")
    #changing downlaod directory seems not to work
    options.add_experimental_option("prefs", {
        "download.default_directory": "~/Downloads"
    })

    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(options=options)
    login_to_edx('gigigioioioi@gmail.com', '.H=zunfsCt8wn]+xBph.wd7*')
    time.sleep(5)
    cookies = driver.get_cookies()
    print(cookies)
    for cookie in cookies:
        if cookie.get('expiry', None) is not None:
            cookie['expires'] = cookie.pop('expiry')
    #save_cookie(driver, "coockie.p")
    #load_cookie(driver, "coockie.p")
    base_url = 'https://courses.edx.org/courses/course-v1:MITx+8.03x+1T2020/course/'
    driver.get(base_url)
    time.sleep(5)
    driver.execute_script('window.print();')
    
    html_of_table_of_contents_page = driver.page_source
    print(html_of_table_of_contents_page)
    re_sebsection_urls = re.compile(r"""['"](https://courses.edx.org/courses/.[^"]*)""")
    subsection_urls = re_sebsection_urls.findall(html_of_table_of_contents_page)
    #remove duplication in order
    print("subsection_urls", subsection_urls)
    subsection_urls_with_no_duplucation = list(dict.fromkeys(subsection_urls)) [1::] #somehow the first element is weird duplicaiton
    print("subsection_urls_with_no_duplucation", subsection_urls_with_no_duplucation)

    for subsection_url in subsection_urls_with_no_duplucation:
        driver.get(subsection_url)
        index = 0
        try:
            while True:
                driver.find_element_by_xpath(f'//*[@id="tab_{index}"]').click()
                time.sleep(5)
                driver.execute_script('window.print();')
                index += 1
        except NoSuchElementException:
            print("next section")
            pass

    print("Done!!")

    '''
    urls = ['https://courses.edx.org/courses/course-v1:MITx+8.01.2x+3T2019a/courseware/week:week5/ls:ls_05_02/?activate_block_id=block-v1%3AMITx%2B8.01.2x%2B3T2019a%2Btype%40sequential%2Bblock%40ls%3Als_05_02',
            'https://courses.edx.org/courses/course-v1:MITx+8.01.2x+3T2019a/courseware/week:week5/ls:ls_05_02/?activate_block_id=block-v1%3AMITx%2B8.01.2x%2B3T2019a%2Btype%40sequential%2Bblock%40ls%3Als_05_02']
    save_as_pdf_at_edx(urls, 'gigigioioioi@gmail.com', '.H=zunfsCt8wn]+xBph.wd7*')
    '''