from fastapi import APIRouter

from app.services.content_based_service import (
    calculate_content_similarity
)

router = APIRouter(
    prefix="/content",
    tags=["Content Based Filtering"]
)

@router.get("/testing")
def testing_content():

    return calculate_content_similarity()