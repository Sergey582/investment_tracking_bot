from app.api.public.modules.assets.serializers import (AssetResponse,
                                                       AssetsListData,
                                                       CreateAssetRequest,
                                                       CurrenciesListData,
                                                       ExpensesQueryFilters,
                                                       Pagination)
from app.core.modules.assets.models import User
from app.core.modules.assets.services import (create_asset, delete_asset,
                                              get_all_currencies, get_asset,
                                              get_assets, get_last_asset_id)
from app.core.modules.users.auth import user_auth_check
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import Response

router = APIRouter()


@router.get(
    "/currencies",
    tags=["asset"],
    summary="Get available currencies",
    response_model=CurrenciesListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_all_categories(
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/assets/{asset_id}",
    tags=["asset"],
    summary="Get asset by id",
    response_model=AssetResponse,
    status_code=status.HTTP_200_OK,
)
async def router_get_asset_by_id(
        asset_id: int,
        user: User = Depends(user_auth_check),
):
    asset = await get_asset(asset_id=asset_id, user=user)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="expense id does not exist")
    return AssetResponse(
        currency=asset.currency,
        number=asset.number,
        name=asset.name,
        price=asset.price,
        average_price=12.3,
        daily_pnl="test",
        total_pnl="test",
        transaction_date=asset.transaction_date,
        created_at=asset.created_at,
        updated_at=asset.updated_at,
    )


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
        asset_id: int,
        user: User = Depends(user_auth_check),
):
    await delete_asset(asset_id=asset_id, user=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/assets/",
    tags=["asset"],
    summary="Get list of assets",
    response_model=AssetsListData,
    status_code=status.HTTP_200_OK,
)
async def router_get_assets(
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
