from datetime import datetime

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

from config.config import settings
from src.wallet.models import Wallet, Transaction
from src.wallet.schemas.transaction_schemas import TransactionCreate
from src.wallet.schemas.wallet_schemas import WalletCreate, WalletAddress


async def create_wallet(wallet: WalletCreate, session: AsyncSession) -> Wallet:
    new_wallet = Wallet(
        address=wallet.address,
        user_id=wallet.user_id,
        private_key=wallet.private_key,
        currency_id=2,
    )
    if await valid_address(new_wallet, session):
        raise HTTPException(status_code=400, detail="Address is already taken.")
    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)
    logger.success(
        f"Wallet {wallet.address} successfully create for user id-{wallet.user_id}"
    )
    return new_wallet


async def valid_address(wallet: WalletCreate, session: AsyncSession) -> Wallet | None:
    result = await session.execute(
        select(Wallet).where(
            Wallet.address == wallet.address and Wallet.user_id == wallet.user_id
        )
    )
    return result.scalar_one_or_none()


async def get_wallet_by_address(
    address: WalletAddress, session: AsyncSession
) -> Wallet | None:
    result = await session.execute(select(Wallet).where(Wallet.address == address))
    return result.scalar_one_or_none()


async def get_wallet(wallet_id: int, session: AsyncSession) -> Wallet | None:
    wallet = await session.get(Wallet, wallet_id)
    return wallet


async def get_all_user_wallets(user_id: int, session: AsyncSession):
    smtp = (
        select(Wallet)
        .where(Wallet.user_id == user_id)
        .options(joinedload(Wallet.currency))
    )
    result = await session.scalars(smtp)
    return result.all()


async def create_transaction(
    tx_hex: str, wallet: Wallet, transaction: TransactionCreate, session: AsyncSession
) -> Transaction:
    new_transaction = Transaction(
        tnx_hash=tx_hex,
        from_address=wallet.address,
        to_address=transaction.to_address,
        value=transaction.value,
        age=datetime.now(),
        tnx_fee=0,
    )
    session.add(new_transaction)
    await session.commit()
    return new_transaction


async def transaction_send(
    wallet: Wallet, transaction: TransactionCreate, session: AsyncSession
) -> Transaction:
    w3 = Web3(Web3.HTTPProvider(settings.QUICK_NODE_URL))
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(wallet.private_key))
    tx_hash = w3.eth.send_transaction(
        {
            "from": wallet.address,
            "value": w3.to_wei(transaction.value, "ether"),
            "to": transaction.to_address,
        }
    )
    tx_hex = w3.to_hex(tx_hash)
    logger.info(tx_hex)
    new_transaction = await create_transaction(tx_hex, wallet, transaction, session)
    return new_transaction


async def get_wallet_transactions(wallet: Wallet, session: AsyncSession):
    smtp = select(Transaction).where(
        or_(
            Transaction.from_address == wallet.address,
            Transaction.to_address == wallet.address,
        )
    )
    result = await session.scalars(smtp)
    return result.all()
