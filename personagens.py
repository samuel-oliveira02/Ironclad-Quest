# personagens.py
import pygame
import constantes as c

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(c.VERDE)
        self.rect = self.image.get_rect(topleft=(x, y))


class Cavaleiro(pygame.sprite.Sprite):
    def __init__(self, x=None, y=100):
        super().__init__()

        # --- FATOR DE ESCALA ---
        self.escala = 2

        # --- CARREGAMENTO DE SPRITES ---
        self.tira_idle = pygame.image.load("assets/IDLE.png").convert_alpha()
        self.tira_walk = pygame.image.load("assets/WALK.png").convert_alpha()
        self.tira_run = pygame.image.load("assets/RUN.png").convert_alpha()
        self.tira_jump = pygame.image.load("assets/JUMP.png").convert_alpha()
        self.tira_attack = pygame.image.load("assets/ATTACK 1.png").convert_alpha()
        self.tira_attack3 = pygame.image.load("assets/ATTACK 3.png").convert_alpha()
        self.tira_defend = pygame.image.load("assets/DEFEND.png").convert_alpha()

        # Quantidade exata de frames
        frames_idles_qtd = 7
        frames_walk_qtd = 8
        frames_run_qtd = 8
        frames_jump_qtd = 5
        frames_attack_qtd = 6
        frames_attack3_qtd = 6
        frames_defend_qtd = 6

        # Recorte e redimensionamento dos frames
        self.frames_idle = self.recortar_e_escalar_tira(self.tira_idle, frames_idles_qtd)
        self.frames_walk = self.recortar_e_escalar_tira(self.tira_walk, frames_walk_qtd)
        self.frames_run = self.recortar_e_escalar_tira(self.tira_run, frames_run_qtd)
        self.frames_jump = self.recortar_e_escalar_tira(self.tira_jump, frames_jump_qtd)
        self.frames_attack = self.recortar_e_escalar_tira(self.tira_attack, frames_attack_qtd)
        self.frames_attack3 = self.recortar_e_escalar_tira(self.tira_attack3, frames_attack3_qtd)
        self.frames_defend = self.recortar_e_escalar_tira(self.tira_defend, frames_defend_qtd)

        # Variável de controle de ataque aéreo
        self.ataque_aereo = False

        # Estado inicial da animação
        self.animacao_atual = self.frames_idle
        self.frame_index = 0
        self.image = self.animacao_atual[self.frame_index]

        # --- HITBOX REAL DO PERSONAGEM ---
        largura_hitbox = 20 * self.escala
        altura_hitbox = 40 * self.escala

        pos_x = x if x is not None else c.LARGURA // 2
        self.rect = pygame.Rect(pos_x, y, largura_hitbox, altura_hitbox)

        # --- VELOCIDADES CONFIGURÁVEIS ---
        self.vel_andar = 3
        self.vel_correr = 6
        self.velocidade_x_atual = 0
        self.velocidade_y = 0
        self.no_chao = False

        # --- ATRIBUTOS DE COMBATE ---
        self.olhando_para_direita = True
        self.atacando = False
        self.defendendo = False
        self.correndo = False
        self.rect_ataque = pygame.Rect(0, 0, 0, 0)

        # --- SISTEMA DE VIDA (HP) ---
        self.vida_max = 100
        self.vida_atual = self.vida_max
        self.invencivel = False
        self.tempo_invencivel = 0
        self.duracao_invencibilidade = 1000

        # Controle de tempo para a troca de frames
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 100

    def recortar_e_escalar_tira(self, tira, qtd_frames):
        lista = []
        largura_frame = tira.get_width() // qtd_frames
        altura_frame = tira.get_height()

        novo_w = largura_frame * self.escala
        novo_h = altura_frame * self.escala

        for i in range(qtd_frames):
            sub_imagem = tira.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            imagem_ampliada = pygame.transform.scale(sub_imagem, (novo_w, novo_h))
            lista.append(imagem_ampliada)
        return lista

    def atualizar_animacao(self):
        animacao_anterior = self.animacao_atual

        if self.atacando:
            if self.ataque_aereo:
                self.animacao_atual = self.frames_attack3
            else:
                self.animacao_atual = self.frames_attack
        elif self.defendendo:
            self.animacao_atual = self.frames_defend
            if self.frame_index >= len(self.animacao_atual):
                self.frame_index = len(self.animacao_atual) - 1
        elif not self.no_chao:
            self.animacao_atual = self.frames_jump
        elif self.velocidade_x_atual != 0:
            if self.correndo:
                self.animacao_atual = self.frames_run
            else:
                self.animacao_atual = self.frames_walk
        else:
            self.animacao_atual = self.frames_idle

        if animacao_anterior != self.animacao_atual:
            self.frame_index = 0
            self.tempo_ultimo_frame = pygame.time.get_ticks()

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1

            if self.atacando and self.frame_index >= len(self.animacao_atual):
                self.atacando = False
                self.ataque_aereo = False
                self.frame_index = 0
            else:
                self.frame_index %= len(self.animacao_atual)

        imagem_frame = self.animacao_atual[self.frame_index]
        if not self.olhando_para_direita:
            self.image = pygame.transform.flip(imagem_frame, True, False)
        else:
            self.image = imagem_frame

    def tomar_dano(self, quantidade):
        tempo_atual = pygame.time.get_ticks()
        if not self.invencivel and not self.defendendo:
            self.vida_atual -= quantidade
            if self.vida_atual < 0:
                self.vida_atual = 0
            self.invencivel = True
            self.tempo_invencivel = tempo_atual
            print(f"Ai! Vida do Cavaleiro: {self.vida_atual}/{self.vida_max}")

    def atualizar_invencibilidade(self):
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_invencivel > self.duracao_invencibilidade:
                self.invencivel = False

    def update(self, plataformas):
        # 1. Aplica a Gravidade
        self.velocidade_y += c.GRAVIDADE
        if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = c.VELOCIDADE_MAX_QUEDA

        # 2. Movimentação Horizontal
        teclas = pygame.key.get_pressed()
        movendo = False
        self.velocidade_x_atual = 0

        if teclas[pygame.K_LSHIFT] and self.no_chao and not self.atacando:
            self.defendendo = True
        else:
            self.defendendo = False

        if teclas[pygame.K_LCTRL]:
            self.correndo = True
            vel_atual = self.vel_correr
        else:
            self.correndo = False
            vel_atual = self.vel_andar

        if not self.defendendo:
            pode_se_mover = (not self.atacando) or (self.atacando and not self.no_chao)

            if pode_se_mover:
                if teclas[pygame.K_LEFT] and self.rect.left > 0:
                    self.rect.x -= vel_atual
                    self.velocidade_x_atual = -vel_atual
                    movendo = True
                    if not self.atacando:
                        self.olhando_para_direita = False
                if teclas[pygame.K_RIGHT] and self.rect.right < c.LARGURA:
                    self.rect.x += vel_atual
                    self.velocidade_x_atual = vel_atual
                    movendo = True
                    if not self.atacando:
                        self.olhando_para_direita = True

        # 3. Movimentação Vertical
        self.rect.y += self.velocidade_y

        # 4. Checagem de Colisão com o Chão/Plataformas
        self.no_chao = False
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisoes:
            if self.velocidade_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        # 5. Comando de Pulo
        if teclas[pygame.K_SPACE] and self.no_chao and not self.atacando and not self.defendendo:
            if movendo and self.correndo:
                self.velocidade_y = c.FORCA_PULO_CORRENDO
            else:
                self.velocidade_y = c.FORCA_PULO_NORMAL
            self.no_chao = False

        # --- 6. LÓGICA DE ATAQUE COM ESPADA ---
        if teclas[pygame.K_x] and not self.atacando and not self.defendendo:
            self.atacando = True
            self.frame_index = 0
            if not self.no_chao:
                self.ataque_aereo = True
            else:
                self.ataque_aereo = False

        if self.atacando:
            largura_espada = 60 * self.escala
            altura_espada = 50 * self.escala
            if self.olhando_para_direita:
                self.rect_ataque = pygame.Rect(self.rect.right, self.rect.centery - (altura_espada // 2),
                                               largura_espada, altura_espada)
            else:
                self.rect_ataque = pygame.Rect(self.rect.left - largura_espada,
                                               self.rect.centery - (altura_espada // 2), largura_espada, altura_espada)
        else:
            self.rect_ataque = pygame.Rect(0, 0, 0, 0)

        self.atualizar_animacao()
        self.atualizar_invencibilidade()


    def draw_custom(self, tela):
        if self.invencivel:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return

        centro_x = self.rect.centerx
        rect_imagem = self.image.get_rect()
        rect_imagem.centerx = centro_x
        rect_imagem.bottom = self.rect.bottom + (23 * self.escala)
        tela.blit(self.image, rect_imagem)


    def desenhar_ataque(self, tela):
        if self.atacando:
            pygame.draw.rect(tela, (255, 0, 0, 100), self.rect_ataque, 2)


class BringerOfDeath(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.escala = 2

        self.frames_idle = []
        for i in range(1, 9):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Idle/Bringer-of-Death_Idle_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_idle.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala), int(imagem.get_height() * self.escala))))

        self.frames_walk = []
        for i in range(1, 9):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Walk/Bringer-of-Death_Walk_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_walk.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala), int(imagem.get_height() * self.escala))))

        self.frames_attack = []
        for i in range(1, 11):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Attack/Bringer-of-Death_Attack_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_attack.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala), int(imagem.get_height() * self.escala))))

        self.frames_death = []
        for i in range(1, 11):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Death/Bringer-of-Death_Death_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_death.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala), int(imagem.get_height() * self.escala))))

        self.animacao_atual = self.frames_walk
        self.frame_index = 0
        self.image = self.animacao_atual[self.frame_index]

        largura_frame = self.image.get_width()
        self.rect = pygame.Rect(x, y, int(largura_frame * 0.22), 45)

        self.velocidade = 1.2
        self.velocidade_y = 0
        self.direcao = -1
        self.olhando_para_direita = False
        self.no_chao = False

        self.atacando = False
        self.raio_ataque = 80
        self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)
        self.deu_dano_nesse_ciclo = False
        self.morrendo = False

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 100

    def update(self, plataformas, jogador=None):
        self.velocidade_y += c.GRAVIDADE
        if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = c.VELOCIDADE_MAX_QUEDA
        self.rect.y += self.velocidade_y

        self.no_chao = False
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisoes:
            if self.velocidade_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        if self.morrendo:
            self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
                self.tempo_ultimo_frame = tempo_atual
                self.frame_index += 1
                if self.frame_index >= len(self.animacao_atual):
                    self.kill()
                    return

            imagem_frame = self.animacao_atual[self.frame_index]
            if self.olhando_para_direita:
                self.image = pygame.transform.flip(imagem_frame, True, False)
            else:
                self.image = imagem_frame
            return

        if self.no_chao and jogador is not None:
            distancia_x = abs(self.rect.centerx - jogador.rect.centerx)
            distancia_y = abs(self.rect.centery - jogador.rect.centery)

            if distancia_x <= self.raio_ataque and distancia_y < 50:
                if not self.atacando:
                    self.atacando = True
                    self.frame_index = 0
                    self.animacao_atual = self.frames_attack
                    self.deu_dano_nesse_ciclo = False
                    if jogador.rect.centerx > self.rect.centerx:
                        self.olhando_para_direita = True
                        self.direcao = 1
                    else:
                        self.olhando_para_direita = False
                        self.direcao = -1

        if self.no_chao and not self.atacando:
            self.animacao_atual = self.frames_walk
            self.rect.x += self.velocidade * self.direcao

            if self.rect.right >= c.LARGURA:
                self.direcao = -1
                self.olhando_para_direita = False
            elif self.rect.left <= 0:
                self.direcao = 1
                self.olhando_para_direita = True

            sensor_x = self.rect.right + 2 if self.direcao == 1 else self.rect.left - 2
            sensor_y = self.rect.bottom + 1
            rect_sensor = pygame.Rect(sensor_x, sensor_y, 1, 1)

            tem_chao = False
            for plat in plataformas:
                if rect_sensor.colliderect(plat.rect):
                    tem_chao = True
                    break

            if not tem_chao:
                self.direcao *= -1
                self.olhando_para_direita = not self.olhando_para_direita

        if self.atacando:
            if 4 <= self.frame_index <= 7:
                largura_ataque = 70 * self.escala
                altura_ataque = 40 * self.escala
                if self.olhando_para_direita:
                    self.rect_ataque_inimigo = pygame.Rect(self.rect.right, self.rect.y, largura_ataque, altura_ataque)
                else:
                    self.rect_ataque_inimigo = pygame.Rect(self.rect.left - largura_ataque, self.rect.y, largura_ataque, altura_ataque)
            else:
                self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1
            if self.atacando and self.frame_index >= len(self.animacao_atual):
                self.atacando = False
                self.frame_index = 0
                self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)
            else:
                self.frame_index %= len(self.animacao_atual)

        imagem_frame = self.animacao_atual[self.frame_index]
        self.image = pygame.transform.flip(imagem_frame, True, False) if self.olhando_para_direita else imagem_frame

    def draw_custom(self, tela):
        rect_imagem = self.image.get_rect()
        rect_imagem.centerx = self.rect.centerx
        rect_imagem.bottom = self.rect.bottom + int(1 * self.escala)
        tela.blit(self.image, rect_imagem)

    def tomar_dano(self):
        if not self.morrendo:
            self.morrendo = True
            self.frame_index = 0
            self.animacao_atual = self.frames_death
            self.tempo_ultimo_frame = pygame.time.get_ticks()