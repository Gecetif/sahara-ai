import asyncio
import random

from modules import faucet, transaction, claim
from .semaphore import semaphore
from .client import Client
from utils.logger import get_logger
import settings


logger = get_logger()


async def process_wallets(data, count, private_key, proxy):
    async with semaphore:

        client = Client(
            private_key=private_key,
            proxy=proxy,
            rpc='https://eth.llamarpc.com'
        )
        logger.info(f'Starting [{count}] {client.account.address} | {proxy}')
        faucet.get_captcha(data)

        if settings.Faucet:
            await faucet.faucet(count, proxy, client)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] sleep between actions - {sleep_time} seconds')
            await asyncio.sleep(sleep_time)

        if settings.Transaction:
            await transaction.transaction(count, private_key, proxy)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] sleep between actions - {sleep_time} seconds')
            await asyncio.sleep(sleep_time)

        if settings.Claim:
            await claim.claim(count, private_key, proxy, client)

    sleep_time = random.randint(settings.sleep_wallets[0], settings.sleep_wallets[1])
    logger.debug(f'Sleep between wallets - {sleep_time} seconds')
    await asyncio.sleep(sleep_time)
