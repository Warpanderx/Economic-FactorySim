class Inventory:
    def __init__(self):
        self.resources = {}  # {resource_name: quantity}

    def add(self, resource: str, amount: int):
        if amount <= 0:
            return
        self.resources[resource] = self.resources.get(resource, 0) + amount

    def remove(self, resource: str, amount: int) -> bool:
        if self.resources.get(resource, 0) >= amount:
            self.resources[resource] -= amount
            return True
        return False

    def has(self, resource: str, amount: int) -> bool:
        return self.resources.get(resource, 0) >= amount

    def get(self, resource: str) -> int:
        return self.resources.get(resource, 0)

    def get_all(self) -> dict:
        return dict(self.resources)

    def __repr__(self):
        return str(self.resources)
