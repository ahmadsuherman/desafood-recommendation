import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.repositories.product_repository import (
    get_products
)

from app.repositories.interaction_repository import (
    get_user_interactions
)


def calculate_content_similarity():

    products = get_products()

    products["content"] = (
        products["name"].fillna("")
        + " "
        + products["category_name"].fillna("")
        + " "
        + products["description"].fillna("")
    )

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(
        products["content"]
    )

    similarity = cosine_similarity(
        tfidf_matrix,
        tfidf_matrix
    )

    return {
        "products": products["id"].tolist(),
        "similarity": similarity.tolist()
    }


def get_content_recommendations(
    user_id,
    top_n=10
):

    products = get_products()

    products["content"] = (
        products["name"].fillna("")
        + " "
        + products["category_name"].fillna("")
        + " "
        + products["description"].fillna("")
    )

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(
        products["content"]
    )

    similarity_matrix = cosine_similarity(
        tfidf_matrix,
        tfidf_matrix
    )

    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=products["id"],
        columns=products["id"]
    )

    user_products = get_user_interactions(
        user_id
    )

    interacted_products = set(
        user_products["product_id"].tolist()
    )

    recommendation_scores = {}

    for _, row in user_products.iterrows():

        product_id = row["product_id"]

        if product_id not in similarity_df.index:
            continue

        similar_products = similarity_df[
            product_id
        ].sort_values(
            ascending=False
        )

        for similar_product, score in similar_products.items():

            if similar_product == product_id:
                continue

            if similar_product in interacted_products:
                continue

            if score <= 0:
                continue

            recommendation_scores[
                similar_product
            ] = recommendation_scores.get(
                similar_product,
                0
            ) + float(score)

    recommendations = sorted(
        recommendation_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

def get_content_similar_products(
    product_id,
    top_n=10
):

    products = get_products()

    products["content"] = (
        products["name"].fillna("")
        + " "
        + products["category_name"].fillna("")
        + " "
        + products["description"].fillna("")
    )

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(
        products["content"]
    )

    similarity_matrix = cosine_similarity(
        tfidf_matrix,
        tfidf_matrix
    )

    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=products["id"],
        columns=products["id"]
    )

    if product_id not in similarity_df.index:
        return []

    similar_products = similarity_df[
        product_id
    ].sort_values(
        ascending=False
    )

    recommendations = []

    for similar_product, score in similar_products.items():

        if similar_product == product_id:
            continue

        if score <= 0:
            continue

        recommendations.append(
            (
                similar_product,
                float(score)
            )
        )

    return recommendations[:top_n]