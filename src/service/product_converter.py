from src.dto.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ProductdetailResponse,
    ProductDescriptionResponse,
    ProductDescriptionListResponse,
)
from src.dao.models.product import Product
from fastapi.encoders import jsonable_encoder
from src.service.subproduct_converter import Converter as SubproductConverter


class Converter:
    def product_db_to_dto(product: Product):
        """
        Convert a product database model to a ProductResponse DTO.
        :param product: Product database model
        :return: ProductResponse DTO
        """
        product_dict = jsonable_encoder(product)
        return ProductResponse(**product_dict)

    def product_response_db_to_dto(product_response: dict):
        """
        Convert a product database response dictionary to a ProductListResponse DTO.
        :param product_response: Dictionary containing products
        :return: ProductListResponse DTO
        """
        return ProductListResponse(
            total_count=len(product_response.get("products", [])),
            products=[
                Converter.product_db_to_dto(product)
                for product in product_response.get("products", [])
            ],
        )

    def product_detail_db_to_dto(product: Product):
        """
        Convert a product database model to a ProductdetailResponse DTO.
        :param product: Product database model
        :return: ProductdetailResponse DTO
        """
        product_dict = jsonable_encoder(product)
        return ProductdetailResponse(**product_dict)

    def product_description_db_to_dto(product: Product):
        """
        Convert a product database model to a ProductDescriptionResponse DTO.
        :param product: Product database model
        :return: ProductDescriptionResponse DTO
        """
        return ProductDescriptionResponse(
            id=product.id,
            category_xref_id=product.category_xref_id,
            brand_id=product.brand_id,
            name=product.name,
            description=product.description,
            data=product.data,
            fabric=product.fabric,
            price=product.price,
            rating=product.rating,
            total_quantity=product.total_quantity,
            status=product.status,
            thumbnail_image=product.thumbnail_image,
            created_by=product.created_by,
            updated_by=product.updated_by,
            created_at=product.created_at,
            subproducts=[
                SubproductConverter.subproduct_size_dto_dto_db(subproduct)
                for subproduct in product.subproducts
            ],
        )

    def product_description_list_response_db_to_dto(product_response: dict):
        """
        Convert a product database response dictionary to a ProductDescriptionListResponse DTO.
        :param product_response: Dictionary containing products
        :return: ProductDescriptionListResponse DTO
        """
        return ProductDescriptionListResponse(
            total_count=len(product_response.get("products", [])),
            products=[
                Converter.product_description_db_to_dto(product)
                for product in product_response.get("products", [])
            ],
        )

    def product_create_dto_to_db(product_create: ProductCreate):
        """
        Convert a ProductCreate DTO to a product database model.
        :param product_create: ProductCreate DTO
        :return: product database model
        """
        return Product(
            id=product_create.id,
            category_xref_id=product_create.category_xref_id,
            brand_id=product_create.brand_id,
            name=product_create.name,
            description=product_create.description,
            data=product_create.data,
            fabric=product_create.fabric,
            price=product_create.price,
            rating=product_create.rating,
            total_quantity=product_create.total_quantity,
            status=product_create.status,
            thumbnail_image=product_create.thumbnail_image,
        )

    def product_update_dto_to_db(product_update: ProductUpdate, product: Product):
        """
        Convert a ProductUpdate DTO to a product database model (updating an existing product).
        :param product_update: ProductUpdate DTO
        :param product: Existing product database model
        :return: Updated product database model
        """
        for key, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        return product
