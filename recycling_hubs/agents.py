from mesa import Agent
from utils import Status


class RecyclingHub(Agent):
    def __init__(self, unique_id, model, max_capacity=1000.):
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

    def __init__(self, unique_id, model, hub=None, lifespan=20, status=Status.passive, material_amount=0.):
        super().__init__(unique_id, model)
        """reference to the  site"""
        self.lifespan = lifespan
        self.status = status

        """amount of material to generated or needed"""
        self.material_amount: float = material_amount

        self.amount_recycled: float = 0.
        self.amount_hub: float = 0.
        self.amount_non_circular: float = 0.

        self.hub = hub

    def account_material_balance(self):
        return self.material_amount - (self.amount_recycled + self.amount_hub + self.amount_non_circular)


class DemolitionProjectAgent(ProjectAgent):
    """An agent doing a demolition project for a given company"""
    def __init__(self, unique_id, model, hub=None, lifespan=20, status=Status.passive, material_amount=0.):

        super().__init__(unique_id, model, hub=hub, lifespan=lifespan, status=status, material_amount=material_amount)

        """waste generation pattern (amount of waste generated per day)"""
        #self.waste_generation_pattern = waste_generation_pattern
        self.conv_recycling = ConventionalWasteRecycling()

    def step(self):
        current_balance = self.account_material_balance()
        if current_balance == 0.:
            self.status = Status.finished

        if self.status == Status.active:
            self.move()

            if current_balance == 0 and self.status != Status.finished:
                print("NOT FINISHED: {} with BALANCE: {}".format(self.status, current_balance))
            if self.lifespan == 0 and self.status != Status.finished:
                print("NOT FINISHED: {} with lifespan: {}".format(self.status, self.lifespan))

            #if self.lifespan > 0:
            if current_balance > 0.:
                if self.hub is not None:
                    if self.hub.has_capacity():
                        current_balance = self.transfer_to_hub(current_balance)
                else:
                    current_balance = self.transfer_to_construction(current_balance)

            if current_balance == 0.:
                self.status = Status.finished

            # last step with remaining material left.
            if self.lifespan == 1 and current_balance > 0:
                self.conv_recycling.dump(current_balance)
                self.amount_non_circular += current_balance
                self.status = Status.finished

            self.lifespan -= 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def transfer_to_hub(self, amount):
        amount_transfered = min(amount, self.hub.get_available_capacity())
        self.amount_recycled += amount_transfered
        self.hub.load(amount_transfered)
        return self.account_material_balance()

    def transfer_to_construction(self, amount):
        if amount > 0:
            self.recycle(amount)
        return self.account_material_balance()

    def recycle(self, amount):

        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        construction_agents = []
        for c in cellmates:
            if isinstance(c, ConstructionProjectAgent) and c.status == Status.active:
                construction_agents.append(c)

        if len(construction_agents) > 0:
            if len(construction_agents) > 1:
                other = self.random.choice(construction_agents)
            else:
                other = construction_agents[0]

            amount_transfered = min(amount, other.account_material_balance())
            self.amount_recycled += amount_transfered
            other.amount_recycled += amount_transfered


"""Construction agents don't move !!!!!!!!!!!!!"""
class ConstructionProjectAgent(ProjectAgent):
    """An agent doing a demolition project for a given company"""
    def __init__(self, unique_id, model, hub=None, lifespan=20, status=Status.passive, material_amount=0.):
        super().__init__(unique_id, model, hub=hub, lifespan=lifespan, status=status, material_amount=material_amount)

        self.raw_material_supply = RawMaterialSupply()

    def step_old(self):
        # The agent's step will go here.
        if self.lifespan == 0 or self.account_material_balance() == 0.:
            self.status = Status.finished

        self.lifespan -= 1

    def step(self):
        current_balance = self.account_material_balance()
        if current_balance == 0.:
            self.status = Status.finished

        if self.status == Status.active:

            if current_balance == 0 and self.status != Status.finished:
                print("NOT FINISHED: {} with BALANCE: {}".format(self.status, current_balance))
            if self.lifespan == 0 and self.status != Status.finished:
                print("NOT FINISHED: {} with lifespan: {}".format(self.status, self.lifespan))

            # if self.lifespan > 0:
            if current_balance > 0.:
                if self.hub is not None:
                    #if self.hub.has_capacity():
                    current_balance = self.transfer_from_hub(current_balance)
                #else:
                    #current_balance = self.transfer_to_construction(current_balance)

            if current_balance == 0.:
                self.status = Status.finished

            # last step with remaining material left.
            if self.lifespan == 1 and current_balance > 0:
                #print("agent id {}, current balance: {}, non_circular before bying: {}".format(self.unique_id, current_balance, self.amount_non_circular))
                self.raw_material_supply.buy(current_balance)
                self.amount_non_circular += current_balance
                #print("amount non_circular after bying: {}".format(self.amount_non_circular))
                self.status = Status.finished

            self.lifespan -= 1

    def transfer_from_hub(self, amount):
        amount_transfered = min(amount, self.hub.stock_level)
        self.amount_hub += amount_transfered
        self.hub.remove(amount_transfered)
        return self.account_material_balance()

class DemolitionSite:
    """A building to be demolished"""

    def __init__(self, location, size, construction_year, factor_concrete):

        """geo position of the site"""
        self.location = location
        self.construction_year = construction_year
        """size in square meter"""
        self.size = size

        """factor to calculate amount of concrete demolition will generate"""
        self.factor_concrete = factor_concrete

    def calculate_supply(self):
        return self.factor_concrete * self.size



