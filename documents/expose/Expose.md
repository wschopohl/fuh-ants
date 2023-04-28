# Ant Colony Simulation
### modeled as a Multi Agent System (MAS)

![ant title image](images/title.jpg)

## Implementation
We plan to implement this simulation in multiple stages. The main stage #1 being the basic goal and the additional stage #2 as further improvement if everything goes according to plan. Each stage is further broken down into milestones.

### Technical Details
We chose **Python** as Programming language. We think that it's compact code style helps to convey the basic concepts and makes this simulation more accesible to a wider group.
We will use [Pygame](https://www.pygame.org) as graphics library to make our simulations more enticing.

## The Stages

### #1 Main Stage
![main stage goal](images/s1m5-harvest.png)
The overall goal of this stage is to have ants running around on a plane, searching for food and using pheromone trails to efficiently harvest those food sources.

The milestones of this stage are as follows:

### M1: Ants roam the plane
![roaming](images/s1m1-roam.png)
Ants are spawned from their nest (grey hole) and start to roam the plane randomly.

*Parameters:*
- ants spawned per second
- maximum random ant rotation per move

### M2: Food is introduced
![food](images/s1m2-food.png)
Certain spots on the plane can contain clusters of food. Food clusters can be placed randomly or at predefined positions. The latter one is interesting to compare ant efficency with varying parameters. Food clusters have a finite amount of food "atoms". When an ant hits a cluster it will pick up one atom of food, each ant can carry one food atom at a time. When ants hit the nest, they have delivered their food atom and are free to get a new one.

### M3: Ants lay pheromones
![pheromones](images/s1m3-pheromone.png)
Ants will lay two types of pheromones when they move. When they are without food, they will leave a "to home" pheromone trace (blue dots). And when they carry food they will leave a "to food" pheromone trace (green dots).

![pheromone decaying](images/s1m3-pheromone-details.png)

The pheromone traces will decay over time, by a decay function. This can be linear or exponential.

*Parameters:*
- pheromone decay function

### M4: Ants sense pheromones
![sensory](images/s1m4-sensor.png)

The ants get equipped with the ability to sense the pheromones. The pheromones will impact their choice of movement angle. They will follow the "to food" traces (green) when they are not carrying food and use the "to home" traces (blue) when they try to deliver food to the nest.

![sensory](images/s1m4-sensor-details.png)
The ants will have a "field of view" defined by an angle *β*  and a distance *d* in which they will recognize pheromones. The different pheromone vectors will be weighted by current pheromone intensity and an average new movement angle will be calculated.

*Parameters:*
- field of view angle
- field of view distance

### M5: Efficient harvesting
![sensory](images/s1m5-harvest.png)
Over time these simple rules should allow the ants to harvest the food sources very efficiently thereby showing the beauty and strength of Multi Agent Systems.

Varying the afore mentioned parameters will allow to simulate different behaviours of the ants.


## #2 Additional Stage: Obstacles
### M1: Walls
An additional stage will be to introduce walls to be able to build obstacles. This will imply to implement collision detection between ants and walls. As a result the simulations will become even more interesting as the ants will now be able to show their strength in solving more complex problems.

### M2: The double bridge experiment
We would be interested to observe the behaviour of our ants in a [double bridge experiment](http://www.scholarpedia.org/article/Ant_colony_optimization#The_double-bridge_experiment). In short, the ants will be confronted with two situations:

![labyrinth](images/s2-bridges-equal.jpeg)
In the first scenario, with two paths of equal length, the ants are expected to randomly choose one of the two paths over time. When repeating this experiment over and over, the probability for both paths should converge to 50%.

![labyrinth](images/s2-bridges-unequal.jpeg)
In the second scenario one of the paths is significantly shorter than the other. Of course, the ants are now expected to choose the shorter path over time. It would be intersting though, if we can arrive at the formula that *Goss et al. (1989)* developed in the article above 

$$p_1=\frac{(m_1+k)^h}{(m_1+k)^h+(m_2+k)^h}$$

and if we can use the parameters of their formula to fine tune the behaviour of our ants to act like normal ants.