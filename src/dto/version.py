"""This module handles request body, response body and field validation"""

from fastapi_camelcase import CamelModel
from pydantic import Field


class VersionResponse(CamelModel):
    version: float = Field(..., title="Version", description="Version")
