import threading
from contextlib import suppress

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.interaction import (
    router as interaction_router
)
from app.api.matrix import (
    router as matrix_router
)
from app.api.collaborative import (
    router as collaborative_router
)
from app.api.content_based import (
    router as content_based_router
)

from app.api.recommendation import (
    router as recommendation_router
)

from app.api.dashboard import (
    router as dashboard_router
)

from app.api.evaluation import (
    router as evaluation_router
)
from app.api.recommendation import (
    generate_all_recommendations_response
)
from app.core.security import (
    require_api_key
)

app = FastAPI(
    title="DesaFood Recommendation API",
    dependencies=[Depends(require_api_key)],
)


def custom_openapi():

    if app.openapi_schema:

        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema.setdefault(
        "security",
        [
            {
                "X-API-KEY": []
            }
        ]
    )

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


def run_generate_all_scheduler(stop_event: threading.Event):

    while not stop_event.wait(3600):

        with suppress(Exception):

            generate_all_recommendations_response()


@app.on_event("startup")
def start_generate_all_scheduler():

    stop_event = threading.Event()
    scheduler_thread = threading.Thread(
        target=run_generate_all_scheduler,
        args=(stop_event,),
        daemon=True,
    )

    app.state.generate_all_scheduler_stop_event = stop_event
    app.state.generate_all_scheduler_thread = scheduler_thread

    scheduler_thread.start()


@app.on_event("shutdown")
def stop_generate_all_scheduler():

    stop_event = getattr(
        app.state,
        "generate_all_scheduler_stop_event",
        None
    )

    if stop_event:

        stop_event.set()

app.include_router(
    interaction_router
)
app.include_router(
    matrix_router
)
app.include_router(
    collaborative_router
)

app.include_router(
    content_based_router
)

app.include_router(
    recommendation_router
)
app.include_router(
    dashboard_router
)

app.include_router(
    evaluation_router
)

@app.get("/")
def home():
    return {
        "message": "DesaFood Recommendation API"
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "https://admin-desafood.ahmadsuherman.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)