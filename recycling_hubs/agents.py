import numpy as np
from mesa import Agent
from utils import Status, calculate_flow, calculate_lifespan


class RecyclingHub(Agent):
    def __init__(self, unique_id, model, max_capacity=100.):
        super().__init__(unique_id, model)
        self.stock_level: float = 0.
        self.max_capacity = max_capacity

    def get_available_capacity(self):
        return self.max_capacity-self.stock_level

    def has_capacity(self):
        return self.get_available_capacity() > 0

    def load(self, amount):
        if self.stock_level + amount > self.max_capacity:
            raise ValueError
        else:
            self.stock_level += amount
            #print("new stock level: {}".format(self.stock_level))

    def remove(self, amount):
        if amount > self.stock_level:
            raise ValueError("stock level not high enough")
        else:
            self.stock_level -= amount

    def step(self):
        if self.stock_level > self.max_capacity:
            print("+++++++++++++++FULL+++++++++++++++")


class ConventionalWasteRecycling:
    def __init__(self):
        self.amount_transfered = 0.

    def dump(self, amount):
        self.amount_transfered += amount


class RawMaterialSupply:
    def __init__(self):
        self.amount_transfered = 0.

    def buy(self, amount):
        self.amount_transfered += amount


class ProjectAgent(Agent):

    def __init__(self, unique_id, model, hub=None, event_rate=5., status=Status.passive, total_amount=0.):
        super().__init__(unique_id, model)

        self.max_lifespan = calculate_lifespan(event_rate)
        self.EPS = 0.09

        #self.lifespan = 0
        self.running_time = 0
        self.status = status

        """total amount of material generated or needed"""
        self.total_amount: float = total_amount
        self.amount_recycled: float = 0.
        self.amount_hub: float = 0.
        self.amount_non_circular: float = 0.

        self.hub = hub
        self.current_amount = 0.
        self.is_recycling = True
        self.event_rate = event_rate
        self.loc = 0.

    def total_amount_balance(self):
        return self.total_amount - (self.amount_recycled + self.amount_hub + self.amount_non_circular)

    def advance_amount_one_step(self):
        time = self.running_time
        delta_amount = calculate_flow(self.total_amount, time, event_rate=self.event_rate, loc=self.loc)
        self.current_amount += delta_amount

    def step(self):
        self.advance_amount_one_step()

        if self.status == Status.passive:
            if self.current_amount > self.EPS:
                self.status = Status.active
        elif self.status == Status.active:

            if self.total_amount_balance() < self.EPS:
                print("finished")
                self.status = Status.finished
            else:
                self.do_business()

                if self.total_amount_balance() < self.EPS:
                    self.status = Status.finished
            #last step
            if self.max_lifespan - self.running_time == 1:
                self.status = Status.lifespan_alert
        elif self.status == Status.lifespan_alert:
            self.do_business()
            if self.total_amount_balance() > self.EPS:
                self.do_wrap_up()
                self.status = Status.incomplete
            else:
                self.status = Status.finished
        elif self.status == Status.finished:
            pass
        elif self.status == Status.incomplete:
            pass
        else:
            print("unhandled status: {}".format(self.status))
        self.running_time += 1


class DemolitionProjectAgent(ProjectAgent):
    """An agent doing a demolition project for a given company"""
    def __init__(self, unique_id, model, recycling_tendency=1., hub=None, event_rate=7, status=Status.passive, total_amount=0.):

        super().__init__(unique_id, model, hub=hub, event_rate=event_rate, status=status, total_amount=total_amount)

        self.is_recycling = self.calculate_recycling(recycling_tendency)
        self.conv_recycling = ConventionalWasteRecycling()

    def calculate_recycling(self, recycling_tendency):
        recycling_variants = ['R', 'NR']
        recycling_distribution = [recycling_tendency, 1 - recycling_tendency]
        chosen_recycling_variant = np.random.choice(recycling_variants, 1, p=recycling_distribution, replace=True)
        return chosen_recycling_variant == 'R'

    def step(self):
        super().step()

    def do_business(self):
        self.move()
        amount = self.current_amount

        if self.is_recycling:
            if self.hub is not None and self.hub.has_capacity():
                self.transfer_to_hub(amount)
            else:
                self.transfer_to_construction(amount)
        else:
            self.transfer_to_conv_recycling(amount)

    def do_wrap_up(self):
        amount = self.total_amount_balance()
        self.conv_recycling.dump(amount)
        self.amount_non_circular += amount
        self.current_amount -= amount
        if abs(self.current_amount) > self.EPS:
            print("++++++++++++++ something miss with current amount: {}".format(self.current_amount))


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def transfer_to_conv_recycling(self, amount):
        self.conv_recycling.dump(amount)
        self.amount_non_circular += amount
        self.current_amount -= amount

    def transfer_to_hub(self, amount):
        amount_transfered = min(amount, self.hub.get_available_capacity())
        self.amount_hub += amount_transfered
        self.hub.load(amount_transfered)
        self.current_amount -= amount_transfered

    def transfer_to_construction(self, amount):

        neighbours = self.model.grid.get_neighbors(self.pos, moore=False, include_center=True)
        construction_agents = []
        for n in neighbours:
            if isinstance(n, ConstructionProjectAgent) and n.status == Status.active:
                construction_agents.append(n)

        if len(construction_agents) > 0:
            if len(construction_agents) > 1:
                other = self.random.choice(construction_agents)
            else:
                other = construction_agents[0]
            amount_transfered = min(amount, other.current_amount)
            self.current_amount -= amount_transfered
            other.current_amount -= amount_transfered
            self.amount_recycled += amount_transfered
            other.amount_recycled += amount_transfered


class ConstructionProjectAgent(ProjectAgent):
    """An agent doing a demolition project for a given company"""
    def __init__(self, unique_id, model, hub=None, event_rate=10, status=Status.passive, total_amount=0.):
        super().__init__(unique_id, model, hub=hub, event_rate=event_rate, status=status, total_amount=total_amount)

        self.raw_material_supply = RawMaterialSupply()
        self.loc = 2.


    def do_business(self):
        amount = self.current_amount

        # for now always recycling.
        if self.is_recycling:
            if self.hub is not None:
                self.transfer_from_hub(amount)

    def transfer_from_hub(self, amount):
        amount_transfered = min(amount, self.hub.stock_level)
        self.amount_hub += amount_transfered
        self.hub.remove(amount_transfered)
        self.current_amount -= amount_transfered

    def do_wrap_up(self):
        amount = self.total_amount_balance()
        self.raw_material_supply.buy(amount)
        self.amount_non_circular += amount
        self.current_amount -= amount

        # TODO sometimes this goes wrong!
        if abs(self.current_amount) > self.EPS:
            print("++++++++++++++ something miss with current amount: {}, setting it to 0.".format(self.current_amount))
            self.current_amount = 0.

    def step(self):
        super().step()

