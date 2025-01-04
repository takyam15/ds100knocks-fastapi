from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field


class RetrievedStore(BaseModel):
    store_cd: Optional[str] = Field(default=None, max_length=6)
    prefecture_cd: Optional[str] = Field(default=None, max_length=2)
    prefectur: Optional[str] = Field(default=None, max_length=5)
    address: Optional[str] = Field(default=None, max_length=128)
    address_kana: Optional[str] = Field(default=None, max_length=128)
    tel_no: Optional[str] = Field(default=None, max_length=20)
    longitude: Optional[Decimal] = Field(default=None)
    latitude: Optional[Decimal] = Field(default=None)
    floor_area: Optional[Decimal] = Field(default=None)


class StoreQuery(BaseModel):
    store_cd_starts_with: Optional[str] = Field(default=None, max_length=6)
    address_includes: Optional[str] = Field(default=None, max_length=128)
    tel_no_pattern: Optional[str] = Field(default=None)
