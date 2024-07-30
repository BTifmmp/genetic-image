from individual import Individual
from PIL import Image
import numpy as np
import random
import shapes

class Population:
    def __init__(
            self,
            target_image: Image,
            shapes_config: shapes.ShapesConfig,
            starting_image: Image=None):
        self.generation = 0
        self.target_image = target_image
        self.starting_image = starting_image
        self.shapes_config = shapes_config
        self.population = []
        
        # Creates starting image if doesnt exist
        if self.starting_image is None:
            self.starting_image = Image.new("L", target_image.size, (0))
        
        # Derrives image size from target
        shapes_config.image_size = target_image.size
            
    def initialize_population(self, number_of_individuals):
        """Creates new population of individuals"""
        for _ in range(number_of_individuals):
            new_individual = Individual()
            new_individual.initialize_shapes(self.shapes_config)
            self.population.append(new_individual)
            
    def get_fittest(self, n: int):
        """Returns n fittest individuals"""
        pop_sorted = sorted(self.population, key=lambda individual: individual.fitness, reverse=True)
        return pop_sorted[:n]
    
    def draw_individuals(self):
        """Draws image of each individual"""
        for individual in self.population:
            individual.draw_image(self.starting_image)
    
    def mutate(self, mutation_rate: float):
        """Mutates each individual"""
        for individual in self.population:
            individual.mutate(mutation_rate, self.shapes_config)
    
    def calculate_fitness(self):
        """
        Calcualtes fitness of each individual
        """
        target_flat = np.array(self.target_image).flatten()
        for individual in self.population:
            individual.calculate_fitness(target_flat)
            
    def next_generation(self, tournament_size: int, crossover_rate: float):
        """
        Creates new generation of individuals using tournamnet selection
        to find parents for new offsprings
        """
        newpopulation = []
        
        # Fills new population with offsprings
        while len(newpopulation) < len(self.population):
            indv1 = self._tournament_select(tournament_size)
            indv2 = self._tournament_select(tournament_size)
            if random.random() < crossover_rate:
                offspirng1, offspirng2 = indv1.crossover(indv2)
                newpopulation.append(offspirng1)
                newpopulation.append(offspirng2)
            else:
                newpopulation.append(indv1)
                newpopulation.append(indv2)
                        
        # Trims population to be exact size as the previous
        newpopulation = newpopulation[:len(self.population)]
        
        self.population = newpopulation
        self.generation += 1
        
    def _tournament_select(self, tournament_size: int) -> Individual:
        # Selects two parents using tournament selection        
        tournament = random.sample(self.population, tournament_size)
        tournament.sort(key=lambda individual: individual.fitness, reverse=True)
        return tournament[0]
    
    