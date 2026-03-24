from typing import Any

from pydantic import BaseModel, Field, field_validator


class ApiResponse(BaseModel):
    message: str | None = Field(None, description="Message")
    data: Any | None = Field(None, description="Data")

    @field_validator("data", mode="before")
    @classmethod
    def dump_models(cls, v: Any) -> Any:
        if isinstance(v, BaseModel):
            return v.model_dump()
        if isinstance(v, list):
            return [
                item.model_dump() if isinstance(item, BaseModel) else item for item in v
            ]
        return v
