import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("assets", "plane.png"))
        self.image = pygame.transform.scale(self.image, (110, 110))
        self.rect = self.image.get_frect(midleft=(10, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 350

        # Laser
        self.can_shoot = True
        self.cooldown_duration = 1000
        self.laser_shoot_time = 0

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * delta_time

        if pygame.mouse.get_just_pressed()[0] and self.can_shoot:
            print("Fire Laser")
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

pygame.init()

# Window Constants, DO NOT CHANGE
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

running = True
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Window Icon and Title
icon_image = pygame.image.load(join("assets", "bronze.png")).convert_alpha()
pygame.display.set_icon(icon_image)
pygame.display.set_caption("SpaceWars.py")

# Background Image
background_image = pygame.image.load(join("assets", "Background.jpg")).convert_alpha()
background_image = pygame.transform.scale(
    background_image, (WINDOW_WIDTH, WINDOW_HEIGHT)
)
background_image_rect = background_image.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)

# Asteroids
asteroid_event = pygame.event.custom_type()
pygame.time.set_timer(asteroid_event,500)

#Sprite Groups
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

while running:
    delta = clock.tick(240) / 1000  # Return Value by default is ms, converted to s

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # Update
    all_sprites.update(delta)

    # Display loop
    display_surface.fill((20, 40, 48))
    display_surface.blit(background_image, background_image_rect)
    all_sprites.draw(display_surface)

    pygame.display.update()
pygame.quit()
