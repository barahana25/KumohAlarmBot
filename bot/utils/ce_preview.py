import asyncio
import requests
from bs4 import BeautifulSoup
import base64
import os

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
    
    text_list = soup.find('div', {"class": "board-contents"})

    # Set img preview
    img_preview = None
    img_preview_base64 = None
    try:
        img_preview = "https://ce.kumoh.ac.kr" + soup.find('div', {"class": "board-contents"}).find('img')['src']
        res = requests.get(img_preview, headers=header)
        with open('./ce_temp.png', 'wb') as f:
            f.write(res.content)

        with open('./ce_temp.png', 'rb') as f:
            base64_str = base64.b64encode(f.read())

        img_preview_base64 = base64_str

        os.remove('./ce_temp.png')
    except:
        pass

    text = ''
    post_text = text_list.get_text(separator='\n', strip=True)
    # for i in text_list:
    #     text += i.getText() + " "
    text = post_text
    # print(text)
    if len(text) <= 100:
        result = text
    else:
        result = f'{text[:100]} ...[더보기]({ce_board_link}?mode=view&articleNo={post_id}&article.offset=0&articleLimit=10)'
    
    return img_preview_base64, result

async def main():
    img, result = await get_preview(538541)
    print("\n".join(map(str, result.splitlines())))
# test
if __name__ == "__main__":
    asyncio.run(main())