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
pygame.mixer.music.load('sons/fundo/musica_fundo.wav')
pygame.mixer.music.set_volume(10.0)
pygame.mixer.music.play(-1)


fundo_game_over = pygame.image.load("sprites/fundo/fundo_game_over.png").convert()
fundo_game_over = pygame.transform.scale(fundo_game_over, (LARGURA, ALTURA))
som_game_over = pygame.mixer.Sound('sons/game_over/som_game_over.wav')
som_game_over.set_volume(10.0)


som_restart = pygame.mixer.Sound('sons/game_over/som_restart.wav')
som_restart.set_volume(5.0)


som_dano = pygame.mixer.Sound('sons/game_over/som_dano.wav')
som_dano.set_volume(5.0)


# carregando sprite de morte dos robôs
animacao_morte = []
animacao_morte_boss = []
numero_de_frames_morte = 8
som_explosao = pygame.mixer.Sound('sons/explosao/som_explosao.wav')
som_explosao.set_volume(3.0)


for i in range(1, numero_de_frames_morte + 1):
    img = pygame.image.load(f'sprites/explosao/explosao-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (100, 100))
    animacao_morte.append(img)


for i in range(1, numero_de_frames_morte + 1):
    img = pygame.image.load(f'sprites/explosao/explosao-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (200, 200))
    animacao_morte_boss.append(img)


# carregando sprite do tiro
animacao_tiro = []
numero_de_frames_tiro = 4
som_tiro = pygame.mixer.Sound('sons/tiro/som_tiro.wav')
som_tiro.set_volume(5.0)


for i in range(1, numero_de_frames_tiro + 1):
    img = pygame.image.load(f'sprites/tiro/tiro-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    animacao_tiro.append(img)



# sprites HUD
maximo_vida = 5  # este valor poderá ser aumentado


sprite_coracao = pygame.image.load('sprites/coracao/coracao_azul.png').convert_alpha()
sprite_coracao = pygame.transform.scale(sprite_coracao, (40, 40))


sprite_coracao_vazio = pygame.image.load('sprites/coracao/coracao_preto.png').convert_alpha()
sprite_coracao_vazio = pygame.transform.scale(sprite_coracao_vazio, (40, 40))


fonte = pygame.font.SysFont(None, 36)


som_joaildo = None
try:
    som_joaildo = pygame.mixer.Sound('sons/easteregg/play_joaildo.wav')
    som_joaildo.set_volume(10.0)
except:
    pass


buff_ativo = False
buff_duracao = 10000
buff_inicio = 0


cacadores_eliminados = 0
CACADORES_PARA_ATIVAR = 10
#POWERUPS
powerup_velocidade_ativo = False
powerup_velocidade_duracao = 6000
powerup_velocidade_inicio = 0


powerup_tiro_triplo_ativo = False
powerup_tiro_triplo_duracao = 6000
powerup_tiro_triplo_inicio = 0



# classe botão
class Botao:
    def __init__(self, texto, x, y, largura, altura, cor_normal, cor_hover, fonte):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.fonte = fonte


    def desenhar(self, tela, mouse_pos):
        cor = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor_normal
        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        texto_render = self.fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(
            texto_render,
            (self.rect.x + (self.rect.width - texto_render.get_width()) // 2,
             self.rect.y + (self.rect.height - texto_render.get_height()) // 2)
        )


    def clicado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)



# FRAMES ENTIDADES
numero_frames_entidade = 4


animacao_player = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/player/player-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    animacao_player.append(img)




animacao_robo_chefe = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/boss/boss-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (150, 150))
    animacao_robo_chefe.append(img)




animacao_robo_lento = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/robo_lento/robo_l-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    animacao_robo_lento.append(img)




animacao_robo_rapido = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/robo_rapido/robo_r-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    animacao_robo_rapido.append(img)




animacao_robo_zigue_zag = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/robo_zigue_zag/robo_z-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    animacao_robo_zigue_zag.append(img)




animacao_saltador = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/robo_saltador/robo_s-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    animacao_saltador.append(img)




animacao_cacador = []
for i in range(1, numero_frames_entidade + 1):
    img = pygame.image.load(f'sprites/robo_cacador/robo_c-00{i:02d}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    animacao_cacador.append(img)





# CLASSE BASE




class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))




    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy






# JOGADOR




class Jogador(Entidade):
    def __init__(self, x, y):
        self.velocidade_base = 5
        self.velocidade_buff = 10
        self.velocidade_powerup = 7.5  # mais rápido que o buff normal
        super().__init__(x, y, self.velocidade_base)
        self.vida = 5
        global animacao_player
        self.frames = animacao_player
        self.frame_atual = 0
        self.ultima_atualizacao = pygame.time.get_ticks()
        self.velocidade_animacao = 150
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=(x, y))




    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultima_atualizacao > self.velocidade_animacao:
            self.ultima_atualizacao = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            centro = self.rect.center
            self.image = self.frames[self.frame_atual]
            self.rect = self.image.get_rect(center=centro)




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




        # limites da tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))
        self.animar()






# TIRO DO JOGADOR




class Tiro(Entidade):
    def __init__(self, x, y, animacao_frames, dx=0):
        super().__init__(x, y, 10)
        self.frames = animacao_frames
        self.dx = dx



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
        self.rect.x += self.dx
        # animação
        if self.frames:
            agora = pygame.time.get_ticks()
            if agora - self.ultima_atualizacao > self.velocidade_animacao:
                self.ultima_atualizacao = agora
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)
                self.image = self.frames[self.frame_atual]




        if self.rect.y < 0 or self.rect.x < -50 or self.rect.x > LARGURA + 50:
            self.kill()






# ROBÔ BASE




class Robo(Entidade):
    def __init__(self, x, y, velocidade, animacao_frames):
        super().__init__(x, y, velocidade)
        self.frames = animacao_frames
        self.frame_atual = 0
        self.ultima_atualizacao = pygame.time.get_ticks()
        self.velocidade_animacao = 150




        if self.frames:
            self.image = self.frames[self.frame_atual]
            self.rect = self.image.get_rect(center=(x, y))




    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultima_atualizacao > self.velocidade_animacao:
            self.ultima_atualizacao = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            centro = self.rect.center
            self.image = self.frames[self.frame_atual]
            self.rect = self.image.get_rect(center=centro)




    def atualizar_posicao(self):
        raise NotImplementedError




    def update(self):
        self.animar()
        self.atualizar_posicao()






# ROBÔS NORMAIS




class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, 3, animacao_robo_zigue_zag)
        self.direcao = 1




    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3




        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1




        if self.rect.y > ALTURA:
            self.kill()





class RoboLento(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, 2, animacao_robo_lento)




    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()





class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, 8, animacao_robo_rapido)




    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()





class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, 3, animacao_saltador)
        self.contador_salto = 0
        self.salto_intervalo = random.randint(40, 90)
        self.forca_salto = random.randint(8, 14)




    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.contador_salto += 4
        if self.contador_salto >= self.salto_intervalo:
            self.rect.y += self.forca_salto
            self.contador_salto = 0




        if self.rect.y > ALTURA:
            self.kill()





class RoboCacador(Robo):
    def __init__(self, x, y, jogador):
        super().__init__(x, y, 6, animacao_cacador)
        self.jogador = jogador




    def atualizar_posicao(self):
        if self.jogador.rect.centerx < self.rect.centerx:
            self.rect.x -= 2
        elif self.jogador.rect.centerx > self.rect.centerx:
            self.rect.x += 2




        self.rect.y += self.velocidade




        if self.rect.y > ALTURA:
            self.kill()





# ROBO CHEFÃO  (BOSS)




class RoboChefao(Robo):
    def __init__(self, x, y, jogador):
        # usa o sprite do robo lento (ampliado)
        super().__init__(x, y, velocidade=2, animacao_frames = animacao_robo_chefe)
        self.jogador = jogador
        self.vida = 30
        self.atirando_timer = 0




    def atualizar_posicao(self):
        # segue lentamente o jogador
        if self.jogador.rect.centerx < self.rect.centerx:
            self.rect.x -= 1
        elif self.jogador.rect.centerx > self.rect.centerx:
            self.rect.x += 1




        # desce e para numa altura fixa
        self.rect.y += self.velocidade
        if self.rect.y > 120:
            self.rect.y = 120




        # dispara periodicamente
        self.atirando_timer += 1
        if self.atirando_timer >= 50:
            self.atirando_timer = 0
            tiro = TiroChefao(self.rect.centerx, self.rect.bottom)
            todos_sprites.add(tiro)
            inimigos.add(tiro)
            som_tiro.play()




    def levar_dano(self):
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
            explosao = Explosao(self.rect.centerx, self.rect.centery, animacao_morte_boss)
            todos_sprites.add(explosao)
            if som_explosao:
                som_explosao.play()






# TIRO DO CHEFÃO




class TiroChefao(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=6)
        self.image = pygame.Surface((22, 22))
        self.image.fill((255, 0, 80))
        self.rect = self.image.get_rect(center=(x, y))




    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()






# FUNDO




class Fundo(pygame.sprite.Sprite):
    def __init__(self, imagem_path):
        super().__init__()
        self.image = pygame.image.load(imagem_path).convert()
        self.image = pygame.transform.scale(self.image, (LARGURA, ALTURA))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)






# EXPLOSÃO




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
                centro = self.rect.center
                self.image = self.frames[self.frame_atual]
                self.rect = self.image.get_rect(center=centro)
            else:
                self.kill()



#cLASSE POWERUPS
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((30, 30))
        if tipo == "velocidade":
            self.image.fill((255, 255, 0))  
        elif tipo == "vida":
            self.image.fill((255, 0, 0))  
        elif tipo == "tiro_triplo":
            self.image.fill((0, 255, 0))    
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 2



    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA + 40:
            self.kill()





# HUD (inclui barra de vida do chefão)




def desenhar_hud(tela, jogador_vida, pontos, buff_ativo_local, cacadores_local,
                 powerup_velocidade_on, powerup_tiro_triplo_on):




    # corações
    if sprite_coracao and sprite_coracao_vazio:
        x_inicial = 10
        y_pos = 10
        for i in range(maximo_vida):
            if i < jogador_vida:
                sprite = sprite_coracao
            else:
                sprite = sprite_coracao_vazio
            tela.blit(sprite, (x_inicial + i * 45, y_pos))




    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    tela.blit(texto_pontos, (LARGURA - texto_pontos.get_width() - 10, 10))




    # buff joaildo
    if buff_ativo_local:
        texto_buff = fonte.render("BUFF ATIVADO!", True, (255, 255, 0))
        tela.blit(texto_buff, (LARGURA//2 - texto_buff.get_width()//2, 50))



    # info power-ups
    y_info = 80
    if powerup_velocidade_on:
        texto_v = fonte.render("VELOCIDADE", True, (0, 255, 0))
        tela.blit(texto_v, (10, y_info))
        y_info += 30
    if powerup_tiro_triplo_on:
        texto_t = fonte.render("TIRO TRIPLO", True, (255, 255, 0))
        tela.blit(texto_t, (10, y_info))




    # BARRA DE VIDA DO CHEFÃO
    
    for inimigo in inimigos:
        if isinstance(inimigo, RoboChefao):
            vida_max = 30
            largura = 300
            altura = 20
            x = LARGURA // 2 - largura // 2
            y = 90




            proporcao = inimigo.vida / vida_max
            largura_atual = int(largura * proporcao)




            pygame.draw.rect(tela, (255, 0, 0), (x, y, largura, altura))
            pygame.draw.rect(tela, (0, 255, 0), (x, y, largura_atual, altura))




            texto = fonte.render("CHEFÃO", True, (255, 255, 255))
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, y - 25))
            break






# TELA GAME OVER




def tela_game_over():
    largura_botao = 200
    altura_botao = 60
    espaco = 40




    total_largura = largura_botao * 2 + espaco
    x_inicial = LARGURA // 2 - total_largura // 2
    y_botoes = ALTURA // 2




    botao_reiniciar = Botao("Reiniciar", x_inicial, y_botoes,
                            largura_botao, altura_botao,
                            (40, 40, 180), (70, 70, 250), fonte)
    botao_sair = Botao("Sair", x_inicial + largura_botao + espaco, y_botoes,
                       largura_botao, altura_botao,
                       (40, 40, 180), (70, 70, 250), fonte)




    game_over = True
    while game_over:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "sair"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_reiniciar.clicado(mouse_pos):
                    return "reiniciar"
                if botao_sair.clicado(mouse_pos):
                    pygame.quit()
                    return "sair"




        TELA.blit(fundo_game_over, (0, 0))




        txt = fonte.render("GAME OVER", True, (255, 255, 255))
        TELA.blit(txt, (LARGURA//2 - txt.get_width()//2, ALTURA//2 - 100))




        botao_reiniciar.desenhar(TELA, mouse_pos)
        botao_sair.desenhar(TELA, mouse_pos)




        pygame.display.flip()
        clock.tick(30)






# RESET DO JOGO




def resetar_jogo():
    global todos_sprites, inimigos, tiros, jogador, pontos, spawn_timer
    global buff_ativo, buff_inicio, cacadores_eliminados, chefao_spawnado
    global powerups, powerup_velocidade_ativo, powerup_tiro_triplo_ativo
    global powerup_velocidade_inicio, powerup_tiro_triplo_inicio
    global maximo_vida




    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()
    powerups.empty()




    fundo_sprite = Fundo('sprites/fundo/fundo.png')
    todos_sprites.add(fundo_sprite)




    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)




    pontos = 0
    spawn_timer = 0




    buff_ativo = False
    buff_inicio = 0
    cacadores_eliminados = 0
    chefao_spawnado = False  # permite novo chefão ao reiniciar


    powerup_velocidade_ativo = False
    powerup_tiro_triplo_ativo = False
    powerup_velocidade_inicio = 0
    powerup_tiro_triplo_inicio = 0

    maximo_vida = 5  # reset do máximo de vida

    jogador.velocidade = jogador.velocidade_base





# INICIALIZAÇÃO DE GRUPOS E VARIÁVEIS




todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
powerups = pygame.sprite.Group()




chefao_spawnado = False  # só vai aparecer uma vez por partida




resetar_jogo()



# controle de spawn de power-ups
powerup_spawn_timer = 0
powerup_spawn_intervalo = 180 




rodando = True
while rodando:
    clock.tick(FPS)




    # EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False




        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # TIRO NORMAL OU TRIPLO
                if powerup_tiro_triplo_ativo:
                    tiro_c = Tiro(jogador.rect.centerx, jogador.rect.y, animacao_tiro, dx=0)
                    tiro_e = Tiro(jogador.rect.centerx, jogador.rect.y, animacao_tiro, dx=-3)
                    tiro_d = Tiro(jogador.rect.centerx, jogador.rect.y, animacao_tiro, dx=3)
                    for tiro in (tiro_c, tiro_e, tiro_d):
                        todos_sprites.add(tiro)
                        tiros.add(tiro)
                else:
                    tiro = Tiro(jogador.rect.centerx, jogador.rect.y, animacao_tiro)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)



                if som_tiro:
                    som_tiro.play()




    
    # SPAWN ÚNICO DO CHEFÃO QUANDO PONTOS >= 100
    
    if pontos >= 100 and not chefao_spawnado:
        chefao = RoboChefao(LARGURA // 2, -200, jogador)
        todos_sprites.add(chefao)
        inimigos.add(chefao)
        chefao_spawnado = True




    # SPAWN NORMAL DOS INIMIGOS
    
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




        # MAS se o chefão estiver vivo, NÃO gera inimigos normais
        if not any(isinstance(i, RoboChefao) for i in inimigos):
            todos_sprites.add(robo)
            inimigos.add(robo)




        spawn_timer = 0


    powerup_spawn_timer += 1
    if powerup_spawn_timer > powerup_spawn_intervalo:
        powerup_spawn_timer = 0
        tipo_pu = random.choice(["velocidade", "vida", "tiro_triplo"])
        x_pu = random.randint(40, LARGURA - 40)
        pu = PowerUp(x_pu, -30, tipo_pu)
        todos_sprites.add(pu)
        powerups.add(pu)




    
    # COLISÃO TIRO DO JOGADOR x INIMIGOS
    
    colisao = pygame.sprite.groupcollide(inimigos, tiros, False, True)




    for inimigo, lista_tiros in colisao.items():




        # Chefão leva dano, não morre direto
        if isinstance(inimigo, RoboChefao):
            for _ in lista_tiros:
                inimigo.levar_dano()
            continue




        # Inimigos normais morrem
        inimigo.kill()
        pontos += 2 if buff_ativo else 1




        # Caçador conta para buff
        if isinstance(inimigo, RoboCacador):
            if not buff_ativo:
                cacadores_eliminados += 1
                if cacadores_eliminados >= CACADORES_PARA_ATIVAR:
                    buff_ativo = True
                    buff_inicio = pygame.time.get_ticks()
                    jogador.velocidade = jogador.velocidade_buff
                    if som_joaildo:
                        som_joaildo.play()




        # explosão normal
        cx = inimigo.rect.centerx
        cy = inimigo.rect.centery
        explosao = Explosao(cx, cy, animacao_morte)
        todos_sprites.add(explosao)
        if som_explosao:
            som_explosao.play()




    # COLISÃO INIMIGOS x JOGADOR
    
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        jogador.vida -= 1
        som_dano.play()

        if jogador.vida <= 0:
            som_game_over.play()
            resultado = tela_game_over()
            som_restart.play()
            if resultado == "reiniciar":
                resetar_jogo()
            else:
                rodando = False



    # COLISÃO JOGADOR x POWER-UPS
    colisao_powerups = pygame.sprite.spritecollide(jogador, powerups, True)
    for pu in colisao_powerups:
        if pu.tipo == "velocidade":
            powerup_velocidade_ativo = True
            powerup_velocidade_inicio = pygame.time.get_ticks()
            jogador.velocidade = jogador.velocidade_powerup
        elif pu.tipo == "vida":
            # se ainda não está com a barra cheia, cura normalmente
            if jogador.vida < maximo_vida:
                jogador.vida += 1
            else:
                # barra cheia: aumenta o máximo e adiciona mais um coração
                maximo_vida += 1
                jogador.vida = maximo_vida
        elif pu.tipo == "tiro_triplo":
            powerup_tiro_triplo_ativo = True
            powerup_tiro_triplo_inicio = pygame.time.get_ticks()


    
    # TEMPO DO BUFF NORMAL (JOAILDO)
    
    if buff_ativo:
        if pygame.time.get_ticks() - buff_inicio > buff_duracao:
            buff_ativo = False
            # se power-up velocidade estiver ativo, mantém a velocidade do power-up,
            # senão volta para base
            if powerup_velocidade_ativo:
                jogador.velocidade = jogador.velocidade_powerup
            else:
                jogador.velocidade = jogador.velocidade_base
            cacadores_eliminados = 0




    # TEMPO DO POWER-UP VELOCIDADE
    if powerup_velocidade_ativo:
        if pygame.time.get_ticks() - powerup_velocidade_inicio > powerup_velocidade_duracao:
            powerup_velocidade_ativo = False
            # se buff joaildo estiver ativo, usa velocidade buff, senão base
            if buff_ativo:
                jogador.velocidade = jogador.velocidade_buff
            else:
                jogador.velocidade = jogador.velocidade_base



    # TEMPO DO POWER-UP TIRO TRIPLO
    if powerup_tiro_triplo_ativo:
        if pygame.time.get_ticks() - powerup_tiro_triplo_inicio > powerup_tiro_triplo_duracao:
            powerup_tiro_triplo_ativo = False




    
    # ATUALIZAÇÃO FINAL
  
    todos_sprites.update()
    powerups.update()  # já estão em todos_sprites, mas garantimos atualização




    TELA.blit(fundo_game_over, (0, 0))
    todos_sprites.draw(TELA)
    desenhar_hud(TELA, jogador.vida, pontos, buff_ativo, cacadores_eliminados,
                 powerup_velocidade_ativo, powerup_tiro_triplo_ativo)




    pygame.display.flip()



pygame.quit()
