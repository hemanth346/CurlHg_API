"""
Pydantic models -> data/response validation/shape
"""
from typing import Dict, Optional, Union

from pydantic import BaseModel


class TickerCreate(BaseModel):
    symbol: str
    info: Dict
    timestamp: int
    datetime: int
    high: Optional[str] = None
    low: Optional[str] = None
    bid: Optional[float] = None
    bidVolume: Optional[str] = None
    ask: Optional[float] = None
    askVolume: Optional[str] = None
    vwap: Optional[str] = None
    open: Optional[float] = None
    close: Optional[float] = None
    last: Optional[float] = None
    baseVolume: Union[str, float, None]
    quoteVolume: Optional[str] = None
    previousClose: Optional[str] = None
    change: Optional[float] = None
    percentage: Optional[float] = None
    average: Optional[float] = None


class TickerRecord(TickerCreate):
    id: int
    
    class Config:
        orm_mode = True
        # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    