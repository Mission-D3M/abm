import enum
from scipy.stats import poisson

"double liefspan with regard to 0.99 percentile"
def calculate_lifespan(event_rate, loc=0):
    ls = int(round(poisson.ppf(0.9999, event_rate, loc=loc))) * 2 + 5
    print("lifespan for event_rate: {} is: {}".format(event_rate, ls))
    return ls

def calculate_flow(amount, t, event_rate, loc):
    value = poisson.pmf(t, event_rate, loc=loc) * amount
    return value

class Status(enum.Enum):
    passive = 'passive'
    active = 'active'
    lifespan_alert = 'lifespan alert'
    finished = 'finished'
    incomplete = 'incomplete'
