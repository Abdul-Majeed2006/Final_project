import pygame


# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Player/Camera properties
CAMERA_SPEED = 10


pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World Scroller")

# --- Load the Background ---
# This is the magic! We load the giant image we just created.
# .convert() optimizes the image format for faster blitting
try:
    world_background = pygame.image.load("background.png").convert()
except FileNotFoundError:
    print("Error: 'background.png' not found.")
    print("Please run 'generate_background.py' first!")

    
# Get the total size of our world
world_width = world_background.get_width()
world_height = world_background.get_height()

print(f"Loaded a {world_width}x{world_height} world.")

# --- Camera and Game Loop ---
camera_x = 0
camera_y = 0  # We can add vertical scrolling too

clock = pygame.time.Clock()
running = True

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # --- Input Handling ---
    # Get a dictionary of all pressed keys
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera_x -= CAMERA_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera_x += CAMERA_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        camera_y -= CAMERA_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        camera_y += CAMERA_SPEED
        
    # --- Camera Clamping ---
    # Stop the camera from scrolling past the edge of the world
    
    # Horizontal clamping
    if camera_x < 0:
        camera_x = 0
    if camera_x > world_width - SCREEN_WIDTH:
        camera_x = world_width - SCREEN_WIDTH
        
    # Vertical clamping
    if camera_y < 0:
        camera_y = 0
    if camera_y > world_height - SCREEN_HEIGHT:
        camera_y = world_height - SCREEN_HEIGHT

    # --- Drawing ---
    
    # We don't need to fill the screen with black,
    # because our background blit will cover the whole thing.
    
    # This is the most important line!
    # We blit the 'world_background' surface onto the 'screen'
    # The 'area' argument (camera_x, camera_y, ...) tells Pygame
    # WHICH PART of the giant image to draw.
    screen.blit(world_background, (0, 0), (camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # You would draw your player, enemies, etc. *here*
    # For example, to draw a "player" always in the center:
    # player_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 15, 30, 30)
    # pygame.draw.rect(screen, (255, 0, 0), player_rect)
    
    # --- Update Display ---
    pygame.display.flip()
    
    # Cap the framerate
    clock.tick(60)
    
pygame.quit()

if __name__ == "__main__":
    main()


