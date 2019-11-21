from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
from agents import ProjectAgent, DemolitionProjectAgent, ConstructionProjectAgent, RecyclingHub
from utils import Status


"""only count once, we take the construction side"""
def calculate_recycled(model):
    construction_agents_amounts = [agent.amount_recycled for agent in model.schedule.agents
                                   if isinstance(agent, ConstructionProjectAgent)]
    return np.sum(construction_agents_amounts)


"""only count once, we take the construction side"""
def calculate_recycled_hub(model):
    construction_agents_amounts = [agent.amount_hub for agent in model.schedule.agents
                                   if isinstance(agent, ConstructionProjectAgent)]
    return np.sum(construction_agents_amounts)*1.


def calculate_non_circular(model):
    agents_amounts = [agent.amount_non_circular for agent in model.schedule.agents
                      if isinstance(agent, ProjectAgent)]
    return np.sum(agents_amounts)*1.


def get_stock_level_hubs(model):
    hubs = [agent.stock_level for agent in model.schedule.agents if isinstance(agent, RecyclingHub)]
    return np.sum(hubs)*1.

class ConcreteRecyclingModel(Model):

    """A model with some number of agents."""
    def __init__(self, num_demolition, num_construction, num_hubs=1, duration=365, width=20, height=20):

        super().__init__()

        self.width = width
        self.height = height
        self.duration = duration
        self.tick_counter = 0

        self.num_demolition = num_demolition
        self.num_construction = num_construction
        self.num_hubs = num_hubs

        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={"Amount direct recycled": calculate_recycled,
                             "Amount recycled via hub": calculate_recycled_hub,
                             "Stock level hubs": get_stock_level_hubs},

            agent_reporters={"Amount": lambda agent: agent.unique_id})

        # create construction hubs
        hubs = []
        for i in range(self.num_hubs):
            a = RecyclingHub(self.next_id(), self)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))
            hubs.append(a)
            self.schedule.add(a)


        # Create agents
        for i in range(self.num_demolition):
            hub = None
            if num_hubs > 0:
                hub = random.choice(hubs)

            a = DemolitionProjectAgent(self.next_id(), self, hub=hub, status=Status.active, material_amount=100.)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

        for i in range(self.num_construction):
            a = ConstructionProjectAgent(self.next_id(), self, status=Status.active, material_amount=70.)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)



        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
        self.tick_counter += 1
        if self.tick_counter >= self.duration:
            self.running = False