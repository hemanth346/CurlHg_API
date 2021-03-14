from typing import Dict, Optional
import json

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionMaker, engine, database

# create db tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['localhost:8000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dependency
def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()

# event handlers to connect and disconnect from the database
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/add_ticker/", response_model=schemas.TickerRecord)
async def add_ticker(ticker: schemas.TickerRecord, db: Session = Depends(get_db)):
    return await crud.create_record(db=db, ticker=ticker)


@app.post("/processfile/")
# https://docs.python.org/3/library/constants.html#Ellipsis
async def upload_process_file(json_file: UploadFile = File(...), db: Session = Depends(get_db)):
    # add validations
    return crud.upload_records(db=db, json_file=json_file.file)


# https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-containing-paths
@app.get("/get_ticker/{symbol:path}")
async def get_ticker_by_symbol(symbol: str, 
            limit: int = Query(
                1,
                title="Query int",
                description="Number of records to get"), 
            db: Session = Depends(get_db),
            ):
    return crud.get_ticker_by_symbol(db=db, ticker_symbol=symbol, limit=limit)


# @app.get("/get_ticker/{id}", response_model=schemas.TickerRecord)
# async def get_ticker_by_id(id: int, db: Session = Depends(get_db)):
#     return crud.get_ticker_by_id(db=db, ticker_id=id)


@app.get("/ticker_details/{symbol:path}")
async def get_ticker_column_for_symbol(symbol: str, 
            limit: int = 1, 
            db: Session = Depends(get_db),
            q: Optional[str] = Query(
                None,
                title="Query string",
                description="Key to search",
                min_length=3,
                max_length=20,
                deprecated=True,            )
            ):
    return crud.get_ticker_column_by_symbol(db=db, ticker_symbol=symbol, limit=limit, q=q)


@app.get("/download/")
async def download_tickers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.download_tickers(db=db, skip = skip, limit = limit)


@app.get("/")
async def main():
    content = """
        <body>
            <form action="/processfile/" enctype="multipart/form-data" method="post">
                <input name="json_file" type="file" accept=".json">
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)

