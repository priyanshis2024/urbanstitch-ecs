from uuid import UUID
from fastapi_camelcase import CamelModel
from pydantic import Field
from typing import List


class ColorResponse(CamelModel):
    color: List[str] = Field(..., title="Color", description="The color of the product")
