# import aiohttp

# async def getText(url : str, header : (dict | None) = None):
#     if header is None:
#         async with aiohttp.ClientSession (connector=aiohttp.TCPConnector(verify_ssl=False, limit_per_host=10), trust_env=True) as session:
#             async with session.get (url = url) as r :
#                 data = await r.text()
#             return data
#     async with aiohttp.ClientSession (connector=aiohttp.TCPConnector(verify_ssl=False, limit_per_host=10), headers=header, trust_env=True) as session:
#         async with session.get (url = url) as r :
#             data = await r.text()
#         return data

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getText(url: str, header: dict | None = None):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        response = session.get(url, headers=header, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None