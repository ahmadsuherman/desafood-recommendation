from fastapi import APIRouter

from app.services.interaction_service import (
    get_interaction_data
)

router = APIRouter(
    prefix="/interaction",
    tags=["Interaction"]
)

@router.get("/testing")
def testing_interactions():

    return {
        "status": True,
        "data": get_interaction_data()
    }