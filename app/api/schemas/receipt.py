from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class ReceiptColumn(str, Enum):
    sales_ymd = 'sales_ymd'
    store_cd = 'store_cd'
    receipt_no = 'receipt_no'
    receipt_sub_no = 'receipt_sub_no'
    sales_epoch = 'sales_epoch'
    customer_id = 'customer_id'
    product_cd = 'product_cd'
    quantity = 'quantity'
    amount = 'amount'


class ReceiptAggregation(str, Enum):
    count = 'count'
    mean = 'mean'
    var = 'var'
    sd = 'sd'
    sum = 'sum'
    max = 'max'
    min = 'min'
    median = 'median'
    mode = 'mode'


class AggregatedColumn:
    column: ReceiptColumn
    aggregation: ReceiptAggregation


class RetrievedReceipt(BaseModel):
    sales_ymd: Optional[int] = Field(default=None)
    store_cd: Optional[str] = Field(default=None, max_length=6)
    receipt_no: Optional[int] = Field(default=None)
    receipt_sub_no: Optional[int] = Field(default=None)
    sales_epoch: Optional[int] = Field(default=None)
    customer_id: Optional[str] = Field(default=None, max_length=14)
    product_cd: Optional[str] = Field(default=None, max_length=10)
    quantity: Optional[int] = Field(default=None)
    amount: Optional[int] = Field(default=None)


class ReceiptQuery(BaseModel):
    amount_min: Optional[int] = Field(default=None)
    amount_max: Optional[int] = Field(default=None)
    quantity_min: Optional[int] = Field(default=None)
    quantity_max: Optional[int] = Field(default=None)
    excluded_product_cd: Optional[str] = Field(default=None, max_length=10)


class RankedReceipt(RetrievedReceipt):
    rank: Optional[int] = Field(default=None)


class RankedReceiptQuery(BaseModel):
    sort_by: ReceiptColumn
    sort_ascending: bool = Field(default=True)
    limit: int = Field(default=10, gte=1, lte=100)
    unique_ranks: bool = Field(default=True)


class GroupedReceipt(RetrievedReceipt):
    records: List[RetrievedReceipt]


class GroupedReceiptQuery(BaseModel):
    group_by: Optional[List[ReceiptColumn]]
    aggregated_columns: List[AggregatedColumn]
    sort_by: Optional[ReceiptColumn] = Field(default=None)
    sort_ascending: bool = Field(default=True)
    limit: int = Field(default=10, gte=1, lte=100)
    