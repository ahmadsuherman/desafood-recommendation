from pydantic import BaseModel

class RecommendationItem(BaseModel):
    product_id: str
    name: str
    score: float