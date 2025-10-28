from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import PRODUCT
from src.dao.db import get_db
from src.dto.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductUpdateStatus,
    ProductdetailResponse,
    ProductDescriptionResponse,
    ProductDescriptionListResponse,
    ProductBulkResponse,
)
from src.service.product_service import product_service
from src.utils.utils import get_current_user
from src.dto.common import ProductSearchPayload
from typing import List
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Product module"])


@router.get(PRODUCT + "/{product_id}", response_model=ProductDescriptionResponse)
async def get_product_by_id(product_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching product details with ID: {product_id}")
    result = await product_service.get_product_by_id(
        product_id=product_id, db_obj=db_obj
    )
    logger.info(
        f"Product details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(PRODUCT, response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    request_payload = product.dict()
    logger.info(f"Creating product details with the payload: {request_payload}")
    result = await product_service.create_product_details(
        product_create=product, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Product details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(PRODUCT + "/bulk", response_model=ProductBulkResponse)
async def create_bulk_product(
    products: List[ProductCreate],
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint creates products and their subproducts in bulk.
    """
    request_payload = products.dict()
    logger.info(f"Creating product details in bulk with the payload: {request_payload}")
    result = await product_service.create_bulk_product_details(
        products_create=products, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"All product details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(PRODUCT + "/{product_id}", response_model=ProductdetailResponse)
async def update_product(
    product_id: UUID,
    product_update: ProductUpdate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing product details in the database.
    """
    request_payload = product_update.dict()
    logger.info(
        f"Updating product details for ID {product_id} with the payload: {request_payload}"
    )
    result = await product_service.update_existing_product(
        product_id=product_id,
        product_update=product_update,
        user_id=user_id,
        db_obj=db_obj,
    )
    logger.info(
        f"Product details updated successfully for {product_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(PRODUCT + "/{product_id}")
async def delete_product(
    product_id: UUID,
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """
    API endpoint to delete a product or a subproduct.

    - If subproduct_id is **not** provided → Deletes the entire product and its subproducts.
    - If subproduct_id is provided → Deletes only the specified subproduct.
    - The user-id header is required for authentication and must belong to an admin.
    """
    logger.info(f"Deleting product details for ID: {product_id}")
    result = await product_service.delete_existing_product(
        product_id=product_id,
        user_id=user_id,
        db_obj=db_obj,
    )
    logger.info(f"Product details deleted successfully.")
    return result


@router.post(PRODUCT + "/search", response_model=ProductDescriptionListResponse)
async def get_all_products(
    payload: ProductSearchPayload,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint fetches products by applying pagination, searching, and sorting.
    """
    logger.info("Fetching all product details.")
    result = await product_service.get_all_products(payload=payload, db_obj=db_obj)
    logger.info(
        f"All product details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.patch(PRODUCT + "/{product_id}" + "/status", response_model=ProductResponse)
async def change_product_status(
    product_id: UUID,
    product_update_status: ProductUpdateStatus,
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """
    This endpoint updates an existing product's status in the database.
    """
    payload = product_update_status.dict()
    logger.info(
        f"Updating product status for ID {product_id} with the payload: {payload}"
    )
    result = await product_service.change_product_status(
        product_id=product_id,
        user_id=user_id,
        product_update_status=product_update_status,
        db_obj=db_obj,
    )
    logger.info(
        f"Product status updated successfully for {product_id} with the response {jsonable_encoder(result)}"
    )
    return result
