import logging
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from authx import RequestToken

from schemas.product import ProductCreate, ProductRead, ProductUpdate
from services.products import ProductService, get_product_service
from services.pdf_generator import generate_products_report
from utils.security import security

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    path="/report",
    summary="Generate and download PDF report of products",
    tags=["Products"]
)
async def get_products_report(product_service: ProductService = Depends(get_product_service)):
    try:
        products = await product_service.get_all()
        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found to generate report"
            )

        # Генеруємо PDF файл за допомогою сервісу
        filepath = generate_products_report("products_report.pdf", products)

        # Повертаємо його користувачу як файл для завантаження
        return FileResponse(
            path=filepath,
            filename="products_report.pdf",
            media_type="application/pdf"
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to generate report")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate report",
        ) from exc


@router.get(
    path="/",
    response_model=list[ProductRead],
    tags=["Products"],
)
async def get_products(product_service: ProductService = Depends(get_product_service)):
    try:
        return await product_service.get_all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get products")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get products",
        ) from exc


@router.get(
    path="/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
async def get_product(
        product_id: int,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        product = await product_service.get_by_id(product_id=product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return product

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get product with id %d", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product",
        ) from exc


@router.post(
    path="/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
)
async def create_product(
        product_data: ProductCreate,
        product_service: ProductService = Depends(get_product_service),
        token: RequestToken = Depends(security.access_token_required)  # Захищено токеном
):
    try:
        return await product_service.create(data=product_data)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create product")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        ) from exc


@router.put(
    path="/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
async def update_product(
        product_id: int,
        product_update: ProductUpdate,
        product_service: ProductService = Depends(get_product_service),
):
    try:
        product = await product_service.update(product_id=product_id, data=product_update)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return product

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product",
        ) from exc


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
)
async def delete_product(
        product_id: int,
        product_service: ProductService = Depends(get_product_service),
        token: RequestToken = Depends(security.access_token_required)  # Захищено токеном
):
    # Рольова модель (RBAC): Перевірка, чи користувач є адміністратором
    user_role = token.custom_claims.get("role")
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Only administrators can delete products"
        )

    try:
        deleted = await product_service.delete(product_id=product_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return None

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product",
        ) from exc