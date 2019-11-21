from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from agents import DemolitionProjectAgent, ConstructionProjectAgent, RecyclingHub
from model import ConcreteRecyclingModel
from utils import Status


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true"
    }

    if isinstance(agent, RecyclingHub):
        #portrayal["text"] = agent.max_capacity
        portrayal["Layer"] = 0
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        portrayal["Color"] = "yellow"

    if isinstance(agent, DemolitionProjectAgent):
        portrayal["Layer"] = 1
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.8
        portrayal["w"] = 0.8
        #portrayal["text"] = str(agent.material_amount)

        if agent.status == Status.finished:
            portrayal["Color"] = "grey"
        else:
            portrayal["Color"] = "green"

    elif isinstance(agent, ConstructionProjectAgent):
        portrayal["Layer"] = 2
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5

        if agent.status == Status.finished:
            portrayal["Color"] = "grey"

        else:
            portrayal["Color"] = "blue"

    return portrayal


#create a 10x10 grid drawn in 500x500 pixels
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# Dark Green
RECYCLING_COLOR = "#0C7C00"
# Dark Blue
RECYCLING_VIA_HUB_COLOR = "#000C7C"
# Dark magenta
HUB_COLOR = "#70007C"

# Red
NON_CIRCULAR_COLOR = "#FF3C33"

line_chart = ChartModule([{"Label": "Amount direct recycled", "Color": RECYCLING_COLOR},
                          {"Label": "Amount reycled via hub", "Color": RECYCLING_VIA_HUB_COLOR},
                          {"Label": "Stock level hubs", "Color": HUB_COLOR}])

model_params_old = {"num_demolition": 20,
                "num_construction": 10,
                "width": 20,
                "height": 20}

model_params = {"num_demolition": UserSettableParameter("slider", "Agents", 20, 1, 50,
                      description="Initial Number of Demolition Project Agents"),
                "num_construction": 20,
                "duration": 25}

# create server, the last params are params needed by the money model:
# number of agents:100, height and width:10
server = ModularServer(ConcreteRecyclingModel,
                       [grid, line_chart],
                       "ConcreteRecyclingModel",
                      model_params=model_params)



#define port and launch the server
server.port = 8521
