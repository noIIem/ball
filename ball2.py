import pygame
import sys
import random

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
WHITE = (255, 255, 255)
colors = [
    (255, 0, 0),  # RED
    (255, 165, 0),  # ORANGE
    (255, 255, 0),  # YELLOW
    (0, 0, 255),  # BLUE
    (0, 128, 0),  # GREEN
    (255, 0, 255),  # LIGHT PURPLE
    (173, 216, 230),  # Light blue
    (0, 128, 128),  # teal
    (255, 192, 203)  # pink
]

# Constants
gravity = 0.12

# Ball properties
ball_radius = 11

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

# Initialize previous color
prev_color = None

# Initialize simulation start flag
simulation_started = False

# Initialize font
font = pygame.font.Font(None, 36)

# Create text surface and rectangle
text = font.render('Click inside the circle to start', True, GREEN)
text_rect = text.get_rect(midbottom=(circle_center[0], circle_center[1] + circle_radius +  50))

# Store the initial state
initial_ball_pos = ball_pos
initial_ball_vel = ball_vel
initial_simulation_started = simulation_started

def reset_simulation():
    global ball_pos, ball_vel, current_color, simulation_started
    ball_pos = initial_ball_pos
    ball_vel = initial_ball_vel
    simulation_started = initial_simulation_started
    current_color = None

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = ((mouse_x - circle_center[0])**2 + (mouse_y - circle_center[1])**2)**0.5
            if distance <= circle_radius:
                if simulation_started:
                    reset_simulation()
                else:
                    ball_pos = [mouse_x, mouse_y]
                    ball_vel = [0, 2]  # Set initial velocity
                    current_color = random.choice(colors)
                    simulation_started = True  # Set simulation start flag to True

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
            while True:
                new_color = random.choice(colors)
                if new_color != current_color:
                    current_color = new_color
                    break

        if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= screen_height:
            ball_vel[1] = -ball_vel[1]
            ball_vel[1] *= momentum_multiplier  # Increase momentum by 1%
            while True:
                new_color = random.choice(colors)
                if new_color != current_color:
                    current_color = new_color
                    break

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
            while True:
                new_color = random.choice(colors)
                if new_color != current_color:
                    current_color = new_color
                    break

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius, 2)

    if ball_pos is not None:
        pygame.draw.circle(screen, current_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    if not simulation_started:
        screen.blit(text, text_rect)

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
