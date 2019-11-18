# Agent based modeling 

Goal: Simulation of stakeholder behavior of recycling concrete ...

Agent Definition (TODO move agent def to separate file)
## Demolition Company Agent

### Attributes 	
       
	name: factor indicating capability to recycle concrete for construction
	type: double

	name: project ids
	type: list of unique keys to demolition projects, initialized at startup


	name: total amount (in cubic meter) of recycled waste for construction use
	type: integer

	name: total amount (in cubic meter) of recycled waste
   	 type: integer

### Behavior

## Demolition Project Manager Agent
Attributes
	name:company
	type:string

	name: projectId, reference to current demolition site
	type: integer

	name: attitude towards  concrete waste generating behavior: 
    	type: enum {with/without the presence of impurities)


## Demolition Site Agent
Attributes
	name:projectId
	type: unique key

	name:location
	type:geoposition
	
	name: size in square meters
	type: int

	name: constructin year
	type: int

	name:total mass
	type: absolute mass in cubic meters
	
	name: waste generation pattern (amount of waste generated per day)
	type: function (or parameter of Poisson distribution used)
https://www.sciencedirect.com/topics/mathematics/poisson-distribution


