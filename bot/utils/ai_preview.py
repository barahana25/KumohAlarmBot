import asyncio
import requests
from bs4 import BeautifulSoup
import base64
import os

if __name__ != "__main__":
    from bot import ai_board_link
else:
    ai_board_link = "https://ai.kumoh.ac.kr/ai/sub0501.do"

# from bot.utils.crawler import getText

async def get_preview(post_id: int) -> tuple:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    link = f"{ai_board_link}?mode=view&articleNo={post_id}&article.offset=0&articleLimit=10"

    html = requests.get(link, headers=header).text
    
    soup = BeautifulSoup(html, 'html.parser')
    
    text_list = soup.find('div', {"class": "board-contents"}).find('pre').find_all('div')[1].find('pre').find('pre').find('div').find('div').find_all('div')

    # Set img preview
    img_preview = None
    img_preview_base64 = None
    try:
        img_preview = "https://ai.kumoh.ac.kr" + soup.find('div', {"class": "board-contents"}).find('img')['src']
        res = requests.get(img_preview, headers=header)
        with open('./ai_temp.png', 'wb') as f:
            f.write(res.content)

        with open('./ai_temp.png', 'rb') as f:
            base64_str = base64.b64encode(f.read())

        img_preview_base64 = base64_str

        os.remove('./ai_temp.png')
    except:
        pass

    text = ''
    for i in text_list:
        text += i.text + '\n'
    print(text)
    
    if len(text) <= 100:
        result = text
    else:
        result = f'{text[:100]} ...[더보기]({ai_board_link}?mode=view&articleNo={post_id}&article.offset=0&articleLimit=10)'
    
    return img_preview_base64, result

# test
if __name__ == "__main__":
    print(asyncio.run(get_preview(538535)))