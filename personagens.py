# personagens.py (Atualizado com Ataque)
import pygame
import constantes as c


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(c.VERDE)
        self.rect = self.image.get_rect(topleft=(x, y))


class Cavaleiro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(c.AZUL)
        self.rect = self.image.get_rect()

        self.rect.x = c.LARGURA // 2
        self.rect.y = 100

        self.velocidade_x = 4
        self.velocidade_y = 0
        self.no_chao = False

        # --- NOVOS ATRIBUTOS DE COMBATE ---
        self.olhando_para_direita = True
        self.atacando = False
        self.timer_ataque = 0
        # O rect_ataque será a hitbox da nossa espada
        self.rect_ataque = pygame.Rect(0, 0, 0, 0)

    def update(self, plataformas):
        # 1. Aplica a Gravidade
        self.velocidade_y += c.GRAVIDADE
        if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = c.VELOCIDADE_MAX_QUEDA

        # 2. Movimentação Horizontal (MELHORADA: Só trava se estiver no chão!)
        teclas = pygame.key.get_pressed()
        movendo = False

        # O jogador PODE se mover se não estiver atacando, OU se estiver atacando MAS estiver no ar!
        pode_se_mover = (not self.atacando) or (self.atacando and not self.no_chao)

        if pode_se_mover:
            if teclas[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.velocidade_x
                movendo = True
                if not self.atacando:  # Não muda de lado no meio do golpe
                    self.olhando_para_direita = False
            if teclas[pygame.K_RIGHT] and self.rect.right < c.LARGURA:
                self.rect.x += self.velocidade_x
                movendo = True
                if not self.atacando:  # Não muda de lado no meio do golpe
                    self.olhando_para_direita = True

        # 3. Movimentação Vertical
        self.rect.y += self.velocidade_y

        # 4. Checagem de Colisão com o Chão
        self.no_chao = False
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisoes:
            if self.velocidade_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        # 5. Comando de Pulo
        if teclas[pygame.K_SPACE] and self.no_chao and not self.atacando:
            if movendo:
                self.velocidade_y = c.FORCA_PULO_CORRENDO
            else:
                self.velocidade_y = c.FORCA_PULO_NORMAL
            self.no_chao = False

        # --- 6. LÓGICA DE ATAQUE (MELHORADA: Acompanha o jogador no ar) ---
        if teclas[pygame.K_x] and not self.atacando:
            self.atacando = True
            self.timer_ataque = c.DURACAO_ATAQUE

        if self.atacando:
            self.timer_ataque -= 1

            # Recalcula a posição da hitbox a cada frame para ela não ficar para trás se ele estiver voando!
            largura_espada = 50
            altura_espada = 40
            if self.olhando_para_direita:
                self.rect_ataque = pygame.Rect(self.rect.right, self.rect.centery - 20, largura_espada, altura_espada)
            else:
                self.rect_ataque = pygame.Rect(self.rect.left - largura_espada, self.rect.centery - 20, largura_espada,
                                               altura_espada)

            if self.timer_ataque <= 0:
                self.atacando = False

    def desenhar_ataque(self, tela):
        # Função para podermos enxergar o golpe enquanto não temos os sprites
        if self.atacando:
            pygame.draw.rect(tela, c.VERMELHO_ATAQUE, self.rect_ataque)


# personagens.py (Atualizado com IA de Borda de Plataforma)

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Corpo do Goblin (Vermelho)
        self.image = pygame.Surface((30, 40))
        self.image.fill(c.VERMELHO)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.velocidade = 2
        self.direcao = 1  # 1 = Direita, -1 = Esquerda

    def update(self, plataformas):
        # 1. Movimentação automática na direção atual
        self.rect.x += self.velocidade * self.direcao

        # 2. Checagem de Borda da Tela
        if self.rect.right >= c.LARGURA:
            self.direcao = -1
        elif self.rect.left <= 0:
            self.direcao = 1

        # 3. LÓGICA DE DETECÇÃO DE BORDA DA PLATAFORMA
        # Criamos um ponto "sensor" logo à frente dos pés do inimigo
        if self.direcao == 1:
            sensor_x = self.rect.right + 2
        else:
            sensor_x = self.rect.left - 2

        sensor_y = self.rect.bottom + 1  # 1 pixel abaixo dos pés

        # Cria um Rect invisível de 1x1 pixel nesse ponto para testar colisão
        rect_sensor = pygame.Rect(sensor_x, sensor_y, 1, 1)

        # Testa se o sensor está tocando em ALGUMA plataforma
        tem_chao_na_frente = False
        for plataforma in plataformas:
            if rect_sensor.colliderect(plataforma.rect):
                tem_chao_na_frente = True
                break

        # Se não tem chão na frente, ele muda de direção para não cair!
        if not tem_chao_na_frente:
            self.direcao *= -1  # Inverte a direção (se era 1 vira -1, se era -1 vira 1)

    def tomar_dano(self):
        self.kill()