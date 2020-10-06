from fastapi import APIRouter

import os
import json
import datetime

from typing import List
from models import PricePlan_Pydantic, PricePlan

router = APIRouter()


@router.get("/priceplans", response_model=List[PricePlan_Pydantic])
async def get_priceplans():
    """
    Get a list of the price plans.
    """
    return await PricePlan_Pydantic.from_queryset(PricePlan.all())


@router.post("/priceplans")
async def parse_priceplans():
    """
    Parse priceplans.json into database.
    """
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


@router.get("/insurance_cost")
async def get_insurance_cost(date: str, cargo_type: str):
    """
    Evaluate insurance cost by date and cargo type.
    """
    typed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    # Getting more closer priceplan by date
    filtered_priceplans = await PricePlan.filter(
        cargo_type=cargo_type,
        active_date__lte=typed_date
    ).order_by("-active_date")

    # Check if price plan found
    if len(filtered_priceplans):
        priceplan = filtered_priceplans[0]
    else:
        return {'insurance_cost': -1, 'error': 'Price plan not found'}

    return {'insurance_cost': priceplan.rate * float(os.environ.get("DECLARED_RATE", 1))}
