import pygame
import random
import sys

# --- Configuration ---
GRID_WIDTH = 5  # Width of the game grid in cells
GRID_HEIGHT = 5 # Height of the game grid in cells
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

def get_next_position_l1_traversal(current_pos, width, height):
    """
    Simple L1 traversal - zigzag pattern row by row.
    Much simpler and more optimal than Hamiltonian cycle.
    """
    x, y = current_pos
    
    # If we're on an even row (0, 2, 4...), move right
    if y % 2 == 0:
        if x < width - 1:
            return (x + 1, y)  # Move right
        else:
            # End of even row - check if we're at the bottom
            if y >= height - 1:
                return (0, 0)  # Wrap to start
            else:
                return (x, y + 1)  # Move down to next row
    # If we're on an odd row (1, 3, 5...), move left
    else:
        if x > 0:
            return (x - 1, y)  # Move left
        else:
            # End of odd row - check if we're at the bottom
            if y >= height - 1:
                return (0, 0)  # Wrap to start
            else:
                return (x, y + 1)  # Move down to next row

class Snake:
    """Represents the snake in the game."""
    def __init__(self):
        self.body: list[tuple[int, int]] = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
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
    pygame.display.set_caption("Snake AI - L1 Traversal")
    clock = pygame.time.Clock()

    snake = Snake()
    
    # Start the snake at position (0,0) for L1 traversal
    start_pos: tuple[int, int] = (0, 0)
    snake.body = [start_pos]

    food = Food()
    food.randomize_position(snake.body)
    
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- AI Logic - Simple L1 Traversal ---
        current_pos = snake.get_head_position()
        next_pos = get_next_position_l1_traversal(current_pos, GRID_WIDTH, GRID_HEIGHT)

        snake.move(next_pos)
        
        # Check for collision with food
        if snake.get_head_position() == food.position:
            snake.grow()
            score += 1
            # If the snake fills the whole screen, we've won.
            if snake.length == GRID_WIDTH * GRID_HEIGHT:
                print("Game Won! The snake has filled the board.")
                # Drawing everything one last time to show the full snake
                screen.fill(BLACK)
                draw_grid(screen)
                snake.draw(screen)
                food.draw(screen)
                score_text = font.render(f"Score: {score}", True, WHITE)
                screen.blit(score_text, (10, 10))
                pygame.display.flip()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
            
            food.randomize_position(snake.body)

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