import secrets
from typing import List

from eth_account import Account
from fastapi import Depends, APIRouter
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from src.dependencies import get_current_user
from src.users.models import User
from src.wallet import service as wallet_service
from src.wallet.dependencies import is_user_wallet
from src.wallet.http.balance import get_multiple_addresses_balance
from src.wallet.models import Wallet
from src.wallet.schemas.transaction_schemas import TransactionCreate
from src.wallet.schemas.wallet_schemas import (
    WalletCreate,
    WalletAddress,
    WalletPrivateKey,
    WalletResponse,
)
from src.wallet.service import (
    get_all_user_wallets,
    transaction_send,
    get_wallet_transactions,
    send_free_eth,
)

wallet_router = APIRouter()


@wallet_router.post("/create-wallet/", response_model=WalletAddress)
async def create_wallet(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    private_key = secrets.token_hex(32)
    acct = Account.from_key(private_key)
    address = acct.address
    logger.info(len(private_key))
    new_wallet = WalletCreate(
        address=address, user_id=current_user.id, private_key=private_key
    )
    await wallet_service.create_wallet(new_wallet, session)
    return new_wallet


@wallet_router.post("/import-wallet/", response_model=WalletAddress)
async def import_wallet(
    data: WalletPrivateKey,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    acct = Account.from_key(data.private_key)
    address = acct.address
    new_wallet = WalletCreate(
        address=address, user_id=current_user.id, private_key=data.private_key
    )
    await wallet_service.create_wallet(new_wallet, session)
    return new_wallet


@wallet_router.get("/my/", response_model=List[WalletResponse])
async def wallet_list(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    wallets = await get_all_user_wallets(user_id=current_user.id, session=session)
    logger.info(wallets)
    if wallets:
        addresses = ",".join([wallet.address for wallet in wallets])
        balances = await get_multiple_addresses_balance(addresses)
        decimal_places = 10**18
        for item in balances:
            item["balance"] = int(item["balance"]) / decimal_places
        logger.success(balances)
    return wallets


@wallet_router.post("/send-transaction/")
async def send_transaction(
    transaction: TransactionCreate,
    wallet: Wallet = Depends(is_user_wallet),
    session: AsyncSession = Depends(get_session),
):
    new_transaction = await transaction_send(
        wallet=wallet, transaction=transaction, session=session
    )
    return new_transaction


@wallet_router.post("/get-free-eth/")
async def get_free_eth(
    wallet: Wallet = Depends(is_user_wallet),
    session: AsyncSession = Depends(get_session),
):
    await send_free_eth(wallet=wallet, session=session)
    return True


@wallet_router.get("/get-wallet-transactions/")
async def watch_transactions(
    wallet: Wallet = Depends(is_user_wallet),
    session: AsyncSession = Depends(get_session),
):
    return await get_wallet_transactions(wallet, session)
