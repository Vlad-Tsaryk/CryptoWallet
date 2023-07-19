from fastapi import Form, UploadFile, File, Depends, HTTPException

from src.dependencies import get_session, get_current_user
from src.ibay.schemas.product_schemas import ProductCreate
from src.users.models import User
from src.wallet.dependencies import is_user_wallet


async def product_form(
    title: str = Form(max_length=50),
    wallet_id: int = Form(gt=0),
    price: float = Form(gt=0),
    photo: UploadFile = File(...),
    user: User = Depends(get_current_user),
    session: Depends = Depends(get_session),
) -> ProductCreate:
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")
    wallet = await is_user_wallet(wallet_id, user, session=session)
    product = ProductCreate(title=title, wallet_id=wallet.id, price=price, photo=photo)
    return product
