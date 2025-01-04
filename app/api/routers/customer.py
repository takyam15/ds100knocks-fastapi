from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.crud_processings.customer import retrieve_customers
from app.api.models.dependencies import get_db
from app.api.schemas.customer import RetrievedCustomer, CustomerQuery

router = APIRouter()


@router.get('/list/', response_model=List[RetrievedCustomer])
async def get_customers(
    customer_query: CustomerQuery = Query(CustomerQuery()), session: Session = Depends(get_db),
    offset: int = Query(default=0), limit = Query(default=10, lte=100)
) -> List[RetrievedCustomer]:
    return retrieve_customers(session, offset, limit, customer_query)
