import requests
from bs4 import BeautifulSoup
import os
import re
import asyncio
import traceback

from bot.utils.database import *
from bot.utils.database import BiskitDB
from bot import biskit_link, LOGGER

async def read_biskit():
    """ 비스킷 새 글 읽기 """
    while True:
        try:
            # 쿠키 필요 없음
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            result = requests.get(biskit_link, headers=header).text  # 해당 링크의 html 코드를 가져옴

            soup = BeautifulSoup(result, 'html.parser')
            content_li = []
            for i in soup.find('ul', {"class": "con_text_box swiper-wrapper"}).find_all('li', {'class': 'swiper-slide swiper-slide-active'}):
                tmp_post_id = i.find('a', {'class':'detailBtn'})['data-params']
                post_id = re.search(r'"encSddpbSeq":"([0-9]+)"', tmp_post_id)
                
                # post_link = f"{biskit_link}/ptfol/imng/icmpNsbjtPgm/findIcmpNsbjtPgmInfo.do?encSddpbSeq={post_id}"

                if post_id is not None:
                    post_id = int(post_id.group(1))
                title = i.find('p', {"class": "pgm_tit"}).text.strip()
                org = i.find('li', {"class": "pgm_tag"}).text.strip()
                if "자율전공학부" in org:
                    continue
                content_li.append(
                    (
                        post_id, # 글 번호
                        title,
                        org
                    )
                )

            content_li.sort(key=lambda x:x[0])

            while True:
                try:
                    BiskitDB().set_database(content_li)
                except:
                    print(traceback.format_exc())
                else:
                    break
    
        except:
            print(traceback.format_exc())
        await asyncio.sleep(60)
