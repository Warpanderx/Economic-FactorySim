from market import Market
from orders import Order
from factories import Factory, FactoryManager
import random
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, market: Market):
        self.market = market
        self.tick_count = 0
        self.factory_manager = FactoryManager()
        self.production_history = {}  # Tracks factory outputs over time
        self.setup_factories()

    def setup_factories(self):
        factory = Factory(
            id="f1",
            owner="npc_factory_1",
            input_requirements={"iron_ore": 2},
            output_production={"iron_plate": 1},
            production_time=2
        )
        self.factory_manager.add_factory(factory)


