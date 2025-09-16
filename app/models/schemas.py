# server/app/models/schemas.py

from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    class_name: str = Field(..., example="brown_spot")
    confidence: float = Field(..., example=0.9876)

    class Config:
        # Pydantic v2 style, untuk Pydantic v1 gunakan schema_extra
        json_schema_extra = {
            "example": {
                "class_name": "brown_spot",
                "confidence": 0.9876
            }
        }