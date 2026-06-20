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
            "boss_morte": "monstro boss death.mp3",
            "bringer_ataque": "monstro 1 hit.mp3",
            "bringer_dor": "monstro 1 pain.mp3",  # <--- NOVO
            "bringer_morte": "monstro 1 death.mp3",
            "necroman_fogo": "fire ball.mp3",  # <--- Nome corrigido aqui
            "necroman_explosao": "necromancer attack 2.mp3",
            "necroman_dor": "monstro 2 pain.mp3",  # <--- NOVO
            "necroman_morte": "monstro 2 death.mp3"
        }

        # 🎯 AGORA CARREGA OS DOIS: Passos de Terra e Passos de Pedra
        for i in range(1, 9):
            sons_para_carregar[f"passo_terra_{i}"] = f"stepdirt_{i}.mp3"
            sons_para_carregar[f"passo_pedra_{i}"] = f"stepstone_{i}.mp3"

            # --- CARREGAMENTO INTELIGENTE ---
            for chave, nome_arquivo in sons_para_carregar.items():
                # Se for hit do jogador contra o monstro, força a pasta do player
                if chave in ["hit_bringer", "hit_necromancer"]:
                    caminho_final = f"{caminho_player}{nome_arquivo}"
                # 🎯 CORRIGIDO: Se a chave tiver "bringer", "necroman" OU "boss", vai para a pasta monster!
                elif "bringer" in chave or "necroman" in chave or "boss" in chave:
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

        if self.sfx_player.get("boss_morte"):
            self.sfx_player["boss_morte"].set_volume(0.8)

    def tocar_sfx_player(self, chave):
        """Toca um som do jogador ou monstro com base na chave informada"""
        som = self.sfx_player.get(chave)
        if som:
            som.play()

    def tocar_passo_aleatorio(self, tipo_chao="terra"):
        import random
        num_aleatorio = random.randint(1, 8)

        # Define a chave correta com base no cenário
        if tipo_chao == "pedra":
            chave_passo = f"passo_pedra_{num_aleatorio}"
        else:
            chave_passo = f"passo_terra_{num_aleatorio}"

        # 🔊 CANAL DE ÁUDIO 1: Para os passos físicos
        if chave_passo in self.sfx_player and self.sfx_player[chave_passo]:
            som_passo = self.sfx_player[chave_passo]
            som_passo.set_volume(0.15)  # Um tiquinho mais alto para escutar bem

            # Pega o Canal 1 do mixer para tocar o passo (evita misturar)
            pygame.mixer.Channel(1).play(som_passo)

        # 🔊 CANAL DE ÁUDIO 2: Para o chacoalhar da armadura
        if "armadura" in self.sfx_player and self.sfx_player["armadura"]:
            som_armadura = self.sfx_player["armadura"]
            som_armadura.set_volume(0.08)  # Deixa a armadura sutil no fundo

            # Pega o Canal 2 do mixer apenas para a armadura
            pygame.mixer.Channel(2).play(som_armadura)

    def tocar_musica_fase(self, caminho_musica, volume=0.2):
        """Carrega e toca a música de fundo em loop infinito"""
        try:
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            print(f"Música {caminho_musica} iniciada com sucesso!")
        except (pygame.error, FileNotFoundError):
            print(f"Erro: Não foi possível carregar a música em: {caminho_musica}")