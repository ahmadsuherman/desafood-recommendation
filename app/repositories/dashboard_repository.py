from sqlalchemy import text

from app.core.database import engine


def get_dashboard_summary():

    query = text("""
        SELECT
            (
                SELECT COUNT(*)
                FROM users u
                JOIN model_has_roles mhr
                    ON u.id = mhr.model_id
                JOIN roles r
                    ON r.id = mhr.role_id
                WHERE r.name = 'Pembeli'
            ) AS total_users,

            (
                SELECT COUNT(*)
                FROM products
            ) AS total_products,

            (
                SELECT COUNT(*)
                FROM user_product_interactions
            ) AS total_interactions,

            (
                SELECT COUNT(*)
                FROM product_recommendations
            ) AS total_recommendations,

            (
                SELECT MAX(generated_at)
                FROM product_recommendations
            ) AS last_recommendation_generated
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query
        ).mappings().first()

        return dict(result)