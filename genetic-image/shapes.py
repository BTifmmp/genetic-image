from __future__ import annotations

import numpy as np
import random
from PIL import ImageDraw

# shapes id's 
SQUARE = "SQUARE"
SQUARE_EMPTY = "SQUARE_EMPTY"
RECTANGLE = "RECTANGLE"
RECTANGLE_EMPTY = "RECTANGLE_EMPTY"
CIRCLE = "CIRCLE"
CIRCLE_EMPTY = "CIRCLE_EMPTY"

class ShapesConfig:
    """ Configuration for all shapes """
    def __init__(self):
        # number of shapes
        self.number_of_shapes = 0
                
        # types
        self.type = CIRCLE
        
        # positioning
        self.image_size = [0, 0]
        
        # sizing
        self.size = 0
        self.outline = 0
        self.rectangle_ratio = 1 # height = size, width = height*ratio
        
        # rotation
        self.rotation = 0

class Shape:
    def new(shapes_config: ShapesConfig) -> Shape:
        """Returns created object of requested shape"""
        return _shapes_creator[shapes_config.type](shapes_config)
    
    def __init__(self, shapes_config: ShapesConfig):
        self.color = (random.randint(0, 255))
    
    def draw(image_draw: ImageDraw):
        pass

class Square(Shape):
    def __init__(self, shapes_config: ShapesConfig):
        super().__init__(shapes_config)
        self.points = []
        
        position = (shapes_config.image_size[0]*random.random(),
                    shapes_config.image_size[1]*random.random())
        size_half = shapes_config.size / 2.0
        
        # Adds points in clockwise order
        self.points.append((position[0]-size_half, position[1]-size_half)) # top left
        self.points.append((position[0]+size_half, position[1]-size_half)) # top right
        self.points.append((position[0]+size_half, position[1]+size_half)) # bottom right
        self.points.append((position[0]-size_half, position[1]+size_half)) # bottom left
        
        if shapes_config.rotation != 0:
            self.points = _rotate_points(self.points, position, shapes_config.rotation)
    
    def draw(self, image_draw: ImageDraw):
        image_draw.polygon(self.points, self.color)

class SquareEmpty(Square):
    def __init__(self, shapes_config: ShapesConfig):
        self.width = shapes_config.outline
        super().__init__(shapes_config)
    
    def draw(self, image_draw: ImageDraw):
        image_draw.polygon(self.points, outline=self.color, width=self.width)

class Rectangle(Shape):
    def __init__(self, shapes_config: ShapesConfig):
        super().__init__(shapes_config)
        self.points = []
        
        position = (shapes_config.image_size[0]*random.random(),
                    shapes_config.image_size[1]*random.random())
        
        size_halfy = shapes_config.size / 2.0
        size_halfx = size_halfy * shapes_config.rectangle_ratio
        
        # Adds points in clockwise order
        self.points.append((position[0]-size_halfx, position[1]-size_halfy)) # top left
        self.points.append((position[0]+size_halfx, position[1]-size_halfy)) # top right
        self.points.append((position[0]+size_halfx, position[1]+size_halfy)) # bottom right
        self.points.append((position[0]-size_halfx, position[1]+size_halfy)) # bottom left
        
        if shapes_config.rotation != 0:
            self.points = _rotate_points(self.points, position, shapes_config.rotation)
    
    def draw(self, image_draw: ImageDraw):
        image_draw.polygon(self.points, self.color)

class RectangleEmpty(Rectangle):
    def __init__(self, shapes_config: ShapesConfig):
        self.width = shapes_config.outline
        super().__init__(shapes_config)
    
    def draw(self, image_draw: ImageDraw):
        image_draw.polygon(self.points, outline=self.color, width=self.width)

class Circle(Shape):
    def __init__(self, shapes_config: ShapesConfig):
        self.points = []
        super().__init__(shapes_config)
        
        position =  (shapes_config.image_size[0]*random.random(),
                          shapes_config.image_size[1]*random.random())
        radius = shapes_config.size / 2.0
        
        self.points.append((position[0] - radius, position[1]-radius))
        self.points.append((position[0] + radius, position[1]+radius))
        
    def draw(self, image_draw: ImageDraw):
        image_draw.ellipse(self.points, self.color)

class CircleEmpty(Circle):
    def __init__(self, shapes_config: ShapesConfig):
        self.width = shapes_config.outline
        super().__init__(shapes_config)
    
    def draw(self, image_draw: ImageDraw):
        image_draw.ellipse(self.points, outline=self.color, width=self.width)   

# shape classes assigned to corresponding id's
_shapes_creator = {
    SQUARE: Square,
    SQUARE_EMPTY: SquareEmpty,
    RECTANGLE: Rectangle,
    RECTANGLE_EMPTY: RectangleEmpty,
    CIRCLE: Circle,
    CIRCLE_EMPTY: CircleEmpty
} 

def _rotate_points(points: list[int, int], origin: list[int], radians: float) -> list[int, int]:
    """Rotates array of points around origin"""
    R = np.array(((np.cos(radians), -np.sin(radians)),
                  (np.sin(radians),  np.cos(radians))))
    origin = np.atleast_2d(origin)
    points = np.atleast_2d(points)
    points = np.squeeze((R @ (points.T-origin.T) + origin.T).T)
    
    # convert to python list of tuples
    points = [(point[0], point[1]) for point in points]
    
    return points

