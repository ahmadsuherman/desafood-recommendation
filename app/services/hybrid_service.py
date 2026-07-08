import pandas as pd

from app.repositories.interaction_repository import (
    get_user_interactions,
    get_all_buyers
)

from app.services.collaborative_service import (
    get_collaborative_recommendations
)

from app.services.content_based_service import (
    get_content_recommendations
)

from app.repositories.recommendation_repository import (
    delete_user_recommendations,
    save_recommendations
)

def normalize_scores(recommendations):

    if not recommendations:
        return {}

    scores = [
        score
        for _, score in recommendations
    ]

    max_score = max(scores)

    if max_score == 0:
        max_score = 1

    normalized = {}

    for product_id, score in recommendations:

        normalized[product_id] = (
            score / max_score
        )

    return normalized


def get_hybrid_recommendations(
    user_id,
    top_n=10,
    cf_weight=0.7,
    cbf_weight=0.3
):

    cf_recommendations = (
        get_collaborative_recommendations(
            user_id,
            top_n=50
        )
    )

    cbf_recommendations = (
        get_content_recommendations(
            user_id,
            top_n=50
        )
    )

    normalized_cf = normalize_scores(
        cf_recommendations
    )

    normalized_cbf = normalize_scores(
        cbf_recommendations
    )

    hybrid_scores = {}

    all_products = set(
        list(normalized_cf.keys())
        +
        list(normalized_cbf.keys())
    )

    for product_id in all_products:

        cf_score = normalized_cf.get(
            product_id,
            0
        )

        cbf_score = normalized_cbf.get(
            product_id,
            0
        )

        hybrid_scores[product_id] = (
            (cf_weight * cf_score)
            +
            (cbf_weight * cbf_score)
        )

    recommendations = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

def generate_hybrid_recommendation(
    user_id,
    top_n=10
):

    user_interactions = get_user_interactions(
        user_id
    )

    # Cold Start
    if user_interactions.empty:

        recommendations = (
            get_popular_products(
                limit=top_n
            )
        )

    else:

        recommendations = (
            get_hybrid_recommendations(
                user_id=user_id,
                top_n=top_n
            )
        )

    delete_user_recommendations(
        user_id
    )

    save_recommendations(
        user_id=user_id,
        recommendations=recommendations,
        algorithm="hybrid"
    )

    return recommendations

def generate_all_recommendations():

    buyers = get_all_buyers()

    total_success = 0

    for user_id in buyers:

        try:

            generate_hybrid_recommendation(
                user_id=user_id
            )

            total_success += 1

        except Exception as e:

            print(
                f"Error User {user_id}: {e}"
            )

    return {
        "total_buyers": len(buyers),
        "success": total_success
    }