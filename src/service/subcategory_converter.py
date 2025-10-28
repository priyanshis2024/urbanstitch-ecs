from src.dao.models.product import Subcategory
from src.dto.subcategory import (
    SubcategoryCreate,
    SubcategoryUpdate,
    Subcategorydetails,
    SubcategoryDetailListResponse,
    Subcategorydetail,
)
from fastapi.encoders import jsonable_encoder


class Converter:
    def subcategory_create_dto_to_db(subcategory_create: SubcategoryCreate):
        """
        Convert a SubcategoryCreate DTO to a subcategory database model.
        :param subcategory_create: SubcategoryCreate DTO
        :return: subcategory database model
        """
        return Subcategory(id=subcategory_create.id, name=subcategory_create.name)

    def subcategory_update_dto_to_db(
        subcategory_update: SubcategoryUpdate, subcategory: Subcategory
    ):
        """
        Convert a SubcategoryUpdate DTO to a subcategory database model
        :param subcategory_update: SubcategoryUpdate DTO
        :param subcategory: Existing subcategory database model
        :return: Updated subcategory database model
        """
        for key, value in subcategory_update.model_dump(exclude_unset=True).items():
            setattr(subcategory, key, value)
        return subcategory

    def subcategory_db_to_dto(subcategory: Subcategory):
        """
        Convert a subcategory database model to a Subcategory.
        :param subcategory: Subcategory database model
        :return: Subcategory
        """
        subcategory_dict = jsonable_encoder(subcategory)
        return Subcategory(**subcategory_dict)

    def subcategory_details_db_to_dto(subcategory: Subcategory):
        subcategory_dict = jsonable_encoder(subcategory)
        return Subcategorydetails(**subcategory_dict)

    def subcategory_response_db_to_dto(
        subcategory_response: SubcategoryDetailListResponse,
    ):
        """
        Convert a subcategory database model to a SubcategoryDetailListResponse DTO.
        :param subcategory_response: Subcategory database model
        :return: SubcategoryDetailListResponse DTO
        """
        return SubcategoryDetailListResponse(
            total_subcategories_count=len(subcategory_response["subcategories"]),
            subcategories=[
                Converter.subcategory_details_db_to_dto(subcategory)
                for subcategory in subcategory_response["subcategories"]
            ],
        )

    def subcategory_detail_db_to_dto(subcategory: Subcategory):
        subcategory_dict = jsonable_encoder(subcategory)
        return Subcategorydetail(**subcategory_dict)
