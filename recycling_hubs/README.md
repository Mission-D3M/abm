# Agent based modeling 

The goal of this protoype is as follows:
Construction hubs improve the circularity in the construction sector 
by optimizing the alignment of material flow from demolition to construction sites

We prove that by simulating the interactions of demolition and construction companies, 
represented by project agents by assessing their effects on the reverse logistics of the construction sector in the province.


## Model Specification

The objective is to build a model capable of capturing the dynamic and interactive nature of main stakeholders 
involved in the reverse logistics of demolition waste material.
Agents involved besides demolition and construction companies, 
are agents in the waste material generation and management
chains such as transportation companies, material reusing companies, recycling companies, and waste incinerators.

For the model of a prototype, we aim for simplicity. 
Therefore we identify a subset of the potential agents with which realistic behaviour generation is still possible. 
Agents identified are construction and demolition project agents, 
construction hub agent, conventional recycling agent, and raw material delivering agent.

### Demolition Project Agent
- Demolishes buildings and generates a progressive waste material flow within a defined period
- Can search for a construction agent to cooperate with
- Decides on the kind of demolition process: whether artifacts should be circularly reused for construction or not
- Decides on how the waste material processing is continued: directly delivered to construction project agents site, 
construction hub or conventional recycled. 

### Construction Project Agent
- Constructs buildings and consumes construction material with a specific time pattern
- Accepts recycled material whenever available form construction hub or demolition project agents
- Only buys raw material at the latest time and only when resources from construction hubs are exhausted

### Construction Hub Agent
- Provides storage capacity for recycled material
- Provides info on stock level
- Rejects storage requests if capacity is reached

### Waste Recycling Agent
- Accepts all offered material

### Raw Material Supply Agent
- Fulfills all requests for raw material
	
	


