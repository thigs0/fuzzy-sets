import os
import sys
import time
import random
import pygame
import numpy as np
from fuzzysets import TriangularFuzzyNumber, AND, MamdaniInference, TakagiSugenoInference, Surface
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# ——— Configurações Fuzzy —————————————————————————————————————————————
#fcactus_near = TriangularFuzzyNumber(r=210, n=100, l=90)
dist_low = TriangularFuzzyNumber(r=0.003, n=0, l=-1)
dist_med = TriangularFuzzyNumber(r=0.08, n=0.05, l=0.02)
dist_high = TriangularFuzzyNumber(r=1, n=0.5, l=0.07)

vel_low = TriangularFuzzyNumber(r=7, n=6, l=5)
vel_high = TriangularFuzzyNumber(r=12, n=9, l=6.999)

#scactus_near = TriangularFuzzyNumber(r=900, n=300, l=90)

#Mamdani Method Fuzzy results:
#jump_zero     = TriangularFuzzyNumber(r=0.0001,   n=0,   l=-1)
#jump_low      = TriangularFuzzyNumber(r=0.801,   n=0.8,   l=0)
#jump_high     = TriangularFuzzyNumber(r=1,   n=0.9,   l=0.8)

#functions for Takagi-Sugeno Method:
def jump_zero(x):return 0
def jump_low(x): return 0.4
def jump_high(x): return 1

#rules for x = distance:
#w1 = AND([dist_low,dist_low])
#w2 = AND([dist_med,dist_med])
#w3 = AND([dist_high,dist_high])

#rules for x1 = distance; x2 = velocity
w1 = AND([dist_low,vel_low])
w2 = AND([dist_med,vel_low])
w3 = AND([dist_high,vel_low])
w4 = AND([dist_low,vel_high])
w5 = AND([dist_med,vel_high])
w6 = AND([dist_high,vel_high])


#w1 = AND([fcactus_near, player_vel])

#Mamdani method:
#mi = MamdaniInference()

#Takagi-Sugeno method:
mi = TakagiSugenoInference()


#rules for x = distance:
#mi.add_rule(antecedent=w1, consequent=jump_low)
#mi.add_rule(antecedent=w2, consequent=jump_high)
#mi.add_rule(antecedent=w3, consequent=jump_zero)
#rules for x1 = distance; x2 = velocity

mi.add_rule(antecedent=w1, consequent=jump_high)
mi.add_rule(antecedent=w2, consequent=jump_zero)
#mi.add_rule(antecedent=w3, consequent=jump_zero)
#mi.add_rule(antecedent=w4, consequent=jump_high)
#mi.add_rule(antecedent=w5, consequent=jump_high)
#mi.add_rule(antecedent=w6, consequent=jump_zero)

#Surface(mi, np.linspace(0, 1, 100), np.linspace(6, 8, 100), np.linspace(0,100,500), "out.png")

#------------------------------------------------------------------------
#criando variáveis para o gráfico
out_graph = np.zeros([5000, 3])# número de pontos analisados, x, y
N = 0

#-----------------------------------------------------------------------
# ——— Inicializa Pygame e Tela ——————————————————————————————————————————
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Dinossauro 🦖")
clock = pygame.time.Clock()
FPS   = 60

# ——— Carrega Sprite-Sheet e define sub-surfaces ———————————————————————
ASSETS_PATH  = os.path.join(os.path.dirname(__file__), "assets")
sprite_sheet = pygame.image.load(os.path.join(ASSETS_PATH, "sprite.png")).convert_alpha()
sw, sh       = sprite_sheet.get_size()

def get_image(rect):
    x, y, w, h = rect
    if x < 0 or y < 0 or x + w > sw or y + h > sh:
        raise ValueError(f"Rect {rect} fora dos limites ({sw}×{sh})")
    return sprite_sheet.subsurface(pygame.Rect(rect)).copy()

# Dino correndo e abaixado
# Dino correndo
dino_run = [
    get_image((1514, 0, 89, 94)),  # Char 1
    get_image((1603, 0, 89, 94)),  # Char 2
]

# Ajuste conforme necessário se os sprites de "agachar" estiverem em outro lugar
dino_duck = [
    get_image((1700, 0, 118, 60)),  # Exemplo, ajustar se inválido
    get_image((1820, 0, 118, 60)),
]

# Cactos pequenos e grandes (baseado no offset que você usou no JS: 446 e 652)
cactus_imgs = [
    get_image((446, 2, 34, 70)),    # Small
    get_image((548, 2, 68, 70)),    # Small double
    #get_image((652, 2, 49, 100)),   # Big
]

# Nuvem (posição presumida, ajustar se necessário)
cloud_img = get_image((0, 50, 46, 14))  # Dentro de 130px

# Background (chão): de y = 104 até 122
sw, sh = sprite_sheet.get_size()
background = get_image((0, 104, sw, 18))  # 2404×18, y = 104


# ——— Variáveis de Jogo —————————————————————————————————————————————
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
font  = pygame.font.SysFont(None, 36)

dino_x     = 50
dino_y     = HEIGHT - dino_run[0].get_height() - 40
dino_vel_y = 0
gravity    = 0.8
is_jumping = False
is_ducking = False
dino_frame = 0

bg_x = 0

cactus_list         = []
cactus_speed        = 6
cactus_spawn_delay  = 1500
last_cactus_time    = pygame.time.get_ticks()

cloud_list          = []
cloud_spawn_delay   = 3000
last_cloud_time     = pygame.time.get_ticks()

score               = 0
time_interval       = 10
last_increase_time  = time.time()
speed_increment     = 0.5

# ——— Funções de Desenho —————————————————————————————————————————————
def draw_background(x):
    screen.blit(background, (x, HEIGHT - dino_run[0].get_height()))

def draw_dino():
    global dino_frame
    seq = dino_duck if is_ducking else dino_run
    img = seq[(dino_frame // 5) % len(seq)]
    screen.blit(img, (dino_x, dino_y))
    dino_frame += 1

def draw_cactus(x):
    img = random.choice(cactus_imgs)
    y   = HEIGHT - img.get_height() - 40
    screen.blit(img, (x, y))
    return pygame.Rect(x, y, img.get_width(), img.get_height())

def game_over():
    msg = font.render("Game Over! Pressione R para reiniciar", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
# Substitua a lista de cactos por uma com tuplas (x, img)
cactus_list = []  # cada item será (x, img)

# ——— Alterações no loop principal ———————————————————————
def main():
    global dino_y, dino_vel_y, is_jumping, is_ducking
    global cactus_speed, score, cactus_list
    global last_cactus_time, last_cloud_time, last_increase_time
    global cloud_list, bg_x
    N = 0
    running      = True
    game_is_over = False

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        # Eventos (sem alterações)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if not game_is_over and e.key == pygame.K_DOWN:
                    is_ducking = True
                    if is_jumping:
                        is_jumping = False
                        dino_vel_y = 0
                        dino_y     = HEIGHT - dino_duck[0].get_height() - 40
                if game_is_over and e.key == pygame.K_r:
                    cactus_list        = []
                    cloud_list         = []
                    cactus_speed       = 6
                    score              = 0
                    is_jumping = is_ducking = False
                    dino_y             = HEIGHT - dino_run[0].get_height() - 40
                    dino_vel_y         = 0
                    last_cactus_time   = pygame.time.get_ticks()
                    last_cloud_time    = pygame.time.get_ticks()
                    last_increase_time = time.time()
                    game_is_over       = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                is_ducking = False

        if not game_is_over:
            # Aumenta dificuldade
            now_time = time.time()
            if now_time - last_increase_time > time_interval:
                cactus_speed       += speed_increment
                last_increase_time  = now_time

            # Física do Dino
            if is_jumping:
                dino_y     += dino_vel_y
                dino_vel_y += gravity
            floor_y = HEIGHT - (dino_duck[0].get_height() if is_ducking else dino_run[0].get_height()) - 40
            if dino_y >= floor_y:
                dino_y     = floor_y
                is_jumping = False

            # Scroll do chão
            bg_x -= cactus_speed
            if bg_x <= -sw:
                bg_x = 0

            # Spawn de cactos
            now = pygame.time.get_ticks()
            if now - last_cactus_time > cactus_spawn_delay:
                cactus_x   = WIDTH + random.randint(0, 200)
                cactus_img = random.choice(cactus_imgs)
                cactus_list.append((cactus_x, cactus_img))
                last_cactus_time = now

            # Spawn de nuvens
            if now - last_cloud_time > cloud_spawn_delay:
                cloud_list.append(WIDTH + random.randint(0,200))
                last_cloud_time = now

            # Move e filtra obstáculos
            new_cactus_list = []
            for x, img in cactus_list:
                x -= cactus_speed
                if x > -100:
                    new_cactus_list.append((x, img))
            cactus_list = new_cactus_list

            cloud_list = [x - (cactus_speed // 2) for x in cloud_list if x > -100]

            # Inferência Fuzzy e Pulo Automático
            # Considera apenas a distância horizontal do cacto mais próximo ao Dino
            if cactus_list:
                nearest_dist = cactus_list[0][0] - (dino_x + dino_run[0].get_width())
            else:
                nearest_dist = WIDTH  # nenhum cacto na tela
            if nearest_dist < 0:
                nearest_dist = 0
            #print(nearest_dist)
            #Distância normalizada:
            norm_dist = nearest_dist / WIDTH
            print(norm_dist)
            #velocidade: cactus_speed
            fuzzy_value = mi.infer([norm_dist,cactus_speed], np.linspace(0, 100, 500))

            out_graph[N,:] = np.array([N, norm_dist, cactus_speed])
            N+=1

            print(norm_dist, cactus_speed)
            if fuzzy_value > 0.0001 and not is_jumping:
                dino_vel_y = -15*fuzzy_value if 15*fuzzy_value > 15 else -15
                is_jumping = True

            # Desenho
            draw_background(bg_x)
            draw_background(bg_x + sw)

            for cx, img in cactus_list:
                y = HEIGHT - img.get_height() - 40
                rect = pygame.Rect(cx, y, img.get_width(), img.get_height())
                screen.blit(img, (cx, y))

                dino_rect = pygame.Rect(
                    dino_x, dino_y,
                    dino_run[0].get_width(),
                    dino_duck[0].get_height() if is_ducking else dino_run[0].get_height()
                )
                if dino_rect.colliderect(rect):
                    game_is_over = True

            for cx in cloud_list:
                screen.blit(cloud_img, (cx, random.randint(50,150)))

            draw_dino()

            # Score
            score += 0.01
            txt = font.render(f"Score: {int(score)}  |  Vel: {cactus_speed:.1f}", True, BLACK)
            screen.blit(txt, (10,10))

        else:
            game_over()
            #ax = Surface(mi, np.linspace(0, 1, 100), np.linspace(6, 8, 100), np.linspace(0,100,500), "out.png")
            for i in range(N):
                print(out_graph[i, 1], out_graph[i, 2])
                ax.scatter(out_graph[i, 1], out_graph[i, 2], 0, color='black')
                plt.savefig(f'out/out{i}.png')

        pygame.display.update()

if __name__ == "__main__":
    main()
