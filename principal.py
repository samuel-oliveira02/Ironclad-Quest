# principal.py
import pygame
import sys
import constantes as c
# Importamos o BringerOfDeath e o Cavaleiro do módulo de personagens
from personagens import Cavaleiro, Plataforma, BringerOfDeath


def desenhar_coracao(superficie, x, y, tamanho, preenchido=True):
    """Desenha um coração usando formas geométricas do Pygame"""
    cor = (255, 0, 0) if preenchido else (70, 70, 70)  # Vermelho se cheio, Cinza se vazio
    raio = tamanho // 4

    # 1. Desenha as duas "bochechas" redondas do topo do coração
    pygame.draw.circle(superficie, cor, (x + raio, y + raio), raio)
    pygame.draw.circle(superficie, cor, (x + tamanho - raio, y + raio), raio)

    # 2. Desenha o bico de baixo (um triângulo)
    pontos_triangulo = [
        (x, y + raio),  # Canto esquerdo
        (x + tamanho, y + raio),  # Canto direito
        (x + tamanho // 2, y + int(tamanho * 0.95))  # Ponta de baixo
    ]
    pygame.draw.polygon(superficie, cor, pontos_triangulo)

    # 3. Desenha uma borda preta fina ao redor para dar destaque
    pygame.draw.circle(superficie, (0, 0, 0), (x + raio, y + raio), raio, 1)
    pygame.draw.circle(superficie, (0, 0, 0), (x + tamanho - raio, y + raio), raio, 1)
    pygame.draw.polygon(superficie, (0, 0, 0), pontos_triangulo, 1)


def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # --- 1. Grupos de Sprites e Cenário ---
    elementos_cenario = pygame.sprite.Group()
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()
    grupo_flechas = pygame.sprite.Group()  # Grupo dedicado para gerenciar os projéteis

    # Cria o Chão e Plataformas
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    plataforma1 = Plataforma(150, 420, 200, 30)
    plataforma2 = Plataforma(450, 300, 200, 30)

    grupo_plataformas.add(chao, plataforma1, plataforma2)
    elementos_cenario.add(chao, plataforma1, plataforma2)

    # Criamos os Bringers of Death em posições estratégicas
    inimigo_chao = BringerOfDeath(600, c.ALTURA - 195)
    inimigo_plat1 = BringerOfDeath(200, 275)
    inimigo_plat2 = BringerOfDeath(500, 155)

    grupo_inimigos.add(inimigo_chao, inimigo_plat1, inimigo_plat2)

    # Cria o Cavaleiro
    jogador = Cavaleiro()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- 2. Atualização da Lógica ---

        # O jogador atualiza e pode retornar uma flecha se o botão 'Z' for pressionado
        retorno_tiro = jogador.update(grupo_plataformas)
        if retorno_tiro is not None:
            grupo_flechas.add(retorno_tiro)

        # Atualização física dos projéteis e inteligência artificial dos monstros
        grupo_flechas.update(grupo_plataformas)
        grupo_inimigos.update(grupo_plataformas, jogador)

        # A) COLISÃO DA FLECHA COM O INIMIGO
        for flecha in grupo_flechas:
            inimigos_atingidos = pygame.sprite.spritecollide(flecha, grupo_inimigos, False)
            for inimigo in inimigos_atingidos:
                if not inimigo.morrendo:
                    inimigo.tomar_dano()
                    flecha.kill()  # A flecha quebra e desaparece ao atingir o alvo

        # B) O JOGADOR ATACA O INIMIGO COM A ESPADA
        if jogador.atacando:
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    inimigo.tomar_dano()

        # C) O INIMIGO ATACA O JOGADOR (Ataque por Foice OU por Contato)
        for inimigo in grupo_inimigos:
            if not inimigo.morrendo:
                # Checagem do Golpe da Foice
                if inimigo.atacando and not inimigo.deu_dano_nesse_ciclo:
                    if inimigo.rect_ataque_inimigo.colliderect(jogador.rect):
                        jogador.tomar_dano(20)
                        inimigo.deu_dano_nesse_ciclo = True

                # Checagem de Contato Físico (Impede passar correndo por dentro)
                if jogador.rect.colliderect(inimigo.rect):
                    jogador.tomar_dano(20)

        # --- 3. Renderização ---
        tela.fill(c.PRETO)

        # Desenha o cenário (Chão e plataformas)
        elementos_cenario.draw(tela)

        # Desenha o jogador com o alinhamento customizado de sprites
        jogador.draw_custom(tela)

        # Desenha cada inimigo ativo respeitando o alinhamento dos sprites gigantes
        for inimigo in grupo_inimigos:
            inimigo.draw_custom(tela)

        # Desenha os projéteis no ar
        grupo_flechas.draw(tela)

        # Desenha a caixa de colisão vermelha da espada se o herói estiver atacando
        jogador.desenhar_ataque(tela)

        # --- DESENHAR OS 5 CORAÇÕES DE VIDA (HUD) ---
        pos_x_inicial = 20
        pos_y = 20
        tamanho_coracao = 24
        espacamento = 30

        for i in range(5):
            vida_necessaria = (i + 1) * 20
            coracao_cheio = jogador.vida_atual >= vida_necessaria
            x_atual = pos_x_inicial + (i * espacamento)
            desenhar_coracao(tela, x_atual, pos_y, tamanho_coracao, preenchido=coracao_cheio)

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    rodar_jogo()