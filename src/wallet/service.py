from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.wallet.models import Wallet
from src.wallet.schemas import WalletCreate, WalletAddress


async def create_wallet(wallet: WalletCreate, session: AsyncSession) -> Wallet:
    new_wallet = Wallet(address=wallet.address, user_id=wallet.user_id, currency_id=2)
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


async def get_all_user_wallets(user_id: int, session: AsyncSession):
    smtp = (
        select(Wallet)
        .where(Wallet.user_id == user_id)
        .options(joinedload(Wallet.currency))
    )
    result = await session.scalars(smtp)
    return result.all()
