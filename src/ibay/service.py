from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.ibay.models import Product, Order
from src.ibay.schemas.product_schemas import ProductCreate
from src.users.models import User
from src.wallet.models import Wallet
from src.wallet.schemas.transaction_schemas import TransactionCreate
from src.wallet.service import transaction_send


async def product_get_by_id(product_id: int, session: AsyncSession) -> Product | None:
    result = await session.execute(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.wallet))
    )
    return result.scalar_one_or_none()


async def product_create(product: ProductCreate, session: AsyncSession) -> Product:
    product_data: dict[str, Any] = product.dict()
    new_product: Product = Product(**product_data)
    session.add(new_product)
    await session.commit()
    return new_product


async def order_create(product_id: int, wallet: Wallet, session: AsyncSession):
    product = await product_get_by_id(product_id, session)
    transaction = TransactionCreate(
        to_address=product.wallet.address, value=product.price
    )
    new_transaction = await transaction_send(wallet, transaction, session)
    new_order = Order(
        user_id=wallet.user_id, product_id=product_id, tnx_hash=new_transaction.tnx_hash
    )
    session.add(new_order)
    await session.commit()
    return new_order


async def product_list(session: AsyncSession):
    result = await session.scalars(select(Product))
    return result.all()


async def order_list(user: User, session: AsyncSession):
    result = await session.scalars(select(Order).where(Order.user_id == user.id))
    return result.all()
