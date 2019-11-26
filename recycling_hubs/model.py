from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
from agents import DemolitionProjectAgent, ConstructionProjectAgent, RecyclingHub, ConventionalWasteRecycling
from utils import Status, calculate_lifespan


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
    #return 100.

def calculate_not_recycled(model):
    agents_amounts = [agent.amount_non_circular for agent in model.schedule.agents
                      if isinstance(agent, DemolitionProjectAgent)]
    return np.sum(agents_amounts)*1.

def calculate_raw_material_consumed(model):
    agents_amounts = [agent.amount_non_circular for agent in model.schedule.agents
                      if isinstance(agent, ConstructionProjectAgent)]
    return np.sum(agents_amounts)*1.


def get_stock_level_hubs(model):
    hubs = [agent.stock_level for agent in model.schedule.agents if isinstance(agent, RecyclingHub)]
    return np.sum(hubs)*1.


def get_demolition_current_amount(model):
    amount = [agent.current_amount for agent in model.schedule.agents if isinstance(agent, DemolitionProjectAgent)]
    return np.sum(amount)*1.


def get_construction_current_amount(model):
    amount = [agent.current_amount for agent in model.schedule.agents if isinstance(agent, ConstructionProjectAgent)]
    return np.sum(amount)*1.

class ConcreteRecyclingModel(Model):

    """A model with some number of agents."""
    def __init__(self, num_demolition, num_construction, recycling_tendency_percentage, num_hubs=1, event_rate_construction=5., event_rate_demolition=3., width=20, height=20):

        super().__init__()

        self.width = width
        self.height = height

        ## TODO calculate duration
        #self.duration = calculate_lifespan(event_rate)

        self.duration = 37
        self.tick_counter = 0

        self.num_demolition = num_demolition
        self.num_construction = num_construction
        self.recycling_tendency = recycling_tendency_percentage/100
        self.num_hubs = num_hubs

        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={"Amount direct recycled": calculate_recycled,
                             "Amount recycled via hub": calculate_recycled_hub,
                             "Amount not recycled": calculate_not_recycled,
                             "Amount raw material consumed": calculate_raw_material_consumed,
                             "Stock level materials in hubs": get_stock_level_hubs,
                             "Supply demolition materials": get_demolition_current_amount,
                             "Demand construction materials": get_construction_current_amount},

            agent_reporters={"Amount": lambda agent: agent.unique_id})

        # create construction hubs
        if num_hubs > 0:
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

            a = DemolitionProjectAgent(self.next_id(), self, recycling_tendency=self.recycling_tendency,
                                       hub=hub, event_rate=event_rate_demolition, status=Status.passive, total_amount=100.)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

        for i in range(self.num_construction):
            hub = None
            if num_hubs > 0:
                hub = random.choice(hubs)

            a = ConstructionProjectAgent(self.next_id(), self,
                                         hub=hub, event_rate=event_rate_construction, status=Status.active, total_amount=100.)
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
