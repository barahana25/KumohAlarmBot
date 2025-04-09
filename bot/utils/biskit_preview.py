import asyncio
import requests
from bs4 import BeautifulSoup
import base64
import os

if __name__ != "__main__":
    from bot import biskit_link
else:
    biskit_link = "https://biskit.kumoh.ac.kr"


def biskit_login():
    JSESSIONID4 = 'a8pCzDU6C1eNT8wUCQYpTa3a7Qt2th78cbZFt1eaNETBRVsOvQizA313wCcHkDEg.a3Vtb2hfZG9tYWluL3lraXR3YXMyX0JJU0tJVA=='
    JSESSIONID = 'VAr7QwgScZTLyHsxCzhVErJfK21ckJyOc9nqPPwnE7pte29kvUXmoCdzZKlomnTX.a3Vtb2hfaG9tZS9QT1JUQUwy'
    Cookie = f'WMONID=NlaPpmASqkd; JSESSIONID4={JSESSIONID4}; JSESSIONID={JSESSIONID};'
    biskit_Cookie = f'WMONID=NlaPpmASqkd; JSESSIONID4={JSESSIONID4}; G_ENABLED_IDPS=google;'

    first_url = "https://biskit.kumoh.ac.kr/sso/index.jsp"

    first_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://biskit.kumoh.ac.kr/common/user/login.do',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    first_res = requests.get(first_url, headers=first_headers, allow_redirects=False)

    print("First Response Headers:")
    print(first_res.headers)

    JSESSIONID4 = first_res.cookies['JSESSIONID4']
    Cookie = f'WMONID=NlaPpmASqkd; JSESSIONID4={JSESSIONID4}; JSESSIONID={JSESSIONID};'
    biskit_Cookie = f'WMONID=NlaPpmASqkd; JSESSIONID4={JSESSIONID4}; G_ENABLED_IDPS=google;'

    second_url = first_res.headers['Location']

    second_headers = {
    'Host': 'sso.kumoh.ac.kr',
    'Cookie': Cookie,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://biskit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    second_res = requests.get(second_url, headers=second_headers, allow_redirects=False)

    print("Second Response Headers:")
    print(second_res.headers)

    ORIGINAL_JESSIONID = second_res.cookies['JSESSIONID']

    third_url = 'https://biskit.kumoh.ac.kr/sso/index.jsp?pmi-sso-return2=none'

    third_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://biskit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    third_res = requests.get(third_url, headers=third_headers, allow_redirects=False)

    print("Third Response Headers:")
    print(third_res.headers)

    fourth_url = third_res.headers['Location']

    fourth_headers = {
    'Host': 'onekit.kumoh.ac.kr',
    'Cookie': Cookie,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://biskit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    fourth_res = requests.get(fourth_url, headers=fourth_headers, allow_redirects=False)

    print("Fourth Response Headers:")
    print(fourth_res.headers)
    JSESSIONID = fourth_res.cookies['JSESSIONID']
    Cookie = f'WMONID=NlaPpmASqkd; JSESSIONID4={JSESSIONID4}; JSESSIONID={JSESSIONID};'


    login_url = "https://onekit.kumoh.ac.kr/proc/Login.eps"

    login_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ko;q=0.7',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': Cookie,
    'host': 'onekit.kumoh.ac.kr',
    'origin': 'https://onekit.kumoh.ac.kr',
    'pragma': 'no-cache',
    'referer': 'https://onekit.kumoh.ac.kr/login.jsp',
    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }
    login_data = {
        'user_id': os.environ['hakbun'],
        'user_password':  os.environ['password'],
    }

    login_res = requests.post(login_url, headers=login_headers, data=login_data, allow_redirects=False)

    print("5 Response Headers:")
    print(login_res.headers)
    JSESSIONID = login_res.cookies['JSESSIONID']
    Cookie = f'WMONID=NlaPpmASqkd; JSESSIONID4={JSESSIONID4}; JSESSIONID={JSESSIONID};'

    sso_url = login_res.headers['Location']
    sso_headers = {
    'Host': 'sso.kumoh.ac.kr',
    'Cookie': f"JSESSIONID={ORIGINAL_JESSIONID}; JSESSIONID4={JSESSIONID4};",
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://onekit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    sso_res = requests.get(sso_url, headers=sso_headers, allow_redirects=False)

    print(sso_res.headers)

    biskit_url = "https://biskit.kumoh.ac.kr/sso/index.jsp"

    biskit_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://onekit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    biskit_res = requests.get(biskit_url, headers=biskit_headers, allow_redirects=False)

    print(biskit_res.headers)

    biskit_sso_url = biskit_res.headers['Location']
    biskit_sso_headers = {
    'Host': 'sso.kumoh.ac.kr',
    'Cookie': f"JSESSIONID4={JSESSIONID4}; JSESSIONID={ORIGINAL_JESSIONID}; _SSO_Global_Logout_url=get%5Ehttps%3A%2F%2Fonekit.kumoh.ac.kr%2Flogout.jsp%3Flogout%3D1%24",
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://onekit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    biskit_sso_res = requests.get(biskit_sso_url, headers=biskit_sso_headers, allow_redirects=False)

    print(biskit_sso_res.headers)

    biskit_sso_1_url = biskit_sso_res.headers['Location']

    biskit_sso_1_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://onekit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    biskit_sso_1_res = requests.get(biskit_sso_1_url, headers=biskit_sso_1_headers, allow_redirects=False)

    print(biskit_sso_1_res.headers)

    biskit_login_url = biskit_sso_1_res.headers['Location']

    biskit_login_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://onekit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    biskit_login_res = requests.get(biskit_login_url, headers=biskit_login_headers, allow_redirects=False)

    print(biskit_login_res.headers)

    biskit_sso_2_url = biskit_login_res.headers['Location']

    biskit_sso_2_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Referer': 'https://onekit.kumoh.ac.kr/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }

    biskit_sso_2_res = requests.get(biskit_sso_2_url, headers=biskit_sso_2_headers, allow_redirects=False)
    print(biskit_sso_2_res.headers)

    biskit_sso_2_soup = BeautifulSoup(biskit_sso_2_res.text, 'html.parser')
    userId = biskit_sso_2_soup.find('input', {'name': 'userId'})['value']

    biskit_login_proc_url = "https://biskit.kumoh.ac.kr/common/user/loginProc.do"

    biskit_login_proc_headers = {
    'Host': 'biskit.kumoh.ac.kr',
    'Cookie': biskit_Cookie,
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'ko-KR',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://biskit.kumoh.ac.kr',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://biskit.kumoh.ac.kr/sso/index.jsp',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
    }
    biskit_login_proc_data = {
        'userId': userId,
        'rtnUrl': ''
    }

    biskit_login_proc_res = requests.post(biskit_login_proc_url, headers=biskit_login_proc_headers, data=biskit_login_proc_data, allow_redirects=False)
    print(biskit_login_proc_res.headers)
    print(biskit_login_proc_res.text)

    return biskit_Cookie


# url = "https://biskit.kumoh.ac.kr/ptfol/imng/icmpNsbjtPgm/findIcmpNsbjtPgmInfo.do?encSddpbSeq=31303033303938"

# headers = {
# 'Host': 'biskit.kumoh.ac.kr',
# 'Cookie': biskit_Cookie,
# 'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
# 'Sec-Ch-Ua-Mobile': '?0',
# 'Sec-Ch-Ua-Platform': '"Windows"',
# 'Accept-Language': 'ko-KR',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
# 'Sec-Fetch-Site': 'same-origin',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-User': '?1',
# 'Sec-Fetch-Dest': 'document',
# 'Referer': 'https://biskit.kumoh.ac.kr/index.do',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Priority': 'u=0, i',
# 'Connection': 'keep-alive',
# }

# res = requests.get(url, headers=headers)
# soup = BeautifulSoup(res.text, 'html.parser')

# for i in soup.find('div', {'class': 'table_wrap'}).find('tbody').find_all('tr'):
#     print(i.text)

async def get_preview(post_id: int) -> tuple:
    biskit_Cookie = biskit_login()
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            'Cookie': biskit_Cookie}

    link = f"{biskit_link}/ptfol/imng/icmpNsbjtPgm/findIcmpNsbjtPgmInfo.do?encSddpbSeq={post_id}"

    html = requests.get(link, headers=header).text
    soup = BeautifulSoup(html, 'html.parser')

    text_list = soup.find('div', {"class": "table_wrap"}).find('tbody')
    text_list = soup.find('div', {"class": "table_wrap"}).find('tbody').find_all('tr')[-1].find_all('p')

    # Set img preview
    img_preview = None
    try:
        img_preview = biskit_link + soup.find('div', {"class": "table_wrap"}).find('tbody').find('img')['src']
        res = requests.get(img_preview, headers=header)
        with open('./tmp/temp.png', 'wb') as f:
            f.write(res.content)

        with open('./temp.png', 'rb') as f:
            base64_str = base64.b64encode(f.read())

        img_preview_base64 = base64_str

        os.remove('./tmp/temp.png')
    except:
        pass

    text = ''
    for i in text_list:
        text += i.get_text() + " "

    if len(text) <= 100:
        result = text
    else:
        result = f'{text[:100]} ...[더보기]({biskit_link}/ptfol/imng/icmpNsbjtPgm/findIcmpNsbjtPgmInfo.do?encSddpbSeq={post_id})'

    title = soup.find('div', {"class": "tab_top_wrap"}).find('h4').text.strip()
    for i in soup.find('div', {"class": "table_wrap"}).find('tbody').find_all('tr'):
        if i.find('th', {"class": "first"}).text.strip() == "운영조직":
            org = i.find_all('td')[0].text.strip()
            author = i.find_all('td')[1].text.strip()

        elif i.find('th', {"class": "first"}).text.strip() == "프로그램 분류":
            category = i.find('td').text.strip()

        elif i.find('th', {"class": "first"}).text.strip() == "신청기간":
            period = i.find('td').text.strip()

        elif i.find('th', {"class": "first"}).text.strip() == "수료 인증서":
            mileage = int(i.find_all('td')[1].text.strip())
            
    post = (0, post_id, title, author, org, category, period, mileage)
    return post, img_preview_base64, result
# test
if __name__ == "__main__":
    print(asyncio.run(get_preview(34915)))



