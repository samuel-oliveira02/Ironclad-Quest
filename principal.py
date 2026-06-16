# principal.py
import pygame
import sys
import constantes as c
from personagens import Cavaleiro, Plataforma, Inimigo  # Importa o Inimigo


def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # Grupos de Sprites
    todos_sprites = pygame.sprite.Group()
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()  # Novo grupo exclusivo para os vilões

    # Cria o Chão e Plataformas
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    plataforma1 = Plataforma(150, 420, 200, 30)
    plataforma2 = Plataforma(450, 300, 200, 30)

    grupo_plataformas.add(chao, plataforma1, plataforma2)
    todos_sprites.add(chao, plataforma1, plataforma2)

    # Cria o Goblin (Posicionado no chão, no canto direito)
    goblin = Inimigo(600, c.ALTURA - 90)  # 90 pixels para ficar certinho em cima do chão
    grupo_inimigos.add(goblin)
    todos_sprites.add(goblin)

    # Cria o Cavaleiro
    jogador = Cavaleiro()
    todos_sprites.add(jogador)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- 2. Atualização da Lógica
        jogador.update(grupo_plataformas)
        grupo_inimigos.update()  # Atualiza a patrulha dos inimigos

        # SISTEMA DE DANOS: Se o jogador estiver atacando...
        if jogador.atacando:
            # Verifica se a hitbox da espada bateu em algum inimigo do grupo
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    inimigo.tomar_dano()  # O Goblin some!

        # --- 3. Renderização
        tela.fill(c.PRETO)
        todos_sprites.draw(tela)
        jogador.desenhar_ataque(tela)

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    rodar_jogo()