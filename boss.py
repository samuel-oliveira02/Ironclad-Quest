import pygame
import os
import random
import constantes as c
import math
from efeitos import Efeito


class ProjetilSopro(pygame.sprite.Sprite):
    """Onda de energia azul que PERSEGUE o jogador e vira para o lado certo"""

    def __init__(self, x, y, para_esquerda):
        super().__init__()
        tira = pygame.image.load("assets/DemonAttackBreath.png").convert_alpha()
        qtd_frames = 11
        largura_frame = tira.get_width() // qtd_frames
        altura_frame = tira.get_height()

        self.para_esquerda_inicial = para_esquerda

        self.frames = []
        for i in range(qtd_frames):
            sub = tira.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            multiplicador_escala = 3
            sub_escalada = pygame.transform.scale(sub, (largura_frame * multiplicador_escala,
                                                        altura_frame * multiplicador_escala))

            if not para_esquerda:
                sub_escalada = pygame.transform.flip(sub_escalada, True, False)

            self.frames.append(sub_escalada)

        self.frame_index = 0
        self.image_base = self.frames[self.frame_index]
        self.image = self.image_base
        self.rect = self.image.get_rect(center=(x, y))

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 60

        self.velocidade_base = 4.5
        self.dano = 15

        self.tempo_criacao = pygame.time.get_ticks()
        self.tempo_vida_max = 4000

    def update(self, plataformas, jogador, grupo_magias, grupo_efeitos, audio):
        dx = jogador.rect.centerx - self.rect.centerx
        dy = jogador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia != 0:
            self.rect.x += int((dx / distancia) * self.velocidade_base)
            self.rect.y += int((dy / distancia) * self.velocidade_base)

            jogador_a_esquerda = dx < 0

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
                self.tempo_ultimo_frame = tempo_atual
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image_base = self.frames[self.frame_index]

                if (self.para_esquerda_inicial and not jogador_a_esquerda) or (
                        not self.para_esquerda_inicial and jogador_a_esquerda):
                    self.image = pygame.transform.flip(self.image_base, True, False)
                else:
                    self.image = self.image_base

        if pygame.time.get_ticks() - self.tempo_criacao > self.tempo_vida_max:
            self.kill()
        if self.rect.right < -100 or self.rect.left > c.LARGURA + 100:
            self.kill()


class BossDemonio(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.animacoes = {"idle": [], "attack": [], "attack_breath": []}
        caminho_base = "assets/demon-Files/Sprites/"

        # 1. Carrega Idle
        for i in range(1, 7):
            img = pygame.image.load(f"{caminho_base}Idle/idle{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            self.animacoes["idle"].append(img)

        # 2. Carrega DemonAttack
        pasta_attack = f"{caminho_base}DemonAttack/"
        if os.path.exists(pasta_attack):
            arquivos = sorted([f for f in os.listdir(pasta_attack) if f.endswith('.png')])
            for arq in arquivos:
                img = pygame.image.load(os.path.join(pasta_attack, arq)).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.animacoes["attack"].append(img)

        # 3. Carrega DemonAttackBreath
        pasta_breath = f"{caminho_base}DemonAttackBreath/"
        if os.path.exists(pasta_breath):
            arquivos = sorted([f for f in os.listdir(pasta_breath) if f.endswith('.png')])
            for arq in arquivos:
                img = pygame.image.load(os.path.join(pasta_breath, arq)).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.animacoes["attack_breath"].append(img)

        self.estado_atual = "idle"
        self.frame_atual = 0
        self.image = self.animacoes[self.estado_atual][self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.vida_max = 600
        self.vida_atual = self.vida_max
        self.olhando_para_esquerda = True

        self.contador_hits = 0
        self.max_hits_antes_fuga = 4
        self.x_destino = x
        self.velocidade_fuga = 8

        self.timer_invulneravel = 0

        self.cooldown_ataque = 100
        self.timer_ataque = 0
        self.velocidade_animacao = 0.15

        self.disparou_ataque = False
        self.som_asa_tocado = False

        # 🎯 NOVO: Carrega as imagens da barra de vida estilizada
        try:
            self.barra_base = pygame.image.load("assets/BigBar_Base.png").convert_alpha()
            self.barra_fill = pygame.image.load("assets/BigBar_Fill.png").convert_alpha()

            # Opcional: Se achar a barra original pequena ou grande, podemos escalá-la aqui.
            # Vamos manter o tamanho original delas primeiro, mas se quiser pode usar pygame.transform.scale
        except pygame.error:
            print("Aviso: Não foi possível carregar as texturas da barra de vida do Boss.")
            self.barra_base = None
            self.barra_fill = None

    def tomar_dano(self, quantidade):
        if self.timer_invulneravel == 0 and self.estado_atual != "retreat":
            self.vida_atual -= quantidade
            if self.vida_atual < 0:
                self.vida_atual = 0

            self.timer_invulneravel = 30
            self.contador_hits += 1

            if self.contador_hits >= self.max_hits_antes_fuga:
                self.contador_hits = 0
                self.estado_atual = "retreat"
                # 🎯 COISA 3: Limita o recuo para não passar dos limites visíveis da arena
                if self.rect.centerx < c.LARGURA // 2:
                    self.x_destino = c.LARGURA - 160
                else:
                    self.x_destino = 160

    def update(self, plataformas, jogador, grupo_magias, grupo_efeitos, audio):
        if self.timer_invulneravel > 0:
            self.timer_invulneravel -= 1

        if self.estado_atual == "retreat":
            if self.rect.centerx < self.x_destino:
                self.rect.x += self.velocidade_fuga
                if self.rect.centerx >= self.x_destino:
                    self.estado_atual = "idle"
            elif self.rect.centerx > self.x_destino:
                self.rect.x -= self.velocidade_fuga
                if self.rect.centerx <= self.x_destino:
                    self.estado_atual = "idle"

            self.olhando_para_esquerda = jogador.rect.centerx < self.rect.centerx

        else:
            self.olhando_para_esquerda = jogador.rect.centerx < self.rect.centerx

            if self.estado_atual == "idle":
                self.timer_ataque += 1
                if self.timer_ataque >= self.cooldown_ataque:
                    self.timer_ataque = 0
                    self.frame_atual = 0
                    self.disparou_ataque = False

                    distancia_ate_jogador = abs(self.rect.centerx - jogador.rect.centerx)

                    if distancia_ate_jogador <= 180:
                        self.estado_atual = "attack"
                    else:
                        self.estado_atual = "attack_breath"

        # 🎯 COISA 3: Trava a posição X dele para impedir que saia da tela durante qualquer animação
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > c.LARGURA:
            self.rect.right = c.LARGURA

        estado_animacao = "idle" if self.estado_atual == "retreat" else self.estado_atual

        self.frame_atual += self.velocidade_animacao
        if self.frame_atual >= len(self.animacoes[estado_animacao]):
            if self.estado_atual in ["attack", "attack_breath"]:
                self.estado_atual = "idle"
                self.timer_ataque = 0
            self.frame_atual = 0

        # =========================================================================
        # 🔊 🎯 NOVO: SISTEMA DE SOM DO BATER DE ASAS DO BOSS FINAL
        # =========================================================================
        if audio and self.estado_atual in ["idle", "retreat", "attack_breath"]:
            frame_inteiro = int(self.frame_atual)

            # Toca o som 1 no frame 1 (Asas batendo para baixo)
            if frame_inteiro == 1 and not self.som_asa_tocado:
                audio.tocar_sfx_player("boss_asa1")
                self.som_asa_tocado = True
            # Toca o som 2 no frame 4 (Asas subindo)
            elif frame_inteiro == 4 and not self.som_asa_tocado:
                audio.tocar_sfx_player("boss_asa2")
                self.som_asa_tocado = True

            # Destrava o som quando ele sai dos frames específicos de batida
            if frame_inteiro not in [1, 4]:
                self.som_asa_tocado = False
        # =========================================================================

        if self.estado_atual == "idle" and int(self.frame_atual) == 2:
            if random.random() < 0.2:
                fumaca = Efeito(self.rect.centerx, self.rect.bottom - 10, "pulo.png", 10, escala=2,
                                velocidade_animacao=50)
                grupo_efeitos.add(fumaca)

        # 🎯 COISA 1: Posição Y ajustada para nascer da cabeça/boca do Boss em animação (centery - 20)
        if self.estado_atual == "attack_breath" and int(self.frame_atual) == 8 and not self.disparou_ataque:
            self.disparou_ataque = True
            px = self.rect.left if self.olhando_para_esquerda else self.rect.right
            projeto_azul = ProjetilSopro(px, self.rect.centery - -140, self.olhando_para_esquerda)
            grupo_magias.add(projeto_azul)
            if audio:
                audio.tocar_sfx_player("necroman_explosao")

        img_original = self.animacoes[estado_animacao][int(self.frame_atual)]

        if self.timer_invulneravel > 0 and (self.timer_invulneravel // 4) % 2 == 0:
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        else:
            if not self.olhando_para_esquerda:
                self.image = pygame.transform.flip(img_original, True, False)
            else:
                self.image = img_original

    def draw_custom(self, tela):
        # Desenha APENAS o sprite do próprio Boss. A barra de vida foi promovida para a HUD principal da Arena!
        tela.blit(self.image, self.rect)