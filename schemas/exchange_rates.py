from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ExchangeRate(BaseModel):
    id: int
    currency: str
    rate: float
    change: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ExchangeRateResponse(BaseModel):
    Date: date = Field(default_factory=date.today)
    rates: List[ExchangeRate]
