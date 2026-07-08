import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from app.services.matrix_service import (
    build_user_product_matrix
)
from app.repositories.interaction_repository import (
    get_user_interactions
)

def calculate_product_similarity():

    matrix = build_user_product_matrix()

    product_matrix = matrix.T

    similarity = cosine_similarity(
        product_matrix
    )

    return {
        "products": product_matrix.index.tolist(),
        "similarity": similarity.tolist()
    }


def get_collaborative_recommendations(
    user_id,
    top_n=10
):

    matrix = build_user_product_matrix()

    product_matrix = matrix.T

    similarity_matrix = cosine_similarity(
        product_matrix
    )

    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=product_matrix.index,
        columns=product_matrix.index
    )

    user_products = get_user_interactions(
        user_id
    )

    recommendation_scores = {}

    for _, row in user_products.iterrows():

        product_id = row["product_id"]

        similar_products = similarity_df[
            product_id
        ].sort_values(
            ascending=False
        )

        for similar_product, score in similar_products.items():

            if similar_product == product_id:
                continue

            recommendation_scores[
                similar_product
            ] = recommendation_scores.get(
                similar_product,
                0
            ) + score

    recommendations = sorted(
        recommendation_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

def get_similar_products(
    product_id,
    top_n=10
):

    similarity_data = (
        calculate_product_similarity()
    )

    products = (
        similarity_data["products"]
    )

    similarity_matrix = (
        similarity_data["similarity"]
    )

    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=products,
        columns=products
    )

    if product_id not in similarity_df.index:

        return []

    similar_products = (
        similarity_df[product_id]
        .sort_values(
            ascending=False
        )
    )

    recommendations = []

    for similar_product, score in similar_products.items():

        if similar_product == product_id:
            continue

        recommendations.append(
            (
                similar_product,
                float(score)
            )
        )

    return recommendations[:top_n]