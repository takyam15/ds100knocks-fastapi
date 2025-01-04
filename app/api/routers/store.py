from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.crud_processings.store import retrieve_stores
from app.api.models.dependencies import get_db
from app.api.schemas.store import RetrievedStore, StoreQuery

router = APIRouter()


@router.get('/list/', response_model=List[RetrievedStore])
async def get_stores(
    session: Session = Depends(get_db),
    offset: int = Query(default=0), limit: int = Query(default=10, lte=100),
    store_query: StoreQuery = Query(default=StoreQuery())
):
    return retrieve_stores(
        session, offset, limit, store_query
    )
