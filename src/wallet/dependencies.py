from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session, get_current_user
from src.users.models import User
from src.wallet.schemas.transaction_schemas import TransactionCreate


async def is_user_wallet(
    transaction: TransactionCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> User:
    # res = await get_wallet_by_address(transaction.from_address, session)
    # if res:
    #     if res.user_id == user.id:
    #         return user
    #     else:
    #         raise HTTPException(status_code=400, detail="It's not your wallet!")
    # raise HTTPException(status_code=404, detail="Wallet not found!")
    return user
