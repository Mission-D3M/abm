

# Agent based modeling 

Goal: Simulation of stakeholder behavior of recycling concrete ...

## Demolition Company Agent

### Attributes 	
       
    name:company name
	type:string
    
    name: factor indicating capability to recycle concrete for construction
	type: double

	name: project ids
	type: list of unique keys to demolition projects, initialized at startup


	name: total amount (in cubic meter) of recycled waste for construction use
	type: integer

	name: total amount (in cubic meter) of recycled waste
   	type: integer

### Behavior

## Demolition Project Agent

### Attributes
	

	name: demolition site
	type: DemolitionSite

	name: attitude towards  concrete waste generating behavior: 
    type: enum {with/without the presence of impurities)
    
    name: waste generation pattern (amount of waste generated per day)
	type: function (or parameter of Poisson distribution used)
https://www.sciencedirect.com/topics/mathematics/poisson-distribution


## Demolition Site - this is NOT an agent
###Attributes
	name:projectId
	type: unique key

	name:location
	type:geoposition
	
	name: size in square meters
	type: int

	name: constructin year
	type: int

	name:factor of concrete used to calculate amount of concrete demolition will generate
	type: double in [0,1]
	
	


