"""This module handles request body, response body and field validation"""

from typing import Optional, List
from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID


class SearchPayload(CamelModel):
    search: Optional[str] = Field(
        title="Search query", description="Search query string"
    )
    sort_order: Optional[str] = Field(
        default="desc", title="Sorting order", description="Sorting order for results"
    )
    sort_by: Optional[str] = Field(
        default="created_at", title="Sort by", description="Field to sort results by"
    )
    limit: Optional[int] = Field(
        default=10, title="Limit", description="Maximum number of results to return"
    )
    offset: Optional[int] = Field(
        default=0, title="Offset", description="Offset for paginated results"
    )


class SearchFilter(CamelModel):
    min_rating: Optional[int] = Field(
        None, title="minimum rating", description="minimum rating value"
    )
    max_rating: Optional[int] = Field(
        None, title="maximum rating", description="maximum rating value"
    )
    min_price: Optional[int] = Field(
        None, title="minimum price", description="minimum price value"
    )
    max_price: Optional[int] = Field(
        None, title="maximum price", description="maximum price value"
    )
    color: Optional[List[str]] = Field(None, title="Color", description="Color value")
    size: Optional[List[UUID]] = Field(None, title="Size", description="Size")
    category: Optional[UUID] = Field(
        None, title="Category", description="Category of the product"
    )
    subcategory: Optional[List[UUID]] = Field(
        None, title="Subcategory", description="Subcategory of the product"
    )
    status: Optional[List[int]] = Field(
        None, title="Status", description="Product stock checking status "
    )


class ProductSearchPayload(CamelModel):
    search: Optional[str] = Field(
        title="Search query", description="Search query string"
    )
    sort_order: Optional[str] = Field(
        default="desc", title="Sorting order", description="Sorting order for results"
    )
    sort_by: Optional[str] = Field(
        default="created_at", title="Sort by", description="Field to sort results by"
    )

    limit: Optional[int] = Field(
        default=10, title="Limit", description="Maximum number of results to return"
    )
    offset: Optional[int] = Field(
        default=0, title="Offset", description="Offset for paginated results"
    )
    filter: Optional[SearchFilter] = Field(
        None, title="Filter", description="Filter criteria for searching product."
    )


class SubproductSearchPayload(CamelModel):
    search: Optional[str] = Field(
        title="Search query", description="Search query string"
    )
    sort_order: Optional[str] = Field(
        default="desc", title="Sorting order", description="Sorting order for results"
    )
    sort_by: Optional[str] = Field(
        default="created_at", title="Sort by", description="Field to sort results by"
    )

    limit: Optional[int] = Field(
        default=10, title="Limit", description="Maximum number of results to return"
    )
    offset: Optional[int] = Field(
        default=0, title="Offset", description="Offset for paginated results"
    )
    filter: Optional[SearchFilter] = Field(
        None, title="Filter", description="Filter criteria for searching product."
    )


class Jsonbody(CamelModel):
    search: Optional[str] = Field(
        default="", title="Search query", description="Search query string"
    )
    sort_order: Optional[str] = Field(
        default="desc", title="Sorting order", description="Sorting order for results"
    )
    sort_by: Optional[str] = Field(
        default="created_at", title="Sort by", description="Field to sort results by"
    )
    limit: Optional[int] = Field(
        default=10, title="Limit", description="Maximum number of results to return"
    )
    offset: Optional[int] = Field(
        default=0, title="Offset", description="Offset for paginated results"
    )


class Json_pagination(CamelModel):
    search: Optional[str] = Field(
        default="", title="Search query", description="Search query string"
    )
    limit: Optional[int] = Field(
        default=10, title="Limit", description="Maximum number of results to return"
    )
    offset: Optional[int] = Field(
        default=0, title="Offset", description="Offset for paginated results"
    )
