import aiohttp

async def getText(url : str, header : (dict | None) = None):
    if header is None:
        async with aiohttp.ClientSession (connector=aiohttp.TCPConnector(verify_ssl=False, limit_per_host=10), trust_env=True) as session:
            async with session.get (url = url) as r :
                data = await r.text()
            return data
    async with aiohttp.ClientSession (connector=aiohttp.TCPConnector(verify_ssl=False, limit_per_host=10), headers=header, trust_env=True) as session:
        async with session.get (url = url) as r :
            data = await r.text()
        return data