from enum import Enum
from pydantic import BaseModel
from uuid import uuid4
from typing import Literal


class OrderType(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Order(BaseModel):
    id: str
    resource_name: str
    quantity: int
    price_per_unit: float
    order_type: OrderType
    owner: str  # Player or NPC ID

    def total_price(self) -> float:
        return self.quantity * self.price_per_unit

    @classmethod
    def create(cls, resource_name: str, quantity: int, price_per_unit: float, order_type: Literal["buy", "sell"], owner: str):
        return cls(
            id=str(uuid4()),
            resource_name=resource_name,
            quantity=quantity,
            price_per_unit=price_per_unit,
            order_type=OrderType(order_type),
            owner=owner,
        )
