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

    def update(self, plataformas):
        # 1. Aplica a Gravidade
        self.velocidade_y += c.GRAVIDADE
        if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = c.VELOCIDADE_MAX_QUEDA

        # 2. Movimentação Horizontal e detecção se está se movendo
        teclas = pygame.key.get_pressed()
        movendo = False

        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade_x
            movendo = True
        if teclas[pygame.K_RIGHT] and self.rect.right < c.LARGURA:
            self.rect.x += self.velocidade_x
            movendo = True

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

        # 5. Comando de Pulo Dinâmico
        if teclas[pygame.K_SPACE] and self.no_chao:
            if movendo:
                # Se estiver correndo, aplica o pulo forte!
                self.velocidade_y = c.FORCA_PULO_CORRENDO
            else:
                # Se estiver parado, aplica o pulo normal
                self.velocidade_y = c.FORCA_PULO_NORMAL

            self.no_chao = False