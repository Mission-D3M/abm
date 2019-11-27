#  Agent-based Modeling for D3M



## Summary


## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## Interactive Model Run

To run the model interactively, open a terminal window in the  `recycling_hub` directory and use `mesa runserver`:

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/), select the model parameters, press Reset, then Start.

## Files

* ``recycling_hub/utils.py``: Defines general functions.
* ``recycling_hub/agents.py``: Defines the agent classes.
* ``recycling_hub/model.py``: Defines the model and the DataCollector functions.
* ``recycling_hub/server.py``: Sets up the interactive visualization server.
* ``recycling_hub/run.py``: Launches a model visualization server.


