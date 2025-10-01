import re
import asyncio
import requests
import traceback
from bs4 import BeautifulSoup

from bot.utils.database import *
from bot.utils.crawler import getText
from bot.utils.database import aiBoardDB
from bot import ai_board_link, LOGGER

async def read_ai():
    """ AI게시판 새 글 읽기 """
    ai_link = ai_board_link
    while True:
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            result = getText(ai_link, header)

            soup = BeautifulSoup(result, 'html.parser')
            content_li = []
            for i in soup.find('div', {"class": "board-list01"}).find('tbody').find_all('tr'):
                # 클래스가 notice 가 아닐 경우
                # if i["class"] != ["notice"]: # 공지사항도 읽도록 수정
                # 링크 가져오기
                post_link = ai_link + i.find("td", {"class": "title left"}).find("a")["href"]

                # 링크에서 글 번호 가져오기
                post_num = re.search(r"&articleNo=([0-9]+)&", post_link)
                if post_num is not None:
                    post_num = int(post_num.group(1))
                title = i.find("td", {"class": "title left"}).find("span", {"class": "title-wrapper"}).text.strip()
                title = re.sub(r'\s+', ' ', title).strip()
                author = i.find("td", {"class": "writer"}).text.strip()
                content_li.append(
                    (
                        post_num, # 글 번호
                        title,
                        author
                    )
                )

            content_li.sort(key=lambda x:x[0])

            while True:
                try:
                    aiBoardDB().set_database(content_li)
                except:
                    print(traceback.format_exc())
                else:
                    break
    
        except:
            print(traceback.format_exc())
        await asyncio.sleep(60)