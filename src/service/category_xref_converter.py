from src.dao.models.product import CategoryXref, Subcategory
from src.dto.category_xref import CategoryXrefResponse, CategoryXrefCreate
from fastapi.encoders import jsonable_encoder
from typing import List, Tuple
from src.dto.subcategory import XrefSubcategoryResponse, Subcategorydetail
from src.dao.models.product import CategoryXref
from src.service.subcategory_converter import Converter as subcategory_converter


class Converter:
    def category_xref_create_dto_to_db(category_xref_create: CategoryXrefCreate):
        """
        Convert a CategoryXrefCreate DTO to a Category xref database model.
        :param category_xref_create: CategoryXrefCreate DTO
        :return: category xref database model
        """
        return CategoryXref(
            category_id=category_xref_create.category_id,
            subcategory_id=category_xref_create.subcategory_id,
            subcategories_type=category_xref_create.subcategories_type,
        )

    def category_xref_db_to_dto(category_xref: CategoryXref):
        """
        Convert a category xref database model to a Categoryxref  DTO.
        :param category: Category database model
        :return: Category xref response
        """
        category_xref_dict = jsonable_encoder(category_xref)
        return CategoryXrefResponse(**category_xref_dict)

    def category_xref_response_db_to_dto(
        category_xrefs: List[Tuple[CategoryXref, Subcategory]],
    ):
        subcategory_details_by_type = {}

        for xref, subcategory in category_xrefs:
            subcategory_dto = subcategory_converter.subcategory_detail_db_to_dto(
                subcategory
            )
            if xref.subcategories_type not in subcategory_details_by_type:
                subcategory_details_by_type[xref.subcategories_type] = []
            subcategory_details_by_type[xref.subcategories_type].append(subcategory_dto)

        return [
            XrefSubcategoryResponse(
                subcategories_type=sub_type,
                total_subcategories_count=len(subcategories),
                subcategories=subcategories,
            )
            for sub_type, subcategories in subcategory_details_by_type.items()
        ]
