import pygame
import sys
import random
import constantes as c
from personagens import Cavaleiro, Plataforma, BringerOfDeath, Necromante
from decoracao import Decoracao, Nuvem  # Importação do novo módulo de decoração
from sons import GerenciadorSons
from item import ItemCura


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

# --- EXEMPLO DE ESTRUTURA DE MONTANHA (Cole onde você gera o mapa) ---

# Função auxiliar para criar um platô de terra maciço rapidamente
def criar_montanha(x_inicio, largura_blocos, altura_blocos, grupo_colisao, grupo_decoracao, bloco_classe):
    largura_bloco = 40  # Ajuste para o tamanho real do seu bloco de colisão/sprite
    altura_bloco = 40
    chao_y = c.ALTURA - 50  # A altura padrão do chão do seu jogo

    for i in range(largura_blocos):
        for j in range(altura_blocos):
            # Calcula a posição de cada bloco de terra para preencher a montanha
            pos_x = x_inicio + (i * largura_bloco)
            pos_y = chao_y - ((j + 1) * altura_bloco)

            if j == altura_blocos - 1:
                # O topo continua tendo colisão (adicionado ao grupo_colisao)
                bloco = bloco_classe(pos_x, pos_y, largura_bloco, altura_bloco, tipo="topo")
                grupo_colisao.add(bloco)
            else:
                # A terra vira apenas cenário visual (adicionado ao grupo_decoracao)
                bloco = bloco_classe(pos_x, pos_y, largura_bloco, altura_bloco, tipo="terra")
                grupo_decoracao.add(bloco)


def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # --- SISTEMA DE ÁUDIO ---
    audio = GerenciadorSons()
    audio.tocar_musica_fase("assets/sons/fase_1 music.mp3", volume=0.15)  # Ajuste o volume se achar alto

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
    grupo_itens = pygame.sprite.Group()

    # Novos grupos de ambientação (Camadas de Fundo e Frente)
    grupo_decoracao_fundo = pygame.sprite.Group()
    grupo_decoracao_frente = pygame.sprite.Group()

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

    # --- GERANDO AS MONTANHAS AO LONGO DOS 7000 PIXELS ---
    # Montanha 1 (Perto do início): 3 blocos de altura, 8 de largura
    criar_montanha(x_inicio=1200, largura_blocos=8, altura_blocos=3, grupo_colisao=grupo_plataformas, grupo_decoracao=grupo_decoracao_fundo,
               bloco_classe=Plataforma)

    # Montanha 2 (Mais alta, no meio da fase): 5 blocos de altura, 12 de largura
    criar_montanha(x_inicio=2800, largura_blocos=12, altura_blocos=5, grupo_colisao=grupo_plataformas, grupo_decoracao=grupo_decoracao_fundo,
               bloco_classe=Plataforma)

    # Montanha 3 (Dupla, estilo Sonic, um platô logo após o outro)
    criar_montanha(x_inicio=4500, largura_blocos=6, altura_blocos=2, grupo_colisao=grupo_plataformas, grupo_decoracao=grupo_decoracao_fundo,
               bloco_classe=Plataforma)
    criar_montanha(x_inicio=4740, largura_blocos=10, altura_blocos=4, grupo_colisao=grupo_plataformas, grupo_decoracao=grupo_decoracao_fundo,
               bloco_classe=Plataforma)

    # --- LEVEL DESIGN: POSIÇÃO DOS INIMIGOS ---
    inimigos_fase = [
        # Adicione estes elementos dentro da sua lista inimigos_fase atual:

        # Inimigo no topo da primeira montanha (X=1200, altura de 3 blocos -> 3 * 40 = 120 pixels para cima)
        Necromante(1350, c.ALTURA - 50 - 120 - 80),

        # Inimigos na patrulha do vale central
        BringerOfDeath(1800, c.ALTURA - 195),
        BringerOfDeath(2400, c.ALTURA - 195),

        # Inimigos no topo da grande montanha (X=2800, altura de 5 blocos -> 5 * 40 = 200 pixels para cima)
        BringerOfDeath(2900, c.ALTURA - 50 - 200 - 140),
        Necromante(3100, c.ALTURA - 50 - 200 - 80),

        # Inimigos na seção final após os 5000 pixels
        Necromante(5200, c.ALTURA - 195),
        BringerOfDeath(6000, c.ALTURA - 195),
        Necromante(6400, c.ALTURA - 195)
    ]
    grupo_inimigos.add(*inimigos_fase)

    # --- LEVEL DESIGN VISUAL: GERADOR DE AMBIENTAÇÃO AUTOMÁTICA ---
    # 1. Nuvens flutuando no céu com velocidades variadas
    for x_nuvem in range(100, COMPRIMENTO_FASE, 450):
        if random.random() > 0.3:
            arquivo_nuvem = random.choice([f"Clouds_0{i}.png" for i in range(1, 9)])
            vel_random = random.uniform(0.05, 0.18)
            grupo_decoracao_fundo.add(
                Nuvem(x_nuvem, random.randint(30, 140), arquivo_nuvem, (130, 65), velocidade=vel_random)
            )

    # 2. Distribuição de moitas, pedras, tocos e ossos pelo chão principal
    assets_moitas_fundo = ["07.png", "08.png", "09.png", "10.png", "11.png"]
    assets_moitas_frente = ["Bushe1.png", "Bushe2.png", "Bushe3.png", "Bushe4.png"]
    assets_pedras = ["Rock1.png", "Rock2.png", "Rock3.png", "Rock4.png"]
    assets_detalhes = ["14.png", "15.png", "16.png", "17.png", "Stump 1.png", "Stump 2.png"]

    x_atual = 60
    chao_y = c.ALTURA - 50
    while x_atual < COMPRIMENTO_FASE - 200:
        sorteio = random.random()
        if sorteio < 0.25:
            # Moitas densas de fundo
            img = random.choice(assets_moitas_fundo)
            grupo_decoracao_fundo.add(Decoracao(x_atual, chao_y - 45, img, (64, 48)))
        elif sorteio < 0.45:
            # Moitas pequenas de grama na frente (cobrem levemente os pés)
            img = random.choice(assets_moitas_frente)
            grupo_decoracao_frente.add(Decoracao(x_atual, chao_y - 25, img, (48, 28)))
        elif sorteio < 0.65:
            # Pedras decorativas
            img = random.choice(assets_pedras)
            grupo_decoracao_frente.add(Decoracao(x_atual, chao_y - 28, img, (38, 30)))
        elif sorteio < 0.75:
            # Sinais, ossos ou tocos de árvore
            img = random.choice(assets_detalhes)
            tam = (48, 48) if "16" in img or "17" in img else (32, 32)
            grupo_decoracao_fundo.add(Decoracao(x_atual, chao_y - tam[1], img, tam))

        x_atual += random.randint(90, 240)

    # 3. Detalhes em cima das plataformas suspensas
    for plat in plataformas_fase:
        if random.random() > 0.4:
            grupo_decoracao_fundo.add(
                Decoracao(plat.rect.x + 15, plat.rect.y - 25, random.choice(assets_moitas_frente), (40, 28)))
        if random.random() > 0.5:
            grupo_decoracao_frente.add(
                Decoracao(plat.rect.right - 45, plat.rect.y - 25, random.choice(assets_pedras), (32, 26)))

    jogador = Cavaleiro(x=150, y=100)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # --- LÓGICA DE ATUALIZAÇÃO DO JOGADOR ---
        jogador.update(grupo_plataformas, audio)

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

        # --- ATUALIZAÇÃO DOS ELEMENTOS DO CENÁRIO ---
        for elemento in grupo_decoracao_fundo:
            if isinstance(elemento, Nuvem):
                elemento.update(scroll_camera)

        # --- ATUALIZAÇÃO DE INIMIGOS E PROJÉTEIS (OTIMIZADO) ---
        for magia in list(grupo_magias):
            magia.update(grupo_plataformas, jogador, audio)
            if magia.rect.right < scroll_camera - 400 or magia.rect.left > scroll_camera + c.LARGURA + 600:
                magia.kill()

        for inimigo in grupo_inimigos:
            if scroll_camera - 400 < inimigo.rect.x < scroll_camera + c.LARGURA + 400:
                if isinstance(inimigo, Necromante):
                    nova_magia = inimigo.update(grupo_plataformas, jogador, audio)
                    if nova_magia is not None:
                        grupo_magias.add(nova_magia)
                else:
                    inimigo.update(grupo_plataformas, jogador, audio)

        # --- ATUALIZAÇÃO DOS ITENS ---
        for item in grupo_itens:
            item.update(grupo_plataformas)

        # --- COLISÕES DE ATAQUES E DANOS ---
        # 1. ATAQUE DO JOGADOR NO INIMIGO
        if jogador.atacando:
            for inimigo in grupo_inimigos:
                if jogador.rect_ataque.colliderect(inimigo.rect):
                    # Se o seu inimigo já tiver uma trava de invencibilidade (ex: não piscar/não tomar dano em sequência)
                    # Certifique-se de que o som só toque se o dano REALMENTE entrar:
                    if hasattr(inimigo, 'invencivel') and not inimigo.invencivel:
                        inimigo.tomar_dano(audio=audio, jogador=jogador)

                        # Adicionamos a checagem se ele já dropou algo neste ciclo de morte
                        if inimigo.morrendo and not getattr(inimigo, 'ja_dropou_item', False):
                            inimigo.ja_dropou_item = True  # <--- Ativa a trava IMEDIATAMENTE!

                            if random.random() < 0.7:  # 50% de chance de cair o bife
                                novo_bife = ItemCura(inimigo.rect.centerx, inimigo.rect.centery, quantidade_cura=20)
                                grupo_itens.add(novo_bife)

                        if jogador.ataque_aereo:
                            audio.tocar_sfx_player("hit_ar")
                        elif inimigo.__class__.__name__ == "BringerOfDeath":
                            audio.tocar_sfx_player("hit_bringer")
                        elif inimigo.__class__.__name__ == "Necromante":
                            audio.tocar_sfx_player("hit_necromancer")
                    elif not hasattr(inimigo, 'invencivel'):
                        # Se seu inimigo ainda não tem sistema de invencibilidade por frames,
                        # ele vai floodar o som. O ideal é aplicar o tomar_dano e o som juntos:
                        inimigo.tomar_dano(audio=audio)

        # 2. ATAQUE DAS MAGIAS E EXPLOSÕES NO JOGADOR (Limpo e Corrigido)
        for magia in grupo_magias:
            if magia.rect.colliderect(jogador.rect):
                nome_classe = magia.__class__.__name__

                # --- CASO 1: BOLA DE FOGO (Defensável) ---
                if nome_classe == "MagiaNecromante":
                    if jogador.defendendo:
                        print("Sucesso: Bola de Fogo bloqueada com o escudo!")
                        audio.tocar_sfx_player("escudo_1")
                        audio.tocar_sfx_player("escudo_2")
                    else:
                        print("Dano: Cavaleiro atingido pela Bola de Fogo!")
                        jogador.tomar_dano(20, audio=audio)
                    magia.kill()  # Some com a bola de fogo

                # --- CASO 2: EXPLOSÃO DO CHÃO (Indefensável) ---
                elif nome_classe == "ExplosaoNecromante":
                    # Deixamos a própria classe controlar o dano e o som através do update dela
                    pass

                # --- CASO ZERO: Fallback de segurança ---
                else:
                    if jogador.defendendo:
                        audio.tocar_sfx_player("escudo_1")
                        audio.tocar_sfx_player("escudo_2")
                    else:
                        jogador.tomar_dano(20, audio=audio)
                    magia.kill()

        # 3. ATAQUE CORPO A CORPO DOS INIMIGOS NO JOGADOR
        for inimigo in grupo_inimigos:
            if not inimigo.morrendo:
                if hasattr(inimigo, 'atacando') and inimigo.atacando:
                    if hasattr(inimigo, 'deu_dano_nesse_ciclo') and not inimigo.deu_dano_nesse_ciclo:
                        if inimigo.rect_ataque_inimigo.colliderect(jogador.rect):
                            if jogador.defendendo:
                                print("Ataque físico bloqueado!")
                                audio.tocar_sfx_player("escudo_1")
                                audio.tocar_sfx_player("escudo_2")
                            else:
                                jogador.tomar_dano(20, audio=audio)
                            inimigo.deu_dano_nesse_ciclo = True

                if jogador.rect.colliderect(inimigo.rect):
                    if hasattr(inimigo, 'nome') and "Explosao" in inimigo.nome:
                        continue
                    jogador.tomar_dano(20, audio=audio)

        # --- 4. COLISÃO DO JOGADOR COM ITENS DE CURA ---
        colisoes_itens = pygame.sprite.spritecollide(jogador, grupo_itens, False)
        for item in colisoes_itens:
            # Só coleta o bife se o jogador tiver perdido pelo menos um pouco de vida
            if jogador.vida_atual < jogador.vida_max:
                jogador.vida_atual += item.quantidade_cura

                # Impede que a vida ultrapasse o limite máximo de 100
                if jogador.vida_atual > jogador.vida_max:
                    jogador.vida_atual = jogador.vida_max

                print(f"Bife coletado! Vida do Cavaleiro: {jogador.vida_atual}/{jogador.vida_max}")

                # --- ATIVA O SOM DE COMER AQUI ---
                if audio is not None:
                    audio.tocar_sfx_player("comer")

                item.kill()  # Faz o bife sumir do mapa

        # --- RENDERIZAÇÃO COM DESLOCAMENTO (PROJEÇÃO DA CÂMERA) ---
        tela.fill(c.PRETO)

        # Camada 0: Parallax Fundo Estático
        scroll_fundo = (scroll_camera * 0.3) % largura_bg
        tela.blit(bg_floresta, (-scroll_fundo, 0))
        tela.blit(bg_floresta, (largura_bg - scroll_fundo, 0))

        # Camada 1: DECORAÇÕES DE FUNDO (Nuvens, arbustos de trás, placas, tocos)
        for dec in grupo_decoracao_fundo:
            rect_p = dec.rect.move(-scroll_camera, 0)
            tela.blit(dec.image, rect_p)

        # Camada 2: Plataformas e Pisos
        for plataforma in grupo_plataformas:
            rect_projetado = plataforma.rect.move(-scroll_camera, 0)
            tela.blit(plataforma.image, rect_projetado)

        # Camada 3: Inimigos
        for inimigo in grupo_inimigos:
            rect_original = inimigo.rect.copy()
            inimigo.rect.x -= scroll_camera
            inimigo.draw_custom(tela)
            inimigo.rect = rect_original

        # Camada 4: Magias e Projéteis
        for magia in grupo_magias:
            if hasattr(magia, 'draw_custom'):
                rect_original = magia.rect.copy()
                magia.rect.x -= scroll_camera
                magia.draw_custom(tela)
                magia.rect = rect_original
            else:
                rect_projetado_magia = magia.rect.move(-scroll_camera, 0)
                tela.blit(magia.image, rect_projetado_magia)

        # Camada 5: Jogador
        rect_original_jogador = jogador.rect.copy()
        jogador.rect.x -= scroll_camera
        jogador.draw_custom(tela)
        if jogador.atacando:
            rect_ataque_projetado = jogador.rect_ataque.move(-scroll_camera, 0)
            pygame.draw.rect(tela, (255, 0, 0, 100), rect_ataque_projetado, 2)
        jogador.rect = rect_original_jogador

        # Camada 6: DECORAÇÕES DE FRENTE (Matinhos e pedras que cobrem o pé do jogador)
        for dec in grupo_decoracao_frente:
            rect_p = dec.rect.move(-scroll_camera, 0)
            tela.blit(dec.image, rect_p)

        # Camada 7: HUD Fixa na Tela
        pos_x_inicial, pos_y, tamanho_coracao, espacamento = 20, 20, 24, 30
        for i in range(5):
            vida_necessaria = (i + 1) * 20
            coracao_cheio = jogador.vida_atual >= vida_necessaria
            desenhar_coracao(tela, pos_x_inicial + (i * espacamento), pos_y, tamanho_coracao, preenchido=coracao_cheio)

        # Camada de Itens de Cura
        for item in grupo_itens:
            rect_projetado_item = item.rect.move(-scroll_camera, 0)
            tela.blit(item.image, rect_projetado_item)

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    rodar_jogo()