import pygame
import sys
import random
import constantes as c
from personagens import Cavaleiro, Plataforma, BringerOfDeath, Necromante
from decoracao import Decoracao, Nuvem  # Importação do novo módulo de decoração
from sons import GerenciadorSons
from item import ItemCura
from boss import BossDemonio, ProjetilSopro
from efeitos import Efeito


def interagir_pause(tela, bg_congelado, audio):
    relogio_pause = pygame.time.Clock()

    try:
        som_navegar = pygame.mixer.Sound("assets/sons/Menu Selection Click.mp3")
        som_confirmar = pygame.mixer.Sound("assets/sons/Menu Confirm.mp3")
    except pygame.error:
        som_navegar = None
        som_confirmar = None

    opcao_selecionada = 0
    opcoes_pause = ["RESUME", "QUIT"]

    volume_original = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(volume_original * 0.4)

    pausado = True
    while pausado:
        tela.blit(bg_congelado, (0, 0))

        filtro = pygame.Surface((c.LARGURA, c.ALTURA), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, 160))
        tela.blit(filtro, (0, 0))

        desenhar_texto(tela, "PAUSE", 48, c.LARGURA // 2, c.ALTURA // 2 - 80, (255, 255, 255))

        for i, opcao in enumerate(opcoes_pause):
            cor = (255, 215, 0) if i == opcao_selecionada else (200, 200, 200)
            prefixo = "> " if i == opcao_selecionada else "  "
            desenhar_texto(tela, prefixo + opcao, 24, c.LARGURA // 2, c.ALTURA // 2 + 20 + (i * 50), cor)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if som_confirmar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                        som_confirmar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                        som_confirmar.play()
                    pygame.mixer.music.set_volume(volume_original)
                    return "resume"

                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_pause)
                    if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                        som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                        som_navegar.play()

                elif evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_pause)
                    if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                        som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                        som_navegar.play()

                elif evento.key == pygame.K_x:
                    if som_confirmar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                        som_confirmar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                        som_confirmar.play()

                    if opcao_selecionada == 0:
                        pygame.mixer.music.set_volume(volume_original)
                        return "resume"
                    elif opcao_selecionada == 1:
                        pygame.mixer.music.stop()
                        return "quit"

        pygame.display.flip()
        relogio_pause.tick(c.FPS)


def exibir_game_over(tela, config_audio):
    """
    Controla a tela escura de Game Over após a animação de morte acabar.
    Retorna 'restart' ou 'quit'.
    """
    relogio_go = pygame.time.Clock()

    # 1. Parâmetros e reprodução da música de Game Over
    v_geral = config_audio.get("vol_geral", 1.0) if config_audio else 1.0
    v_musica = config_audio.get("vol_musica", 0.6) if config_audio else 0.6
    v_sfx = config_audio.get("vol_sfx", 0.8) if config_audio else 0.8

    try:
        pygame.mixer.music.load("assets/sons/game_over music.mp3")
        pygame.mixer.music.set_volume(v_musica * v_geral)
        pygame.mixer.music.play(0)
    except pygame.error:
        print("Aviso: Música de Game Over não encontrada.")

    try:
        som_navegar = pygame.mixer.Sound("assets/sons/Menu Selection Click.mp3")
        som_confirmar = pygame.mixer.Sound("assets/sons/Menu Confirm.mp3")
    except pygame.error:
        som_navegar = som_confirmar = None

    opcao_selecionada = 0
    opcoes = ["RESTART", "QUIT"]

    while True:
        tela.fill((0, 0, 0))  # Tela completamente escura

        # Título GAME OVER destacado em Vermelho
        desenhar_texto(tela, "GAME OVER", 54, c.LARGURA // 2, c.ALTURA // 2 - 80, (180, 20, 20))

        # Opções de Menu
        for i, opcao in enumerate(opcoes):
            cor = (255, 215, 0) if i == opcao_selecionada else (140, 140, 140)
            prefixo = "> " if i == opcao_selecionada else "  "
            desenhar_texto(tela, prefixo + opcao, 26, c.LARGURA // 2, c.ALTURA // 2 + 30 + (i * 50), cor)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    if som_navegar and v_sfx > 0:
                        som_navegar.set_volume(v_sfx * v_geral)
                        som_navegar.play()
                elif evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    if som_navegar and v_sfx > 0:
                        som_navegar.set_volume(v_sfx * v_geral)
                        som_navegar.play()
                elif evento.key == pygame.K_x:
                    if som_confirmar and v_sfx > 0:
                        som_confirmar.set_volume(v_sfx * v_geral)
                        som_confirmar.play()

                    if opcao_selecionada == 0:  # RESTART
                        pygame.mixer.music.stop()
                        return "restart"
                    elif opcao_selecionada == 1:  # QUIT
                        pygame.mixer.music.stop()
                        return "quit"

        pygame.display.flip()
        relogio_go.tick(c.FPS)


class BannerObjetivo:
    def __init__(self, texto, config_audio=None):
        # Carrega a imagem do Ribbon
        try:
            self.image_base = pygame.image.load("assets/BigRibbons.png").convert_alpha()
            # Opcional: Ajuste a escala se achar que ficou muito grande ou pequeno
            self.image = pygame.transform.scale(self.image_base, (450, 140))
        except pygame.error:
            # Caso não ache a imagem, cria um retângulo de fallback
            self.image = pygame.Surface((450, 100), pygame.SRCALPHA)
            self.image.fill((20, 40, 60, 200))

        self.rect = self.image.get_rect()

        # Posição X centralizada na tela
        self.rect.centerx = c.LARGURA // 2

        # Começa totalmente escondido acima da tela
        self.rect.bottom = 0

        self.texto = texto
        self.velocidade = 5
        self.estado = "descendo"  # Estados: "descendo", "esperando", "subindo", "fim"

        # Controle de tempo para ficar parado na tela
        self.tempo_inicio_espera = 0
        self.duracao_espera = 3000  # 3 segundos parado no centro

        # 🔊 Efeito sonoro opcional ao aparecer (se tiver um som de "pop" ou "quest")
        if config_audio:
            # Aqui você pode tocar um som se quiser no futuro
            pass

    def update(self):
        tempo_atual = pygame.time.get_ticks()

        if self.estado == "descendo":
            # Desce até uma altura legal (ex: Y = 60)
            if self.rect.top < 60:
                self.rect.y += self.velocidade
            else:
                self.rect.top = 60
                self.estado = "esperando"
                self.tempo_inicio_espera = tempo_atual

        elif self.estado == "esperando":
            # Conta 3 segundos
            if tempo_atual - self.tempo_inicio_espera > self.duracao_espera:
                self.estado = "subindo"

        elif self.estado == "subindo":
            # Sobe até sumir da tela de novo
            if self.rect.bottom > 0:
                self.rect.y -= self.velocidade
            else:
                self.estado = "fim"

    def draw(self, tela):
        if self.estado == "fim":
            return

        # 1. Desenha o Ribbon na tela
        tela.blit(self.image, self.rect)

        # 2. Desenha o texto "Defeat all enemies" por cima dele
        # (Ajuste o tamanho da fonte e cor amarela conforme seu gosto)
        # Se você tiver a função 'desenhar_texto', usamos ela centralizada no rect do banner
        cor_amarela = (255, 215, 0)

        # Como o Ribbon tem as pontas para baixo, o centro vertical real pode precisar de um leve ajuste
        desenhar_texto(
            tela,
            self.texto,
            24,
            self.rect.centerx,
            self.rect.centery - 5,  # Leve ajuste para centralizar no pergaminho
            cor_amarela
        )

def desenhar_texto(tela, texto, tamanho, x, y, cor=(255, 255, 255), centralizado=True):
    # Usa a fonte padrão do sistema, ou substitua por sua fonte .ttf customizada
    fonte = pygame.font.SysFont("arial", tamanho, bold=True)
    superficie_texto = fonte.render(texto, True, cor)
    rect_texto = superficie_texto.get_rect()
    if centralizado:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
    tela.blit(superficie_texto, rect_texto)

def rodar_menu():
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # --- SISTEMA DE ÁUDIO NO MENU ---
    audio = GerenciadorSons()
    # Se você tiver uma música de menu específica, mude o caminho aqui:
    audio.tocar_musica_fase("assets/sons/menu music.mp3", volume=0.9)

    # 🛠️ CARREGAMENTO DOS SONS REAIS DO MENU (Com tratamento de erro)
    try:
        som_navegar = pygame.mixer.Sound("assets/sons/Menu Selection Click.mp3")
        som_confirmar = pygame.mixer.Sound("assets/sons/Menu Confirm.mp3")
        som_voltar = pygame.mixer.Sound("assets/sons/Menu Error.mp3")
    except pygame.error:
        print("Aviso: Um ou mais sons do menu não puderam ser carregados.")
        som_navegar = None
        som_confirmar = None
        som_voltar = None

    # --- CARREGAMENTO DE FUNDO ---
    try:
        bg_menu = pygame.image.load("assets/HR_Dark Gothic Castle.png").convert()
        bg_menu = pygame.transform.scale(bg_menu, (c.LARGURA, c.ALTURA))
    except FileNotFoundError:
        bg_menu = pygame.Surface((c.LARGURA, c.ALTURA))
        bg_menu.fill((15, 10, 25))

    # Máquina de Estados do Menu: "principal", "options", "how_to_play"
    estado_atual = "principal"

    # Índices de seleção para os menus
    opcao_selecionada = 0  # 0: New Game, 1: Options, 2: How to Play, 3: Exit
    slider_selecionado = 0  # 0: Geral, 1: Música, 2: SFX, 3: Tela, 4: Voltar

    # Variáveis de Configuração simuladas (Valores de 0.0 a 1.0)
    vol_geral = 1.0
    vol_musica = 0.6
    vol_sfx = 0.8
    modo_tela_cheia = False

    opcoes_principais = ["NEW GAME", "OPTIONS", "HOW TO PLAY", "QUIT"]

    rodando = True
    while rodando:
        tela.blit(bg_menu, (0, 0))

        # Filtro escuro para dar contraste aos textos
        filtro = pygame.Surface((c.LARGURA, c.ALTURA), pygame.SRCALPHA)
        filtro.fill((0, 0, 0, 120))
        tela.blit(filtro, (0, 0))

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # -----------------------------------------------------------------
                # CONTROLES DA TELA PRINCIPAL
                # -----------------------------------------------------------------
                if estado_atual == "principal":
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_principais)
                        # 🎯 Toca som de navegar
                        if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_navegar.play()

                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_principais)
                        # 🎯 Toca som de navegar
                        if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_navegar.play()


                    elif evento.key == pygame.K_x:  # CONFIRMAR (X)
                        # 🎯 Toca som de confirmar
                        if som_confirmar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_confirmar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_confirmar.play()

                        if opcao_selecionada == 0:
                            pygame.mixer.music.stop()
                            # Retorna um dicionário com todas as configurações salvas pelo usuário
                            return {
                                "vol_geral": vol_geral,
                                "vol_musica": vol_musica,
                                "vol_sfx": vol_sfx
                            }
                        elif opcao_selecionada == 1:
                            estado_atual = "options"
                        elif opcao_selecionada == 2:
                            estado_atual = "how_to_play"
                        elif opcao_selecionada == 3:
                            pygame.quit()
                            sys.exit()

                # -----------------------------------------------------------------
                # CONTROLES DA TELA DE OPÇÕES (CORRIGIDO)
                # -----------------------------------------------------------------
                elif estado_atual == "options":
                    # 🎯 A variável começa aqui, antes de testar as teclas!
                    volume_alterado = False

                    if evento.key == pygame.K_z:  # VOLTAR (Z)
                        # 🎯 Toca som de voltar
                        if som_voltar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_voltar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_voltar.play()
                        estado_atual = "principal"


                    elif evento.key == pygame.K_UP:
                        slider_selecionado = (slider_selecionado - 1) % 5
                        # 🎯 Toca som de navegar
                        if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_navegar.play()


                    elif evento.key == pygame.K_DOWN:
                        slider_selecionado = (slider_selecionado + 1) % 5
                        # 🎯 Toca som de navegar
                        if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_navegar.play()

                    elif evento.key == pygame.K_LEFT:
                        if slider_selecionado == 0:
                            vol_geral = max(0.0, vol_geral - 0.1)
                        elif slider_selecionado == 1:
                            vol_musica = max(0.0, vol_musica - 0.1)
                        elif slider_selecionado == 2:
                            vol_sfx = max(0.0, vol_sfx - 0.1)
                        volume_alterado = True

                    elif evento.key == pygame.K_RIGHT:
                        if slider_selecionado == 0:
                            vol_geral = min(1.0, vol_geral + 0.1)
                        elif slider_selecionado == 1:
                            vol_musica = min(1.0, vol_musica + 0.1)
                        elif slider_selecionado == 2:
                            vol_sfx = min(1.0, vol_sfx + 0.1)
                        volume_alterado = True

                    elif evento.key == pygame.K_x:  # Interagir no botão Voltar ou Mudar Tela
                        # 🎯 Toca som de confirmar
                        if som_confirmar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_confirmar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_confirmar.play()

                        if slider_selecionado == 3:
                            modo_tela_cheia = not modo_tela_cheia
                            if modo_tela_cheia:
                                tela = pygame.display.set_mode((c.LARGURA, c.ALTURA), pygame.FULLSCREEN)
                            else:
                                tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
                        elif slider_selecionado == 4:
                            estado_atual = "principal"

                    # 🎯 SE O VOLUME FOI ALTERADO, SALVA NA CLASSE PARA AS OUTRAS FASES SABEREM!
                    if volume_alterado:
                        GerenciadorSons.vol_geral = vol_geral
                        GerenciadorSons.vol_musica = vol_musica
                        GerenciadorSons.vol_sfx = vol_sfx

                        volume_musica_real = vol_musica * vol_geral
                        pygame.mixer.music.set_volume(volume_musica_real)

                        # 🎯 Toca o som de clique clássico ao mexer na barra de volume
                        if som_navegar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_navegar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_navegar.play()

                # -----------------------------------------------------------------
                # CONTROLES DA TELA HOW TO PLAY
                # -----------------------------------------------------------------
                elif estado_atual == "how_to_play":
                    if evento.key in [pygame.K_z, pygame.K_x]:
                        # 🎯 Toca som de voltar
                        if som_voltar and GerenciadorSons.vol_sfx > 0 and GerenciadorSons.vol_geral > 0:
                            som_voltar.set_volume(GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
                            som_voltar.play()
                        estado_atual = "principal"

        # -----------------------------------------------------------------
        # RENDERIZAÇÃO DE ACORDO COM O ESTADO
        # -----------------------------------------------------------------
        if estado_atual == "principal":
            desenhar_texto(tela, "IRONCLAD QUEST", 52, c.LARGURA // 2, 120, (180, 40, 50))

            for i, opcao in enumerate(opcoes_principais):
                cor = (255, 215, 0) if i == opcao_selecionada else (200, 200, 200)
                prefixo = "> " if i == opcao_selecionada else "  "
                desenhar_texto(tela, prefixo + opcao, 26, c.LARGURA // 2, 260 + (i * 50), cor)

        elif estado_atual == "options":
            desenhar_texto(tela, "OPTIONS", 40, c.LARGURA // 2, 80, (180, 40, 50))

            # Helper para desenhar Sliders visuais
            def desenhar_slider(label, valor, index_linha, ativo):
                cor_txt = (255, 215, 0) if ativo else (200, 200, 200)
                desenhar_texto(tela, label, 22, 200, 180 + (index_linha * 50), cor_txt, centralizado=False)
                # Barra externa do slider
                pygame.draw.rect(tela, (50, 50, 50), (450, 185 + (index_linha * 50), 200, 15))
                # Preenchimento interno
                pygame.draw.rect(tela, cor_txt, (450, 185 + (index_linha * 50), int(200 * valor), 15))

            desenhar_slider("MASTER VOLUME", vol_geral, 0, slider_selecionado == 0)
            desenhar_slider("MUSIC VOLUME", vol_musica, 1, slider_selecionado == 1)
            desenhar_slider("SFX VOLUME", vol_sfx, 2, slider_selecionado == 2)

            # Opção de Modo de Tela
            cor_tela = (255, 215, 0) if slider_selecionado == 3 else (200, 200, 200)
            texto_tela = "FULLSCREEN" if modo_tela_cheia else "WINDOWED"
            desenhar_texto(tela, f"DISPLAY MODE:  [{texto_tela}]", 22, 250, 380, cor_tela, centralizado=False)

            # Botão Voltar interno
            cor_voltar = (255, 215, 0) if slider_selecionado == 4 else (200, 200, 200)
            desenhar_texto(tela, "BACK TO MENU", 24, c.LARGURA // 2, 460, cor_voltar)

        elif estado_atual == "how_to_play":
            desenhar_texto(tela, "HOW TO PLAY", 40, c.LARGURA // 2, 80, (180, 40, 50))

            comandos = [
                "SETAS  -  MOVER O CAVALEIRO",
                "ESPAÇO  -  PULAR",
                "X  -  ATACAR / CONFIRMAR NO MENU",
                "Z  -  RETORNAR / VOLTAR NO MENU",
                "LSHIFT - DEFENDER",
                "LCTRL - CORRER",
                "ESC  -  PAUSAR O JOGO",
            ]
            for i, cmd in enumerate(comandos):
                desenhar_texto(tela, cmd, 20, c.LARGURA // 2, 180 + (i * 45), (220, 220, 220))

        # 🎯 LEGENDA FIXA DE BOTÕES NO CANTO INFERIOR DIREITO
        txt_legenda = "[X] CONFIRMAR   [Z] VOLTAR"
        desenhar_texto(tela, txt_legenda, 16, c.LARGURA - 228, c.ALTURA - 25, (150, 150, 150), centralizado=False)

        pygame.display.flip()
        relogio.tick(c.FPS)


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


def rodar_jogo(config_audio=None):
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # --- SISTEMA DE ÁUDIO ---
    audio = GerenciadorSons()

    # Valores padrão caso o menu não envie nada
    v_geral, v_musica, v_sfx = 1.0, 0.6, 0.8
    if config_audio:
        v_geral = config_audio["vol_geral"]
        v_musica = config_audio["vol_musica"]
        v_sfx = config_audio["vol_sfx"]

    volume_musica_real = v_musica * v_geral
    volume_sfx_real = v_sfx * v_geral

    # Aplica o volume de SFX no gerenciador (se sua classe sons.py tiver suporte,
    # caso contrário o Pygame aplica o volume individual nos mixers)
    # Se o seu GerenciadorSons tiver um método para mudar o volume do SFX, chame-o aqui, ex: audio.set_volume_sfx(volume_sfx_real)

    # 🎯 Som de impacto na transição de fase inicial ajustado
    try:
        som_transicao = pygame.mixer.Sound("assets/sons/transição de fase.mp3")
        som_transicao.set_volume(volume_sfx_real)  # <--- Agora obedece o volume do SFX!
        som_transicao.play()
    except pygame.error:
        print("Aviso: Não foi possível tocar o som de transição da Fase 1")

    audio.tocar_musica_fase("assets/sons/fase_1 music.mp3",
                            volume=volume_musica_real)  # <--- Agora obedece o volume do Menu!

    # --- PARALLAX BACKGROUND ---
    try:
        bg_floresta = pygame.image.load("assets/Lamora HR.png").convert()
        bg_floresta = pygame.transform.scale(bg_floresta,
                                             (int(bg_floresta.get_width() * (c.ALTURA / bg_floresta.get_height())),
                                              c.ALTURA))
        largura_bg = bg_floresta.get_width()

        # Camada 1: Nuvens (Fundo bem distante) - Carrega a imagem real
        bg_nuvens = pygame.image.load("assets/clouds.png").convert_alpha()
        bg_nuvens = pygame.transform.scale(bg_nuvens,
                                           (int(bg_nuvens.get_width() * (c.ALTURA / bg_nuvens.get_height())), c.ALTURA))
        largura_nuvens = bg_nuvens.get_width()

        # Camada 2: Floresta distante (Silhuetas) - Carrega a imagem real
        bg_silhuetas = pygame.image.load("assets/trees.png").convert_alpha()
        bg_silhuetas = pygame.transform.scale(bg_silhuetas,
                                              (int(bg_silhuetas.get_width() * (c.ALTURA / bg_silhuetas.get_height())),
                                               c.ALTURA))
        largura_silhuetas = bg_silhuetas.get_width()

    except FileNotFoundError:
        # Fallback SE os arquivos não existirem
        bg_floresta = pygame.Surface((c.LARGURA, c.ALTURA))
        bg_floresta.fill((25, 25, 40))
        largura_bg = c.LARGURA

        bg_nuvens = pygame.Surface((c.LARGURA, c.ALTURA))
        bg_nuvens.fill((0, 0, 0, 0))
        largura_nuvens = c.LARGURA

        bg_silhuetas = pygame.Surface((c.LARGURA, c.ALTURA))
        bg_silhuetas.fill((0, 0, 0, 0))
        largura_silhuetas = c.LARGURA

    # --- FUNÇÃO AUXILIAR PARA RECORTAR APENAS UMA ÁRVORE DO SPRITESHEET ---
    def carregar_uma_arvore(caminho_asset):
        img_original = pygame.image.load(caminho_asset).convert_alpha()
        # Divide a largura total por 8 para pegar apenas o primeiro frame da tira
        largura_frame = img_original.get_width() // 8
        altura_frame = img_original.get_height()
        subsurface_arvore = img_original.subsurface(pygame.Rect(0, 0, largura_frame, altura_frame))
        return pygame.transform.scale(subsurface_arvore, (160, 220))  # Escala imponente para o jogo

    try:
        arvore1_img = carregar_uma_arvore("assets/Tree1.png")
        arvore2_img = carregar_uma_arvore("assets/Tree2.png")
    except FileNotFoundError:
        arvore1_img = arvore2_img = pygame.Surface((160, 220))
        arvore1_img.fill((30, 120, 30))

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
    grupo_efeitos = pygame.sprite.Group()

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
    criar_montanha(x_inicio=1200, largura_blocos=8, altura_blocos=3, grupo_colisao=grupo_plataformas,
                   grupo_decoracao=grupo_decoracao_fundo, bloco_classe=Plataforma)
    criar_montanha(x_inicio=2800, largura_blocos=12, altura_blocos=5, grupo_colisao=grupo_plataformas,
                   grupo_decoracao=grupo_decoracao_fundo, bloco_classe=Plataforma)
    criar_montanha(x_inicio=4500, largura_blocos=6, altura_blocos=2, grupo_colisao=grupo_plataformas,
                   grupo_decoracao=grupo_decoracao_fundo, bloco_classe=Plataforma)
    criar_montanha(x_inicio=4740, largura_blocos=10, altura_blocos=4, grupo_colisao=grupo_plataformas,
                   grupo_decoracao=grupo_decoracao_fundo, bloco_classe=Plataforma)

    # --- LEVEL DESIGN: POSIÇÃO DOS INIMIGOS ---
    inimigos_fase = [
        Necromante(1350, c.ALTURA - 50 - 120 - 80),
        BringerOfDeath(1800, c.ALTURA - 195),
        BringerOfDeath(2400, c.ALTURA - 195),
        BringerOfDeath(2900, c.ALTURA - 50 - 200 - 140),
        Necromante(3100, c.ALTURA - 50 - 200 - 80),
        Necromante(5200, c.ALTURA - 195),
        BringerOfDeath(6000, c.ALTURA - 195),
        Necromante(6400, c.ALTURA - 195)
    ]
    grupo_inimigos.add(*inimigos_fase)

    # =========================================================================
    # 🏰 CRIAÇÃO DO CASTELO NO FIM DA FASE 1
    # =========================================================================
    # Como a fase tem COMPRIMENTO_FASE = 7000 e o castelo tem 960px de largura,
    # posicionamos ele em X = 6040 para que a parede direita termine cravada em 7000!
    # O chão fica em c.ALTURA - 50 (550). Como o castelo tem 540 de altura, ele começa em Y = 10.
    castelo_final = Decoracao(
        x=COMPRIMENTO_FASE - 960,
        y=c.ALTURA - 1 - 540,
        nome_asset="HR_Dark Gothic Castle_Sprite.png",
        escala=(960, 540)
    )
    grupo_decoracao_fundo.add(castelo_final)

    # --- LEVEL DESIGN VISUAL: GERADOR DE AMBIENTAÇÃO AUTOMÁTICA ---
    # 1. Nuvens flutuando no céu com velocidades variadas
    for x_nuvem in range(100, COMPRIMENTO_FASE, 450):
        if random.random() > 0.3:
            arquivo_nuvem = random.choice([f"Clouds_0{i}.png" for i in range(1, 9)])
            vel_random = random.uniform(0.05, 0.18)
            grupo_decoracao_fundo.add(
                Nuvem(x_nuvem, random.randint(30, 140), arquivo_nuvem, (130, 65), velocidade=vel_random)
            )

    # 2. Distribuição de moitas, pedras, tocos e ossos pelo chão principal (Com checagem de altura)
    assets_moitas_fundo = ["07.png", "08.png", "09.png", "10.png", "11.png"]
    assets_moitas_frente = ["Bushe1.png", "Bushe2.png", "Bushe3.png", "Bushe4.png"]
    assets_pedras = ["Rock1.png", "Rock2.png", "Rock3.png", "Rock4.png"]
    assets_detalhes = ["14.png", "15.png", "16.png", "17.png", "Stump 1.png", "Stump 2.png"]

    x_atual = 60
    while x_atual < COMPRIMENTO_FASE - 200:
        # --- DETECTOR DE ALTURA DINÂMICO APERFEIÇOADO ---
        chao_atual_y = c.ALTURA - 50

        # Guardaremos as plataformas que cruzam este X
        plataformas_no_x = []
        for plat in grupo_plataformas:
            if plat.rect.left <= x_atual <= plat.rect.right:
                plataformas_no_x.append(plat)

        # Se houver plataformas neste ponto, precisamos decidir se é uma montanha ou algo flutuante
        if plataformas_no_x:
            # Encontramos a plataforma mais alta (menor valor de Y)
            mais_alta = min(plataformas_no_x, key=lambda p: p.rect.y)

            # SE a plataforma mais alta estiver muito longe do chão (ex: Y menor que 450)
            # e não houver blocos embaixo dela, ela é uma plataforma suspensa (Aérea).
            # Nesse caso, ignoramos ela para que a vegetação nasça no chão!
            if mais_alta.rect.y < 450 and len(plataformas_no_x) == 1:
                chao_atual_y = c.ALTURA - 50  # Mantém no chão principal
            else:
                chao_atual_y = mais_alta.rect.y  # É uma montanha maciça, pode subir o chão!

        sorteio = random.random()

        # --- CAMADA DE ÁRVORES MAIS DENSA ---
        # Aumentamos a chance de 0.15 para 0.35 para nascerem muito mais árvores
        if sorteio < 0.35:
            if chao_atual_y == c.ALTURA - 50:
                img_escolhida = random.choice([arvore1_img, arvore2_img])
                nova_arvore = Decoracao(x_atual, chao_atual_y - 220, "Tree1.png", (160, 220))
                nova_arvore.image = img_escolhida
                grupo_decoracao_fundo.add(nova_arvore)

                # Diminuímos o pulo de 180 para 85 pixels.
                # Como a árvore tem 160 de largura, elas vão se sobrepor parcialmente,
                # criando aquele efeito de floresta profunda e realista!
                x_atual += 85
                continue

        elif sorteio < 0.50:  # Ajustado os limites para manter o equilíbrio dos outros objetos
            img = random.choice(assets_moitas_fundo)
            grupo_decoracao_fundo.add(Decoracao(x_atual, chao_atual_y - 45, img, (64, 48)))

        elif sorteio < 0.60:
            img = random.choice(assets_moitas_frente)
            grupo_decoracao_frente.add(Decoracao(x_atual, chao_atual_y - 25, img, (48, 28)))

        elif sorteio < 0.75:
            img = random.choice(assets_pedras)
            grupo_decoracao_frente.add(Decoracao(x_atual, chao_atual_y - 28, img, (38, 30)))

        elif sorteio < 0.85:
            img = random.choice(assets_detalhes)
            tam = (48, 48) if "16" in img or "17" in img else (32, 32)
            grupo_decoracao_fundo.add(Decoracao(x_atual, chao_atual_y - tam[1], img, tam))

        # Diminuímos o passo geral para o mapa ter decoração em quase todos os cantos
        x_atual += random.randint(40, 120)

    # 3. Detalhes em cima das plataformas suspensas
    for plat in plataformas_fase:
        if random.random() > 0.4:
            grupo_decoracao_fundo.add(
                Decoracao(plat.rect.x + 15, plat.rect.y - 25, random.choice(assets_moitas_frente), (40, 28)))
        if random.random() > 0.5:
            grupo_decoracao_frente.add(
                Decoracao(plat.rect.right - 45, plat.rect.y - 25, random.choice(assets_pedras), (32, 26)))

    jogador = Cavaleiro(x=150, y=100, grupo_efeitos=grupo_efeitos)
    jogador.grupo_efeitos_ref = grupo_efeitos  # Dá ao jogador acesso ao grupo de efeitos

    banner_objetivo = BannerObjetivo("Defeat all enemies", config_audio)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # 🎯 Se apertar ESC, entra no sub-loop de Pause
                if evento.key == pygame.K_ESCAPE:
                    fundo_congelado = tela.copy()
                    resultado_pause = interagir_pause(tela, fundo_congelado, audio)

                    # Se clicou em QUIT na tela de pause, encerra esta fase e retorna pro menu
                    if resultado_pause == "quit":
                        rodando = False
                        return "voltou_pro_menu"

        # --- LÓGICA DE ATUALIZAÇÃO DO JOGADOR ---
        jogador.update(grupo_plataformas, audio)

        if jogador.fim_animacao_morte:
            # 🎬 Faz um efeito suave de Fade-Out apagando o cenário aos poucos
            for alpha in range(0, 255, 5):
                fade_surf = pygame.Surface((c.LARGURA, c.ALTURA))
                fade_surf.fill((0, 0, 0))
                fade_surf.set_alpha(alpha)
                tela.blit(fade_surf, (0, 0))
                pygame.display.flip()
                pygame.time.delay(10)

            # Abre o menu de Game Over
            resultado_go = exibir_game_over(tela, config_audio)

            if resultado_go == "restart":
                return "reiniciar_fase"
            else:
                return "voltou_pro_menu"

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

        # --- CHECAGEM DE PROGRESSÃO (ENTRADA DO CASTELO GÓTICO) ---
        if jogador.rect.colliderect(castelo_final.rect):
            # Quando o jogador passar do meio do castelo (onde fica o portão principal)
            # E todos os inimigos da fase estiverem derrotados:
            if jogador.rect.centerx >= castelo_final.rect.centerx and len(grupo_inimigos) == 0:
                print("Adentrando os portões do castelo... Iniciando a Boss Battle!")
                pygame.mixer.music.stop()
                rodando = False
                return jogador  # Retorna o jogador avançando para a Arena!

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

        grupo_efeitos.update()

        # Atualiza o comportamento do banner
        banner_objetivo.update()

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

                        if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
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
                        if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                            audio.tocar_sfx_player("escudo_1")
                            audio.tocar_sfx_player("escudo_2")
                    else:
                        print("Dano: Cavaleiro atingido pela Bola de Fogo!")
                        jogador.tomar_dano(20, audio=audio)

                        # --- ADICIONA A EXPLOSÃO DE FOGO ---
                        from efeitos import Efeito  # Garanta que está importado no principal.py também
                        explosao_fogo = Efeito(jogador.rect.centerx, jogador.rect.centery, "Fire_01.png", qtd_frames=8,
                                               escala= 1, velocidade_animacao=60)
                        grupo_efeitos.add(explosao_fogo)
                    magia.kill()  # Some com a bola de fogo

                # --- CASO 2: EXPLOSÃO DO CHÃO (Indefensável) ---
                elif nome_classe == "ExplosaoNecromante":
                    # Deixamos a própria classe controlar o dano e o som através do update dela
                    pass

                # --- CASO ZERO: Fallback de segurança ---
                else:
                    if jogador.defendendo:
                        if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
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
                                if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
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
                    if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                        audio.tocar_sfx_player("comer")

                item.kill()  # Faz o bife sumir do mapa

        # --- RENDERIZAÇÃO COM DESLOCAMENTO (PROJEÇÃO DA CÂMERA) ---
        tela.fill(c.PRETO)

        # Camada 0A: O seu fundo original (Lamora HR)
        scroll_fundo = (scroll_camera * 0.1) % largura_bg
        tela.blit(bg_floresta, (-scroll_fundo, 0))
        tela.blit(bg_floresta, (largura_bg - scroll_fundo, 0))

        # Camada 0B: Parallax das Nuvens Novas com Cobertura Total
        scroll_nuvens = (scroll_camera * 0.2) % largura_nuvens
        pos_x_nuvens = -scroll_nuvens - largura_nuvens
        while pos_x_nuvens < c.LARGURA:
            tela.blit(bg_nuvens, (pos_x_nuvens, 0))
            pos_x_nuvens += largura_nuvens

        # Camada 0C: CÁLCULO DE COBERTURA TOTAL PARA AS SILHUETAS
        ponto_ancora = int(scroll_camera * 0.45)
        offset_silhueta = ponto_ancora % largura_silhuetas

        # Começamos a desenhar um bloco antes da tela para garantir a emenda na esquerda
        pos_x_desenho = -offset_silhueta - largura_silhuetas

        # O laço preenche a tela da esquerda para a direita até passar do limite visível
        while pos_x_desenho < c.LARGURA:
            tela.blit(bg_silhuetas, (pos_x_desenho, 0))
            pos_x_desenho += largura_silhuetas

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
        jogador.rect = rect_original_jogador

        for ef in grupo_efeitos:
            rect_p = ef.rect.move(-scroll_camera, 0)
            tela.blit(ef.image, rect_p)

        # Camada 6: DECORAÇÕES DE FRENTE (Matinhos e pedras que cobrem o pé do jogador)
        for dec in grupo_decoracao_frente:
            rect_p = dec.rect.move(-scroll_camera, 0)
            tela.blit(dec.image, rect_p)

        # Desenha o Banner de Objetivo se ele não tiver terminado
        if banner_objetivo.estado != "fim":
            banner_objetivo.draw(tela)

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

def rodar_arena(jogador_fase1=None, config_audio=None):
    pygame.init()
    tela = pygame.display.set_mode((c.LARGURA, c.ALTURA))
    pygame.display.set_caption("Ironclad Quest")
    relogio = pygame.time.Clock()

    # --- SISTEMA DE ÁUDIO ---
    audio = GerenciadorSons()
    # --- REGISTRO EXCLUSIVO DOS SONS DO ESCUDO E MOVIMENTOS DO BOSS FINAL ---
    caminho_player = "assets/player/"
    caminho_monster = "assets/monster/"  # 🎯 Nova pasta adicionada

    try:
        # (Sons do escudo que você já tem...)
        som1 = pygame.mixer.Sound(f"{caminho_player}som escudo 1.mp3")
        som1.set_volume(0.6)
        audio.sfx_player["som escudo 1"] = som1

        som2 = pygame.mixer.Sound(f"{caminho_player}som escudo 2.mp3")
        som2.set_volume(0.6)
        audio.sfx_player["som escudo 2"] = som2

        # 🎯 INJEÇÃO DOS NOVOS SONS DO BOSS FINAL
        audio.sfx_player["boss_hit"] = pygame.mixer.Sound(f"{caminho_monster}boss hit 1.mp3")
        audio.sfx_player["boss_hit"].set_volume(0.5)

        audio.sfx_player["boss_miss"] = pygame.mixer.Sound(f"{caminho_monster}boss no hit.mp3")
        audio.sfx_player["boss_miss"].set_volume(0.4)

        audio.sfx_player["boss_pain"] = pygame.mixer.Sound(f"{caminho_monster}monstro boss pain.mp3")
        audio.sfx_player["boss_pain"].set_volume(0.6)

        audio.sfx_player["boss_asa1"] = pygame.mixer.Sound(f"{caminho_monster}boss asas 1.mp3")
        audio.sfx_player["boss_asa1"].set_volume(0.3)

        audio.sfx_player["boss_asa2"] = pygame.mixer.Sound(f"{caminho_monster}boss asas 2.mp3")
        audio.sfx_player["boss_asa2"].set_volume(0.3)

        print("Sons do Boss Final carregados com sucesso!")
    except (pygame.error, FileNotFoundError) as e:
        print(f"Aviso: Erro ao carregar sons do Boss: {e}")
        # Fallbacks de segurança para não quebrar o jogo caso falte arquivo
        for chave in ["boss_hit", "boss_miss", "boss_pain", "boss_asa1", "boss_asa2"]:
            audio.sfx_player[chave] = None

    # Recupera volumes do menu
    v_geral, v_musica, v_sfx = 1.0, 0.6, 0.8
    if config_audio:
        v_geral = config_audio["vol_geral"]
        v_musica = config_audio["vol_musica"]
        v_sfx = config_audio["vol_sfx"]

    volume_musica_real = v_musica * v_geral
    volume_sfx_real = v_sfx * v_geral

    audio.tocar_musica_fase("assets/sons/boss music.mp3", volume=volume_musica_real)

    # 🎯 Toca o som épico de transição ao entrar na Arena do Boss com volume certo!
    try:
        som_transicao_boss = pygame.mixer.Sound("assets/sons/transição de fase.mp3")
        som_transicao_boss.set_volume(volume_sfx_real)
        som_transicao_boss.play()
    except pygame.error:
        print("Aviso: Não foi possível tocar o som de transição na Arena")

    # --- CARREGAMENTO DOS 4 LAYERS DA ARENA (FIXOS) ---
    try:
        bg1 = pygame.transform.scale(pygame.image.load("assets/background.png").convert(), (c.LARGURA, c.ALTURA))
        bg2 = pygame.transform.scale(pygame.image.load("assets/background2.png").convert_alpha(), (c.LARGURA, c.ALTURA))
        bg3 = pygame.transform.scale(pygame.image.load("assets/background3.png").convert_alpha(), (c.LARGURA, c.ALTURA))
        bg4 = pygame.transform.scale(pygame.image.load("assets/background4.png").convert_alpha(), (c.LARGURA, c.ALTURA))

        # --- RECORTE COPIADO DO SEU PADRÃO ---
        textura_arena = pygame.image.load("assets/Tilemap_Elevation.png").convert_alpha()

        # Área do bloco dentro do arquivo PNG
        area_recorte = pygame.Rect(48, 55, 48, 48)
        bloco_recortado = textura_arena.subsurface(area_recorte)

        # Repetição do bloco (Tiling)
        textura_chao = pygame.Surface((c.LARGURA, 50), pygame.SRCALPHA)
        for x in range(0, c.LARGURA, 48):
            textura_chao.blit(bloco_recortado, (x, 0))

        textura_plataforma = pygame.Surface((180, 32), pygame.SRCALPHA)
        for x in range(0, 180, 48):
            textura_plataforma.blit(bloco_recortado, (x, 0))

    except FileNotFoundError:
        bg1 = pygame.Surface((c.LARGURA, c.ALTURA))
        bg1.fill((40, 20, 20))
        bg2 = bg3 = bg4 = None
        textura_chao = textura_plataforma = None

    # --- GRUPOS DE SPRITES ---
    grupo_plataformas = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()
    grupo_magias = pygame.sprite.Group()
    grupo_itens = pygame.sprite.Group()
    grupo_efeitos = pygame.sprite.Group()

    # 1. Chão principal da arena
    chao_arena = Plataforma(0, c.ALTURA - 50, c.LARGURA, 50)
    if textura_chao:
        chao_arena.image = textura_chao
    grupo_plataformas.add(chao_arena)

    # 2. Duas plataformas simétricas na mesma altura
    altura_plataformas = c.ALTURA - 220
    largura_plat = 160
    alt_plat = 32

    plat_esquerda = Plataforma(40, altura_plataformas, largura_plat, alt_plat)
    plat_direita = Plataforma(c.LARGURA - 40 - largura_plat, altura_plataformas, largura_plat, alt_plat)

    if textura_plataforma:
        plat_esquerda.image = textura_plataforma
        plat_direita.image = textura_plataforma

    grupo_plataformas.add(plat_esquerda, plat_direita)

    # --- INICIALIZAÇÃO DOS PERSONAGENS ---
    if jogador_fase1:
        jogador = jogador_fase1
        jogador.rect.x = 100
        jogador.rect.y = c.ALTURA - 150
        jogador.grupo_efeitos_ref = grupo_efeitos
    else:
        jogador = Cavaleiro(x=100, y=c.ALTURA - 150, grupo_efeitos=grupo_efeitos)

    # --- INSTANCIAR O BOSS FINAL ---
    boss = BossDemonio(c.LARGURA // 2, c.ALTURA - 400)  # Ajustado Y para ficar numa altura boa de bater
    grupo_inimigos.add(boss)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # 🎯 Se apertar ESC durante o boss, congela a luta
                if evento.key == pygame.K_ESCAPE:
                    fundo_congelado = tela.copy()
                    resultado_pause = interagir_pause(tela, fundo_congelado, audio)

                    # Se escolheu voltar para o menu
                    if resultado_pause == "quit":
                        rodando = False
                        return "voltou_pro_menu"

        # --- ATUALIZAÇÃO ---
        jogador.update(grupo_plataformas, audio, tipo_chao="pedra")

        if jogador.fim_animacao_morte:
            # 🎬 Faz um efeito suave de Fade-Out apagando o cenário aos poucos
            for alpha in range(0, 255, 5):
                fade_surf = pygame.Surface((c.LARGURA, c.ALTURA))
                fade_surf.fill((0, 0, 0))
                fade_surf.set_alpha(alpha)
                tela.blit(fade_surf, (0, 0))
                pygame.display.flip()
                pygame.time.delay(10)

            # Abre o menu de Game Over
            resultado_go = exibir_game_over(tela, config_audio)

            if resultado_go == "restart":
                return "reiniciar_fase"
            else:
                return "voltou_pro_menu"

        # Barreiras físicas das paredes da Arena (Cenário Fixo)
        if jogador.rect.left < 0:
            jogador.rect.left = 0
        if jogador.rect.right > c.LARGURA:
            jogador.rect.right = c.LARGURA

        # MODIFICADO: Atualização do Boss com os novos parâmetros exigidos pelo novo boss.py
        boss.update(grupo_plataformas, jogador, grupo_magias, grupo_efeitos, audio)

        # Atualização dos demais grupos
        grupo_magias.update(grupo_plataformas, jogador, grupo_magias, grupo_efeitos, audio)
        grupo_efeitos.update()

        # --- NOVO: SISTEMA DE COLISÕES E COMBATE ---

        # 1. Cavaleiro atacando o Boss
        if hasattr(jogador, 'atacando') and jogador.atacando:
            if hasattr(jogador, 'rect_ataque') and jogador.rect_ataque.colliderect(boss.rect):
                if not boss.morto and boss.timer_invulneravel == 0 and boss.estado_atual != "retreat":
                    boss.tomar_dano(15)

                    if audio and not boss.morto:  # Só toca dor se ele não morreu
                        if audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                            audio.tocar_sfx_player("boss_pain")

                    # Se o golpe matou o boss neste frame, spawna a grande explosão!
                    if boss.morto:
                        # Spawna a animação usando o seu arquivo "boss morte.png" (8 frames)
                        explosao_morte = Efeito(
                            boss.rect.centerx, boss.rect.centery,
                            "boss morte.png", qtd_frames=8, escala=4, velocidade_animacao=30
                        )
                        grupo_efeitos.add(explosao_morte)
                    else:
                        hit_visual = Efeito(boss.rect.centerx, boss.rect.centery, "Boss hit.png", 3, escala=2,
                                            velocidade_animacao=40)
                        grupo_efeitos.add(hit_visual)

        # 2. Projéteis do Boss (Sopro Azul) acertando o Cavaleiro
        colisoes_magia = pygame.sprite.spritecollide(jogador, grupo_magias, True)
        for magia in colisoes_magia:
            # Verifica se o jogador está ativo defendendo
            if hasattr(jogador, 'defendendo') and jogador.defendendo:
                dano_final = magia.dano // 3
                jogador.tomar_dano(dano_final)

                # 🔊 ALTERADO AQUI: Toca os dois arquivos simultaneamente para somar os áudios
                if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                    audio.tocar_sfx_player("som escudo 1")
                    audio.tocar_sfx_player("som escudo 2")

                # Instancia a animação de colisão no escudo (11 frames)
                efeito_defend = Efeito(
                    jogador.rect.centerx,
                    jogador.rect.centery,
                    "DemonAttackBreath DEFEND.png",
                    qtd_frames=10,
                    escala=2,
                    velocidade_animacao=40
                )
                grupo_efeitos.add(efeito_defend)

            else:  # 🎯 CORRIGIDO: Agora alinhado perfeitamente com o "if hasattr"
                # Caso seja atingido sem escudo ativo (Efeito normal de Hit)
                jogador.tomar_dano(magia.dano, audio=audio)
                efeito_sopro_hit = Efeito(
                    jogador.rect.centerx,
                    jogador.rect.centery,
                    "DemonAttackBreath hit.png",
                    qtd_frames=8,
                    escala=2,
                    velocidade_animacao=50
                )
                grupo_efeitos.add(efeito_sopro_hit)

        # 3. Ataque Físico/Corpo a Corpo do Boss (Quando ele usa a animação 'attack')
        if boss.estado_atual == "attack" and int(boss.frame_atual) == 6:  # Frame exato do golpe
            if boss.rect.colliderect(jogador.rect):
                dano_fisico = 10
                if hasattr(jogador, 'defendendo') and jogador.defendendo:
                    dano_fisico = 2
                    if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                        audio.tocar_sfx_player("som escudo 1")
                        audio.tocar_sfx_player("som escudo 2")
                else:
                    jogador.tomar_dano(dano_fisico, audio=audio)

                # 🎯 ADICIONADO AQUI: Som do boss acertando o golpe de perto
                if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                    audio.tocar_sfx_player("boss_hit")
            else:
                # 🎯 ADICIONADO AQUI: Se ele atacou no frame correto mas o jogador desviou, toca o vento do golpe (miss)
                # Usamos uma trava simples para tocar apenas uma vez por ataque
                if audio and not getattr(boss, "som_miss_tocado", False):
                    if audio and audio.__class__.vol_sfx > 0 and audio.__class__.vol_geral > 0:
                        audio.tocar_sfx_player("boss_miss")
                    boss.som_miss_tocado = True

        # Reseta a trava do som de erro quando ele sai do estado de ataque
        if boss.estado_atual != "attack":
            boss.som_miss_tocado = False

        # --- RENDERIZAÇÃO ---
        if bg2:
            tela.blit(bg1, (0, 0))
            tela.blit(bg2, (0, 0))
            tela.blit(bg3, (0, 0))
            tela.blit(bg4, (0, 0))
        else:
            tela.blit(bg1, (0, 0))

        # Desenhar as plataformas
        for plat in grupo_plataformas:
            tela.blit(plat.image, plat.rect)

        # Desenhar Entidades
        for inimigo in grupo_inimigos:
            inimigo.draw_custom(tela)

        for magia in grupo_magias:
            tela.blit(magia.image, magia.rect)

        jogador.draw_custom(tela)

        for ef in grupo_efeitos:
            tela.blit(ef.image, ef.rect)

        # =========================================================================
        # 🎯 HUD: RENDERIZAÇÃO DA BARRA DO BOSS NA FRENTE DE TUDO (E SEM COLISÃO)
        # =========================================================================
        if hasattr(boss, 'barra_base') and boss.barra_base:
            porcentagem = max(0, boss.vida_atual / boss.vida_max)

            # Seus valores calibrados com perfeição!
            LARGURA_MOLDURA_DESEJADA = 700
            ALTURA_MOLDURA_DESEJADA = 50

            LARGURA_VERMELHO_REAL = 208
            OFFSET_X_INTERNO = -5
            OFFSET_Y_INTERNO = 13
            ALTURA_MASCARA_ESCURA = 20
            COR_DO_VAO_INTERNO = (34, 18, 22)

            # Redimensiona o asset puxando a imagem guardada no boss
            barra_esticada = pygame.transform.scale(
                boss.barra_base,
                (LARGURA_MOLDURA_DESEJADA, ALTURA_MOLDURA_DESEJADA)
            )

            x_barra = (c.LARGURA - LARGURA_MOLDURA_DESEJADA) // 2
            y_barra = c.ALTURA - ALTURA_MOLDURA_DESEJADA - 5

            # Desenha a moldura por cima do Cavaleiro e dos efeitos
            tela.blit(barra_esticada, (x_barra, y_barra))

            # Desenha a máscara por cima se houver dano
            if porcentagem < 1.0:
                offset_automatico_x = (LARGURA_MOLDURA_DESEJADA - LARGURA_VERMELHO_REAL) // 2
                largura_vida_perdida = int(LARGURA_VERMELHO_REAL * (1.0 - porcentagem))

                if largura_vida_perdida > 0:
                    x_escuro = x_barra + offset_automatico_x + (
                                LARGURA_VERMELHO_REAL - largura_vida_perdida) + OFFSET_X_INTERNO
                    y_escuro = y_barra + OFFSET_Y_INTERNO

                    pygame.draw.rect(
                        tela,
                        COR_DO_VAO_INTERNO,
                        (x_escuro, y_escuro, largura_vida_perdida, ALTURA_MASCARA_ESCURA)
                    )

        # HUD de Vida fixa
        pos_x_inicial, pos_y, tamanho_coracao, espacamento = 20, 20, 24, 30
        for i in range(5):
            vida_necessaria = (i + 1) * 20
            coracao_cheio = jogador.vida_atual >= vida_necessaria
            desenhar_coracao(tela, pos_x_inicial + (i * espacamento), pos_y, tamanho_coracao, preenchido=coracao_cheio)

        # =========================================================================
        # 🎬 EFEITOS VISUAIS DE MORTE DO BOSS (PISCAR + ESCURECER TELA)
        # =========================================================================
        if boss.morto:
            # 1. Efeito de piscar em preto e branco (alterna a cada 5 frames nos primeiros 60 frames)
            if boss.timer_morte < 60:
                if (boss.timer_morte // 5) % 2 == 0:
                    # Cria um flash branco semi-transparente cobrindo o jogo
                    flash = pygame.Surface((c.LARGURA, c.ALTURA))
                    flash.fill((255, 255, 255))
                    flash.set_alpha(100)  # Intensidade do branco
                    tela.blit(flash, (0, 0))
                else:
                    # Cria o flash preto alternado (Efeito estroboscópico de cinema)
                    flash = pygame.Surface((c.LARGURA, c.ALTURA))
                    flash.fill((0, 0, 0))
                    flash.set_alpha(130)
                    tela.blit(flash, (0, 0))

            # 2. Efeito de escurecimento total (Fade Out) após os flashes (dos frames 60 a 150)
            elif boss.timer_morte >= 60:
                # Calcula a opacidade escura crescendo gradualmente até 255 (totalmente preto)
                progresso_fade = min(255, int((boss.timer_morte - 60) * 2.8))

                filtro_escuro = pygame.Surface((c.LARGURA, c.ALTURA))
                filtro_escuro.fill((0, 0, 0))
                filtro_escuro.set_alpha(progresso_fade)
                tela.blit(filtro_escuro, (0, 0))

                # Se a tela ficou totalmente escura, para a música e encerra/reinicia a arena
                if progresso_fade >= 255:
                    pygame.mixer.music.stop()
                    # Aqui você pode chamar uma tela de vitória futuramente!
                    rodando = False
                    # =========================================================================

        pygame.display.flip()
        relogio.tick(c.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    while True:
        config_audio = rodar_menu()

        # --- LOOP INTERNO DA FASE 1 (Permite restarts) ---
        while True:
            resultado_fase1 = rodar_jogo(config_audio)

            if resultado_fase1 == "reiniciar_fase":
                continue  # Reinicia a fase 1 limpando tudo!
            elif resultado_fase1 == "voltou_pro_menu":
                break  # Quebra o laço e volta pro Menu Principal

            # Se não foi nenhum dos dois, o jogador passou de fase!
            jogador_avancando = resultado_fase1

            # --- LOOP INTERNO DA ARENA (Permite restarts) ---
            resultado_arena = None
            while True:
                resultado_arena = rodar_arena(jogador_avancando, config_audio)
                if resultado_arena == "reiniciar_fase":
                    continue  # Reinicia apenas a Arena do Boss!
                break

            if resultado_arena == "voltou_pro_menu":
                break