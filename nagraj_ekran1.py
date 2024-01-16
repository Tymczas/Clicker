import pygame, sys
import time

pygame.init()
screen = pygame.display.set_mode((400, 300))

# Set time to exit after 30 seconds
end_time = time.time() + 30

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Exit if q is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()

    # Check if end time has passed
    if time.time() > end_time:
        break

    # Drawing code goes here

    pygame.display.flip()

# Save mp4 file after loop
pygame.quit()