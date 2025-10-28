"""Service Status Endpoint"""

from http import HTTPStatus

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Healthcheck module"])


@router.get("/healthcheck", status_code=HTTPStatus.OK)
def health_check():
    """returns the service status"""
    return HTTPStatus.OK
