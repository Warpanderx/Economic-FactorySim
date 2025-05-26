from market import Market
from orders import Order
from factories import Factory, FactoryManager
import matplotlib.pyplot as plt
import random


class Simulation:
    def __init__(self, market: Market):
        self.market = market
        self.tick_count = 0
        self.factory_manager = FactoryManager()
        self.production_history = {}
        self.setup_factories()

    def setup_factories(self):
        # One example factory that turns iron_ore into iron_plate
        factory = Factory(
            id="f1",
            owner="npc_factory_1",
            input_requirements={"iron_ore": 2},
            output_production={"iron_plate": 1},
            production_time=2
        )
        self.factory_manager.add_factory(factory)

    def run_tick(self):
        self.tick_count += 1
        print(f"\n--- Tick {self.tick_count} ---")

        # Simulate NPC buy/sell orders
        self.simulate_npc_trading()

        # Feed factories (simulate free iron_ore for now)
        self.factory_manager.feed_all({
            "npc_factory_1": {"iron_ore": 2}
        })

        # Tick factories
        self.factory_manager.tick_all()

        # Collect outputs from factories
        produced = self.factory_manager.collect_all_outputs()
        for owner, outputs in produced.items():
            print(f"{owner} produced: {outputs}")

            # Track production history
            if owner not in self.production_history:
                self.production_history[owner] = {}
            for resource, qty in outputs.items():
                if resource not in self.production_history[owner]:
                    self.production_history[owner][resource] = []
                self.production_history[owner][resource].append(qty)

        # Ensure every resource has an entry for this tick, even if 0
        for owner in self.production_history:
            for resource in self.production_history[owner]:
                if resource not in produced.get(owner, {}):
                    self.production_history[owner][resource].append(0)

        # Match trade orders in the market
        self.market.match_orders()

        # Print latest prices
        for resource, price_list in self.market.price_history.items():
            if price_list:
                print(f"{resource} latest price: {price_list[-1]}")

    def simulate_npc_trading(self):
        """Fake some NPC behavior — randomly place buy/sell orders."""
        resources = ["iron_plate", "circuit_board"]
        for resource in resources:
            if random.random() < 0.5:
                # Sell order
                price = round(random.uniform(6, 12), 2)
                qty = random.randint(5, 15)
                order = Order.create(resource, qty, price, "sell", "npc_vendor")
                self.market.place_order(order)
            else:
                # Buy order
                price = round(random.uniform(7, 13), 2)
                qty = random.randint(3, 10)
                order = Order.create(resource, qty, price, "buy", "npc_buyer")
                self.market.place_order(order)

    def plot_overview(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Plot production - sum all resource amounts per tick per owner
        for owner, productions in self.production_history.items():
            # productions is a list of dicts {resource: amount}
            # sum values in each dict for total units produced at that tick
            total_units = [sum(prod.values()) if isinstance(prod, dict) else prod for prod in productions]
            ax1.plot(total_units, label=owner)

        ax1.set_title("Factory Production Over Time")
        ax1.set_xlabel("Tick")
        ax1.set_ylabel("Units Produced")
        ax1.legend()
        ax1.grid(True)

        # Plot resource prices
        for resource, prices in self.market.price_history.items():
            if prices:
                ax2.plot(prices, label=resource)

        ax2.set_title("Resource Prices Over Time")
        ax2.set_xlabel("Tick")
        ax2.set_ylabel("Price")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

