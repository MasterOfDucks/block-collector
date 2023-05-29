import pygame
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sprite-Beispiel")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TRANSPARENT_RED = (255, 0, 0, 128)

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, score_value=1, is_deadly=False):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.score_value = score_value
        self.is_deadly = is_deadly

    def update(self):
        self.rect.y += 1
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = random.randrange(-100, -10)
            self.rect.x = random.randrange(0, WINDOW_WIDTH)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

all_sprites_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
red_block_group = pygame.sprite.Group()
blue_block_group = pygame.sprite.Group()

block = Block(BLACK, 20, 15)
block.rect.x = random.randrange(WINDOW_WIDTH)
block.rect.y = random.randrange(-100, -10)
all_sprites_group.add(block)
block_group.add(block)

player = Player()
all_sprites_group.add(player)

done = False
clock = pygame.time.Clock()
score = 0

# Soundeffekt für Punkt einsammeln
pick_up_sound = pygame.mixer.Sound("piep_sound.wav")


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if random.random() < 0.1:
        block = Block(BLACK, 20, 15)
        block.rect.x = random.randrange(WINDOW_WIDTH)
        block.rect.y = random.randrange(-100, -10)
        all_sprites_group.add(block)
        block_group.add(block)

    if random.random() < 0.005:
        red_block = Block(TRANSPARENT_RED, 20, 15, is_deadly=True)
        red_block.rect.x = random.randrange(WINDOW_WIDTH)
        red_block.rect.y = random.randrange(-100, -10)
        all_sprites_group.add(red_block)
        red_block_group.add(red_block)

    if random.random() < 0.01:
        blue_block = Block(BLUE, 20, 15, score_value=2)
        blue_block.rect.x = random.randrange(WINDOW_WIDTH)
        blue_block.rect.y = random.randrange(-100, -10)
        all_sprites_group.add(blue_block)
        blue_block_group.add(blue_block)

    all_sprites_group.update()

    block_hit_list = pygame.sprite.spritecollide(player, block_group, True)
    for block in block_hit_list:
        player.score += block.score_value
        pick_up_sound.play()  # Piepton-Sound abspielen

    red_block_hit_list = pygame.sprite.spritecollide(player, red_block_group, True)
    if red_block_hit_list and any(block.is_deadly for block in red_block_hit_list):
        done = True

    blue_block_hit_list = pygame.sprite.spritecollide(player, blue_block_group, True)
    for block in blue_block_hit_list:
        player.score += block.score_value
        pick_up_sound.play()  # Piepton-Sound abspielen

    screen.fill(WHITE)
    all_sprites_group.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render("Punktestand: " + str(player.score), True, BLACK)
    screen.blit(score_text, [10, 10])

    pygame.display.flip()
    clock.tick(60)

# Pygame beenden
pygame.quit()
