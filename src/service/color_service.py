from src.service.size_converter import Converter
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.color_converter import Converter
from src.dao.color import color_dao
from uuid import UUID
from typing import Optional, List
from src.dto.common import Json_pagination


class ColorService:
    async def get_all_distinct_color(
        self,
        db_obj: AsyncSession,
        json: Json_pagination,
        category_id: Optional[UUID] = None,
        subcategory_id: Optional[List[UUID]] = None,
    ):
        """
        Service function to fetch distinct colors.
        """
        response = await color_dao.all_distinct_color(
            db_obj=db_obj,
            search=json.search,
            limit=json.limit,
            offset=json.offset,
            category_id=category_id,
            subcategory_id=subcategory_id,
        )
        return Converter.color_db_to_dto(response)


color_service = ColorService()
