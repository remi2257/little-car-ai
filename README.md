# little-car-ai
Hi, my name is Remi LUX. I'm currently in my final year of Computer Vision Degree in Grenoble INP - Phelma. Welcome to my project

My algorithm aims to teach a car to drive through AI.

<p align="center">
<img src="https://github.com/remi2257/little-car-ai/blob/master/images/First_True_Design.png"  width="500"/>
</p>


## How it's work ?

I'm using the method of Genetic Evolution to improve my AI over generations.
1. The Neural Net can access to information from the LIDAR and car's speed.
2. The NN outputs correspond at the command on the wheel (Go straight, turn left,
turn right) and the gas' command (None, Speed Up, Slow Down)
3. At each state, agents receive rewards if they are doing what we want them to do 
(Basically, being on the road and going fast)
4. A certain percentage of agents which received biggest rewards are used
to generate the next generation, thanks to mutation
5. The cycle is repeated

## Evolution, TODO list, Q&A, ...
### TODO LIST
#### Firstly

- [x] Create World
- [x] Create Playable Car
- [x] Add Bots
- [x] Create LIDAR
- [x] Give Control to AI
- [x] Neural Network
- [X] Train on Easy Tracks

#### And Then

- [ ] Better
- [ ] Faster
- [ ] Stronger
- [ ] Q - Learning
- [ ] Multi-threading Processing
- [ ] GPU Processing
- [ ] Create Playground
- [ ] Draw Track from Paper Sheet
- [ ] Test environment with different type of drivers

### Evolution of the Algorithm

| Version | Game Render |
:-------------------------:|:-------------------------:
1.0 | <img src="https://github.com/remi2257/little-car-ai/blob/master/images/good_mutation_v1_0.png" width="400"/>
0.6 | <img src="https://github.com/remi2257/little-car-ai/blob/master/images/First_Mutation.png" width="400"/>
0.3 | <img src="https://github.com/remi2257/little-car-ai/blob/master/images/First_True_Design.png" width="400"/>
0.2 | <img src="https://github.com/remi2257/little-car-ai/blob/master/images/First_LIDAR.png" width="400"/> |

### Versions List

- v1.1 : Add drawing Module | 15/07/19 (I'm Back :D)
- v1.0 : First working version | 02/07/19
- v0.6 : AI & Evolution Algorithm | 30/06/19
- v0.3 : Evolved Playground design | 28/06/19
- v0.2 : First Playground design | 27/06/19


