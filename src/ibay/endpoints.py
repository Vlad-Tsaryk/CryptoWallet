from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session, get_current_user
from src.ibay.dependencies import product_form
from src.ibay.schemas.product_schemas import ProductCreate, ProductResponse
from src.ibay.service import product_create, order_create, product_list, order_list
from src.users.models import User
from src.wallet.dependencies import is_user_wallet

ibay_router = APIRouter()


@ibay_router.post("/create-product/")
async def create_product(
    product: ProductCreate = Depends(product_form),
    session: Depends = Depends(get_session),
):
    new_product = await product_create(product, session)
    return new_product


@ibay_router.post("/buy-product/")
async def buy_product(
    product_id: int,
    wallet: Depends = Depends(is_user_wallet),
    session: Depends = Depends(get_session),
):
    new_order = await order_create(product_id, wallet, session)
    return new_order


@ibay_router.get("/products/", response_model=List[ProductResponse])
async def get_product_list(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    products = await product_list(session)
    return products


@ibay_router.get("/orders/")
async def get_order_list(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    orders = await order_list(user, session)
    return orders
