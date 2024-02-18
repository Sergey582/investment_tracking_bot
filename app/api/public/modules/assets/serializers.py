from datetime import datetime, date
from typing import List, Optional, Sequence

from pydantic import BaseModel, validator

from app.core.modules.assets.constants import CURRENCIES


class CreateAssetRequest(BaseModel):
    number: float
    price: float
    name: str
    currency: str
    transaction_date: Optional[datetime] = None

    @validator('currency')
    def validate_currency(cls, value: int):
        if value not in CURRENCIES:
            raise ValueError('Invalid currency')
        return value


class AssetResponse(BaseModel):
    number: float
    price: float
    name: str
    currency: str
    daily_pnl: float
    total_pnl: float
    daily_percent_pnl: float
    total_sum: float
    average_price: float


class AssetHistoryResponse(BaseModel):
    number: float
    price: float
    name: str
    currency: str
    created_at: datetime


class AssetHistoryListResponse(BaseModel):
    assets: List[AssetHistoryResponse]


class Pagination(BaseModel):
    from_id: Optional[int]
    limit: Optional[int]


class ExpensesQueryFilters(BaseModel):
    transaction_date_from: Optional[datetime]
    transaction_date_to: Optional[datetime]


class AssetData(BaseModel):
    currency: str
    total_sum: float
    full_name: str
    number: float
    name: str
    daily_pnl: float
    daily_percent_pnl: float


class AssetsListData(BaseModel):
    next_id: Optional[int] = None
    messages: Sequence[AssetData]


class CategoryStatisticsData(BaseModel):
    total_amount: float
    category: int
    display_category: str


class CategoriesStatisticsData(BaseModel):
    data: List[CategoryStatisticsData]


class CategoryData(BaseModel):
    category: int
    display_category: str


class CategoriedListData(BaseModel):
    data: List[CategoryData]


class CurrenciesListData(BaseModel):
    data: List[str]


class TickersListData(BaseModel):
    tickers: List[str]
