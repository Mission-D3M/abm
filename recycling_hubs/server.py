from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from agents import DemolitionProjectAgent, ConstructionProjectAgent, RecyclingHub
from model import ConcreteRecyclingModel
from utils import Status


# Dark Green
RECYCLING_COLOR = "#0C7C00"
# Dark Blue
RECYCLING_VIA_HUB_COLOR = "#000C7C"
# Dark magenta
HUB_COLOR = "#70007C"

# Red
NOT_RECYCLED_COLOR = "#FF3C33"

# Orange
RAW_MATERIAL_CONSUMED_COLOR = "orange"


def agent_portrayal(agent):
    portrayal = {"Filled": "true",
                 "Layer": 0
    }
    if isinstance(agent, RecyclingHub):
        portrayal["Layer"] = 0
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.8
        portrayal["w"] = 0.8
        portrayal["Color"] = HUB_COLOR

    if isinstance(agent, DemolitionProjectAgent):
        portrayal["Layer"] = 1
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        #portrayal["text"] = str(agent.material_amount)

        if agent.status == Status.finished:
            portrayal["Color"] = "grey"
        elif agent.is_recycling:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "brown"

    elif isinstance(agent, ConstructionProjectAgent):
        portrayal["Layer"] = 2
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5

        if agent.status == Status.finished:
            portrayal["Color"] = "grey"

        else:
            portrayal["Color"] = "blue"
    return portrayal


#create a 20x20 grid drawn in 500x500 pixels
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)


line_chart_recycling = ChartModule([{"Label": "Amount direct recycled", "Color": RECYCLING_COLOR},
                                    {"Label": "Amount recycled via hub", "Color": RECYCLING_VIA_HUB_COLOR},
                                    {"Label": "Amount not recycled", "Color": NOT_RECYCLED_COLOR},
                                    {"Label": "Amount raw material consumed", "Color": RAW_MATERIAL_CONSUMED_COLOR}])

line_chart_material_flow = ChartModule([{"Label": "Supply demolition materials", "Color": "red"},
                                        {"Label": "Demand construction materials", "Color": "green"},
                                        {"Label": "Stock level materials in hubs", "Color": HUB_COLOR}])

model_params = {"num_demolition": UserSettableParameter("slider", "Demolition projects", 20, 1, 50,
                      description="Number of demolition project agents"),
                "num_construction": UserSettableParameter("slider", "Construction projects", 40, 1, 50,
                      description="Number of construction project agents"),
                "num_hubs": UserSettableParameter("slider", "Number of recycling hubs", 1, 0, 7,
                      description="Number of recycling hub agents"),
                "event_rate_demolition": UserSettableParameter("slider", "Event rate for demolition", 3., 0.5, 10.,
                      description="Average time between events, this determines the pattern of generated demolition material"),
                "event_rate_construction": UserSettableParameter("slider", "Event rate for construction", 5., 0.5, 10.,
                      description="Average time between events, this determines the demand pattern for construction material"),
                "recycling_tendency_percentage": UserSettableParameter("slider", "Demolition agent's tendency(%) towards recycling", 100., 0.,100.,
                      description="Probability that a demolition chooses to recycle waste")}

server = ModularServer(ConcreteRecyclingModel,
                       [grid, line_chart_recycling, line_chart_material_flow],
                       "ConcreteRecyclingModel",
                      model_params=model_params)



#define port and launch the server
server.port = 8521
