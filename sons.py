import pygame

class GerenciadorSons:
    # 🎯 VARIÁVEIS ESTÁTICAS DE CLASSE: Compartilhadas por TODO O JOGO
    vol_geral = 1.0
    vol_musica = 0.6
    vol_sfx = 0.8

    def __init__(self):
        pygame.mixer.init()

        # --- DICIONÁRIO DE SONS DO JOGADOR E MONSTROS (SFX) ---
        self.sfx_player = {}
        caminho_player = "assets/player/"
        caminho_monster = "assets/monster/"

        sons_para_carregar = {
            "hit_bringer": "player hit 1.mp3",
            "hit_necromancer": "player hit 2.mp3",
            "hit_ar": "player hit air.mp3",
            "errou_1": "player no hit 1.mp3",
            "errou_2": "player no hit 2.mp3",
            "errou_ar": "player no hit air.mp3",
            "escudo_1": "som escudo 1.mp3",
            "escudo_2": "som escudo 2.mp3",
            "armadura": "armadura som.mp3",
            "pulo": "player jump.mp3",
            "dor": "painh.mp3",
            "comer": "food song.mp3",

            # --- SONS DOS MONSTROS ---
            "boss_morte": "monstro boss death.mp3",
            "bringer_ataque": "monstro 1 hit.mp3",
            "bringer_dor": "monstro 1 pain.mp3",
            "bringer_morte": "monstro 1 death.mp3",
            "necroman_fogo": "fire ball.mp3",
            "necroman_explosao": "necromancer attack 2.mp3",
            "necroman_dor": "monstro 2 pain.mp3",
            "necroman_morte": "monstro 2 death.mp3"
        }

        # 1. Primeiro adicionamos todos os passos ao dicionário
        for i in range(1, 9):
            sons_para_carregar[f"passo_terra_{i}"] = f"stepdirt_{i}.mp3"
            sons_para_carregar[f"passo_pedra_{i}"] = f"stepstone_{i}.mp3"

        # 2. AGORA SIM (Fora do laço anterior): Fazemos o carregamento inteligente uma única vez!
        for chave, nome_arquivo in sons_para_carregar.items():
            if chave in ["hit_bringer", "hit_necromancer"]:
                caminho_final = f"{caminho_player}{nome_arquivo}"
            elif "bringer" in chave or "necroman" in chave or "boss" in chave:
                caminho_final = f"{caminho_monster}{nome_arquivo}"
            else:
                caminho_final = f"{caminho_player}{nome_arquivo}"

            try:
                som = pygame.mixer.Sound(caminho_final)
                som.set_volume(0.4)  # Volume base
                self.sfx_player[chave] = som
            except (pygame.error, FileNotFoundError):
                print(f"Aviso: Não foi possível carregar o som: {caminho_final}")
                self.sfx_player[chave] = None

        # --- AJUSTES DE VOLUMES ESPECÍFICOS ---
        if self.sfx_player.get("pulo"): self.sfx_player["pulo"].set_volume(0.4)
        if self.sfx_player.get("dor"): self.sfx_player["dor"].set_volume(0.4)
        if self.sfx_player.get("bringer_ataque"): self.sfx_player["bringer_ataque"].set_volume(0.7)
        if self.sfx_player.get("necroman_fogo"): self.sfx_player["necroman_fogo"].set_volume(0.6)
        if self.sfx_player.get("necroman_explosao"): self.sfx_player["necroman_explosao"].set_volume(0.6)
        if self.sfx_player.get("bringer_morte"): self.sfx_player["bringer_morte"].set_volume(0.7)
        if self.sfx_player.get("necroman_morte"): self.sfx_player["necroman_morte"].set_volume(0.7)
        if self.sfx_player.get("comer"): self.sfx_player["comer"].set_volume(0.5)
        if self.sfx_player.get("boss_morte"): self.sfx_player["boss_morte"].set_volume(0.8)

    def atualizar_volumes(self, vol_geral, vol_sfx, vol_musica):
        """Método novo para quando você decidir sincronizar o menu com as fases"""
        self.vol_geral = vol_geral
        self.vol_sfx = vol_sfx
        self.vol_musica = vol_musica
        pygame.mixer.music.set_volume(self.vol_musica * self.vol_geral)

    def tocar_sfx_player(self, chave):
        """Toca um som multiplicando o volume padrão pelo volume do SFX global"""
        som = self.sfx_player.get(chave)
        if som:
            # Obtém o volume atual do som e multiplica pelas diretrizes do SFX/Geral
            vol_base = som.get_volume()
            som.set_volume(vol_base * GerenciadorSons.vol_sfx * GerenciadorSons.vol_geral)
            som.play()
            # Restaura o volume base para não estragar as próximas chamadas
            som.set_volume(vol_base)

    def tocar_passo_aleatorio(self, tipo_chao="terra"):
        import random
        num_aleatorio = random.randint(1, 8)

        if tipo_chao == "pedra":
            chave_passo = f"passo_pedra_{num_aleatorio}"
        else:
            chave_passo = f"passo_terra_{num_aleatorio}"

        # 🔊 CANAL DE ÁUDIO 1: Passos
        if chave_passo in self.sfx_player and self.sfx_player[chave_passo]:
            som_passo = self.sfx_player[chave_passo]
            vol_real_passo = 0.15 * self.vol_sfx * self.vol_geral
            som_passo.set_volume(vol_real_passo)
            pygame.mixer.Channel(1).play(som_passo)

        # 🔊 CANAL DE ÁUDIO 2: Armadura
        if "armadura" in self.sfx_player and self.sfx_player["armadura"]:
            som_armadura = self.sfx_player["armadura"]
            vol_real_armadura = 0.08 * self.vol_sfx * self.vol_geral
            som_armadura.set_volume(vol_real_armadura)
            pygame.mixer.Channel(2).play(som_armadura)

    def tocar_musica_fase(self, caminho_musica, volume=0.2):
        """Carrega e toca a música multiplicando pelo volume global"""
        try:
            pygame.mixer.music.load(caminho_musica)
            # Aplica a proporção correta baseada no volume d menu
            pygame.mixer.music.set_volume(volume * GerenciadorSons.vol_musica * GerenciadorSons.vol_geral)
            pygame.mixer.music.play(-1)
            print(f"Música {caminho_musica} iniciada com sucesso!")
        except (pygame.error, FileNotFoundError):
            print(f"Erro: Não foi possível carregar a música em: {caminho_musica}")