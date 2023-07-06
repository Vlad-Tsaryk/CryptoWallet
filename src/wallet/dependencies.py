from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session, get_current_user
from src.users.models import User
from src.wallet.models import Wallet
from src.wallet.service import get_wallet


async def is_user_wallet(
    wallet_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Wallet:
    wallet = await get_wallet(wallet_id=wallet_id, session=session)
    if wallet:
        if wallet.user_id == user.id:
            return wallet
        else:
            raise HTTPException(status_code=400, detail="It's not your wallet!")
    raise HTTPException(status_code=404, detail="Wallet not found!")
