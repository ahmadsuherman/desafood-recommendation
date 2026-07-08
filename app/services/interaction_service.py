from app.repositories.interaction_repository import get_interactions

def get_interaction_data():

    df = get_interactions()

    return df.to_dict(
        orient="records"
    )