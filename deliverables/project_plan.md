## Traffic control system simulation
#### Authors:
* Elbert Fliek (s1917188)
* Albert Thie (s1652184)
* Noël Lüneburg (s177315)

### The main problem to be addressed
Traffic control system on individual, or multiple intersections do not use signals from individual cars in a meaningful way, except for road sensors often placed in the proximity of traffic lights. There are proposed systems that do try to use these signals, in light of automation technology.

### State of the art
Current systems either use individual car signals, big data from traffic logs or a combination of both. Some use sorting algorithms on individual cars with which they can communicate real time, others also use prediction of future cars arriving.  

### Contribution to the problem addressed
Cars are modelled as a single entity with fixed properties. By modelling different kinds of vehicles with variable size dimensions, speed, etc., the system will be better fitted to the real world. This will present problems to the system that use real time communication, as they will need more information to make an appropriate que and sorting plan. 

### Expected results
A system better equipped to handle complex traffic situations with different vehicles, reducing wait time at intersections. The trade-off is that the system will be more computationally expensive than current solutions. 

### Relevance of the topic
Reducing congestion has benefits to the environment as well as the local economy, because travelling time is reduced. Furthermore, a centralized control system is required as long as cars cannot communicate freely among each other. By implementing a more real life like simulation, we hope to bring a real life implementation closer.

### Reference paper
L. Li, D. Wen and D. Yao, "A Survey of Traffic Control With Vehicular Communications," *in IEEE Transactions on Intelligent Transportation Systems*, vol. 15, no. 1, pp. 425-432, Feb. 2014.
