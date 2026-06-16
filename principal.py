# principal.py
import pygame
import sys
import constantes as c
from personagens import Cavaleiro, Plataforma, Inimigo  # Importa o Inimigo


def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest - Demo ADS")
    relogio = pygame.time.Clock()

    # Grupos de Sprites
    todos_sprites = pygame.sprite.Group()
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()  # Grupo exclusivo para os vilões

    # Cria o Chão e Plataformas
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    plataforma1 = Plataforma(150, 420, 200, 30)
    plataforma2 = Plataforma(450, 300, 200, 30)

    grupo_plataformas.add(chao, plataforma1, plataforma2)
    todos_sprites.add(chao, plataforma1, plataforma2)

    # --- AQUI ADICIONAMOS OS TRÊS GOBLINS ---
    # Goblin 1: No chão principal (Canto direito)
    goblin_chao = Inimigo(600, c.ALTURA - 90)

    # Goblin 2: Em cima da Plataforma 1 (da esquerda, que está em y=420)
    # Colocamos o Y em 380 para ele ficar apoiado nela (420 - 40 de altura do goblin)
    goblin_plat1 = Inimigo(200, 380)

    # Goblin 3: Em cima da Plataforma 2 (da direita, que está em y=300)
    # Y em 260 (300 - 40 de altura do goblin)
    goblin_plat2 = Inimigo(500, 260)

    # Adiciona todos no grupo de inimigos e no grupo geral de desenho
    grupo_inimigos.add(goblin_chao, goblin_plat1, goblin_plat2)
    todos_sprites.add(goblin_chao, goblin_plat1, goblin_plat2)

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

        # --- AQUI ATUALIZAMOS A LINHA PASSANDO AS PLATAFORMAS ---
        grupo_inimigos.update(grupo_plataformas)

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