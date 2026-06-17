import pygame
import random
import constantes as c


class Decoracao(pygame.sprite.Sprite):
    def __init__(self, x, y, nome_asset, escala=None):
        super().__init__()
        caminho = f"assets/{nome_asset}"
        try:
            self.image = pygame.image.load(caminho).convert_alpha()
            if escala:
                self.image = pygame.transform.scale(self.image, escala)
        except (pygame.error, FileNotFoundError):
            # Fallback seguro caso o arquivo falhe
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.image.fill((0, 200, 0, 150))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Nuvem(pygame.sprite.Sprite):
    def __init__(self, x, y, nome_asset, escala=None, velocidade=0.2):
        super().__init__()
        caminho = f"assets/{nome_asset}"
        try:
            self.image = pygame.image.load(caminho).convert_alpha()
            if escala:
                self.image = pygame.transform.scale(self.image, escala)
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((60, 30), pygame.SRCALPHA)
            self.image.fill((255, 255, 255, 100))

        self.rect = self.image.get_rect()
        self.x_flutuante = float(x)
        self.rect.y = y
        self.velocidade = velocidade

    def update(self, scroll_camera):
        # Movimento autônomo constante para a nuvem
        self.x_flutuante += self.velocidade
        self.rect.x = int(self.x_flutuante)

        # Se a nuvem sumir muito para trás, ela ressurge lá na frente do mapa
        if self.rect.right < scroll_camera - 200:
            self.x_flutuante += c.LARGURA + random.randint(300, 800)