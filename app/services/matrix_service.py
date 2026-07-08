from app.repositories.interaction_repository import get_interactions

def build_user_product_matrix():

    df = get_interactions()

    matrix = df.pivot_table(
        index='user_id',
        columns='product_id',
        values='total_score',
        fill_value=0
    )

    return matrix