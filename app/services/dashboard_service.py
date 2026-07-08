from app.repositories.dashboard_repository import (
    get_dashboard_summary
)


def summary_dashboard():

    summary = get_dashboard_summary()

    total_users = summary[
        "total_users"
    ]

    total_interactions = summary[
        "total_interactions"
    ]

    average_interaction = 0

    if total_users > 0:

        average_interaction = round(
            total_interactions / total_users,
            2
        )

    return {
        "total_users":
            summary["total_users"],

        "total_products":
            summary["total_products"],

        "total_interactions":
            summary["total_interactions"],

        "total_recommendations":
            summary["total_recommendations"],

        "average_interaction_per_user":
            average_interaction,

        "last_recommendation_generated":
            summary[
                "last_recommendation_generated"
            ]
    }