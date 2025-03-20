from hexbytes import HexBytes

from fake_useragent import UserAgent
from eth_typing import ChecksumAddress, HexStr
from eth_account.signers.local import LocalAccount
from web3.exceptions import Web3Exception
from web3 import AsyncWeb3


class Client:
    private_key: str
    rpc: str
    proxy: str | None
    w3: AsyncWeb3
    account: LocalAccount

    def __init__(self, private_key: str, rpc: str, proxy: str | None = None):
        self.private_key = private_key
        self.rpc = rpc
        self.proxy = proxy

        if self.proxy:
            if 'http' not in self.proxy:
                self.proxy = f'http://{self.proxy}'

        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': UserAgent().chrome
        }

        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(
            endpoint_uri=rpc,
            request_kwargs={'proxy': self.proxy, 'headers': self.headers}
        ))
        self.account = self.w3.eth.account.from_key(private_key)

        self.random_account = self.w3.eth.account.create()

    async def send_transaction(
            self,
            to: str | ChecksumAddress,
            data: HexStr | None = None,
            from_: str | ChecksumAddress | None = None,
            increase_gas: float = 1,
            value: int | None = None,
    ) -> HexBytes | None:
        if not from_:
            from_ = self.account.address

        tx_params = {
            'chainId': await self.w3.eth.chain_id,
            'nonce': await self.w3.eth.get_transaction_count(self.account.address),
            'from': AsyncWeb3.to_checksum_address(from_),
            'to': AsyncWeb3.to_checksum_address(to),
            'gasPrice': await self.w3.eth.gas_price
        }

        if data:
            tx_params['data'] = data
        if value:
            tx_params['value'] = value

        gas = await self.w3.eth.estimate_gas(tx_params)
        tx_params['gas'] = gas * increase_gas

        sign = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        return await self.w3.eth.send_raw_transaction(sign.rawTransaction)

    async def verif_tx(self, tx_hash: HexBytes, timeout: int = 200) -> str:
        data = await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        if data.get('status') == 1:
            return tx_hash.hex()
        raise Web3Exception(f'transaction failed {data["transactionHash"].hex()}')
    