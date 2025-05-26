from market import Market
from simulation import Simulation

market = Market()
sim = Simulation(market)

for _ in range(100000):
    sim.run_tick()

sim.plot_overview()