import pygame


class GerenciadorSons:
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
            "bringer_ataque": "monstro 1 hit.mp3",
            "bringer_dor": "monstro 1 pain.mp3",  # <--- NOVO
            "bringer_morte": "monstro 1 death.mp3",
            "necroman_fogo": "fire ball.mp3",  # <--- Nome corrigido aqui
            "necroman_explosao": "necromancer attack 2.mp3",
            "necroman_dor": "monstro 2 pain.mp3",  # <--- NOVO
            "necroman_morte": "monstro 2 death.mp3"
        }

        # Adiciona os 8 passos dinamicamente para poupar código:
        for i in range(1, 9):
            sons_para_carregar[f"passo_{i}"] = f"stepdirt_{i}.mp3"

            # --- CARREGAMENTO INTELIGENTE ---
            for chave, nome_arquivo in sons_para_carregar.items():
                # Se for hit do jogador contra o monstro, força a pasta do player
                if chave in ["hit_bringer", "hit_necromancer"]:
                    caminho_final = f"{caminho_player}{nome_arquivo}"
                # Define a pasta correta baseada na chave do som para os demais
                elif "bringer" in chave or "necroman" in chave:
                    caminho_final = f"{caminho_monster}{nome_arquivo}"
                else:
                    caminho_final = f"{caminho_player}{nome_arquivo}"

                try:
                    som = pygame.mixer.Sound(caminho_final)
                    som.set_volume(0.4)  # Volume padrão para os cortes
                    self.sfx_player[chave] = som
                except (pygame.error, FileNotFoundError):
                    print(f"Aviso: Não foi possível carregar o som: {caminho_final}")
                    self.sfx_player[chave] = None

        # --- AJUSTES DE VOLUMES ESPECÍFICOS (Agora após o carregamento real) ---
        if self.sfx_player.get("pulo"):
            self.sfx_player["pulo"].set_volume(0.4)

        if self.sfx_player.get("dor"):
            self.sfx_player["dor"].set_volume(0.4)

        if self.sfx_player.get("bringer_ataque"):
            self.sfx_player["bringer_ataque"].set_volume(0.7)

        if self.sfx_player.get("necroman_fogo"):
            self.sfx_player["necroman_fogo"].set_volume(0.6)

        if self.sfx_player.get("necroman_explosao"):
            self.sfx_player["necroman_explosao"].set_volume(0.6)

        if self.sfx_player.get("bringer_morte"):
            self.sfx_player["bringer_morte"].set_volume(0.7)


        if self.sfx_player.get("necroman_morte"):
            self.sfx_player["necroman_morte"].set_volume(0.7)

        if self.sfx_player.get("comer"):
            self.sfx_player["comer"].set_volume(0.5)

    def tocar_sfx_player(self, chave):
        """Toca um som do jogador ou monstro com base na chave informada"""
        som = self.sfx_player.get(chave)
        if som:
            som.play()

    def tocar_passo_aleatorio(self):
        import random
        # Escolhe um número de 1 a 8
        num_aleatorio = random.randint(1, 8)
        chave_passo = f"passo_{num_aleatorio}"

        # --- AJUSTE DE VOLUME DOS PASSOS (10% do volume original) ---
        if chave_passo in self.sfx_player:
            self.sfx_player[chave_passo].set_volume(0.1)

        # --- AJUSTE DE VOLUME DA ARMADURA (10% do volume original) ---
        if "armadura" in self.sfx_player:
            self.sfx_player["armadura"].set_volume(0.1)

        # Agora que estão baixinhos, toca os dois juntos!
        self.tocar_sfx_player(chave_passo)
        self.tocar_sfx_player("armadura")

    def tocar_musica_fase(self, caminho_musica, volume=0.2):
        """Carrega e toca a música de fundo em loop infinito"""
        try:
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            print(f"Música {caminho_musica} iniciada com sucesso!")
        except (pygame.error, FileNotFoundError):
            print(f"Erro: Não foi possível carregar a música em: {caminho_musica}")