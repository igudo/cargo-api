from fastapi import APIRouter

import json
import datetime

from typing import List
from models import PricePlan_Pydantic, PricePlan

router = APIRouter()


@router.get("/priceplans", response_model=List[PricePlan_Pydantic])
async def get_priceplans():
    return await PricePlan_Pydantic.from_queryset(PricePlan.all())


@router.post("/priceplan")
async def parse_priceplans():
    try:
        with open("priceplans.json") as json_file:
            data = json.load(json_file)
            for date in data:
                typed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

                for priceplan in data[date]:
                    await PricePlan.get_or_create(
                        active_date=typed_date,
                        cargo_type=priceplan['cargo_type'],
                        rate=float(priceplan['rate']),
                    )
    except Exception as e:
        return {'success': False, 'error': str(e)}
    return {'success': True}
