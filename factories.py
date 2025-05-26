from inventory import Inventory


class Factory:
    def __init__(self, id: str, owner: str, input_requirements: dict, output_production: dict, production_time: int):
        self.id = id
        self.owner = owner
        self.input_requirements = input_requirements  # e.g., {"iron_ore": 2}
        self.output_production = output_production    # e.g., {"iron_plate": 1}
        self.production_time = production_time        # number of ticks to produce
        self.current_timer = 0
        self.active = False
        self.inventory = Inventory()  # Each factory has its own storage

    def tick(self):
        if self.active:
            self.current_timer -= 1
            if self.current_timer <= 0:
                for resource, amount in self.output_production.items():
                    self.inventory.add(resource, amount)
                self.active = False
        else:
            # Check if we have all required inputs
            if all(self.inventory.has(res, amt) for res, amt in self.input_requirements.items()):
                for res, amt in self.input_requirements.items():
                    self.inventory.remove(res, amt)
                self.current_timer = self.production_time
                self.active = True


class FactoryManager:
    def __init__(self):
        self.factories = []

    def add_factory(self, factory: Factory):
        self.factories.append(factory)

    def feed_all(self, resources_per_factory: dict):
        """
        resources_per_factory: {
            "npc_factory_1": {"iron_ore": 5},
            "npc_factory_2": {"copper": 3}
        }
        """
        for factory in self.factories:
            if factory.owner in resources_per_factory:
                for resource, amount in resources_per_factory[factory.owner].items():
                    factory.inventory.add(resource, amount)

    def tick_all(self):
        for factory in self.factories:
            factory.tick()

    def collect_all_outputs(self) -> dict:
        outputs = {}
        for factory in self.factories:
            owner = factory.owner
            for resource, amount in factory.inventory.get_all().items():
                if amount > 0:
                    outputs.setdefault(owner, {}).setdefault(resource, 0)
                    outputs[owner][resource] += amount
                    factory.inventory.remove(resource, amount)
        return outputs
