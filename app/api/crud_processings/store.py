from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.models.models import StoreModel
from app.api.schemas.store import RetrievedStore, StoreQuery


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def retrieve_stores(session: Session, offset: int, limit: int, store_query: StoreQuery) -> List[RetrievedStore]:
    statement = select(StoreModel).offset(offset).limit(limit)
    if store_query.store_cd_starts_with is not None:
        statement = statement.where(StoreModel.store_cd.startswith(store_query.store_cd_starts_with))
    if store_query.address_includes is not None:
        statement = statement.where(StoreModel.address.contains(store_query.address_includes))
    if store_query.tel_no_pattern is not None:
        pass  # TODO
    stores = [
        RetrievedStore.model_validate(model_to_dict(store)) for store in session.scalars(statement).all()
    ]
    return stores
