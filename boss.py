import pygame
import os
import random
import constantes as c


class BossDemonio(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- CARREGAMENTO DE ANIMAÇÕES ---
        self.animacoes = {"idle": [], "attack": [], "attack_breath": []}
        caminho_base = "assets/demon-Files/Sprites/"

        # 1. Carrega Idle (6 frames)
        for i in range(1, 7):
            img = pygame.image.load(f"{caminho_base}Idle/idle{i}.png").convert_alpha()
            # Multiplicamos o tamanho por 2 (ou mais) para o Boss ficar gigante na tela!
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            self.animacoes["idle"].append(img)

        # 2. Carrega DemonAttack (Garante ler todos os frames da pasta automaticamente)
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

        # --- ESTADOS E ATRIBUTOS ---
        self.estado_atual = "idle"
        self.frame_atual = 0
        self.image = self.animacoes[self.estado_atual][self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Atributos de Combate
        self.vida_max = 600
        self.vida_atual = self.vida_max
        self.olhando_para_esquerda = True

        # Timers de IA
        self.cooldown_ataque = 120  # Tempo em frames entre um golpe e outro
        self.timer_ataque = 0
        self.velocidade_animacao = 0.15

    def update(self, plataformas, jogador, audio):
        # 1. Olhar sempre na direção do jogador
        if jogador.rect.centerx < self.rect.centerx:
            self.olhando_para_esquerda = True
        else:
            self.olhando_para_esquerda = False

        # 2. Lógica de decisão de Ataques
        if self.estado_atual == "idle":
            self.timer_ataque += 1
            if self.timer_ataque >= self.cooldown_ataque:
                self.timer_ataque = 0
                self.frame_atual = 0
                # Sorteia qual dos dois ataques ele vai desferir
                self.estado_atual = random.choice(["attack", "attack_breath"])
                if audio:
                    audio.tocar_sfx_player("necroman_explosao")  # Som imponente de impacto

        # 3. Avançar os frames da animação
        self.frame_atual += self.velocidade_animacao
        if self.frame_atual >= len(self.animacoes[self.estado_atual]):
            if self.estado_atual != "idle":
                # Quando a animação do ataque de 18 frames acabar, volta ao Idle
                self.estado_atual = "idle"
                self.timer_ataque = 0
            self.frame_atual = 0

        # Aplica a imagem correspondente invertendo o lado se necessário
        img_original = self.animacoes[self.estado_atual][int(self.frame_atual)]
        if not self.olhando_para_esquerda:
            self.image = pygame.transform.flip(img_original, True, False)
        else:
            self.image = img_original

    def draw_custom(self, tela):
        # Desenha o Boss
        tela.blit(self.image, self.rect)

        # --- BARRA DE VIDA DO CHEFÃO NO TOPO DA TELA ---
        largura_barra = 500
        x_barra = (c.LARGURA - largura_barra) // 2
        y_barra = 30

        # Borda/Fundo cinza escuro
        pygame.draw.rect(tela, (35, 35, 35), (x_barra, y_barra, largura_barra, 18))
        # Barra vermelha preenchida com base na vida atual
        porcentagem = max(0, self.vida_atual / self.vida_max)
        pygame.draw.rect(tela, (180, 0, 0), (x_barra, y_barra, int(largura_barra * porcentagem), 18))