from fastapi import APIRouter

from app.services.collaborative_service import (
    calculate_product_similarity
)

router = APIRouter(
    prefix="/collaborative",
    tags=["Collaborative Filtering"]
)

@router.get("/testing")
def testing_cf():

    return calculate_product_similarity()