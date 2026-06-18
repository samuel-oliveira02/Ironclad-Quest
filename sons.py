import pygame


class GerenciadorSons:
    def __init__(self):
        pygame.mixer.init()

        # --- DICIONÁRIO DE SONS DO JOGADOR (SFX) ---
        self.sfx_player = {}
        caminho_player = "assets/player/"

        sons_para_carregar = {
            "hit_bringer": "player hit 1.mp3",
            "hit_necromancer": "player hit 2.mp3",
            "hit_ar": "player hit air.mp3",
            "errou_1": "player no hit 1.mp3",
            "errou_2": "player no hit 2.mp3",
            "errou_ar": "player no hit air.mp3",
            "escudo_1": "som escudo 1.mp3",
            "escudo_2": "som escudo 2.mp3"
        }

        for chave, nome_arquivo in sons_para_carregar.items():
            try:
                som = pygame.mixer.Sound(f"{caminho_player}{nome_arquivo}")
                som.set_volume(0.4)  # Volume padrão para os cortes
                self.sfx_player[chave] = som
            except (pygame.error, FileNotFoundError):
                print(f"Aviso: Não foi possível carregar o som: {caminho_player}{nome_arquivo}")
                self.sfx_player[chave] = None

    def tocar_sfx_player(self, chave):
        """Toca um som do jogador com base na chave informada"""
        som = self.sfx_player.get(chave)
        if som:
            som.play()

    def tocar_musica_fase(self, caminho_musica, volume=0.2):
        """Carrega e toca a música de fundo em loop infinito"""
        try:
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            print(f"Música {caminho_musica} iniciada com sucesso!")
        except (pygame.error, FileNotFoundError):
            print(f"Erro: Não foi possível carregar a música em: {caminho_musica}")