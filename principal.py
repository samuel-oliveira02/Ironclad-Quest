# principal.py
import pygame
import sys
import constantes as c
from personagens import Cavaleiro, Plataforma


def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # Grupos de Sprites
    todos_sprites = pygame.sprite.Group()
    grupo_plataformas = pygame.sprite.Group()

    # 1. O Chão Principal (x, y, largura, altura)
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    grupo_plataformas.add(chao)
    todos_sprites.add(chao)

    # 2. Novas Plataformas Flutuantes (Blocos verdes no ar para teste)
    # Plataforma da esquerda (mais baixa)
    plataforma1 = Plataforma(150, 420, 200, 30)
    # Plataforma da direita (mais alta)
    plataforma2 = Plataforma(450, 300, 200, 30)

    # Adiciona as novas plataformas nos grupos
    grupo_plataformas.add(plataforma1, plataforma2)
    todos_sprites.add(plataforma1, plataforma2)

    # Cria o Cavaleiro
    jogador = Cavaleiro()
    todos_sprites.add(jogador)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Atualiza o jogador passando as plataformas para ele checar a colisão
        jogador.update(grupo_plataformas)

        tela.fill(c.PRETO)
        todos_sprites.draw(tela)

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    rodar_jogo()