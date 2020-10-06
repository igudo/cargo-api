from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class PricePlan(models.Model):
    """
    The Price Plan model
    """

    id = fields.IntField(pk=True)
    cargo_type = fields.CharField(max_length=30, default="misc")
    rate = fields.FloatField()
    active_date = fields.DateField()

PricePlan_Pydantic = pydantic_model_creator(PricePlan, name="PricePlan")
