import pygame
import math
import colorsys
import random

# Initialize Pygame
pygame.init()

# Get screen info and set up fullscreen
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Barnsley Fern Animation")

# Colors
BLACK = (0, 0, 0)

class FernFractal:
    def __init__(self):
        self.points = []
        self.current_iteration = 0
        self.max_iterations = 100000  # More points for a denser fern
        self.animation_speed = 0.01
        self.animation_progress = 0
        self.color_hue = 0
        self.scale_factor = 0.8
        self.min_scale = 0.0001  # Deep zoom capability
        self.max_scale = 5.0
        self.zoom_speed = 0.1
        self.offset_x = 0
        self.offset_y = 0
        self.move_speed = 20
        self.last_zoom_time = 0
        self.last_move_time = 0
        self.zoom_delay = 200
        self.move_delay = 200
        self.point_size = 1
        
    def transform_point(self, x, y, transform_type):
        if transform_type == 0:  # Stem
            return 0, 0.16 * y
        elif transform_type == 1:  # Successively smaller leaflets
            return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif transform_type == 2:  # Largest left-hand leaflet
            return 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:  # Largest right-hand leaflet
            return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
    
    def generate_points(self, iteration):
        points = []
        x, y = 0, 0
        
        # Generate points for the current iteration
        for _ in range(iteration):
            # Choose transformation based on probability
            r = random.random()
            if r < 0.01:
                transform = 0
            elif r < 0.86:
                transform = 1
            elif r < 0.93:
                transform = 2
            else:
                transform = 3
            
            # Apply transformation
            x, y = self.transform_point(x, y, transform)
            
            # Scale and position the point
            scaled_x = WIDTH/2 + self.offset_x + x * WIDTH * self.scale_factor * 0.1
            scaled_y = HEIGHT/2 + self.offset_y - y * HEIGHT * self.scale_factor * 0.1
            
            points.append((scaled_x, scaled_y))
        
        return points
    
    def update(self, zoom_in=False, zoom_out=False, move_x=0, move_y=0):
        current_time = pygame.time.get_ticks()
        
        # Handle zoom with delay
        if (zoom_in or zoom_out) and (current_time - self.last_zoom_time) > self.zoom_delay:
            if zoom_in:
                self.scale_factor = min(self.max_scale, 
                                      self.scale_factor + self.zoom_speed)
            elif zoom_out:
                self.scale_factor = max(self.min_scale, 
                                      self.scale_factor - self.zoom_speed)
            self.last_zoom_time = current_time
        
        # Handle movement with delay
        if (move_x != 0 or move_y != 0) and (current_time - self.last_move_time) > self.move_delay:
            self.offset_x += move_x * self.move_speed
            self.offset_y += move_y * self.move_speed
            self.last_move_time = current_time
        
        self.animation_progress += self.animation_speed
        if self.animation_progress >= 1:
            self.animation_progress = 0
            self.current_iteration = min(self.current_iteration + 1000, self.max_iterations)
        
        self.color_hue = (self.color_hue + 0.001) % 1.0
    
    def draw(self, screen):
        # Draw background
        screen.fill(BLACK)
        
        # Get points for current iteration
        points = self.generate_points(self.current_iteration)
        
        # Draw points with color gradient
        for i, point in enumerate(points):
            progress = i / len(points)
            hue = (self.color_hue + progress * 0.3) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = tuple(int(c * 255) for c in rgb)
            
            # Draw point with glow effect
            for size in range(3, 0, -1):
                alpha = int(255 * (size / 3))
                glow_color = (*color, alpha)
                pygame.draw.circle(screen, glow_color, 
                                 (int(point[0]), int(point[1])), 
                                 self.point_size * size)

def main():
    clock = pygame.time.Clock()
    fractal = FernFractal()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        
        # WASD movement
        if keys[pygame.K_a]: move_x -= 1
        if keys[pygame.K_d]: move_x += 1
        if keys[pygame.K_w]: move_y -= 1
        if keys[pygame.K_s]: move_y += 1
        
        # Arrow key zoom
        zoom_in = keys[pygame.K_UP]
        zoom_out = keys[pygame.K_DOWN]
        
        fractal.update(zoom_in=zoom_in, zoom_out=zoom_out, 
                      move_x=move_x, move_y=move_y)
        fractal.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 