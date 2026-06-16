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

    # Cria o Chão Provisório (x=0, y=550, largura=800, altura=50)
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    grupo_plataformas.add(chao)
    todos_sprites.add(chao)

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