from src.dao.models.product import Category, Subcategory, CategoryXref
from src.dto.category import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    Categorydetails,
    CategoryDetailListResponse,
)
from src.dto.subcategory import Subcategorydetail
from typing import List
from fastapi.encoders import jsonable_encoder


class Converter:
    def category_create_dto_to_db(category_create: CategoryCreate):
        """
        Convert a CategoryCreate DTO to a Category database model.
        :param category_create: CategoryCreate DTO
        :return: category database model
        """
        return Category(id=category_create.id, name=category_create.name)

    def category_details_db_to_dto(category: Category):
        category_dict = jsonable_encoder(category)
        return Categorydetails(**category_dict)

    def category_response_db_to_dto(category_response: CategoryDetailListResponse):
        """
        Convert a category database model to a CategoryDetailListResponse DTO.
        :param category_response: Category database model
        :return: CategoryDetailListResponse DTO
        """
        return CategoryDetailListResponse(
            total_categories_count=len(category_response["categories"]),
            categories=[
                Converter.category_details_db_to_dto(category)
                for category in category_response["categories"]
            ],
        )

    def category_db_to_dto(category: Category, subcategories: List[Subcategory] = []):
        """
        Convert a category and subcategory database model to a Category and Subcategory DTO.
        :param category: Category database model
        :subcategories: Subcategory DTO
        :return: Category + Subcategory
        """
        category_dict = jsonable_encoder(category)

        category_dict["total_subcategories_count"] = len(subcategories)
        category_dict["subcategories"] = [
            Subcategorydetail(id=sub.id, name=sub.name, status=sub.status)
            for sub in subcategories
        ]
        return CategoryResponse(**category_dict)

    def category_update_dto_to_db(category_update: CategoryUpdate, category: Category):
        """
        Convert a CategoryUpdate DTO to a category database model (updating an existing category).
        :param Category_update: CategoryUpdate DTO
        :param category: Existing category database model
        :return: Updated category database model
        """
        for key, value in category_update.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        return category
