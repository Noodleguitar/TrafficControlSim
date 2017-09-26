## Traffic control system simulation
#### Authors:
* Elbert Fliek (s1917188)
* Albert Thie (s1652184)
* Noël Lüneburg (s177315)

### The main problem to be addressed
Traffic control system on individual, or multiple intersections do not use signals from individual cars in a meaningful way, except for road sensors often placed in the proximity of traffic lights. There are proposed systems that do try to use these signals, in light of automation technology. The first of the systems that has gone from simulations to actual implentation in a real world situation is one that is based on the paper "Self-Control of Traffic Lights and Vehicle Flows in Urban Road Networks" by Lämmer et al. (http://stefanlaemmer.de/)

### State of the art
Currently this systems uses a pressure differential model, to allow individual traffic lights to communicate their current vehicles and expected vehicles based on observing these vehicles approaching the intersection. The model by Lämmer attempts to clear intersections much quicker by anticipating not only the arrival of new vehicles, but also the time that it would to take to clear the vehicles that are already waiting, so that arriving vehicles have to brake as little as possible. By including the potential future wait time, they reduce intersection wait times and give priority to arriving buses.

### Contribution to the problem addressed
Currently this model is only used with communicating traffic lights which are able to observe cars. However the traffic lights have no knowledge (other then possibly preselection in lanes, which does not occur in the real world experiment) if cars will turn left, right or go straight on. By creating a model where cars transfer their intended destination, efficiency could be increased in situations where cars are approaching the intersection from different compatible angles. For example two cars approaching from opposite sides of the crossing which both intend to head straight on can do so at the same time. This would require the traffic light to split arriving cars into subqueus orded by their destination, allowing them to communicate which pathway on the intersection would be occupied by cars in their lane. As a proof of concept, we will design a system based on the basic idea of the travel flow model, but which is able to differentiate between cars heading to different parts of the intersection and thus plan more efficiently.

### Expected results
A system which also uses destination data from individual cars would be able to divide an intersection in to passable routes, further decreasing wait times, especially in low traffic conditions (as the probability of the cars waiting having compatible angles increases with less vehicles in the ceue).

### Relevance of the topic
Reducing congestion has benefits to the environment as well as the local economy, because travelling time is reduced. While currently cars are not yet able to communicate their destination electronicly, self driving cars would be able to do so. In this way we can look ahead at the possibilities that these cars provide. Alternatively a system where the information provided by the indicator lights used by human drivers is used in the system could also be considered.

### Reference paper
"Self-Control of Traffic Lights and Vehicle Flows in Urban Road Networks", 2008
https://arxiv.org/pdf/0802.0403.pdf
We believe this is a good paper to use as the authors are from the university of Dresden and ETH Zurich, and the paper has been cited 240 times. The fact that it has been used for the first real life system test is also very nice.
