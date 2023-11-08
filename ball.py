import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball Simulation")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Constants
gravity = 0.125

# Ball properties
ball_radius = 11
ball_color = YELLOW

# Circle properties
circle_radius = 200
circle_color = GREEN
circle_center = (screen_width // 2, screen_height // 2)

# Initialize ball position to None
ball_pos = None

# Ball velocity (set to [2, 0] initially)
ball_vel = [1, 0]

# Momentum multiplier
momentum_multiplier = 1.01

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and ball_pos is None:
            ball_pos = list(pygame.mouse.get_pos())
            ball_vel = [2, 0]  # Set initial velocity

    if ball_pos is not None:
        # Apply gravity to ball
        ball_vel[1] += gravity

        # Update ball position
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Bounce off walls
        if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= screen_width:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= momentum_multiplier  # Increase momentum by 1%

        if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= screen_height:
            ball_vel[1] = -ball_vel[1]
            ball_vel[1] *= momentum_multiplier  # Increase momentum by 1%

        # Keep ball inside the circle
        distance = ((ball_pos[0] - circle_center[0])**2 + (ball_pos[1] - circle_center[1])**2)**0.5
        if distance > circle_radius - ball_radius:
            norm_vector = [(ball_pos[0] - circle_center[0]) / distance,
                           (ball_pos[1] - circle_center[1]) / distance]
            ball_pos[0] = int(circle_center[0] + norm_vector[0] * (circle_radius - ball_radius))
            ball_pos[1] = int(circle_center[1] + norm_vector[1] * (circle_radius - ball_radius))
            dot_product = 2 * (ball_vel[0] * norm_vector[0] + ball_vel[1] * norm_vector[1])
            ball_vel[0] -= dot_product * norm_vector[0]
            ball_vel[1] -= dot_product * norm_vector[1]
            ball_vel[0] *= momentum_multiplier  # Increase momentum by 1%
            ball_vel[1] *= momentum_multiplier  # Increase momentum by 1%

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius, 2)

    if ball_pos is not None:
        pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
