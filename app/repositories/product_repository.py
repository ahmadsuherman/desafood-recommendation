import pandas as pd
from app.core.database import engine
from sqlalchemy import text

def get_products():

    query = """
    SELECT
        p.id,
        p.name,
        p.description,
        c.name AS category_name
    FROM products p
    INNER JOIN categories c
        ON c.id = p.category_id
    WHERE p.is_active = 1
    """

    return pd.read_sql(query, engine)

def get_popular_products(limit=10):

    query = text("""
        SELECT
            product_id,
            (
                LOG(1 + SUM(
                    CASE
                        WHEN type='click'
                        THEN 1
                        ELSE 0
                    END
                ))
            )

            +

            SUM(
                CASE
                    WHEN type='add_to_cart'
                    THEN 3
                    ELSE 0
                END
            )

            +

            SUM(
                CASE
                    WHEN type='purchase'
                    THEN 5
                    ELSE 0
                END
            )

        AS total_score
        FROM user_product_interactions
        GROUP BY product_id
        ORDER BY total_score DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "limit": limit
            }
        )

        rows = result.fetchall()

    return [
        (
            row.product_id,
            float(row.total_score)
        )
        for row in rows
    ]

def get_product_by_id(product_id):

    query = text("""
        SELECT
            id,
            name,
            price,
            image
        FROM products
        WHERE id = :product_id
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "product_id": product_id
            }
        )

        row = result.fetchone()

    if not row:
        return None

    return {
        "id": str(row.id),
        "name": row.name,
        "price": float(row.price),
        "image": row.image
    }

def get_product_name(
    product_id
):

    product = get_product_by_id(
        product_id
    )

    if not product:
        return None

    return product["name"]