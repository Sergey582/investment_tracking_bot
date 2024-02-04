from datetime import datetime
from typing import List, Optional

from app.core.modules.assets.constants import CURRENCIES
from app.core.modules.assets.models import Asset, User


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


async def get_asset(user: User, asset_id: int, ) -> Optional[Asset]:
    asset = await Asset.filter(
        user=user,
        id=asset_id,
    ).first()
    return asset


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

    result = []

    for asset in assets:
        result.append({
            'id': asset.pk,
            'currency': asset.currency,
            'number': asset.number,
            'total_sum': asset.price * asset.number,
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
