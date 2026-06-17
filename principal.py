# principal.py
import pygame
import sys
import constantes as c
from personagens import Cavaleiro, Plataforma, BringerOfDeath, Necromante


def desenhar_coracao(superficie, x, y, tamanho, preenchido=True):
    cor = (255, 0, 0) if preenchido else (70, 70, 70)
    raio = tamanho // 4
    pygame.draw.circle(superficie, cor, (x + raio, y + raio), raio)
    pygame.draw.circle(superficie, cor, (x + tamanho - raio, y + raio), raio)
    pontos_triangulo = [(x, y + raio), (x + tamanho, y + raio), (x + tamanho // 2, y + int(tamanho * 0.95))]
    pygame.draw.polygon(superficie, cor, pontos_triangulo)
    pygame.draw.circle(superficie, (0, 0, 0), (x + raio, y + raio), raio, 1)
    pygame.draw.circle(superficie, (0, 0, 0), (x + tamanho - raio, y + raio), raio, 1)
    pygame.draw.polygon(superficie, (0, 0, 0), pontos_triangulo, 1)


def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # --- Grupos de Sprites ---
    elementos_cenario = pygame.sprite.Group()
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()
    grupo_magias = pygame.sprite.Group()  # Grupo para os feitiços do Mago (Bola de fogo e Explosão)

    # Cenário
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    plataforma1 = Plataforma(150, 420, 200, 30)
    plataforma2 = Plataforma(450, 300, 200, 30)

    grupo_plataformas.add(chao, plataforma1, plataforma2)
    elementos_cenario.add(chao, plataforma1, plataforma2)

    # Inimigos
    inimigo_chao = BringerOfDeath(600, c.ALTURA - 195)
    inimigo_plat1 = BringerOfDeath(200, 275)

    # Necromante na Plataforma 2
    mago_necromante = Necromante(530, 220)

    grupo_inimigos.add(inimigo_chao, inimigo_plat1, mago_necromante)

    jogador = Cavaleiro()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- Lógica de Atualização ---
        jogador.update(grupo_plataformas)

        # --- CORREÇÃO 1: Passar o jogador para o update das magias (essencial para a explosão do chão funcionar)
        for magia in list(grupo_magias):
            magia.update(grupo_plataformas, jogador)

        # Atualiza inimigos e checa se o Necromante gerou um projétil
        for inimigo in grupo_inimigos:
            if isinstance(inimigo, Necromante):
                nova_magia = inimigo.update(grupo_plataformas, jogador)
                if nova_magia is not None:
                    grupo_magias.add(nova_magia)
            else:
                inimigo.update(grupo_plataformas, jogador)

        # A) Jogador ataca os inimigos (Bringer ou Necromante)
        if jogador.atacando:
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    inimigo.tomar_dano()

        # B) Colisões com Projéteis Mágicos (Apenas para a Bola de Fogo, pois a Explosão já se resolve sozinha)
        for magia in grupo_magias:
            # Checa se é a bola de fogo (ela possui o atributo 'vel_x')
            if hasattr(magia, 'vel_x') and magia.rect.colliderect(jogador.rect):
                if jogador.defendendo:
                    print("Bloqueado com o Escudo!")
                else:
                    jogador.tomar_dano(20)
                magia.kill()

        # C) Ataques físicos dos inimigos de perto
        for inimigo in grupo_inimigos:
            if not inimigo.morrendo:
                if hasattr(inimigo, 'atacando') and inimigo.atacando:
                    if hasattr(inimigo, 'deu_dano_nesse_ciclo') and not inimigo.deu_dano_nesse_ciclo:
                        if inimigo.rect_ataque_inimigo.colliderect(jogador.rect):
                            jogador.tomar_dano(20)
                            inimigo.deu_dano_nesse_ciclo = True

                # Checagem de Contato Físico
                if jogador.rect.colliderect(inimigo.rect):
                    jogador.tomar_dano(20)

        # --- Desenho de Elementos ---
        tela.fill(c.PRETO)
        elementos_cenario.draw(tela)
        jogador.draw_custom(tela)

        # --- CORREÇÃO 2: Renderizar magias com suporte a draw_custom se necessário
        for magia in grupo_magias:
            if hasattr(magia, 'draw_custom'):
                magia.draw_custom(tela)
            else:
                tela.blit(magia.image, magia.rect)

        for inimigo in grupo_inimigos:
            inimigo.draw_custom(tela)

        jogador.desenhar_ataque(tela)

        # HUD de Corações
        pos_x_inicial, pos_y, tamanho_coracao, espacamento = 20, 20, 24, 30
        for i in range(5):
            vida_necessaria = (i + 1) * 20
            coracao_cheio = jogador.vida_atual >= vida_necessaria
            desenhar_coracao(tela, pos_x_inicial + (i * espacamento), pos_y, tamanho_coracao, preenchido=coracao_cheio)

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    rodar_jogo()