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


#create a 10x10 grid drawn in 500x500 pixels
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)


line_chart_recycling = ChartModule([{"Label": "Amount direct recycled", "Color": RECYCLING_COLOR},
                          {"Label": "Amount recycled via hub", "Color": RECYCLING_VIA_HUB_COLOR},
                          {"Label": "Stock level hubs", "Color": HUB_COLOR},
                          {"Label": "Amount not recycled", "Color": NOT_RECYCLED_COLOR},
                          {"Label": "Amount raw material consumed", "Color": RAW_MATERIAL_CONSUMED_COLOR}])

line_chart_material_flow = ChartModule([{"Label": "Demolition Material Flow", "Color": "red"},
                          {"Label": "Construction Material Flow", "Color": "green"}])

model_params = {"num_demolition": UserSettableParameter("slider", "Demolition Projects", 20, 1, 50,
                      description="Initial Number of Demolition Project Agents"),

                "num_construction": UserSettableParameter("slider", "Construction Projects", 20, 1, 50,
                      description="Initial Number of Construction Project Agents"),
                "num_hubs": UserSettableParameter("slider", "Number of Recycling Hubs", 1, 0, 7,
                      description="Number Recycling Hub Agents"),
                "event_rate": UserSettableParameter("slider", "Event Rate for Demolition", 5., 0.5, 10.,
                      description="Event rate determines pattern of demolition and construction material flow"),
                "recycling_tendency_percentage": UserSettableParameter("slider", "Demolition Agent's tendency towards Recycling", 100., 0.,100.,
                      description="Probability that a demolition chooses to recycle waste")}

# create server, the last params are params needed by the money model:
# number of agents:100, height and width:10
server = ModularServer(ConcreteRecyclingModel,
                       [grid, line_chart_recycling, line_chart_material_flow],
                       "ConcreteRecyclingModel",
                      model_params=model_params)



#define port and launch the server
server.port = 8521
