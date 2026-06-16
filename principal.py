# principal.py
import pygame
import sys
import constantes as c
# Importamos o BringerOfDeath e removemos o Inimigo antigo
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

    # Grupos de Sprites
    elementos_cenario = pygame.sprite.Group()
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()  # Grupo exclusivo para os novos inimigos

    # Cria o Chão e Plataformas
    chao = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    plataforma1 = Plataforma(150, 420, 200, 30)
    plataforma2 = Plataforma(450, 300, 200, 30)

    grupo_plataformas.add(chao, plataforma1, plataforma2)
    elementos_cenario.add(chao, plataforma1, plataforma2)

    # --- ADICIONANDO OS INIMIGOS 1 (Bringer of Death) ---
    # Criamos três deles em posições estratégicas
    inimigo_chao = BringerOfDeath(600, c.ALTURA - 195)
    inimigo_plat1 = BringerOfDeath(200, 275)
    inimigo_plat2 = BringerOfDeath(500, 155)

    # Adiciona todos no grupo de inimigos para controlar a IA e o dano de uma vez só
    grupo_inimigos.add(inimigo_chao, inimigo_plat1, inimigo_plat2)

    # Cria o Cavaleiro
    jogador = Cavaleiro()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- 2. Atualização da Lógica
        jogador.update(grupo_plataformas)

        # Atualiza a movimentação e animação de todos os inimigos do grupo
        grupo_inimigos.update(grupo_plataformas)

        # SISTEMA DE DANOS: Se o jogador estiver atacando...
        if jogador.atacando:
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    inimigo.tomar_dano()  # O inimigo atingido morre

        # O INIMIGO ATACA O JOGADOR
        # Se qualquer inimigo encostar no rect do jogador, o jogador toma 20 de dano
        colisao_com_inimigo = pygame.sprite.spritecollide(jogador, grupo_inimigos, False)
        if colisao_com_inimigo:
            jogador.tomar_dano(20)

        # --- 3. Renderização
        tela.fill(c.PRETO)

        # Desenha o fundo e plataformas primeiro
        elementos_cenario.draw(tela)

        # Desenha o jogador com o método customizado de alinhamento
        jogador.draw_custom(tela)

        # Como o grupo do Pygame não sabe usar o 'draw_custom',
        # fazemos um loop para desenhar cada inimigo corretamente!
        for inimigo in grupo_inimigos:
            inimigo.draw_custom(tela)

        # Desenha a hitbox do ataque se o herói estiver golpeando
        jogador.desenhar_ataque(tela)

        # --- DESENHAR OS 5 CORAÇÕES DE VIDA (HUD) ---
        pos_x_inicial = 20  # Posição X do primeiro coração
        pos_y = 20  # Posição Y dos corações
        tamanho_coracao = 24  # Tamanho em pixels de cada coração
        espacamento = 30  # Distância entre um coração e outro

        for i in range(5):
            # Cada coração representa 20 de HP (Coração 1: 20, Coração 2: 40, etc.)
            vida_necessaria = (i + 1) * 20

            # Se a vida atual do jogador for maior ou igual à necessária, o coração fica cheio
            coracao_cheio = jogador.vida_atual >= vida_necessaria

            # Calcula a posição X de cada um na fila
            x_atual = pos_x_inicial + (i * espacamento)

            # Chama a nossa função para desenhar na tela
            desenhar_coracao(tela, x_atual, pos_y, tamanho_coracao, preenchido=coracao_cheio)

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    rodar_jogo()