"""Service Version Endoint"""

from http import HTTPStatus

from fastapi import APIRouter
from src.version import SERVICE_APP_VERSION
from src.dto.version import VersionResponse

router = APIRouter(tags=["Version module"])


@router.get("/version", status_code=HTTPStatus.OK, response_model=VersionResponse)
def get_version():
    """returns the service version"""
    return {"version": SERVICE_APP_VERSION}
