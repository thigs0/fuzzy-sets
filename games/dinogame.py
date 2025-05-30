import pygame
import random
import sys
import time
import numpy as np
from fuzzysets import TriangularFuzzyNumber, Tnorm, AND, MamdaniInference

# Definição dos números fuzzy
fcactus_near = TriangularFuzzyNumber(r=210, n=100, l=90)
scactus_near = TriangularFuzzyNumber(r=900, n=300, l=90)
jump = TriangularFuzzyNumber(r=1, n=0, l=-1)

# Sistema fuzzy
w1 = AND([fcactus_near, scactus_near])
mi = MamdaniInference()
mi.add_rule(antecedent=w1, consequent=jump)

# Inicializa o pygame
pygame.init()

# Tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Dinossauro 🦖")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DINO_COLOR = (0, 150, 0)
CACTUS_COLOR = (150, 75, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Dinossauro
dino_width = 40
dino_height = 60
duck_height = 30
dino_x = 50
dino_y = HEIGHT - dino_height - 40
dino_vel_y = 0
is_jumping = False
is_ducking = False
gravity = 0.8

# Cactos
cactus_width = 20
cactus_height = 40
cactus_speed = 6
cactus_spawn_delay = 1500
last_cactus_time = pygame.time.get_ticks()
cactus_list = []

# Fonte
font = pygame.font.SysFont(None, 36)

# Score
score = 0
start_time = time.time()
time_interval = 10
last_increase_time = start_time
speed_increment = 0.5

def draw_dino(x, y, ducking=False):
    height = duck_height if ducking else dino_height
    pygame.draw.rect(screen, DINO_COLOR, (x, y, dino_width, height))

def draw_cactus(x, y):
    pygame.draw.rect(screen, CACTUS_COLOR, (x, y, cactus_width, cactus_height))

def game_over():
    msg = font.render("Game Over! Pressione R para reiniciar", True, BLACK)
    screen.blit(msg, (WIDTH // 2 - 180, HEIGHT // 2))
    pygame.display.update()

def main():
    global dino_y, dino_vel_y, is_jumping, cactus_speed, score
    global is_ducking, last_increase_time, cactus_list, last_cactus_time

    running = True
    game_is_over = False

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Teclas de abaixar e reiniciar
            if event.type == pygame.KEYDOWN:
                if not game_is_over:
                    if event.key == pygame.K_DOWN:
                        is_ducking = True
                        if is_jumping:
                            is_jumping = False
                            dino_vel_y = 0
                            dino_y = HEIGHT - duck_height - 40
                else:
                    if event.key == pygame.K_r:
                        score = 0
                        cactus_list = []
                        cactus_speed = 6
                        dino_y = HEIGHT - dino_height - 40
                        dino_vel_y = 0
                        is_jumping = False
                        is_ducking = False
                        game_is_over = False
                        last_increase_time = time.time()
                        last_cactus_time = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_ducking = False

        if not game_is_over:
            # Aumenta a dificuldade com o tempo
            current_time = time.time()
            if current_time - last_increase_time > time_interval:
                cactus_speed += speed_increment
                last_increase_time = current_time

            # Atualiza posição do dino
            dino_y += dino_vel_y
            dino_vel_y += gravity

            if not is_ducking and dino_y >= HEIGHT - dino_height - 40:
                dino_y = HEIGHT - dino_height - 40
                is_jumping = False
            elif is_ducking and dino_y >= HEIGHT - duck_height - 40:
                dino_y = HEIGHT - duck_height - 40
                is_jumping = False

            # Spawn de cactos
            now = pygame.time.get_ticks()
            if now - last_cactus_time > cactus_spawn_delay:
                cactus_x = WIDTH + random.randint(0, 200)
                cactus_list.append(cactus_x)
                last_cactus_time = now

            # Move e filtra cactos
            cactus_list = [x - cactus_speed for x in cactus_list if x > -cactus_width]

            # Fuzzy: define entradas e decide se pula
            inputs = cactus_list[:2] if len(cactus_list) >= 2 else cactus_list + [WIDTH + 200] * (2 - len(cactus_list))
            print(mi.infer(inputs, np.linspace(0, 100, 500)), inputs)
            fuzzy_output = mi.infer(inputs, np.linspace(0, 100, 500))

            if fuzzy_output > 0 and not is_jumping:
                dino_vel_y = -15
                is_jumping = True

            # Colisão
            dino_height_actual = duck_height if is_ducking else dino_height
            dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height_actual)

            for cactus_x in cactus_list:
                draw_cactus(cactus_x, HEIGHT - cactus_height - 40)
                cactus_rect = pygame.Rect(cactus_x, HEIGHT - cactus_height - 40, cactus_width, cactus_height)
                if dino_rect.colliderect(cactus_rect):
                    game_is_over = True

            # Pontuação
            score += 0.01

            # Desenho
            draw_dino(dino_x, dino_y, is_ducking)
            score_text = font.render(f"Score: {int(score)}  |  Velocidade: {round(cactus_speed, 1)}", True, BLACK)
            screen.blit(score_text, (10, 10))
        else:
            game_over()

        pygame.display.update()

# Inicia o jogo
main()

