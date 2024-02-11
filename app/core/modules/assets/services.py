from datetime import datetime
from linecache import cache
from typing import List, Optional, Dict

from app.core.modules.assets.constants import CURRENCIES
from app.core.modules.assets.models import Asset, User
from app.core.modules.binance.client import binance_client


async def create_asset(
        user: User,
        price: float,
        currency: str,
        name: str,
        number: float,
        transaction_date: Optional[datetime] = None
):
    await Asset.create(
        user=user,
        price=price,
        currency=currency,
        name=name,
        number=number,
        transaction_date=transaction_date,
    )


def get_assets_prices(assets_names: List[str]) -> Dict[str, float]:
    assets_prices = cache.get("assets_prices")
    if not assets_prices:
        assets_prices = binance_client.get_assets_prices(assets_names=[assets_names])
    cache.setdefault("assets_prices", assets_prices)
    return assets_prices


async def get_asset_history(user: User, asset_name: str, ) -> Optional[Asset]:
    assets = Asset.filter(
        user=user,
        id=asset_name,
    ).all()
    return assets


async def get_asset(user: User, asset_name: str, ) -> Optional[dict]:
    assets = await Asset.filter(
        user=user,
        name=asset_name,
    ).all()

    if not assets:
        return None

    asset_sum = 0
    asset_number = 0
    for asset in assets:
        asset_sum += asset.number * asset.price
        asset_number += asset.number

    # current_asset_price = get_assets_prices(assets_names=[asset_name, ])[asset_name]

    asset_info = {
        "currency": asset.currency,
        "number": asset_number,
        "name": asset_name,
        "price": 1,  # current_asset_price,
        "average_price": asset_sum / asset_number,
        "daily_pnl": "test",
        "total_pnl": 1,  # asset_sum - asset_number * current_asset_price,
    }
    return asset_info


async def delete_asset(user: User, asset_id: int):
    await Asset.filter(id=asset_id, user=user).delete()


async def get_assets(
        user: User,
        from_id: int,
        limit: int,
        transaction_date_from: datetime,
        transaction_date_to: datetime,
) -> List[dict]:
    assets_query = Asset.filter(user=user)

    if from_id:
        assets_query = assets_query.filter(pk__lte=from_id).order_by('-id')

    if transaction_date_from:
        assets_query = assets_query.filter(transaction_date__gte=transaction_date_from)

    if transaction_date_to:
        assets_query = assets_query.filter(transaction_date__lte=transaction_date_to)

    if limit:
        assets_query = assets_query.limit(limit + 1)

    assets = await assets_query

    # assets_names = [asset.name for asset in assets]
    # assets_prices = binance_client.get_assets_prices(assets_names=assets_names)

    result = []

    for asset in assets:
        result.append({
            'id': asset.pk,
            'currency': asset.currency,
            'number': asset.number,
            'total_sum': 1,  # assets_prices[asset.name] * asset.number,
            'name': asset.name,
            'full_name': asset.name,
            'transaction_date': asset.transaction_date,
            'daily_pnl': "test",
            'created_at': asset.created_at,
            'updated_at': asset.updated_at,
        })

    return result


def get_last_asset_id(assets: list, limit: int):
    if limit and len(assets) == limit + 1:
        last_id = assets[-1]["id"]
        assets = assets[:-1]
    else:
        last_id = None
    return assets, last_id


def get_all_currencies() -> List[str]:
    return CURRENCIES
