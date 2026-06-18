import pygame


class Efeito(pygame.sprite.Sprite):
    def __init__(self, x, y, arquivo_imagem, qtd_frames, escala=2, velocidade_animacao=60):
        super().__init__()

        # Carrega a tira de sprites do efeito
        tira = pygame.image.load(f"assets/{arquivo_imagem}").convert_alpha()
        largura_frame = tira.get_width() // qtd_frames
        altura_frame = tira.get_height()

        # Recorta e escala os frames
        self.frames = []
        for i in range(qtd_frames):
            sub = tira.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            sub_escalada = pygame.transform.scale(sub, (largura_frame * escala, altura_frame * escala))
            self.frames.append(sub_escalada)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # Centraliza o efeito na posição desejada
        self.rect = self.image.get_rect(center=(x, y))

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = velocidade_animacao

    def update(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1

            # Se a animação acabou, o efeito se destrói sozinho!
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]