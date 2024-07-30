from population import Population 
from PIL import Image
import shapes
import math
import time

# Images
TARGET_IMAGE_PATH = ""
STARTING_IMAGE_PATH = "" # Optional
IMAGE_SCALE = 0.25 # Lower scale improves efficency
# Shapes
SHAPE_TYPE = shapes.CIRCLE
SHAPE_SIZE = 10
SHAPE_ROTATION = 0 # Radians - math.pi = 180degree
SHAPE_OUTLINE = 0
# Algorithm
NUMBER_OF_SHAPES = 3000
NUMBER_OF_INDIVIDUALS = 400
MUTATION_RATE = 0.0004
CROSSOVER_RATE = 0.9
TOURNAMENT_SIZE = 8
# Saving
SAVE_DIR_PATH = "imgs" # Absolute or relative to main.py
SAVE_IMG_EVERY = 50

def main():
    total_start = time.time()
    
    target = Image.open(TARGET_IMAGE_PATH)
    target = target.convert('L')
    target = target.resize((round(target.size[0]*IMAGE_SCALE), round(target.size[1]*IMAGE_SCALE)))
    
    target.save(f"target_mona.png", "PNG")
    return
    
    shapes_config = shapes.ShapesConfig()
    shapes_config.type = shapes.SQUARE_EMPTY
    shapes_config.rotation = SHAPE_ROTATION
    shapes_config.outline = SHAPE_OUTLINE
    shapes_config.size = SHAPE_SIZE
    shapes_config.number_of_shapes = NUMBER_OF_SHAPES
    
    pop = Population(target, shapes_config)
    print("Initializing population")
    pop.initialize_population(NUMBER_OF_INDIVIDUALS)
    
    while True:
        gen_start = time.time()
        print(f"___Generation {pop.generation}___")
        
        pop.draw_individuals()
        pop.calculate_fitness()
        
        top = pop.get_fittest(1)
        print(f"Highest fitness: {top[0].fitness}")           
        
        if pop.generation % SAVE_IMG_EVERY == 0:
            for ind in top:
                ind.image.save(f"{SAVE_DIR_PATH}/gen{pop.generation}.png", "PNG")
        
        pop.next_generation(TOURNAMENT_SIZE, CROSSOVER_RATE)
        pop.mutate(MUTATION_RATE)
        
        gen_end = time.time()
        print(f"Generation time: {gen_end-gen_start}")
        print(f"Total time: {gen_end-total_start}")
        
        
if __name__ == "__main__":
    main()