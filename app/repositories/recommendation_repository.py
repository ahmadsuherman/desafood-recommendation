from sqlalchemy import text

from app.core.database import engine

import uuid


def delete_user_recommendations(
    user_id
):

    query = text("""
        DELETE
        FROM product_recommendations
        WHERE user_id = :user_id
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "user_id": user_id
            }
        )


def save_recommendations(
    user_id,
    recommendations,
    algorithm="hybrid"
):

    query = text("""
        INSERT INTO product_recommendations
        (
            id,
            user_id,
            product_id,
            relevance_score,
            algorithm,
            generated_at,
            created_at,
            updated_at
        )
        VALUES
        (
            :id,
            :user_id,
            :product_id,
            :relevance_score,
            :algorithm,
            NOW(),
            NOW(),
            NOW()
        )
    """)

    with engine.begin() as conn:

        for product_id, score in recommendations:

            conn.execute(
                query,
                {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "product_id": product_id,
                    "relevance_score": float(score),
                    "algorithm": algorithm
                }
            )