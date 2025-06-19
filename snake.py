import pygame
import random
import sys

# --- Configuration ---
GRID_WIDTH = 20  # Width of the game grid in cells
GRID_HEIGHT = 20 # Height of the game grid in cells
CELL_SIZE = 30   # Size of each cell in pixels
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
GAME_SPEED = 10 # Increased speed since AI is now smarter

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
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]



class SimpleSnakeAI:
    """Simple and efficient AI that moves directly towards food using delta calculation."""
    
    def get_next_move(self, snake, food_pos):
        """Determine the next best move using simple delta calculation."""
        head = snake.get_head_position()
        
        # Calculate deltas
        dx = food_pos[0] - head[0]
        dy = food_pos[1] - head[1]
        
        # Determine preferred directions based on larger delta
        preferred_directions = []
        
        # Prioritize the direction with the larger absolute delta
        if abs(dx) >= abs(dy):
            # Horizontal movement is preferred
            if dx > 0:
                preferred_directions.append(RIGHT)
            elif dx < 0:
                preferred_directions.append(LEFT)
            
            # Then vertical
            if dy > 0:
                preferred_directions.append(DOWN)
            elif dy < 0:
                preferred_directions.append(UP)
        else:
            # Vertical movement is preferred
            if dy > 0:
                preferred_directions.append(DOWN)
            elif dy < 0:
                preferred_directions.append(UP)
            
            # Then horizontal
            if dx > 0:
                preferred_directions.append(RIGHT)
            elif dx < 0:
                preferred_directions.append(LEFT)
        
        # Try preferred directions first
        for direction in preferred_directions:
            next_pos = (head[0] + direction[0], head[1] + direction[1])
            if self.is_safe_move(next_pos, snake):
                return direction
        
        # If preferred directions are blocked, try any safe direction
        for direction in DIRECTIONS:
            next_pos = (head[0] + direction[0], head[1] + direction[1])
            if self.is_safe_move(next_pos, snake):
                return direction
        
        # Last resort: continue in current direction if possible
        next_pos = (head[0] + snake.direction[0], head[1] + snake.direction[1])
        if self.is_safe_move(next_pos, snake):
            return snake.direction
        
        # Emergency fallback
        return RIGHT
    
    def is_safe_move(self, pos, snake):
        """Check if a position is safe (within bounds and not on snake body)."""
        x, y = pos
        
        # Check boundaries
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        
        # Check if position is on snake body
        if pos in snake.body:
            return False
        
        return True

class Snake:
    """Represents the snake in the game."""
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
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

    def move(self):
        """Moves the snake one step forward in current direction."""
        head = self.get_head_position()
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        """Increases the snake's length by one."""
        self.length += 1

    def draw(self, surface):
        """Draws the snake on the screen."""
        for i, segment in enumerate(self.body):
            r = pygame.Rect((segment[0] * CELL_SIZE, segment[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
            # Make head slightly different color
            color = (0, 200, 0) if i == 0 else GREEN
            pygame.draw.rect(surface, color, r)
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
    pygame.display.set_caption("Snake AI - Smart Pathfinding")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    food.randomize_position(snake.body)
    ai = SimpleSnakeAI()

    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- AI Logic ---
        # Get the next best move from our smart AI
        next_direction = ai.get_next_move(snake, food.position)
        snake.turn(next_direction)
        snake.move()
        
        # Check for wall collision
        head = snake.get_head_position()
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            print(f"Game Over! Hit wall. Final Score: {score}")
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        
        # Check for self collision
        if head in snake.body[1:]:
            print(f"Game Over! Hit self. Final Score: {score}")
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        
        # Check for collision with food
        if head == food.position:
            snake.grow()
            score += 1
            food.randomize_position(snake.body)
            print(f"Score: {score}")
            
            # Check if won
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
