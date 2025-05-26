from orders import Order, OrderType
from collections import defaultdict
from typing import List


class Market:
    def __init__(self):
        # Separate order books for each resource
        self.buy_orders = defaultdict(list)
        self.sell_orders = defaultdict(list)
        self.price_history = defaultdict(list)

    def place_order(self, order: Order):
        if order.order_type == OrderType.BUY:
            self.buy_orders[order.resource_name].append(order)
        else:
            self.sell_orders[order.resource_name].append(order)

    def match_orders(self):
        """Match buy and sell orders for each resource."""
        for resource in list(self.buy_orders.keys()):
            buys = sorted(self.buy_orders[resource], key=lambda o: o.price_per_unit, reverse=True)
            sells = sorted(self.sell_orders[resource], key=lambda o: o.price_per_unit)

            new_buys, new_sells = [], []
            trades = []

            while buys and sells:
                buy = buys[0]
                sell = sells[0]

                if buy.price_per_unit >= sell.price_per_unit:
                    traded_qty = min(buy.quantity, sell.quantity)
                    trade_price = (buy.price_per_unit + sell.price_per_unit) / 2

                    # Log the trade
                    trades.append({
                        "resource": resource,
                        "quantity": traded_qty,
                        "price": trade_price,
                        "buyer": buy.owner,
                        "seller": sell.owner,
                    })

                    # Update quantities
                    buy.quantity -= traded_qty
                    sell.quantity -= traded_qty

                    if buy.quantity == 0:
                        buys.pop(0)
                    if sell.quantity == 0:
                        sells.pop(0)
                else:
                    # No match possible
                    break

            self.buy_orders[resource] = buys
            self.sell_orders[resource] = sells

            if trades:
                avg_price = sum(t["price"] for t in trades) / len(trades)
                self.price_history[resource].append(avg_price)

    def get_latest_price(self, resource: str):
        if self.price_history[resource]:
            return self.price_history[resource][-1]
        return None
