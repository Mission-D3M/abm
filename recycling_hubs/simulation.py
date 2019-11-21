from model import ConcreteRecyclingModel
import matplotlib.pyplot as plt


def collect_data():
    model = ConcreteRecyclingModel(20, 10, 20, 20)
    for i in range(50):
        model.step()
    amount = model.datacollector.get_model_vars_dataframe()
    amount.plot()

    agent_amount = model.datacollector.get_agent_vars_dataframe()
    print(agent_amount.head())

    plt.show()

collect_data()