from __future__ import annotations

from PIL import Image, ImageDraw
from skimage.metrics import structural_similarity
import numpy as np
import random
import shapes

class Individual:    
    def __init__(self, shapes: list[shapes.Shape] = []):
        self.shapes = shapes
        self.fitness = 0.0
        self.image = None
        
    def crossover(self, other: Individual) -> tuple[Individual, Individual]:
        """Creates two offspring using uniform gene mixing method"""
        # Shapes are not deep copies
        shapes1 = []
        shapes2 = []
        
        for i in range(len(self.shapes)):
            if random.random() < 0.5:
                shapes1.append(self.shapes[i])
                shapes2.append(other.shapes[i])
            else:
                shapes1.append(other.shapes[i])
                shapes2.append(self.shapes[i])
                
        return Individual(shapes1), Individual(shapes2)
        
    def initialize_shapes(self, shapes_config: shapes.ShapesConfig):
        """Creates a new set of shapes"""
        self.shapes = []
        
        for _ in range(shapes_config.number_of_shapes):
            shape = shapes.Shape.new(shapes_config)
            self.shapes.append(shape)
    
    def draw_image(self, starting_image: Image):
        """Draws all shapes into image"""
        self.image = starting_image.copy()
        draw = ImageDraw.Draw(self.image)
        for shape in self.shapes:
            shape.draw(draw)
        
    def calculate_fitness(self, target_image_flat: np.ndarray):
        """Calculates how fit an individual is and set its score"""
        image_flat = np.array(self.image).flatten()        
        self.fitness = structural_similarity(image_flat, target_image_flat, data_range=255)
        
    def mutate(self, mutation_rate: float, shapes_config: shapes.ShapesConfig):
        """Replaces randomly selected shapes with new ones"""
        for i in range(len(self.shapes)):
            if random.random() < mutation_rate:
                shape = shapes.Shape.new(shapes_config)
                self.shapes[i] = shape
                
        