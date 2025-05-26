from enum import Enum
from pydantic import BaseModel


class ResourceType(str, Enum):
    RAW = "raw"
    INTERMEDIATE = "intermediate"
    FINAL = "final"


class Resource(BaseModel):
    name: str
    type: ResourceType
    base_value: float

RESOURCE_CATALOG = {
    "iron_ore": Resource(name="Iron Ore", type=ResourceType.RAW, base_value=5),
    "copper_ore": Resource(name="Copper Ore", type=ResourceType.RAW, base_value=4),
    "iron_plate": Resource(name="Iron Plate", type=ResourceType.INTERMEDIATE, base_value=10),
    "circuit_board": Resource(name="Circuit Board", type=ResourceType.FINAL, base_value=20),
} #These are all subject to change and names will almost certainly change.

