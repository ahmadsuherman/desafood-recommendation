from fastapi import APIRouter

from app.services.collaborative_service import (
    get_collaborative_recommendations
)

from app.services.content_based_service import (
    calculate_content_similarity,
    get_content_recommendations
)

from app.services.hybrid_service import (
    get_hybrid_recommendations,
    generate_hybrid_recommendation,
    generate_all_recommendations
)

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)

@router.get("/collaborative/{user_id}")
def collaborative_recommendation(
    user_id: str
):

    recommendations = (
        get_collaborative_recommendations(
            user_id
        )
    )

    return {
        "user_id": user_id,
        "recommendations": [
            {
                "product_id": product_id,
                "score": score
            }
            for product_id, score
            in recommendations
        ]
    }


@router.get("/content/{user_id}")
def content_recommendation(
    user_id: str
):

    recommendations = (
        get_content_recommendations(
            user_id
        )
    )

    return {
        "user_id": user_id,
        "recommendations": [
            {
                "product_id": product_id,
                "score": score
            }
            for product_id, score
            in recommendations
        ]
    }

@router.get("/hybrid/{user_id}")
def hybrid_recommendation(
    user_id: str
):

    recommendations = (
        get_hybrid_recommendations(
            user_id
        )
    )

    return {
        "user_id": user_id,
        "recommendations": [
            {
                "product_id": product_id,
                "score": score
            }
            for product_id, score
            in recommendations
        ]
    }

@router.post("/generate/{user_id}")
def generate_recommendation(
    user_id: str
):

    recommendations = (
        generate_hybrid_recommendation(
            user_id=user_id
        )
    )

    return {
        "status": True,
        "message": "Recommendation generated",
        "total": len(
            recommendations
        ),
        "recommendations": [
            {
                "product_id": product_id,
                "score": score
            }
            for product_id, score
            in recommendations
        ]
    }

@router.post("/generate-all")
def generate_all():

    return generate_all_recommendations_response()


def generate_all_recommendations_response():

    result = (
        generate_all_recommendations()
    )

    return {
        "status": True,
        "message": "All recommendations generated",
        **result
    }