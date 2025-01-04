from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.api.models.models import ReceiptModel
from app.api.schemas.receipt import (
    ReceiptColumn, RetrievedReceipt, ReceiptQuery, RankedReceipt, RankedReceiptQuery,
    GroupedReceiptQuery, ReceiptAggregation
)


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def retrieve_receipts(
        session: Session, columns: Optional[List[ReceiptColumn]],
        offset: int, limit: int
    ) -> List[RetrievedReceipt]:
    if columns is None:
        receipts = [
            RetrievedReceipt.model_validate(model_to_dict(receipt)) for receipt in session.scalars(select(ReceiptModel).offset(offset).limit(limit)).all()
        ]
    else:
        selected_columns = [getattr(ReceiptModel, column.value) for column in columns]
        receipts = [
            RetrievedReceipt.model_validate(receipt._asdict()) for receipt in session.execute(select(*selected_columns).offset(offset).limit(limit)).all()
        ]
    return receipts


def filter_by_values(statement, receipt_query):
    if receipt_query.amount_min is not None:
        statement = statement.where(ReceiptModel.amount >= receipt_query.amount_min)
    if receipt_query.amount_max is not None:
        statement = statement.where(ReceiptModel.amount <= receipt_query.amount_max)
    if receipt_query.quantity_min is not None:
        statement = statement.where(ReceiptModel.quantity >= receipt_query.quantity_min)
    if receipt_query.quantity_max is not None:
        statement = statement.where(ReceiptModel.quantity <= receipt_query.quantity_max)
    if receipt_query.excluded_product_cd is not None:
        statement = statement.where(ReceiptModel.product_cd != receipt_query.excluded_product_cd)
    return statement


def retrieve_customer_receipts(
        session: Session, columns: Optional[List[ReceiptColumn]],
        customer_id: str, receipt_query: ReceiptQuery
) -> List[RetrievedReceipt]:
    if columns is None:
        statement = select(ReceiptModel).filter_by(customer_id=customer_id)
        statement = filter_by_values(statement, receipt_query)
        receipts = [
            RetrievedReceipt.model_validate(model_to_dict(receipt)) for receipt in session.scalars(statement).all()
        ]
    else:
        selected_columns = [getattr(ReceiptModel, column.value) for column in columns]
        statement = select(*selected_columns).filter_by(customer_id=customer_id)
        statement = filter_by_values(statement, receipt_query)
        receipts = [
            RetrievedReceipt.model_validate(receipt._asdict()) for receipt in session.execute(statement).all()
        ]
    return receipts


def retrieve_ranked_receipts(
        session: Session, columns: Optional[List[ReceiptColumn]],
        ranked_receipt_query: RankedReceiptQuery
) -> List[RankedReceipt]:
    if columns is None:
        statement = select(ReceiptModel).order_by(ranked_receipt_query.sort_by).limit(ranked_receipt_query.limit)
        receipts = [
            RankedReceipt.model_validate(model_to_dict(receipt)) for receipt in session.scalars(statement).all()
        ]
    else:
        selected_columns = [getattr(ReceiptModel, column.value) for column in columns]
        statement = select(*selected_columns).order_by(ranked_receipt_query.sort_by).limit(ranked_receipt_query.limit)
        receipts = [
            RankedReceipt.model_validate(receipt._asdict()) for receipt in session.execute(statement).all()
        ]
    if ranked_receipt_query.unique_ranks:
        for i, receipt in enumerate(receipts):
            receipt.rank = i + 1
    else:
        for i, receipt in enumerate(receipts):
            if i >= 1 and receipt[i-1].amount == receipt.amount:
                receipt.rank = receipt[i-1].rank
            else:
                receipt.rank = i + 1
    return receipts


def retrieve_grouped_receipts(
        session: Session,
        grouped_receipt_query: GroupedReceiptQuery
) -> List[RetrievedReceipt]:
    aggregated_functions = []
    for column in grouped_receipt_query.aggregated_columns:
        if column.aggregation == ReceiptAggregation.count:
            aggregated_functions.append(
                func.count(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.mean:
            aggregated_functions.append(
                func.avg(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.var:
            aggregated_functions.append(
                func.var(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.sd:
            aggregated_functions.append(
                func.stddev(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.sum:
            aggregated_functions.append(
                func.sum(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.max:
            aggregated_functions.append(
                func.max(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.min:
            aggregated_functions.append(
                func.min(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.median:
            aggregated_functions.append(
                func.median(getattr(ReceiptModel, column.column).label(column.column))
            )
        elif column.aggregation == ReceiptAggregation.mode:
            aggregated_functions.append(
                func.mode(getattr(ReceiptModel, column.column).label(column.column))
            )
    statement = select(*grouped_receipt_query.group_by, *aggregated_functions).group_by(*grouped_receipt_query.group_by)
    receipts = [
        RetrievedReceipt.model_validate(receipt._asdict()) for receipt in session.execute(statement).all()
    ]
    return receipts
