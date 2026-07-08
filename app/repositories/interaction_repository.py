import pandas as pd
from app.core.database import engine
from sqlalchemy import text

def get_interactions():

    query = """
    SELECT
        user_id,
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
    GROUP BY user_id, product_id
    """

    return pd.read_sql(query, engine)


def get_user_interactions(user_id):

    query = f"""
    SELECT
        user_id,
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
    WHERE user_id = '{user_id}'
    GROUP BY user_id, product_id
    """

    return pd.read_sql(query, engine)


def get_user_interacted_products(user_id):
    query = text("""
        SELECT DISTINCT product_id
        FROM user_product_interactions
        WHERE user_id = :user_id
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {"user_id": user_id}
        )

        return {
            row.product_id
            for row in result
        }
    
def get_all_buyers():

    query = text("""
        SELECT
            u.id
        FROM users u
        INNER JOIN model_has_roles mhr
            ON mhr.model_id = u.id
        INNER JOIN roles r
            ON r.id = mhr.role_id
        WHERE r.name = 'Pembeli'
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        rows = result.fetchall()

    return [
        row.id
        for row in rows
    ]