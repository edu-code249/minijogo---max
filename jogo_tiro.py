import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Robot Defense - Template")

FPS = 60
clock = pygame.time.Clock()

# fundo game over
fundo_game_over = pygame.image.load("sprites/fundo/fundo.png").convert()
fundo_game_over = pygame.transform.scale(fundo_game_over, (LARGURA, ALTURA))

# carregando sprite de morte dos robôs
animacao_morte = []
numero_de_frames_morte = 8
som_explosao = pygame.mixer.Sound('sons/explosao/som_explosao.wav')
som_explosao.set_volume(0.3)

for i in range(1, numero_de_frames_morte + 1):
    img = pygame.image.load(f'sprites/explosao/explosao-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (100, 100))
    animacao_morte.append(img)

# carregando sprite do tiro
animacao_tiro = []
numero_de_frames_tiro = 4
som_tiro = pygame.mixer.Sound('sons/tiro/som_tiro.wav')
som_tiro.set_volume(0.2)

for i in range(1, numero_de_frames_tiro + 1):
    img = pygame.image.load(f'sprites/tiro/tiro-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    animacao_tiro.append(img)

# carregando os sprites do coração e dos pontos
maximo_vida = 5

sprite_coracao = pygame.image.load('sprites/coracao/coracao_azul.png').convert_alpha()
sprite_coracao = pygame.transform.scale(sprite_coracao, (40, 40))

sprite_coracao_vazio = pygame.image.load('sprites/coracao/coracao_preto.png').convert_alpha()
sprite_coracao_vazio = pygame.transform.scale(sprite_coracao_vazio, (40, 40))

fonte = pygame.font.SysFont(None, 36)

# carregando frames dos robôs e do personagem principal
numero_frames_entidade = 6
animacao_player = []
animacao_robo_lento = []
animacao_robo_rapido = []
animacao_robo_zigue_zag = []
animacao_saltador = []
animacao_cacador = []

# CLASSE BASE
class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image.fill((0, 255, 0))  # verde
        self.vida = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.mover(self.velocidade, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y, animacao_frames):
        super().__init__(x, y, 10)
        self.image = animacao_tiro[0]
        self.frames = animacao_frames

        if not self.frames:
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 255, 0))
        else:
            self.frame_atual = 0
            self.image = self.frames[self.frame_atual]
            self.ultima_atualizacao = pygame.time.get_ticks()
            self.velocidade_animacao = 100
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= self.velocidade
        if self.frames:
            agora = pygame.time.get_ticks()
            if agora - self.ultima_atualizacao > self.velocidade_animacao:
                self.ultima_atualizacao = agora
                self.frame_atual += 1
                if self.frame_atual >= len(self.frames):
                    self.frame_atual = 0
                self.image = self.frames[self.frame_atual]

        if self.rect.y < 0:
            self.kill()

# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))  # vermelho

    def atualizar_posicao(self):
        raise NotImplementedError

# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# robô lento
class RoboLento(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.image.fill((0, 0, 255))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# robô rapido
class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)
        self.image.fill((255, 165, 0))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# robô saltador
class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.image.fill((100, 255, 100))  # roxo?
        self.contador_salto = 0
        self.salto_intervalo = random.randint(40, 90)
        self.forca_salto = random.randint(8, 14)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

        # contador para decidir a hora de saltar
        self.contador_salto += 4
        if self.contador_salto >= self.salto_intervalo:
            self.rect.y += self.forca_salto
            self.contador_salto = 0

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# robô caçador
class RoboCacador(Robo):
    def __init__(self, x, y, jogador):
        super().__init__(x, y, velocidade=4)
        self.jogador = jogador
        self.image.fill((255, 0, 255))  # rosa

    def atualizar_posicao(self):
        # seguir o jogador horizontalmente
        if self.jogador.rect.centerx < self.rect.centerx:
            self.rect.x -= 2
        elif self.jogador.rect.centerx > self.rect.centerx:
            self.rect.x += 2

        # avança para baixo
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# classe para o fundo do jogo
class Fundo(pygame.sprite.Sprite):
    def __init__(self, imagem_path):
        super().__init__()
        self.image = pygame.image.load(imagem_path).convert()
        self.image = pygame.transform.scale(self.image, (LARGURA, ALTURA))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

# classe para a explosão
class Explosao(pygame.sprite.Sprite):
    def __init__(self, centro_x, centro_y, animacao_frames):
        super().__init__()
        self.frames = animacao_frames

        self.frame_atual = 0
        self.ultima_atualizacao = pygame.time.get_ticks()
        self.velocidade_animacao = 50

        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=(centro_x, centro_y))

    def update(self):
        agora = pygame.time.get_ticks()

        if agora - self.ultima_atualizacao > self.velocidade_animacao:
            self.ultima_atualizacao = agora
            self.frame_atual += 1

            if self.frame_atual < len(self.frames):
                self.image = self.frames[self.frame_atual]
                centro = self.rect.center
                self.rect = self.image.get_rect(center=centro)
            else:
                self.kill()

# carregando imagens do HUD
def desenhar_hud(tela, jogador_vida, pontos):
    if sprite_coracao and sprite_coracao_vazio:
        x_inicial = 10
        y_pos = 10

        for i in range(maximo_vida):
            if i < jogador_vida:
                sprite_a_desenhar = sprite_coracao
            else:
                sprite_a_desenhar = sprite_coracao_vazio
            tela.blit(sprite_a_desenhar, (x_inicial + i * 45, y_pos))
    else:
        texto_vida = fonte.render(f"Vida: {jogador_vida}", True, (255, 255, 255))
        tela.blit(texto_vida, (10, 10))

    texto_backup = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    tela.blit(texto_backup, (LARGURA - 10 - texto_backup.get_width(), 10))

def tela_game_over():
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                pygame.quit()
                return "sair"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # R para reiniciar
                    game_over = False
                    return "reiniciar"
                if event.key == pygame.K_ESCAPE:  # ESC para sair
                    game_over = False
                    pygame.quit()
                    return "sair"

        # fundo da tela de game over
        TELA.blit(fundo_game_over, (0, 0))

        texto_game_over = fonte.render("GAME OVER", True, (255, 0, 0))
        texto_restart = fonte.render("Pressione R para reiniciar", True, (255, 255, 255))
        texto_sair = fonte.render("ESC para sair", True, (255, 255, 255))

        TELA.blit(texto_game_over, (LARGURA // 2 - texto_game_over.get_width() // 2, ALTURA // 2 - 60))
        TELA.blit(texto_restart, (LARGURA // 2 - texto_restart.get_width() // 2, ALTURA // 2))
        TELA.blit(texto_sair, (LARGURA // 2 - texto_sair.get_width() // 2, ALTURA // 2 + 40))

        pygame.display.flip()
        clock.tick(15)

def resetar_jogo():
    global todos_sprites, inimigos, tiros, jogador, pontos, spawn_timer

    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()

    # recria fundo
    fundo_sprite = Fundo('sprites/fundo/fundo.png')
    todos_sprites.add(fundo_sprite)

    # recria jogador
    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)

    pontos = 0
    spawn_timer = 0

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

resetar_jogo()

rodando = True
while rodando:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y, animacao_tiro)
                todos_sprites.add(tiro)
                tiros.add(tiro)
                if som_tiro:
                    som_tiro.play()

    spawn_timer += 1
    if spawn_timer > 40:
        tipo = random.choice(["zigue", "lento", "rapido", "saltador", "cacador"])
        x_spawn = random.randint(40, LARGURA - 40)

        if tipo == "zigue":
            robo = RoboZigueZague(x_spawn, -40)
        elif tipo == "lento":
            robo = RoboLento(x_spawn, -40)
        elif tipo == "rapido":
            robo = RoboRapido(x_spawn, -40)
        elif tipo == "saltador":
            robo = RoboSaltador(x_spawn, -40)
        elif tipo == "cacador":
            robo = RoboCacador(x_spawn, -40, jogador)

        todos_sprites.add(robo)
        inimigos.add(robo)
        spawn_timer = 0

    # colisão tiro x robô
    colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)

    # acionando a animação de explosão
    for robo_destruido in colisao.keys():
        pontos += len(colisao)

        centro_x = robo_destruido.rect.centerx
        centro_y = robo_destruido.rect.centery

        if animacao_morte:
            explosao = Explosao(centro_x, centro_y, animacao_morte)
            todos_sprites.add(explosao)
            if som_explosao:
                som_explosao.play()

    # colisão robô x jogador
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        jogador.vida -= 1
        if jogador.vida <= 0:
            resultado = tela_game_over()
            if resultado == "reiniciar":
                resetar_jogo()
            else: 
                rodando = False

    # atualizar
    todos_sprites.update()

    # desenhar
    TELA.blit(fundo_game_over, (0, 0))
    todos_sprites.draw(TELA)
    desenhar_hud(TELA, jogador.vida, pontos)

    pygame.display.flip()

pygame.quit()
