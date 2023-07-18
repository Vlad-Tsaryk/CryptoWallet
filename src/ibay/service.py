from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.ibay.models import Product
from src.ibay.schemas.product_schemas import ProductCreate


async def product_create(product: ProductCreate, session: AsyncSession) -> Product:
    product_data: dict[str, Any] = product.dict()
    new_product: Product = Product(**product_data)
    session.add(new_product)
    await session.commit()
    return new_product
