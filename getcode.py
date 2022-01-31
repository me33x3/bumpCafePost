import os
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time

def get_code():
    load_dotenv()

    chrome_path = os.environ.get('CHROME_PATH')
    driver_path = os.environ.get('DRIVER_PATH')
    naver_id = os.environ.get('NAVER_ID')
    naver_pw = os.environ.get('NAVER_PW')
    naver_cid = os.environ.get('NAVER_CLIENT_ID')
    naver_redirect = os.environ.get('NAVER_REDIRECT')

    # exe debuger chrome
    subprocess.Popen(
        fr'{chrome_path} --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    driver.implicitly_wait(10)

    # 1차 로그인
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element_by_name('id').send_keys(naver_id)
    driver.find_element_by_name('pw').send_keys(naver_pw)
    driver.find_element_by_xpath('//*[@id="log.login"]').click()

    # 2차 로그인
    '''
    driver.find_element_by_name('pw').send_keys(naver_pw)
    time.sleep(30)
    print('!')
    driver.find_element_by_xpath('//*[@id="log.login"]').click()
    '''

    # 인증
    time.sleep(30)

    print(naver_cid)
    print(naver_redirect)

    state = "REWERWERTATE"
    req_url = f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={naver_cid}&redirect_uri={naver_redirect}&state={state}'

    driver.get(req_url)
    ##########################
    # XXX: 최초 1회만 반드시 필요하고 이후엔 불필요함
    driver.find_element_by_xpath('//*[@id="confirm_terms"]/a[2]').click()
    ##########################
    redirect_url = driver.current_url
    temp = re.split('code=', redirect_url)
    code = re.split('&state=', temp[1])[0]
    driver.quit()

    print('code : ', code)
    print('redirect_url : ', redirect_url)

get_code()