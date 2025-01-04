from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.crud_processings import retrieve_receipts, retrieve_customer_receipts, retrieve_ranked_receipts, retrieve_grouped_receipts
from app.api.models.dependencies import get_db
from app.api.schemas import ReceiptColumn, RetrievedReceipt, ReceiptQuery, RankedReceipt, RankedReceiptQuery, GroupedReceipt, GroupedReceiptQuery


router = APIRouter()


@router.get('/list/', response_model=List[RetrievedReceipt])
async def get_receipts(
    session: Session = Depends(get_db),
    columns: Optional[List[ReceiptColumn]] = Query(default=None),
    offset: int = Query(default=0), limit: int = Query(default=10, lte=100)
) -> List[RetrievedReceipt]:
    return retrieve_receipts(session, columns, offset, limit)


@router.get('/list/{customer_id}/', response_model=List[RetrievedReceipt])
async def get_customer_receipts(
    customer_id: str, receipt_query: ReceiptQuery = Query(default=ReceiptQuery()),
    session: Session = Depends(get_db),
    columns: Optional[List[ReceiptColumn]] = Query(default=None),
) -> List[RetrievedReceipt]:
    return retrieve_customer_receipts(session, columns, customer_id, receipt_query)


@router.get('/list/ranked/', response_model=List[RankedReceipt])
async def get_ranked_receipts(
    ranked_receipt_query: RankedReceiptQuery = Query(default=RankedReceiptQuery()),
    session: Session = Depends(get_db),
    columns: Optional[List[ReceiptColumn]] = Query(default=None)
) -> List[RankedReceipt]:
    return retrieve_ranked_receipts(session, columns, ranked_receipt_query)


@router.get('/list/grouped', response_model=List[RetrievedReceipt])
async def get_grouped_receipts(
    grouped_receipt_query: GroupedReceiptQuery = Query(default=GroupedReceiptQuery()),
    session: Session = Depends(get_db),
    columns: Optional[List[ReceiptColumn]] = Query(default=None)
) -> List[RetrievedReceipt]:
    return retrieve_grouped_receipts(session, columns, grouped_receipt_query)
