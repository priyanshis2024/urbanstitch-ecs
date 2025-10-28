"""This module handles request body, response body and field validation"""

from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID


class CategoryXrefCreate(CamelModel):
    category_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    subcategory_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    subcategories_type: str = Field(
        Field(
            ...,
            title="Subcategories type",
            description="The subcategory type which identify the type of the subcategory",
        )
    )


class CategoryXrefResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category_xref"
    )
    category_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    subcategory_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    subcategories_type: str = Field(
        Field(
            ...,
            title="Subcategories type",
            description="The subcategory type which identify the type of the subcategory",
        )
    )
