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
    pygame.display.set_caption("Ironclad Quest - Fase 1: Floresta (Mapa Fixo)")
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

    # --- CONFIGURAÇÃO DA FASE LONGA FIXA ---
    COMPRIMENTO_FASE = 7000
    scroll_camera = 0
    borda_para_mover_camera = 350
    DISTANCIA_FIM_DA_FASE = COMPRIMENTO_FASE - c.LARGURA

    # --- Grupos de Sprites ---
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()
    grupo_magias = pygame.sprite.Group()

    # Criamos um único chão contínuo e sólido do início (0) até o final
    chao_principal = Plataforma(0, c.ALTURA - 50, COMPRIMENTO_FASE, 50)
    grupo_plataformas.add(chao_principal)

    # --- LEVEL DESIGN: PLATAFORMAS FIXAS ---
    plataformas_fase = [
        Plataforma(400, 420, 200, 32),
        Plataforma(850, 320, 200, 32),
        Plataforma(1400, 380, 250, 32),
        Plataforma(2000, 440, 300, 32),
        Plataforma(2800, 320, 200, 32),
        Plataforma(3500, 400, 400, 32),
    ]
    grupo_plataformas.add(*plataformas_fase)

    # --- LEVEL DESIGN: POSIÇÃO DOS INIMIGOS ---
    inimigos_fase = [
        BringerOfDeath(600, c.ALTURA - 195),
        Necromante(950, 320 - 80),
        Necromante(1500, 380 - 80),
        BringerOfDeath(2200, c.ALTURA - 195),
        Necromante(2900, 320 - 80),
    ]
    grupo_inimigos.add(*inimigos_fase)

    jogador = Cavaleiro(x=150, y=100)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- LÓGICA DE ATUALIZAÇÃO DO JOGADOR ---
        jogador.update(grupo_plataformas)

        # BARREIRA INVISÍVEL ESQUERDA: Impede o jogador de voltar para trás do limite da tela
        if jogador.rect.left < scroll_camera:
            jogador.rect.left = scroll_camera

        # BARREIRA DIREITA ABSOLUTA: Impede o jogador de ultrapassar o final físico
        if jogador.rect.right > COMPRIMENTO_FASE:
            jogador.rect.right = COMPRIMENTO_FASE

        # --- SISTEMA DE CÂMERA ---
        if jogador.rect.right - scroll_camera > c.LARGURA - borda_para_mover_camera:
            scroll_camera += jogador.velocidade_x_atual
        elif jogador.rect.left - scroll_camera < borda_para_mover_camera and scroll_camera > 0:
            scroll_camera += jogador.velocidade_x_atual

        # Impede a câmera de mostrar o vazio antes de 0 e além do final
        if scroll_camera < 0:
            scroll_camera = 0
        elif scroll_camera > DISTANCIA_FIM_DA_FASE:
            scroll_camera = DISTANCIA_FIM_DA_FASE

        # --- CHECAGEM DE PROGRESSÃO (FIM DA FASE) ---
        if scroll_camera >= DISTANCIA_FIM_DA_FASE and jogador.rect.right >= COMPRIMENTO_FASE - 50:
            if len(grupo_inimigos) == 0:
                print("Fase 1 Limpa! Transição para a Arena liberada.")

        # --- ATUALIZAÇÃO DE INIMIGOS E PROJÉTEIS (OTIMIZADO) ---
        for magia in list(grupo_magias):
            magia.update(grupo_plataformas, jogador)
            if magia.rect.right < scroll_camera - 400 or magia.rect.left > scroll_camera + c.LARGURA + 600:
                magia.kill()

        for inimigo in grupo_inimigos:
            if scroll_camera - 400 < inimigo.rect.x < scroll_camera + c.LARGURA + 400:
                if isinstance(inimigo, Necromante):
                    nova_magia = inimigo.update(grupo_plataformas, jogador)
                    if nova_magia is not None:
                        grupo_magias.add(nova_magia)
                else:
                    inimigo.update(grupo_plataformas, jogador)

        # --- COLISÕES DE ATAQUES E DANOS ---
        # 1. ATAQUE DO JOGADOR NO INIMIGO
        if jogador.atacando:
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    inimigo.tomar_dano()

                # 2. ATAQUE DAS MAGIAS E EXPLOSÕES NO JOGADOR
                for magia in grupo_magias:
                    if magia.rect.colliderect(jogador.rect):
                        nome_classe = magia.__class__.__name__

                        # DIAGNÓSTICO: Vamos ver exatamente o que está colidindo
                        print(f"Colisão com magia: {nome_classe} | Escudo ativo: {jogador.defendendo}")

                        # Se for a explosão (ou qualquer classe que não seja a BolaDeFogo)
                        if "Explosao" in nome_classe or nome_classe != "BolaDeFogo":
                            # FORÇA BRUTA: Ignora o escudo e aplica o dano direto!
                            print("!!! EXPLOSÃO IGNOROU O ESCUDO !!!")
                            jogador.tomar_dano(25)

                            # Em vez de marcar 'causou_dano', removemos a magia da tela imediatamente
                            # para evitar que ela dê dano em múltiplos frames seguidos
                            magia.kill()
                        else:
                            # Se for a BolaDeFogo normal, o escudo funciona
                            if jogador.defendendo:
                                print("Ataque mágico normal bloqueado com o escudo!")
                            else:
                                jogador.tomar_dano(20)
                            magia.kill()

        # 3. ATAQUE CORPO A CORPO DOS INIMIGOS NO JOGADOR
        for inimigo in grupo_inimigos:
            if not inimigo.morrendo:
                if hasattr(inimigo, 'atacando') and inimigo.atacando:
                    if hasattr(inimigo, 'deu_dano_nesse_ciclo') and not inimigo.deu_dano_nesse_ciclo:
                        if inimigo.rect_ataque_inimigo.colliderect(jogador.rect):
                            if jogador.defendendo:
                                print("Ataque físico bloqueado!")
                            else:
                                jogador.tomar_dano(20)
                            inimigo.deu_dano_nesse_ciclo = True

                # Dano por contato direto com o corpo do monstro
                if jogador.rect.colliderect(inimigo.rect):
                    # Impede que corpos mortos ou magias interpretadas como inimigos causem dano duplo
                    if hasattr(inimigo, 'nome') and "Explosao" in inimigo.nome:
                        continue
                    jogador.tomar_dano(20)

        # --- RENDERIZAÇÃO COM DESLOCAMENTO (PROJEÇÃO DA CÂMERA) ---
        tela.fill(c.PRETO)

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

        # Desenha magias e explosões roxas (Método de movimentação isolada por Blit Seguro)
        for magia in grupo_magias:
            if hasattr(magia, 'draw_custom'):
                rect_original = magia.rect.copy()
                magia.rect.x -= scroll_camera
                magia.draw_custom(tela)
                magia.rect = rect_original
            else:
                # Se for a explosão padrão, movemos apenas a renderização sem bagunçar a colisão física
                rect_projetado_magia = magia.rect.move(-scroll_camera, 0)
                tela.blit(magia.image, rect_projetado_magia)

        # Desenha jogador
        rect_original_jogador = jogador.rect.copy()
        jogador.rect.x -= scroll_camera
        jogador.draw_custom(tela)
        if jogador.atacando:
            rect_ataque_projetado = jogador.rect_ataque.move(-scroll_camera, 0)
            pygame.draw.rect(tela, (255, 0, 0, 100), rect_ataque_projetado, 2)
        jogador.rect = rect_original_jogador

        # HUD Fixa na Tela
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