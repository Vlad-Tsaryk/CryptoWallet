from fastapi import APIRouter, Depends

from src.dependencies import get_session
from src.ibay.dependencies import product_form
from src.ibay.schemas.product_schemas import ProductCreate
from src.ibay.service import product_create

ibay_router = APIRouter()


@ibay_router.post("/create-product/")
async def create_product(
    product: ProductCreate = Depends(product_form),
    session: Depends = Depends(get_session),
):
    new_product = await product_create(product, session)
    return new_product
