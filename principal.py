import pygame
import sys
import random
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
    pygame.display.set_caption("Ironclad Quest - Fase 1: Floresta")
    relogio = pygame.time.Clock()

    # --- PARALLAX BACKGROUND ---
    try:
        bg_floresta = pygame.image.load("assets/Lamora HR.png").convert()
        bg_floresta = pygame.transform.scale(bg_floresta,
                                             (bg_floresta.get_width() * (c.ALTURA / bg_floresta.get_height()),
                                              c.ALTURA))
    except FileNotFoundError:
        bg_floresta = pygame.Surface((c.LARGURA, c.ALTURA))
        bg_floresta.fill((25, 25, 40))
    largura_bg = bg_floresta.get_width()

    # --- VARIÁVEIS DE CÂMERA E PROGRESSÃO ---
    scroll_camera = 0
    borda_para_mover_camera = 350

    # Define a distância gigante para durar os 3 minutos de gameplay
    DISTANCIA_FIM_DA_FASE = 45000

    # --- Grupos de Sprites ---
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()
    grupo_magias = pygame.sprite.Group()

    # Sistema de Chão Infinito Revezado
    largura_bloco_chao = c.LARGURA + 200
    chao1 = Plataforma(0, c.ALTURA - 50, largura_bloco_chao, 50)
    chao2 = Plataforma(largura_bloco_chao, c.ALTURA - 50, largura_bloco_chao, 50)
    grupo_plataformas.add(chao1, chao2)

    # Lista para controlar e mover os chãos dinamicamente
    lista_chaos = [chao1, chao2]

    # Primeiras plataformas aéreas manuais para o começo do mapa
    grupo_plataformas.add(Plataforma(400, 420, 200, 32))
    grupo_plataformas.add(Plataforma(850, 320, 200, 32))

    jogador = Cavaleiro(x=150, y=100)

    # Controladores de Spawns futuros
    proximo_spawn_plataforma_x = 1200

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- LÓGICA DE ATUALIZAÇÃO DO JOGADOR ---
        jogador.update(grupo_plataformas)

        # --- SISTEMA DE CÂMERA ---
        if jogador.rect.right - scroll_camera > c.LARGURA - borda_para_mover_camera:
            scroll_camera += jogador.velocidade_x_atual
        elif jogador.rect.left - scroll_camera < borda_para_mover_camera and scroll_camera > 0:
            scroll_camera += jogador.velocidade_x_atual

        if scroll_camera < 0:
            scroll_camera = 0

        # --- GERADOR INFINITO DE CHÃO (ANTI-QUEDAS) ---
        for chao in lista_chaos:
            # Se um bloco de chão ficou completamente para trás da visão da tela, joga ele para a frente
            if chao.rect.right < scroll_camera:
                chao.rect.x += largura_bloco_chao * 2

        # --- GERADOR DE OBSTÁCULOS E INIMIGOS À FRENTE DA TELA ---
        if scroll_camera + c.LARGURA > proximo_spawn_plataforma_x:
            # Escolhe uma posição X na frente da tela do jogador
            spawn_x = scroll_camera + c.LARGURA + random.randint(50, 300)
            spawn_y = random.choice([300, 360, 420])
            largura_random = random.randint(160, 320)

            # Cria a nova plataforma
            nova_plat = Plataforma(spawn_x, spawn_y, largura_random, 32)
            grupo_plataformas.add(nova_plat)

            # Spawna inimigos baseando-se na nova plataforma ou no chão abaixo dela
            if random.random() > 0.4:
                # Criar um Bringer no chão ou na plataforma
                y_inimigo = spawn_y - 145 if random.random() > 0.5 else c.ALTURA - 195
                grupo_inimigos.add(BringerOfDeath(spawn_x + 30, y_inimigo))
            else:
                # Criar um Necromante
                y_mago = spawn_y - 80 if random.random() > 0.5 else c.ALTURA - 130
                grupo_inimigos.add(Necromante(spawn_x + 40, y_mago))

            # Define onde será o próximo obstáculo
            proximo_spawn_plataforma_x = spawn_x + largura_random + random.randint(250, 500)

        # --- CHECAGEM DE PROGRESSÃO ---
        if scroll_camera >= DISTANCIA_FIM_DA_FASE:
            # Impede o avanço do scroll e avisa o fim da fase
            scroll_camera = DISTANCIA_FIM_DA_FASE
            if len(grupo_inimigos) == 0:
                print("Fase 1 Limpa! Transição para a Arena liberada.")

        # --- ATUALIZAÇÃO DE INIMIGOS E PROJÉTEIS ---
        for magia in list(grupo_magias):
            magia.update(grupo_plataformas, jogador)

        for inimigo in grupo_inimigos:
            if isinstance(inimigo, Necromante):
                nova_magia = inimigo.update(grupo_plataformas, jogador)
                if nova_magia is not None:
                    grupo_magias.add(nova_magia)
            else:
                inimigo.update(grupo_plataformas, jogador)

            # Se o inimigo ficou muito para trás, remove para liberar memória
            if inimigo.rect.right < scroll_camera - 300:
                inimigo.kill()

        # --- COLISÕES DE ATAQUES E DANOS ---
        if jogador.atacando:
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    inimigo.tomar_dano()

        for magia in grupo_magias:
            if magia.rect.colliderect(jogador.rect):
                if jogador.defendendo:
                    print("Ataque mágico bloqueado!")
                else:
                    jogador.tomar_dano(20)
                magia.kill()

        for inimigo in grupo_inimigos:
            if not inimigo.morrendo:
                if hasattr(inimigo, 'atacando') and inimigo.atacando:
                    if hasattr(inimigo, 'deu_dano_nesse_ciclo') and not inimigo.deu_dano_nesse_ciclo:
                        if inimigo.rect_ataque_inimigo.colliderect(jogador.rect):
                            jogador.tomar_dano(20)
                            inimigo.deu_dano_nesse_ciclo = True

                if jogador.rect.colliderect(inimigo.rect):
                    jogador.tomar_dano(20)

        # --- RENDERIZAÇÃO COM DESLOCAMENTO ---
        tela.fill(c.PRETO)

        # Fundo Parallax repetido
        scroll_fundo = (scroll_camera * 0.3) % largura_bg
        tela.blit(bg_floresta, (-scroll_fundo, 0))
        tela.blit(bg_floresta, (largura_bg - scroll_fundo, 0))

        # Desenha as plataformas e pisos
        for plataforma in grupo_plataformas:
            rect_projetado = plataforma.rect.move(-scroll_camera, 0)
            tela.blit(plataforma.image, rect_projetado)

        # Desenha inimigos
        for inimigo in grupo_inimigos:
            rect_original = inimigo.rect.copy()
            inimigo.rect.x -= scroll_camera
            inimigo.draw_custom(tela)
            inimigo.rect = rect_original

        # Desenha magias
        for magia in grupo_magias:
            rect_original = magia.rect.copy()
            magia.rect.x -= scroll_camera
            if hasattr(magia, 'draw_custom'):
                magia.draw_custom(tela)
            else:
                tela.blit(magia.image, magia.rect)
            magia.rect = rect_original

        # Desenha jogador
        rect_original_jogador = jogador.rect.copy()
        jogador.rect.x -= scroll_camera
        jogador.draw_custom(tela)
        if jogador.atacando:
            rect_ataque_projetado = jogador.rect_ataque.move(-scroll_camera, 0)
            pygame.draw.rect(tela, (255, 0, 0, 100), rect_ataque_projetado, 2)
        jogador.rect = rect_original_jogador

        # HUD Fixa
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