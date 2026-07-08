from fastapi import APIRouter

from app.services.matrix_service import (
    build_user_product_matrix
)

router = APIRouter(
    prefix="/matrix",
    tags=["Matrix"]
)

@router.get("/testing")
def testing_matrix():

    matrix = build_user_product_matrix()

    return {
        "status": True,
        "total_users": len(matrix.index),
        "total_products": len(matrix.columns),
        "users": matrix.index.tolist(),
        "products": matrix.columns.tolist(),
        "matrix": matrix.values.tolist()
    }