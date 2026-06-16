# constantes.py

# Configurações da Janela
LARGURA = 800
ALTURA = 600
FPS = 60

# Física do Jogo
GRAVIDADE = 0.8               # Força que puxa o herói para baixo a cada frame
FORCA_PULO_NORMAL = -14              # Força do impulso para cima (negativo no Pygame vai para o topo)
FORCA_PULO_CORRENDO = -18     # Pulo com impulso da corrida!
VELOCIDADE_MAX_QUEDA = 10     # Limite para o herói não cair rápido demais (terminal velocity)

# Cores Principais (RGB)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)           # Cor provisória para o nosso chão