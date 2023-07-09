from functools import lru_cache

from web3 import Web3

from config.config import settings


@lru_cache()
def get_web3() -> Web3:
    return Web3(Web3.HTTPProvider(settings.QUICK_NODE_URL))
