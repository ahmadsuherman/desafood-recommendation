import pandas as pd

from sqlalchemy import text

from app.core.database import engine


def get_all_interactions():

    query = text("""
        SELECT
            user_id,
            product_id,
            score
        FROM user_product_interactions
    """)

    with engine.connect() as connection:

        df = pd.read_sql(
            query,
            connection
        )

    return df