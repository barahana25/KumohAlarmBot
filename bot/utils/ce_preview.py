import asyncio
import requests
from bs4 import BeautifulSoup

if __name__ != "__main__":
    from bot import ce_board_link
else:
    ce_board_link = "https://ce.kumoh.ac.kr/ce/sub0501.do"

# from bot.utils.crawler import getText

async def get_preview(post_id: int) -> tuple:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    link = f"{ce_board_link}?mode=view&articleNo={post_id}&article.offset=0&articleLimit=10"

    html = requests.get(link, headers=header).text
    
    soup = BeautifulSoup(html, 'html.parser')
    
    text_list = soup.find('div', {"class": "board-contents"}).find_all('p')

    # Set img preview
    img_preview = None
    try:
        img_preview = soup.find('div', {"class": "board-contents"}).find('img')['src']
    except:
        pass

    text = ''
    for i in text_list:
        text += i.get_text() + " "
    
    if len(text) <= 100:
        result = text
    else:
        result = f'{text[:100]} ...[더보기]({ce_board_link}?mode=view&articleNo={post_id}&article.offset=0&articleLimit=10)'
    
    return img_preview, result

# test
if __name__ == "__main__":
    print(asyncio.run(get_preview(34915)))