import pygame
import random

# Initialize Pygame
pygame.init()

# Screen size
WIDTH = 500
HEIGHT = 400

# Colors
BLUE = pygame.Color("blue")
LIGHTBLUE = pygame.Color("lightblue")
DARKBLUE = pygame.Color("darkblue")

WHITE = pygame.Color("white")
RED = pygame.Color("red")
YELLOW = pygame.Color("yellow")
MAGENTA = pygame.Color("magenta")
ORANGE = pygame.Color("orange")

# Custom events
SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2


# Rectangle Sprite Class
class RectangleSprite(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        # Rectangle shape
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        # Random movement direction
        self.velocity = [random.choice([-3, 3]), random.choice([-3, 3])]

    # Enemy movement
    def update(self):

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        boundary_hit = False

        # Bounce left/right
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity[0] = -self.velocity[0]
            boundary_hit = True

        # Bounce top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.velocity[1] = -self.velocity[1]
            boundary_hit = True

        # Trigger color changes
        if boundary_hit:
            pygame.event.post(
                pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))
            pygame.event.post(
                pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))

    # Change rectangle color
    def change_color(self):
        self.image.fill(random.choice([WHITE, YELLOW, MAGENTA, ORANGE]))


# Change background color
def change_background_color():
    global bg_color
    bg_color = random.choice([BLUE, LIGHTBLUE, DARKBLUE])


# Create sprite groups
all_sprites = pygame.sprite.Group()

# Player rectangle
player = RectangleSprite(RED, 60, 40)
player.rect.x = 200
player.rect.y = 150

# Enemy rectangle
enemy = RectangleSprite(WHITE, 60, 40)
enemy.rect.x = random.randint(0, WIDTH - 60)
enemy.rect.y = random.randint(0, HEIGHT - 40)

# Add only 2 sprites
all_sprites.add(player)
all_sprites.add(enemy)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rectangle Collision Game")

# Background color
bg_color = BLUE

# Clock
clock = pygame.time.Clock()

# Game loop
running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == SPRITE_COLOR_CHANGE_EVENT:
            enemy.change_color()

        elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
            change_background_color()

    # Keyboard controls for player rectangle
    keys = pygame.key.get_pressed()

    speed = 5

    if keys[pygame.K_LEFT]:
        player.rect.x -= speed

    if keys[pygame.K_RIGHT]:
        player.rect.x += speed

    if keys[pygame.K_UP]:
        player.rect.y -= speed

    if keys[pygame.K_DOWN]:
        player.rect.y += speed

    # Keep player inside screen
    if player.rect.left < 0:
        player.rect.left = 0

    if player.rect.right > WIDTH:
        player.rect.right = WIDTH

    if player.rect.top < 0:
        player.rect.top = 0

    if player.rect.bottom > HEIGHT:
        player.rect.bottom = HEIGHT

    # Update enemy only
    enemy.update()

    # End game if rectangles touch
    if pygame.sprite.collide_rect(player, enemy):
        print("Game Over!")
        running = False

    # Draw everything
    screen.fill(bg_color)

    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

# Quit game
pygame.quit()