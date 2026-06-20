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

class Castelo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Carrega a versão Epic HR de alta resolução
            self.image = pygame.image.load("assets/HR_Dark Gothic Castle_Sprite.png").convert_alpha()
            # Caso queira ajustar o tamanho dele dinamicamente, você pode usar scale:
            # self.image = pygame.transform.scale(self.image, (960, 540))
        except pygame.error:
            print("Aviso: Não foi possível carregar o sprite do Castelo.")
            # Fallback visual caso a imagem falhe
            self.image = pygame.Surface((200, 200))
            self.image.fill((50, 50, 50))

        self.rect = self.image.get_rect()
        # Posiciona o castelo pela base inferior para ele assentar bem no chão/plataforma
        self.rect.dark_bottom = y
        self.rect.centerx = x

    def update(self):
        pass