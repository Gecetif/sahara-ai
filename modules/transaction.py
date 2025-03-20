import random

from core.client import Client
from utils.logger import get_logger


logger = get_logger()


async def transaction(count, private_key, proxy):
    client = Client(
        private_key=private_key,
        proxy=proxy,
        rpc='https://testnet.saharalabs.ai',
    )

    amount = int(random.uniform(0.0001, 0.001) * 10 ** 18)

    tx_hash = None
    try:
        tx_hash = await client.send_transaction(
            to=client.random_account.address,
            value=amount,
        )
    except ValueError:
        logger.warning(f'[{count}] {client.account.address} | Не хватает баланса для транзакции')

    if tx_hash:
        try:
            await client.verif_tx(tx_hash=tx_hash)
            logger.success(f'[{count}] {client.account.address} | tx_hash - {tx_hash.hex()} | Сделал трансфер на рандомный кошелёк')
        except Exception as err:
            logger.error(f'[{count}] {client.account.address} | Транзакция зафейлилась. Ошибка - {err}')
