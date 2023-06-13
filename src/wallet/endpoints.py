import secrets
from typing import Annotated, List

from eth_account import Account
from fastapi import Depends, APIRouter
from loguru import logger
from propan import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_broker, get_session
from src.dependencies import get_current_user
from src.users.models import User
from src.wallet import service as wallet_service
from src.wallet.schemas import (
    WalletCreate,
    WalletAddress,
    WalletPrivateKey,
    WalletResponse,
)
from src.wallet.service import get_all_user_wallets

wallet_router = APIRouter()


# @wallet_router.get("/test")
# async def hello_http(broker: Annotated[RabbitBroker, Depends(get_broker)]):
#     await broker.publish("Hello, Rabbit!", "test")
#     return "Hello, HTTP!"


@wallet_router.post("/create-wallet/", response_model=WalletAddress)
async def create_wallet(
    broker: Annotated[RabbitBroker, Depends(get_broker)],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    private_key = "0x" + secrets.token_hex(32)
    acct = Account.from_key(private_key)
    address = acct.address
    new_wallet = WalletCreate(address=address, user_id=current_user.id)
    await wallet_service.create_wallet(new_wallet, session)
    await broker.publish(address, "test")
    return new_wallet


@wallet_router.post("/import-wallet/", response_model=WalletAddress)
async def import_wallet(
    data: WalletPrivateKey,
    broker: Annotated[RabbitBroker, Depends(get_broker)],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    acct = Account.from_key(data.private_key)
    address = acct.address
    new_wallet = WalletCreate(address=address, user_id=current_user.id)
    await wallet_service.create_wallet(new_wallet, session)
    await broker.publish(address, "test")
    return new_wallet


@wallet_router.get("/my/", response_model=List[WalletResponse])
async def wallet_list(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    wallets = await get_all_user_wallets(user_id=current_user.id, session=session)
    logger.info(wallets)
    return wallets
    pass


# @wallet_router.event("wallet")
# async def test(m):
#     print(m)
