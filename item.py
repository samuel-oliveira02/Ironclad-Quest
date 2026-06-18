# item.py
import pygame
import constantes as c


class ItemCura(pygame.sprite.Sprite):
    def __init__(self, x, y, quantidade_cura=20):  # <-- 20 = 1 Coração (Fácil de mudar!)
        super().__init__()
        self.escala = 0.5

        try:
            imagem_original = pygame.image.load("assets/food.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original,
                                                (int(imagem_original.get_width() * self.escala),
                                                 int(imagem_original.get_height() * self.escala)))
        except FileNotFoundError:
            self.image = pygame.Surface((16, 16))
            self.image.fill((0, 255, 0))

        # Define a hitbox baseada no tamanho novo e ajusta para nascer nos pés do monstro
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Atributos físicos
        self.velocidade_y = -4  # Pulinho para cima ao dropar
        self.quantidade_cura = quantidade_cura
        self.no_chao = False

    def update(self, plataformas, jogador=None, audio=None):
        # Aplica gravidade
        if not self.no_chao:
            self.velocidade_y += c.GRAVIDADE
            if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
                self.velocidade_y = c.VELOCIDADE_MAX_QUEDA
            self.rect.y += self.velocidade_y

        # Colisão com o chão
        self.no_chao = False
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisoes:
            if self.velocidade_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True