# Genetic Image
## Overview
This project uses a genetic algorithm to recreate images with simple shapes like circles, squares, rectangles. The algorithm evolves a population of images to minimize the difference between a target image and the generated images over successive generations.
## Results
## Algorithm Details
### Fitness
The fitness function determines how closely the image composed of shapes matches the original image. This project utilizes the Structural Similarity Index Measure (SSIM) from the scikit-image library.
### Mutation
The mutation process replaces one of the genes with a newly generated one, with each gene having a probability of mutation equal to mutation rate.
### Parent Selection
Parents are selected using a tournaments selection, which randomly selects a subset of individuals form population and return the fittest one of them.
### Crossoever
Crossover is perfomred using uniform method, where each gene has a 50% chance of being inherited from either parent. Two parents produce two offsprings with opposing genes.
## What affects execution speed
- image size
- population size
- number of shapes being used
- usign outline width higher than 1
- size of shapes
## Usage
Python version 3.9 or higher\
Installing requirements
```
pip install -r requirments.txt
```
All algortihm's controls are inside ```genetic-image/main.py``` file
```python
# Images
TARGET_IMAGE_PATH = ""
STARTING_IMAGE_PATH = "" # Optional
IMAGE_SCALE = 0.25 # Lower scale improves efficency
# Shapes
SHAPE_TYPE = shapes.CIRCLE
SHAPE_SIZE = 10
SHAPE_ROTATION = 0 # Radians
SHAPE_OUTLINE = 0
# Algorithm
NUMBER_OF_SHAPES = 2000
NUMBER_OF_INDIVIDUALS = 100
MUTATION_RATE = 0.0005
CROSSOVER_RATE = 0.9
TOURNAMENT_SIZE = 8
# Saving
SAVE_DIR_PATH = "imgs"
SAVE_IMG_EVERY = 50
```
Running
```
py main.py
```
