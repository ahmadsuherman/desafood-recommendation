from fastapi import APIRouter

from app.services.collaborative_service import (
    get_collaborative_recommendations
)

from app.services.content_based_service import (
    get_content_recommendations
)

from app.services.hybrid_service import (
    get_hybrid_recommendations
)

from app.repositories.product_repository import (
    get_product_by_id
)

from app.services.matrix_service import (
    build_user_product_matrix
)

from app.services.collaborative_service import (
    get_similar_products
)

from app.services.content_based_service import (
    get_content_similar_products
)

from app.services.dashboard_service import (
    summary_dashboard
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/hybrid-analysis/{user_id}"
)
def hybrid_analysis(
    user_id: str
):

    collaborative = (
        get_collaborative_recommendations(
            user_id,
            top_n=10
        )
    )

    content = (
        get_content_recommendations(
            user_id,
            top_n=10
        )
    )

    hybrid = (
        get_hybrid_recommendations(
            user_id,
            top_n=10
        )
    )

    collaborative_result = []

    for product_id, score in collaborative:

        product = get_product_by_id(
            product_id
        )

        collaborative_result.append({
            "product_id": product_id,
            "product_name": product["name"],
            "score": score
        })

    content_result = []

    for product_id, score in content:

        product = get_product_by_id(
            product_id
        )

        content_result.append({
            "product_id": product_id,
            "product_name": product["name"],
            "score": score
        })

    hybrid_result = []

    for product_id, score in hybrid:

        product = get_product_by_id(
            product_id
        )

        hybrid_result.append({
            "product_id": product_id,
            "product_name": product["name"],
            "score": score
        })

    return {
        "user_id": user_id,
        "collaborative": collaborative_result,
        "content_based": content_result,
        "hybrid": hybrid_result
    }

@router.get("/matrix")
def dashboard_matrix():

    matrix = build_user_product_matrix()

    total_users = len(matrix.index)

    total_products = len(matrix.columns)

    total_cells = (
        total_users
        *
        total_products
    )

    filled_cells = (
        matrix.astype(bool)
        .sum()
        .sum()
    )

    empty_cells = (
        total_cells
        -
        filled_cells
    )

    sparsity_percentage = round(
        (
            empty_cells
            /
            total_cells
        )
        *
        100,
        2
    )

    density_percentage = round(
        (
            filled_cells
            /
            total_cells
        )
        *
        100,
        2
    )

    return {
        "total_users": total_users,
        "total_products": total_products,
        "matrix_size": (
            f"{total_users}x{total_products}"
        ),
        "total_cells": total_cells,
        "filled_cells": int(
            filled_cells
        ),
        "empty_cells": int(
            empty_cells
        ),
        "sparsity_percentage":
            sparsity_percentage,
        "density_percentage":
            density_percentage
    }

@router.get(
    "/collaborative-similarity/{product_id}"
)
def collaborative_similarity(
    product_id: str
):

    product = get_product_by_id(
        product_id
    )

    if not product:
        return {
            "status": False,
            "message": "Product not found"
        }

    similar_products = (
        get_similar_products(
            product_id
        )
    )

    results = []

    for similar_product_id, score in similar_products:

        similar_product = (
            get_product_by_id(
                similar_product_id
            )
        )

        if not similar_product:
            continue

        results.append({
            "product_id": similar_product_id,
            "product_name":
                similar_product["name"],
            "score":
                round(score, 4)
        })

    return {
        "method":
            "collaborative_filtering",

        "description":
            "Kemiripan berdasarkan pola interaksi pengguna",

        "product_id":
            product["id"],

        "product_name":
            product["name"],

        "similar_products":
            results
    }

@router.get(
    "/content-similarity/{product_id}"
)
def content_similarity(
    product_id: str
):

    product = get_product_by_id(
        product_id
    )

    if not product:
        return {
            "status": False,
            "message": "Product not found"
        }

    similar_products = (
        get_content_similar_products(
            product_id
        )
    )

    results = []

    for similar_product_id, score in similar_products:

        similar_product = (
            get_product_by_id(
                similar_product_id
            )
        )

        if not similar_product:
            continue

        results.append({
            "product_id":
                similar_product_id,

            "product_name":
                similar_product["name"],

            "score":
                round(score, 4)
        })

    return {
        "method":
            "content_based_filtering",

        "description":
            "Kemiripan berdasarkan nama, kategori dan deskripsi produk",

        "product_id":
            product["id"],

        "product_name":
            product["name"],

        "similar_products":
            results
    }

@router.get("/summary")
def dashboard_summary():

    summary = summary_dashboard()

    return {
        "status": True,
        "data": summary
    }