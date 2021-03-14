import json
from typing import TextIO 

from sqlalchemy.orm import Session

from . import models, schemas


# def get_ticker_by_id(db:Session, ticker_id:int):
#     return db.query(models.Ticker).filter(models.Ticker.id == ticker_id).first()


def get_ticker_by_symbol(db:Session, ticker_symbol:str, limit: int = 1):
    return db.query(models.Ticker).filter(models.Ticker.symbol == ticker_symbol).limit(limit).all()


def get_ticker_column_by_symbol(db:Session, ticker_symbol:str, limit: int = 1, q:str = None):
    if q:
        return db.query(models.Ticker.symbol, getattr(models.Ticker, q)).filter(models.Ticker.symbol == ticker_symbol).limit(limit).all()
    return db.query(models.Ticker).filter(models.Ticker.symbol == ticker_symbol).limit(limit).all()

def download_tickers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticker).offset(skip).limit(limit).all()


def create_record(db: Session, ticker: schemas.TickerRecord):
    db_record = models.Ticker(**ticker.dict()) # pass all the pydantic model data as key value pair
    db.add(db_record)
    db.commit()
    db.refresh(db_record) # to update any new data from the database, like the generated ID
    return db_record


def upload_records(db: Session, json_file: TextIO):
    # use multiprocessing
    initial_count = db.query(models.Ticker).count()
    for record in json.load(json_file).values():
        print(record['symbol'])
        db_record = models.Ticker(**record) # pass dict as key value pair
        db.add(db_record)
        db.commit()
        db.refresh(db_record) # to update any new data from the database, like the generated ID
    return {'Uploaded records' : db.query(models.Ticker).count() - initial_count}
