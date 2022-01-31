import json
import os
import re
import urllib.request
from selenium import webdriver
from dotenv import load_dotenv

def get_naver_token():
    load_dotenv()

    driver_path = os.environ.get('DRIVER_PATH')
    naver_id = os.environ.get('NAVER_ID')
    naver_pw = os.environ.get('NAVER_PW')
    naver_cid = os.environ.get('NAVER_CLIENT_ID')
    naver_csec = os.environ.get('NAVER_CLIENT_SECRET')
    naver_redirect = os.environ.get('NAVER_BLOG_REDIRECT')

    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(3)
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element_by_name('id').send_keys(naver_id)
    driver.find_element_by_name('pw').send_keys(naver_pw)
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

    state = "REWERWERTATE"
    req_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=%s' % (naver_cid, naver_redirect, state)

    driver.get(req_url)
    ##########################
    # XXX: 최초 1회만 반드시 필요하고 이후엔 불필요함
    driver.find_element_by_xpath('//*[@id="confirm_terms"]/a[2]').click()
    ##########################
    redirect_url = driver.current_url
    temp = re.split('code=', redirect_url)
    code = re.split('&state=', temp[1])[0]
    driver.quit()

    print(redirect_url)
    print(code)

    url = 'https://nid.naver.com/oauth2.0/token?'
    data = 'grant_type=authorization_code' + '&client_id=' + naver_cid + '&client_secret=' + naver_csec + '&redirect_uri=' + naver_redirect + '&code=' + code + '&state=' + state

    request = urllib.request.Request(url, data=data.encode("utf-8"))
    request.add_header('X-Naver-Client-Id', naver_cid)
    request.add_header('X-Naver-Client-Secret', naver_redirect)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    token = ''
    if rescode == 200:
        response_body = response.read()
        js = json.loads(response_body.decode('utf 8'))
        token = js['access_token']
    else:
        print("Error Code:", rescode)
        return None

    if len(token) == 0:
        return None
    print(token)
    return token

get_naver_token()