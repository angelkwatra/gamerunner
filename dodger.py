import pygame
from sys import exit
from random import randint, choice
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/run1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/run2.png').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/player/run3.png').convert_alpha()
        player_walk_4 = pygame.image.load('graphics/player/run4.png').convert_alpha()
        player_walk_5 = pygame.image.load('graphics/player/run5.png').convert_alpha()
        player_walk_6 = pygame.image.load('graphics/player/run6.png').convert_alpha()
        player_walk_7 = pygame.image.load('graphics/player/run7.png').convert_alpha()
        player_walk_8 = pygame.image.load('graphics/player/run8.png').convert_alpha()

        self.player_index = 0

        self.player_idle_right = pygame.image.load('graphics/player/idle.png').convert_alpha()
        self.player_idle_left = pygame.transform.flip(self.player_idle_right, True, False).convert_alpha()

        self.player_walk_right = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6, player_walk_7, player_walk_8]
        self.player_walk_left = list(map(lambda img: pygame.transform.flip(img, True, False).convert_alpha(), self.player_walk_right))

        self.player_jump_right = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_jump_left = pygame.transform.flip(self.player_jump_right, True, False).convert_alpha()

        self.image = self.player_walk_right[self.player_index]
        self.rect = self.image.get_rect(midbottom=(PLAYER_START_X, GROUND_LEVEL))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(JUMP_SOUND_VOLUME)

        self.x_direction = X_DIRECTIONS[0]




    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_LEVEL:
            self.gravity = -PLAYER_JUMP_HEIGHT
            self.jump_sound.play()
        if keys[pygame.K_RIGHT] and self.rect.right <= 800:
            self.rect.x += PLAYER_SPEED
            self.player_index += PLAYER_ANIMATION_SPEED
            if self.player_index >= len(self.player_walk_right): self.player_index = 0
            self.x_direction = X_DIRECTIONS[1]
            self.image = self.player_walk_right[int(self.player_index)]
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= PLAYER_SPEED
            self.player_index += PLAYER_ANIMATION_SPEED
            if self.player_index >= len(self.player_walk_left): self.player_index = 0
            self.x_direction = X_DIRECTIONS[0]
            self.image = self.player_walk_left[int(self.player_index)]
        if not keys[pygame.K_SPACE] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            if self.x_direction == X_DIRECTIONS[0]:
                self.image = self.player_idle_left
            else:
                self.image = self.player_idle_right

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

    def animation_state(self):
        if self.rect.bottom < GROUND_LEVEL:
            if self.x_direction == X_DIRECTIONS[0]:
                self.image = self.player_jump_left
            else:
                self.image = self.player_jump_right

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.speed = 0
        self.y_deviation = 0
        self.y_direction = choice(["down", "up"])
        self.x_direction = choice(["left", "right"])

        if type == 'bird':
            bird_1 = pygame.image.load('graphics/bird/fly1.png').convert_alpha()
            bird_2 = pygame.image.load('graphics/bird/fly2.png').convert_alpha()
            self.frames = [bird_1, bird_2]
            self.speed = BIRD_SPEED
            self.y_deviation = BIRD_DEVIATION
            y_pos = BIRD_MEDIAN_POSITION
        else:
            minotaur_1 = pygame.image.load('graphics/minotaur/minotaur1.png').convert_alpha()
            minotaur_2 = pygame.image.load('graphics/minotaur/minotaur2.png').convert_alpha()
            minotaur_3 = pygame.image.load('graphics/minotaur/minotaur3.png').convert_alpha()
            minotaur_4 = pygame.image.load('graphics/minotaur/minotaur4.png').convert_alpha()
            minotaur_5 = pygame.image.load('graphics/minotaur/minotaur5.png').convert_alpha()
            minotaur_6 = pygame.image.load('graphics/minotaur/minotaur6.png').convert_alpha()
            minotaur_7 = pygame.image.load('graphics/minotaur/minotaur7.png').convert_alpha()
            minotaur_8 = pygame.image.load('graphics/minotaur/minotaur8.png').convert_alpha()
            minotaur_9 = pygame.image.load('graphics/minotaur/minotaur9.png').convert_alpha()
            minotaur_10 = pygame.image.load('graphics/minotaur/minotaur10.png').convert_alpha()
            minotaur_11 = pygame.image.load('graphics/minotaur/minotaur11.png').convert_alpha()
            minotaur_12 = pygame.image.load('graphics/minotaur/minotaur12.png').convert_alpha()
            self.frames = [minotaur_1, minotaur_2, minotaur_3, minotaur_4, minotaur_5, minotaur_6, minotaur_7, minotaur_8, minotaur_9, minotaur_10,
                           minotaur_11, minotaur_12]
            y_pos = GROUND_LEVEL
            self.speed = MINOTAUR_SPEED

        if self.x_direction == "right":
            self.frames = list(map(lambda img: pygame.transform.flip(img, True, False).convert_alpha(), self.frames))
        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        if self.x_direction == "left":
            self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        else:
            self.rect = self.image.get_rect(midbottom=(randint(-100, -50), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        if self.x_direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.y_deviation > 0:
            if self.rect.y > BIRD_MEDIAN_POSITION + self.y_deviation:
                self.y_direction = "up"
            elif self.rect.y < BIRD_MEDIAN_POSITION - self.y_deviation:
                self.y_direction = "down"
            if self.y_direction == "up":
                self.rect.y -= 1
            else:
                self.rect.y += 1
        self.destroy()

    def destroy(self):
        if self.x_direction == "left" and self.rect.x <= -100:
            self.kill()
        if self.x_direction == "right" and self.rect.x >= 900:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = score_font.render(f'Score: {current_time}', False, FONT_COLOR)
    score_rect = score_surf.get_rect(center=SCORE_POSITION)
    screen.blit(score_surf, score_rect)
    return current_time


def write_score_to_file(score):
    with open('score_history.txt', 'a') as file:
        file.write(str(score) + '\n')

def get_high_score():
    try:
        with open('high_score.txt', 'r') as file:
            return int(file.readline())
    except FileNotFoundError:
        return 0  # If file doesn't exist, set current high score to 0
def write_high_score_to_file(score):
    current_high_score = get_high_score()
    # If the new score is greater than the current high score, overwrite it in the file
    if score > current_high_score:
        with open('high_score.txt', 'w') as file:
            file.write(str(score))

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
title_font = pygame.font.Font('font/Pixeltype.ttf', 80)
score_font = pygame.font.Font('font/Pixeltype.ttf', 30)
final_score_font = pygame.font.Font('font/Pixeltype.ttf', 30)
high_score_font = pygame.font.Font('font/Pixeltype.ttf', 30)
message_font = pygame.font.Font('font/Pixeltype.ttf', 30)
game_active = False
start_time = 0
score = 0
isScoreStoredForCurrentGameNumber = False
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(BG_MUSIC_VOLUME)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.jpg').convert()

obstacle_rect_list = []

player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/player/title.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = title_font.render(GAME_TITLE, False, FONT_COLOR)
game_name_rect = game_name.get_rect(center=TITLE_POSITION)

game_message = message_font.render('Press space to start', False, FONT_COLOR)
game_message_rect = game_message.get_rect(center=MESSAGE_POSITION)

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, OBSTACLE_TIMER)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:  # start screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                isScoreStoredForCurrentGameNumber = False

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird', 'bird', 'minotaur'])))


    if game_active:
        screen.blit(sky_surface, (0, 0))
        width_covered = 0
        while width_covered < 800:
            screen.blit(ground_surface, (width_covered, GROUND_LEVEL))
            width_covered += ground_surface.get_width()
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

    else:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        obstacle_rect_list.clear()
        player_gravity = 0
        high_score = get_high_score()
        high_score_message = high_score_font.render(f'High Score: {high_score}', False, FONT_COLOR)
        score_message = final_score_font.render(f'Your score: {score}', False, FONT_COLOR)
        score_message_rect = score_message.get_rect(center=FINAL_SCORE_POSITION)
        high_score_message_rect = high_score_message.get_rect(center=HIGH_SCORE_POSITION)

        if score > 0 and not isScoreStoredForCurrentGameNumber:
            isScoreStoredForCurrentGameNumber = True
            write_score_to_file(score)
            write_high_score_to_file(score)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(high_score_message, high_score_message_rect)
            player.sprite.rect.x = PLAYER_START_X

    pygame.display.update()
    clock.tick(60)
