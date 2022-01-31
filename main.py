import os
import sys
import requests
import urllib.request

clientId = "DyLwQnjeEAE5IODvr2yR"



token = ""
header = "Bearer " + token # Bearer 다음에 공백 추가
clubid = "28468238" # 카페 고유 ID값
menuid = "9"  # 게시판 고유 ID값
url = "https://openapi.naver.com/v1/cafe/" + clubid + "/menu/" + menuid + "/articles"

subject = urllib.parse.quote("네이버 Cafe api Test Python")
content = urllib.parse.quote("<font color='red'>python multi-part</font>로 첨부한 글입니다. <br> python 이미지 첨부 <br> <img src='#0' />")
data = {'subject': subject, 'content': content}
files = [
    ('image', ('images/1.jpg', open('images/1.jpg', 'rb'), 'image/jpeg', {'Expires': '0'})),
    ('image', ('images/2.jpg', open('images/2.jpg', 'rb'), 'image/jpeg', {'Expires': '0'})),
    ('image', ('images/3.jpg', open('images/3.jpg', 'rb'), 'image/jpeg', {'Expires': '0'}))
    ]

headers = {'Authorization': header }
response = requests.post(url, headers=headers, data=data, files=files)

rescode = response.status_code
if(rescode == 200):
    print(response.text)
else:
    print(rescode)