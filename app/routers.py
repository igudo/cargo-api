from fastapi import APIRouter

from typing import List
from models import PricePlan_Pydantic, PricePlan

router = APIRouter()


@router.get("/priceplans", response_model=List[PricePlan_Pydantic])
async def get_priceplans():
    return await PricePlan_Pydantic.from_queryset(PricePlan.all())
