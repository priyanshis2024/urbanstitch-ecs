from src.dto.subproduct import (
    SubproductCreate,
    SubproductUpdate,
    SubproductResponse,
    SubproductDetailResponse,
    SubproductListingResponse,
    SubproductDetailListResponse,
    SubproductSizeResponse,
)
from fastapi.encoders import jsonable_encoder
from src.dao.models.product import Subproduct


class Converter:
    def subproduct_db_to_dto(subproduct_response: SubproductResponse):
        """
        Convert a Subproduct database model to a SubproductResponse DTO.
        :param subproduct: Subproduct database model
        :return: SubproductResponse DTO
        """
        subproduct_dict = jsonable_encoder(subproduct_response)
        return SubproductResponse(**subproduct_dict)

    def subproduct_listing_db_to_dto(subproduct: Subproduct):
        """
        Convert a Subproduct DB model to SubproductDetailResponse DTO.
        """
        return SubproductListingResponse(
            id=subproduct.id,
            product_id=subproduct.products.id,
            category_xref_id=subproduct.products.category_xref_id,
            category_id=subproduct.products.category_xrefs.category_id,
            subcategory_id=subproduct.products.category_xrefs.subcategory_id,
            brand_id=subproduct.products.brand_id,
            name=subproduct.products.name,
            description=subproduct.products.description,
            price=subproduct.price,
            rating=subproduct.products.rating,
            color=subproduct.color,
            quantity=subproduct.quantity,
            images=(
                subproduct.images.split(",")
                if isinstance(subproduct.images, str)
                else subproduct.images
            ),
        )

    def subproduct_detail_db_to_dto(subproduct: Subproduct):
        """
        Convert a Subproduct DB model to SubproductDetailResponse DTO.
        """
        size = subproduct.sizes

        return SubproductDetailResponse(
            id=subproduct.id,
            product_id=subproduct.products.id,
            category_xref_id=subproduct.products.category_xref_id,
            category_id=subproduct.products.category_xrefs.category_id,
            subcategory_id=subproduct.products.category_xrefs.subcategory_id,
            brand_id=subproduct.products.brand_id,
            size_id=subproduct.size_id,
            size=size.size,
            name=subproduct.products.name,
            description=subproduct.products.description,
            data=subproduct.products.data,
            fabric=subproduct.products.fabric,
            price=subproduct.price,
            rating=subproduct.products.rating,
            color=subproduct.color,
            quantity=subproduct.quantity,
            images=(
                subproduct.images.split(",")
                if isinstance(subproduct.images, str)
                else subproduct.images
            ),
        )

    def subproduct_detail_response_db_to_dto(subproduct_response: dict):
        """
        Convert a subproduct database response dictionary to a DTO.
        """
        return SubproductDetailListResponse(
            total_subproduct_count=len(subproduct_response.get("subproducts", [])),
            subproducts=[
                Converter.subproduct_listing_db_to_dto(subproduct)
                for subproduct in subproduct_response.get("subproducts", [])
            ],
        )

    def subproduct_create_dto_to_db(subproduct_create: SubproductCreate) -> Subproduct:
        """
        Convert a SubproductCreate DTO to a Subproduct database model.
        :param subproduct_create: SubproductCreate DTO
        :return: Subproduct database model
        """
        return Subproduct(
            id=subproduct_create.id,
            product_id=subproduct_create.product_id,
            size_id=subproduct_create.size_id,
            price=subproduct_create.price,
            color=subproduct_create.color,
            quantity=subproduct_create.quantity,
            images=subproduct_create.images,
            status=subproduct_create.status,
        )

    def subproduct_update_dto_to_db(
        subproduct_update: SubproductUpdate, subproduct: Subproduct
    ):
        """
        Convert a SubproductUpdate DTO to a Subproduct database model (updating an existing Subproduct).
        :param subproduct_update: SubproductUpdate DTO
        :param subproduct: Existing Subproduct database model
        :return: Updated Subproduct database model
        """
        for key, value in subproduct_update.model_dump(exclude_unset=True).items():
            setattr(subproduct, key, value)
        return subproduct

    def subproduct_size_dto_dto_db(subproduct: Subproduct):
        """
        Convert a SubproductSize DTO to a Subproduct database model.
        :param subproduct: SubproductSize DTO
        :return: Subproduct database model
        """
        size = subproduct.sizes

        return SubproductSizeResponse(
            id=subproduct.id,
            product_id=subproduct.product_id,
            size_id=subproduct.size_id,
            size=size.size,
            data=size.data,
            price=subproduct.price,
            color=subproduct.color,
            quantity=subproduct.quantity,
            images=subproduct.images,
            status=subproduct.status,
            created_by=subproduct.created_by,
            updated_by=subproduct.updated_by,
            created_at=subproduct.created_at,
            updated_at=subproduct.updated_at,
        )
