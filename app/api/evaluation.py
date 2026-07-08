from fastapi import APIRouter

from app.services.evaluation_service import (
    evaluate_model
)

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.get("/metrics")
def evaluation_metrics():

    return evaluate_model()