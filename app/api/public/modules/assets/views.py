import os

from app.api.public.modules.assets.serializers import (
    AssetHistoryListResponse, AssetResponse, AssetsListData,
    CreateAssetRequest, CurrenciesListData, ExpensesQueryFilters, Pagination, TickersListData)
from app.core.modules.assets.models import User
from app.core.modules.assets.services import (create_asset, delete_asset,
                                              get_all_currencies, get_asset,
                                              get_asset_history, get_assets,
                                              get_last_asset_id, get_tickers)
from app.core.modules.users.auth import user_auth_check
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status

router = APIRouter()


@router.get(
    "/currencies",
    tags=["asset"],
    summary="Get available currencies",
    response_model=CurrenciesListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_all_categories(
        response: Response,
        user: User = Depends(user_auth_check),
):
    data = get_all_currencies()
    return CurrenciesListData(data=data)


@router.post(
    "/assets",
    tags=["asset"],
    summary="Create asset",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_create_asset(
        request_data: CreateAssetRequest,
        user: User = Depends(user_auth_check),
):
    await create_asset(
        user=user,
        number=request_data.number,
        currency=request_data.currency,
        name=request_data.name,
        price=request_data.price,
        transaction_date=request_data.transaction_date,
    )
    r = Response(status_code=status.HTTP_204_NO_CONTENT)
    return r


@router.get(
    "/assets/{asset_name}",
    tags=["asset"],
    summary="Get asset by asset_name",
    response_model=AssetResponse,
    status_code=status.HTTP_200_OK,
)
async def router_get_asset_by_id(
        response: Response,
        asset_name: str,
        user: User = Depends(user_auth_check),
):
    asset = await get_asset(asset_name=asset_name, user=user)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="expense id does not exist")
    return AssetResponse(**asset)


@router.get(
    "/assets/{asset_name}/history",
    tags=["asset"],
    summary="Get asset history",
    response_model=AssetHistoryListResponse,
    status_code=status.HTTP_200_OK,
)
async def router_get_asset_by_id(
        response: Response,
        name: str,
        user: User = Depends(user_auth_check),
):
    assets = await get_asset_history(asset_name=name, user=user)
    return AssetHistoryListResponse(assets=assets)


#
#
# @router.patch(
#     "/expense/{expense_id}",
#     tags=["expense"],
#     summary="Update expense",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def router_update_expense(
#         expense_id: int,
#         data: UpdateExpenseRequest,
#         user: User = Depends(user_auth_check),
# ):
#     await update_expense(
#         user=user,
#         expense_id=expense_id,
#         currency=data.currency,
#         category=data.category,
#         amount=data.amount,
#         transaction_date=data.transaction_date,
#     )
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# Create a route to delete an expense by ID
@router.delete(
    "/expenses/{asset_id}",
    tags=["asset"],
    summary="Delete asset",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_delete_expense(
        response: Response,
        asset_id: int,
        user: User = Depends(user_auth_check),
):
    await delete_asset(asset_id=asset_id, user=user)
    r = Response(status_code=status.HTTP_204_NO_CONTENT)
    r.headers["Access-Control-Allow-Origin"] = os.environ["host"]
    return r


@router.get(
    "/assets/",
    tags=["asset"],
    summary="Get list of assets",
    response_model=AssetsListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_assets(
        response: Response,
        pagination: Pagination = Depends(),
        filters: ExpensesQueryFilters = Depends(),
        user: User = Depends(user_auth_check),
):
    messages = await get_assets(
        user=user,
        from_id=pagination.from_id,
        limit=pagination.limit,
        transaction_date_from=filters.transaction_date_from,
        transaction_date_to=filters.transaction_date_to,
    )

    messages, next_id = get_last_asset_id(messages, pagination.limit)
    return AssetsListData(messages=messages, next_id=next_id)


@router.get(
    "/tickers/",
    tags=["asset"],
    summary="Get list of available tickers",
    response_model=TickersListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_assets(
        user: User = Depends(user_auth_check),
):
    tickers = await get_tickers()

    return TickersListData(tickers=tickers)
