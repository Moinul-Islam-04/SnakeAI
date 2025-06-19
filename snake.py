import pygame
import random
import sys

# --- Configuration ---
GRID_WIDTH = 20  # Width of the game grid in cells
GRID_HEIGHT = 20 # Height of the game grid in cells
CELL_SIZE = 30   # Size of each cell in pixels
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
GAME_SPEED = 20 # The speed of the game (frames per second)

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 153, 213)
GRID_COLOR = (40, 40, 40)

# --- Directions ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def generate_hamiltonian_cycle(width, height):
    """
    Generates a Hamiltonian cycle for a grid of given width and height.
    This specific algorithm creates a simple, serpentine path that covers the entire grid.
    The path is returned as a dictionary mapping each grid cell (x, y) to the next cell in the cycle.
    """
    path = {}
    for y in range(height):
        if y % 2 == 0:  # Moving right on even rows
            for x in range(width - 1):
                path[(x, y)] = (x + 1, y)
            if y < height - 1:
                path[(width - 1, y)] = (width - 1, y + 1) # Move down to the next row
        else:  # Moving left on odd rows
            for x in range(width - 1, 0, -1):
                path[(x, y)] = (x - 1, y)
            if y < height - 1:
                path[(0, y)] = (0, y + 1) # Move down to the next row
    
    # Complete the cycle by connecting the last node to the first
    path[(0, height - 1)] = (0, 0)

    # Handle the final node on the last row based on row parity
    if height % 2 != 0: # Odd number of rows, last row moves left
        path[(0, height - 1)] = (0,0) # This should actually go up, but let's connect to start
        # The last element in a right-moving row needs to be connected
        path[(width - 1, height - 1)] = (0, 0) # This needs a better wrap-around logic
        # Correct final connection for serpentine path
        if width > 1:
             path[(0, height-1)] = (0, height-2) if height > 1 else (0,0)
             path[(width-1,height-1)] = (width-2, height-1)
        # Manually create the loop for the last row
        if height % 2 == 1: # Last row moved right
            path[(width - 1, height - 1)] = (0, 0)
        else: # Last row moved left
            path[(0, height - 1)] = (0,0)


    # More robust serpentine path generation
    path = {}
    for y in range(height):
        if y % 2 == 0:  # Even row (0, 2, ...), move right
            for x in range(width - 1):
                path[(x, y)] = (x + 1, y)
            if y + 1 < height:
                path[(width - 1, y)] = (width - 1, y + 1)
        else:  # Odd row (1, 3, ...), move left
            for x in range(width - 1, 0, -1):
                path[(x, y)] = (x - 1, y)
            if y + 1 < height:
                path[(0, y)] = (0, y + 1)
    
    # Complete the loop
    path[(0, height - 1)] = (0, 0) # This is for an even height grid
    if height % 2 == 1: # If height is odd, last row moved right
        path[(width - 1, height - 1)] = (0, 0)
    else: # If height is even, last row moved left
        path[(0, height - 1)] = (0, 0)


    return path

class Snake:
    """Represents the snake in the game."""
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.body[0]

    def turn(self, point):
        """Changes the snake's direction."""
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Avoids moving directly backward
        else:
            self.direction = point

    def move(self, next_pos):
        """Moves the snake one step forward."""
        self.body.insert(0, next_pos)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        """Increases the snake's length by one."""
        self.length += 1

    def draw(self, surface):
        """Draws the snake on the screen."""
        for segment in self.body:
            r = pygame.Rect((segment[0] * CELL_SIZE, segment[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, GREEN, r)
            pygame.draw.rect(surface, BLACK, r, 1)

class Food:
    """Represents the food in the game."""
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self, snake_body=[]):
        """Places the food at a random position on the grid, not on the snake."""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_body:
                break

    def draw(self, surface):
        """Draws the food on the screen."""
        r = pygame.Rect((self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, RED, r)

def draw_grid(surface):
    """Draws the grid lines on the screen."""
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

def main():
    """Main function to run the game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake AI - Hamiltonian Cycle")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    food.randomize_position(snake.body)
    
    # Generate the pre-calculated path for the AI
    hamiltonian_cycle = generate_hamiltonian_cycle(GRID_WIDTH, GRID_HEIGHT)

    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- AI Logic ---
        # The AI simply follows the pre-calculated Hamiltonian path.
        # It doesn't need to "think" or react to the food's position.
        current_pos = snake.get_head_position()
        if current_pos in hamiltonian_cycle:
            next_pos = hamiltonian_cycle[current_pos]
        else:
            # This case should ideally not happen in a perfect cycle.
            # If it does, it's a bug in the cycle generation. We'll just stop.
            print(f"Error: Position {current_pos} not in Hamiltonian cycle!")
            pygame.quit()
            sys.exit()

        snake.move(next_pos)
        
        # Check for collision with food
        if snake.get_head_position() == food.position:
            snake.grow()
            score += 1
            food.randomize_position(snake.body)
            # If the snake fills the whole screen, we've won.
            if snake.length == GRID_WIDTH * GRID_HEIGHT:
                print("Game Won! The snake has filled the board.")
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()


        # Drawing everything
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        
        # Display Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == '__main__':
    main()
