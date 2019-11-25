import enum
from scipy.stats import poisson

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1, 1)
# mu = 10

# x = np.arange(poisson.ppf(0.01, mu), poisson.ppf(0.99, mu))
# print(x)
# x = range(-10,20)
# ax.plot(x, poisson.pmf(x, mu, loc=5), 'bo', ms=8, label='poisson pmf')
# ax.vlines(x, 0, poisson.pmf(x, mu, loc=5), colors='b', lw=5, alpha=0.5)
# plt.show()

"double liefspan with regard to 0.99 percentile"
def calculate_lifespan(event_rate, loc=0):
    return int(round(poisson.ppf(0.9999, event_rate, loc=loc)))*2

def calculate_flow(amount, t, event_rate, loc):
    value = poisson.pmf(t, event_rate, loc=loc) * amount
    return value

class Status(enum.Enum):
    passive = 'passive'
    active = 'active'
    lifespan_alert = 'lifespan alert'
    finished = 'finished'
    incomplete = 'incomplete'
