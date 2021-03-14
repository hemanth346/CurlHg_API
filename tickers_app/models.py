"""
SQLAlchemy models i.e. DB tables via Sqlalchemy ORM
"""
from sqlalchemy import Column, Float, Integer, String, JSON, BigInteger

from .database import Base

class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    info = Column(JSON)
    timestamp = Column(BigInteger)
    datetime = Column(BigInteger)
    high = Column(String)
    low = Column(String)
    bid = Column(Float)
    bidVolume = Column(String)
    ask = Column(Float)
    askVolume = Column(String)
    vwap = Column(String)
    open = Column(Float)
    close = Column(Float)
    last = Column(Float)
    baseVolume = Column(String)
    quoteVolume = Column(String)
    previousClose = Column(String)
    change = Column(Float)
    percentage = Column(Float)
    average = Column(Float)
