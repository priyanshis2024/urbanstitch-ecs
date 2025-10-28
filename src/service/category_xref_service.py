from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.dao.category_xref import category_xref_dao
from src.service.category_xref_converter import Converter
from src.exceptions.category_xref import CategoryXrefSubcategoryNotFound
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class CategoryXrefService:
    async def get_all_subcategories_by_category_id(
        self, category_id: UUID, db_obj: AsyncSession
    ):
        category_xrefs = (
            await category_xref_dao.get_subcategories_from_category_xref_by_category_id(
                db_obj, category_id
            )
        )

        if not category_xrefs:
            logger.error(
                f"Category with id '{category_id}' does not have subcategories in the system."
            )
            raise CategoryXrefSubcategoryNotFound(
                category_id=category_id,
                message=ErrorMessage.CATEGORY_XREF_SUBCATEGORY_NOT_FOUND.format(
                    category_id=category_id
                ),
            )
        return Converter.category_xref_response_db_to_dto(category_xrefs)


category_xref_service = CategoryXrefService()
