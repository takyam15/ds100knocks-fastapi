from datetime import date
from enum import Enum
from typing import Optional, Tuple

from pydantic import BaseModel, Field


class SortOption(str, Enum):
    ascending = 'ascending'
    decending = 'decending'


class CustomerColumn(str, Enum):
    birth_day = 'birth_day'


class RetrievedCustomer(BaseModel):
    customer_id: Optional[str] = Field(default=None, max_length=14)
    customer_name: Optional[str] = Field(default=None, max_length=20)
    gender_cd: Optional[str] = Field(default=None, max_length=1)
    gender: Optional[str] = Field(default=None, max_length=2)
    birth_day: Optional[date] = Field(default=None)
    age: Optional[int] = Field(default=None)
    postal_cd: Optional[str] = Field(default=None, max_length=8)
    address: Optional[str] = Field(default=None, max_length=128)
    application_store_cd: Optional[str] = Field(default=None, max_length=16)
    application_date: Optional[str] = Field(default=None, max_length=8)
    status_cd: Optional[str] = Field(default=None, max_length=12)


class CustomerQuery(BaseModel):
    customer_id_starts_with: Optional[str] = Field(default=None, max_length=14)
    status_cd_starts_with: Optional[str] = Field(default=None, max_length=12)
    status_cd_ends_with: Optional[str] = Field(default=None, max_length=12)
    sort_by: Optional[CustomerColumn] = Field(default=None)
    sort_ascending: Optional[bool] = Field(default=None)
