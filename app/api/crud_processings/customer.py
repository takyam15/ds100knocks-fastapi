from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.models.models import CustomerModel
from app.api.schemas.customer import RetrievedCustomer, CustomerQuery


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def retrieve_customers(session: Session, offset: int, limit: int, customer_query: CustomerQuery) -> List[RetrievedCustomer]:
    statement = select(CustomerModel)
    if customer_query.customer_id_starts_with is not None:
        statement = statement.where(CustomerModel.customer_id.startswith(customer_query.customer_id_starts_with))
    if customer_query.status_cd_starts_with is not None:
        statement = statement.where(CustomerModel.stats_cd.startswith(customer_query.status_cd_starts_with))
    if customer_query.status_cd_ends_with is not None:
        statement = statement.where(CustomerModel.status_cd.endswith(customer_query.status_cd_ends_with))
    if customer_query.sort_by is not None:
        if customer_query.sort_ascending is None:
            sort_ascending = True
        else:
            sort_ascending = customer_query.sort_ascending.lower() == 'true'
        if sort_ascending:
            statement = statement.order_by(getattr(CustomerModel, customer_query.sort_by))
        else:
            statement = statement.order_by(getattr(CustomerModel, customer_query.sort_by).desc())
    statement = statement.offset(offset).limit(limit)
    customers = [
        RetrievedCustomer.model_validate(model_to_dict(customer)) for customer in session.scalars(statement).all()
    ]
    return customers
