import random
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from app.repositories.evaluation_repository import (
    get_all_interactions
)

from app.services.hybrid_service import (
    get_hybrid_recommendations
)


def evaluate_model():

    interactions = (
        get_all_interactions()
    )

    if len(interactions) < 10:

        return {
            "status": False,
            "message":
                "Not enough interaction data"
        }

    interactions = interactions.sample(
        frac=1,
        random_state=42
    )

    split_index = int(
        len(interactions) * 0.8
    )

    train = interactions.iloc[
        :split_index
    ]

    test = interactions.iloc[
        split_index:
    ]

    actual_scores = []
    predicted_scores = []

    for _, row in test.iterrows():

        user_id = row["user_id"]

        product_id = row["product_id"]

        actual_score = float(
            row["score"]
        )

        recommendations = (
            get_hybrid_recommendations(
                user_id,
                top_n=50
            )
        )

        predicted_score = 0

        for pid, score in recommendations:

            if pid == product_id:

                predicted_score = score
                break

        actual_scores.append(
            actual_score
        )

        predicted_scores.append(
            predicted_score
        )

    mae = mean_absolute_error(
        actual_scores,
        predicted_scores
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual_scores,
            predicted_scores
        )
    )

    return {
        "status": True,

        "total_interactions":
            len(interactions),

        "training_data":
            len(train),

        "testing_data":
            len(test),

        "mae":
            round(float(mae), 4),

        "rmse":
            round(float(rmse), 4)
    }