# personagens.py
import pygame
import constantes as c


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, tipo="chao"):
        super().__init__()
        self.tipo = tipo

        # Criamos a superfície do tamanho exato pedido
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)

        try:
            # Tenta carregar o seu tilemap.
            textura_original = pygame.image.load("assets/Tilemap_color3.png").convert_alpha()
            # Ajustado para preencher de forma correta e sem distorções (32x32)
            tile_escalado = pygame.transform.scale(textura_original, (800, 100))

            # Preenche o bloco repetindo a textura
            for bloco_x in range(0, largura, 32):
                for bloco_y in range(0, altura, 32):
                    self.image.blit(tile_escalado, (bloco_x, bloco_y))
        except FileNotFoundError:
            # Se não achar o arquivo, mantém o bloco cinza de reserva
            self.image.fill((45, 45, 55))
            pygame.draw.rect(self.image, (30, 30, 40), (0, 0, largura, altura), 4)
            pygame.draw.line(self.image, (70, 70, 85), (0, 0), (largura, 0), 2)

        self.rect = self.image.get_rect(topleft=(x, y))


class Cavaleiro(pygame.sprite.Sprite):
    def __init__(self, x=None, y=100):
        super().__init__()

        # --- FATOR DE ESCALA ---
        self.escala = 2

        # --- CARREGAMENTO DE SPRITES ---
        self.tira_idle = pygame.image.load("assets/IDLE.png").convert_alpha()
        self.tira_walk = pygame.image.load("assets/WALK.png").convert_alpha()
        self.tira_run = pygame.image.load("assets/RUN.png").convert_alpha()
        self.tira_jump = pygame.image.load("assets/JUMP.png").convert_alpha()
        self.tira_attack = pygame.image.load("assets/ATTACK 1.png").convert_alpha()
        self.tira_attack2 = pygame.image.load("assets/ATTACK 2.png").convert_alpha()
        self.tira_attack3 = pygame.image.load("assets/ATTACK 3.png").convert_alpha()
        self.tira_defend = pygame.image.load("assets/DEFEND.png").convert_alpha()

        # Quantidade exata de frames
        frames_idles_qtd = 7
        frames_walk_qtd = 8
        frames_run_qtd = 8
        frames_jump_qtd = 5
        frames_attack_qtd = 6
        frames_attack2_qtd = 5
        frames_attack3_qtd = 6
        frames_defend_qtd = 6

        # Recorte e redimensionamento dos frames
        self.frames_idle = self.recortar_e_escalar_tira(self.tira_idle, frames_idles_qtd)
        self.frames_walk = self.recortar_e_escalar_tira(self.tira_walk, frames_walk_qtd)
        self.frames_run = self.recortar_e_escalar_tira(self.tira_run, frames_run_qtd)
        self.frames_jump = self.recortar_e_escalar_tira(self.tira_jump, frames_jump_qtd)
        self.frames_attack = self.recortar_e_escalar_tira(self.tira_attack, frames_attack_qtd)
        self.frames_attack2 = self.recortar_e_escalar_tira(self.tira_attack2, frames_attack2_qtd)
        self.frames_attack3 = self.recortar_e_escalar_tira(self.tira_attack3, frames_attack3_qtd)
        self.frames_defend = self.recortar_e_escalar_tira(self.tira_defend, frames_defend_qtd)

        self.tempo_ultimo_passo = 0
        # Cooldown em milissegundos (ex: 350ms andando, 220ms correndo)
        self.intervalo_passo = 350

        # Controle de Ataques e Combos
        self.ataque_aereo = False
        self.tipo_ataque_atual = 1
        self.tempo_ultimo_ataque = 0
        self.janela_combo = 800

        # Estado inicial da animação
        self.animacao_atual = self.frames_idle
        self.frame_index = 0
        self.image = self.animacao_atual[self.frame_index]

        # --- HITBOX REAL DO PERSONAGEM ---
        largura_hitbox = 20 * self.escala
        altura_hitbox = 40 * self.escala

        pos_x = x if x is not None else 150
        self.rect = pygame.Rect(pos_x, y, largura_hitbox, altura_hitbox)

        # --- VELOCIDADES CONFIGURÁVEIS ---
        self.vel_andar = 3
        self.vel_correr = 6
        self.velocidade_x_atual = 0
        self.velocidade_y = 0
        self.no_chao = False

        # --- ATRIBUTOS DE COMBATE ---
        self.olhando_para_direita = True
        self.atacando = False
        self.defendendo = False
        self.correndo = False
        self.rect_ataque = pygame.Rect(0, 0, 0, 0)

        # --- SISTEMA DE VIDA (HP) ---
        self.vida_max = 100
        self.vida_atual = self.vida_max
        self.invencivel = False
        self.tempo_invencivel = 0
        self.duracao_invencibilidade = 1000

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 100
        self.som_ataque_tocado = False  # <--- Nova trava de som

    def recortar_e_escalar_tira(self, tira, qtd_frames):
        lista = []
        largura_frame = tira.get_width() // qtd_frames
        altura_frame = tira.get_height()

        novo_w = largura_frame * self.escala
        novo_h = altura_frame * self.escala

        for i in range(qtd_frames):
            sub_imagem = tira.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            imagem_ampliada = pygame.transform.scale(sub_imagem, (novo_w, novo_h))
            lista.append(imagem_ampliada)
        return lista

    def atualizar_animacao(self):
        animacao_anterior = self.animacao_atual

        if self.atacando:
            if self.ataque_aereo:
                self.animacao_atual = self.frames_attack3
            elif self.tipo_ataque_atual == 2:
                self.animacao_atual = self.frames_attack2
            else:
                self.animacao_atual = self.frames_attack
        elif self.defendendo:
            self.animacao_atual = self.frames_defend
            if self.frame_index >= len(self.animacao_atual):
                self.frame_index = len(self.animacao_atual) - 1
        elif not self.no_chao:
            self.animacao_atual = self.frames_jump
        elif self.velocidade_x_atual != 0:
            if self.correndo:
                self.animacao_atual = self.frames_run
            else:
                self.animacao_atual = self.frames_walk
        else:
            self.animacao_atual = self.frames_idle

        if animacao_anterior != self.animacao_atual:
            self.frame_index = 0
            self.tempo_ultimo_frame = pygame.time.get_ticks()

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1

            if self.atacando and self.frame_index >= len(self.animacao_atual):
                self.atacando = False
                self.ataque_aereo = False
                self.frame_index = 0
                self.tempo_ultimo_ataque = pygame.time.get_ticks()
                self.som_ataque_tocado = False  # <--- LIBERA A TRAVA AQUI quando o ataque acaba!
            else:
                self.frame_index %= len(self.animacao_atual)

        imagem_frame = self.animacao_atual[self.frame_index]
        if not self.olhando_para_direita:
            self.image = pygame.transform.flip(imagem_frame, True, False)
        else:
            self.image = imagem_frame

    def tomar_dano(self, quantidade, indefensavel=False, audio=None):
        tempo_atual = pygame.time.get_ticks()
        if not self.invencivel and (indefensavel or not self.defendendo):
            # --- TRILHA DE ÁUDIO DE DANO ---
            if audio is not None:
                audio.tocar_sfx_player("dor")

            self.vida_atual -= quantidade
            if self.vida_atual < 0:
                self.vida_atual = 0
            self.invencivel = True
            self.tempo_invencivel = tempo_atual
            print(f"Ai! Vida do Cavaleiro: {self.vida_atual}/{self.vida_max}")

    def atualizar_invencibilidade(self):
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_invencivel > self.duracao_invencibilidade:
                self.invencivel = False

    def update(self, plataformas, audio=None):
        self.velocidade_y += c.GRAVIDADE
        if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = c.VELOCIDADE_MAX_QUEDA

        teclas = pygame.key.get_pressed()
        movendo = False
        self.velocidade_x_atual = 0

        if teclas[pygame.K_LSHIFT] and self.no_chao and not self.atacando:
            self.defendendo = True
        else:
            self.defendendo = False

        if teclas[pygame.K_LCTRL]:
            self.correndo = True
            vel_atual = self.vel_correr
        else:
            self.correndo = False
            vel_atual = self.vel_andar

        if not self.defendendo:
            pode_se_mover = (not self.atacando) or (self.atacando and not self.no_chao)

            if pode_se_mover:
                if teclas[pygame.K_LEFT]:
                    if self.rect.left > 0:
                        self.rect.x -= vel_atual
                        self.velocidade_x_atual = -vel_atual
                        movendo = True
                        if not self.atacando:
                            self.olhando_para_direita = False

                if teclas[pygame.K_RIGHT]:
                    self.rect.x += vel_atual
                    self.velocidade_x_atual = vel_atual
                    movendo = True
                    if not self.atacando:
                        self.olhando_para_direita = True

        # Movimento e Colisão Y
        self.rect.y += self.velocidade_y
        self.no_chao = False
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisoes:
            if self.velocidade_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        if teclas[pygame.K_SPACE] and self.no_chao and not self.atacando and not self.defendendo:
            if movendo and self.correndo:
                self.velocidade_y = c.FORCA_PULO_CORRENDO
            else:
                self.velocidade_y = c.FORCA_PULO_NORMAL
            self.no_chao = False

            # --- TRILHA DE ÁUDIO DO PULO ---
            if audio is not None:
                audio.tocar_sfx_player("pulo")

        if teclas[pygame.K_x] and not self.atacando and not self.defendendo:
            tempo_atual = pygame.time.get_ticks()

            if tempo_atual - self.tempo_ultimo_ataque < self.janela_combo and self.tipo_ataque_atual == 1:
                self.tipo_ataque_atual = 2
            else:
                self.tipo_ataque_atual = 1

            self.atacando = True
            self.frame_index = 0

            # --- SISTEMA DE SFX COM TRAVA DE REPETIÇÃO ---
            if audio and not self.som_ataque_tocado:  # <--- Só entra se ainda não tocou
                if not self.no_chao:
                    self.ataque_aereo = True
                    audio.tocar_sfx_player("errou_ar")
                else:
                    self.ataque_aereo = False
                    if self.tipo_ataque_atual == 2:
                        audio.tocar_sfx_player("errou_2")
                    else:
                        audio.tocar_sfx_player("errou_1")

                self.som_ataque_tocado = True  # <--- ATIVA A TRAVA imediatamente após tocar!

            if not self.no_chao:
                self.ataque_aereo = True
            else:
                self.ataque_aereo = False

        if self.atacando:
            largura_espada = 18 * self.escala
            altura_espada = 18 * self.escala
            if self.olhando_para_direita:
                self.rect_ataque = pygame.Rect(self.rect.right, self.rect.centery - (altura_espada // 2),
                                               largura_espada, altura_espada)
            else:
                self.rect_ataque = pygame.Rect(self.rect.left - largura_espada,
                                               self.rect.centery - (altura_espada // 2), largura_espada, altura_espada)
        else:
            self.rect_ataque = pygame.Rect(0, 0, 0, 0)

            # --- SISTEMA DE AUDIO DE PASSOS E ARMADURA ---
            if self.no_chao and self.velocidade_x_atual != 0 and not self.atacando and not self.defendendo:
                tempo_atual = pygame.time.get_ticks()

                # Ajusta o ritmo dos passos: se estiver correndo, os passos são mais rápidos!
                if self.correndo:
                    self.intervalo_passo = 220  # Passos rápidos
                else:
                    self.intervalo_passo = 380  # Passos normais de caminhada

                # Se passou o tempo do cooldown, toca o som!
                if tempo_atual - self.tempo_ultimo_passo > self.intervalo_passo:
                    if audio is not None:
                        audio.tocar_passo_aleatorio()
                    self.tempo_ultimo_passo = tempo_atual

        self.atualizar_animacao()
        self.atualizar_invencibilidade()

    def draw_custom(self, tela):
        if self.invencivel:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return

        centro_x = self.rect.centerx
        rect_imagem = self.image.get_rect()
        rect_imagem.centerx = centro_x
        rect_imagem.bottom = self.rect.bottom + (23 * self.escala)
        tela.blit(self.image, rect_imagem)

    def desenhar_ataque(self, tela):
        if self.atacando:
            pygame.draw.rect(tela, (255, 0, 0, 100), self.rect_ataque, 2)


class BringerOfDeath(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.escala = 2

        self.frames_idle = []
        for i in range(1, 9):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Idle/Bringer-of-Death_Idle_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_idle.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala),
                                                                    int(imagem.get_height() * self.escala))))

        self.frames_walk = []
        for i in range(1, 9):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Walk/Bringer-of-Death_Walk_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_walk.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala),
                                                                    int(imagem.get_height() * self.escala))))

        self.frames_attack = []
        for i in range(1, 11):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Attack/Bringer-of-Death_Attack_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_attack.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala),
                                                                      int(imagem.get_height() * self.escala))))

        self.frames_death = []
        for i in range(1, 11):
            caminho = f"assets/Bringer-of-Death/Individual Sprite/Death/Bringer-of-Death_Death_{i}.png"
            imagem = pygame.image.load(caminho).convert_alpha()
            self.frames_death.append(pygame.transform.scale(imagem, (int(imagem.get_width() * self.escala),
                                                                     int(imagem.get_height() * self.escala))))

        self.animacao_atual = self.frames_walk
        self.frame_index = 0
        self.image = self.animacao_atual[self.frame_index]

        largura_hitbox = 35 * self.escala
        self.rect = pygame.Rect(x, y, largura_hitbox, 45)

        self.velocidade = 1.2
        self.velocidade_y = 0
        self.direcao = -1
        self.olhando_para_direita = False
        self.no_chao = False

        self.atacando = False
        self.raio_ataque = 80
        self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)
        self.deu_dano_nesse_ciclo = False
        self.morrendo = False

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 100
        self.som_ataque_tocado = False

    def update(self, plataformas, jogador=None, audio=None):
        self.velocidade_y += c.GRAVIDADE
        if self.velocidade_y > c.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = c.VELOCIDADE_MAX_QUEDA
        self.rect.y += self.velocidade_y

        self.no_chao = False
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisoes:
            if self.velocidade_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        if self.morrendo:
            self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
                self.tempo_ultimo_frame = tempo_atual
                self.frame_index += 1
                if self.frame_index >= len(self.animacao_atual):
                    self.kill()
                    return

            imagem_frame = self.animacao_atual[self.frame_index]
            if self.olhando_para_direita:
                self.image = pygame.transform.flip(imagem_frame, True, False)
            else:
                self.image = imagem_frame
            return

        if self.no_chao and jogador is not None:
            distancia_x = abs(self.rect.centerx - jogador.rect.centerx)
            distancia_y = abs(self.rect.centery - jogador.rect.centery)

            if distancia_x <= self.raio_ataque and distancia_y < 50:
                if not self.atacando:
                    self.atacando = True
                    self.frame_index = 0
                    self.animacao_atual = self.frames_attack
                    self.deu_dano_nesse_ciclo = False
                    if jogador.rect.centerx > self.rect.centerx:
                        self.olhando_para_direita = True
                        self.direcao = 1
                    else:
                        self.olhando_para_direita = False
                        self.direcao = -1

        if self.no_chao and not self.atacando:
            self.animacao_atual = self.frames_walk
            self.rect.x += self.velocidade * self.direcao

            # --- CORREÇÃO DA TRAVA DA TELA: Removido c.LARGURA ---
            # O inimigo agora caminha na sua patrulha livremente sem bater em bordas invisíveis
            sensor_x = self.rect.right + 2 if self.direcao == 1 else self.rect.left - 2
            sensor_y = self.rect.bottom + 1
            rect_sensor = pygame.Rect(sensor_x, sensor_y, 1, 1)

            tem_chao = False
            for plat in plataformas:
                if rect_sensor.colliderect(plat.rect):
                    tem_chao = True
                    break

            if not tem_chao:
                self.direcao *= -1
                self.olhando_para_direita = not self.olhando_para_direita

        if self.atacando:
            if 4 <= self.frame_index <= 7:
                largura_ataque = 70 * self.escala
                altura_ataque = 40 * self.escala
                if self.olhando_para_direita:
                    self.rect_ataque_inimigo = pygame.Rect(self.rect.right, self.rect.y, largura_ataque, altura_ataque)
                else:
                    self.rect_ataque_inimigo = pygame.Rect(self.rect.left - largura_ataque, self.rect.y, largura_ataque,
                                                           altura_ataque)
            else:
                self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1

            # --- CORREÇÃO DA CONDIÇÃO DE SOM ---
            # Usando >= 4 garante que mesmo se o frame passar voando, a trava segura o som uma única vez!
            if self.atacando and self.frame_index >= 4 and not self.som_ataque_tocado:
                if audio is not None:
                    audio.tocar_sfx_player("bringer_ataque")
                self.som_ataque_tocado = True  # Ativa a trava

            if self.atacando and self.frame_index >= len(self.animacao_atual):
                self.atacando = False
                self.frame_index = 0
                self.rect_ataque_inimigo = pygame.Rect(0, 0, 0, 0)
                self.som_ataque_tocado = False  # <--- LIBERA A TRAVA para o próximo ataque!
            else:
                self.frame_index %= len(self.animacao_atual)

        imagem_frame = self.animacao_atual[self.frame_index]
        self.image = pygame.transform.flip(imagem_frame, True, False) if self.olhando_para_direita else imagem_frame

    def draw_custom(self, tela):
        rect_imagem = self.image.get_rect()
        rect_imagem.centerx = self.rect.centerx
        rect_imagem.bottom = self.rect.bottom + int(1 * self.escala)
        tela.blit(self.image, rect_imagem)

    def tomar_dano(self, audio=None): # <--- Adicionei o argumento audio
        if not self.morrendo:
            self.morrendo = True
            self.frame_index = 0
            self.animacao_atual = self.frames_death
            self.tempo_ultimo_frame = pygame.time.get_ticks()
            if audio is not None:
                audio.tocar_sfx_player("bringer_morte")


class MagiaNecromante(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao_x, direcao_y, olhando_para_direita, escala=2):
        super().__init__()
        self.escala = escala

        self.tira_magia = pygame.image.load("assets/fire-ball.png").convert_alpha()
        self.frames = []
        largura_frame = self.tira_magia.get_width() // 3
        altura_frame = self.tira_magia.get_height()

        for i in range(3):
            sub = self.tira_magia.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            sub_escalada = pygame.transform.scale(sub,
                                                  (int(largura_frame * self.escala), int(altura_frame * self.escala)))

            if not olhando_para_direita:
                sub_escalada = pygame.transform.flip(sub_escalada, True, False)

            self.frames.append(sub_escalada)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        vetor_velocidade = pygame.math.Vector2(direcao_x, direcao_y)
        if vetor_velocidade.length() > 0:
            vetor_velocidade = vetor_velocidade.normalize() * 5
        else:
            vetor_velocidade = pygame.math.Vector2(5, 0)

        self.vel_x = vetor_velocidade.x
        self.vel_y = vetor_velocidade.y

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 80

    def update(self, plataformas, jogador=None, audio=None):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # --- CORREÇÃO DA TRAVA DA MAGIA: Removido c.LARGURA ---
        # Agora a magia viaja pelo mapa e só morre se sair da altura vertical do jogo
        if self.rect.y > c.ALTURA or self.rect.y < -100:
            self.kill()


class ExplosaoNecromante(pygame.sprite.Sprite):
    def __init__(self, x, y, escala=2):
        super().__init__()
        self.escala = escala
        self.indefensavel = True
        self.causou_dano = False

        self.tira_ataque2 = pygame.image.load("assets/enemy-death.png").convert_alpha()
        self.frames = []
        largura_frame = self.tira_ataque2.get_width() // 7
        altura_frame = self.tira_ataque2.get_height()

        for i in range(7):
            sub = self.tira_ataque2.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            sub_escalada = pygame.transform.scale(sub,
                                                  (int(largura_frame * self.escala), int(altura_frame * self.escala)))
            self.frames.append(sub_escalada)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.v_animacao = 90
        self.causou_dano = False

    def update(self, plataformas, jogador=None, audio=None):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.kill()
                return

            self.image = self.frames[self.frame_index]

        if jogador is not None and 2 <= self.frame_index <= 5 and not self.causou_dano:
            if self.rect.colliderect(jogador.rect):
                jogador.tomar_dano(25, indefensavel=True, audio=audio)
                self.causou_dano = True


class Necromante(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.escala = 2

        self.sheet = pygame.image.load("assets/Necromancer_creativekind-Sheet.png").convert_alpha()

        self.w_original = 160
        self.h_original = 128

        self.frames_idle = self.recortar_linha(0, 8)
        self.frames_attack = self.recortar_linha(2, 13)
        self.frames_death = self.recortar_linha(6, 10)

        self.animacao_atual = self.frames_idle
        self.frame_index = 0
        self.image = self.animacao_atual[self.frame_index]

        self.rect = pygame.Rect(x, y, 22 * self.escala, 40 * self.escala)

        self.olhando_para_direita = True
        self.atacando = False
        self.morrendo = False
        self.deu_ataque_nesse_ciclo = False
        self.som_magia_tocado = False

        self.raio_deteccao = 350
        self.cooldown_ataque = 1300
        self.v_animacao = 90
        self.ultimo_ataque = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()

    def recortar_linha(self, linha, qtd_frames):
        lista = []
        for i in range(qtd_frames):
            rect_recorte = pygame.Rect(i * self.w_original, linha * self.h_original, self.w_original, self.h_original)
            sub_imagem = self.sheet.subsurface(rect_recorte)
            ampliada = pygame.transform.scale(sub_imagem,
                                              (self.w_original * self.escala, self.h_original * self.escala))
            lista.append(ampliada)
        return lista

    def update(self, plataformas, jogador=None, audio=None):
        if self.morrendo:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
                self.tempo_ultimo_frame = tempo_atual
                self.frame_index += 1
                if self.frame_index >= len(self.animacao_atual):
                    self.kill()
                    return
            self.image = self.animacao_atual[self.frame_index] if self.olhando_para_direita else pygame.transform.flip(
                self.animacao_atual[self.frame_index], True, False)
            return

        self.rect.y += 2
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for plat in colisoes:
            self.rect.bottom = plat.rect.top

        ataque_gerado = None

        if jogador is not None:
            vetor_centro_necro = pygame.math.Vector2(self.rect.center)
            vetor_centro_jog = pygame.math.Vector2(jogador.rect.center)
            distancia = vetor_centro_necro.distance_to(vetor_centro_jog)

            if not self.atacando:
                if jogador.rect.centerx > self.rect.centerx:
                    self.olhando_para_direita = True
                else:
                    self.olhando_para_direita = False

            tempo_atual = pygame.time.get_ticks()
            if distancia <= self.raio_deteccao and not self.atacando:
                if tempo_atual - self.ultimo_ataque > self.cooldown_ataque:
                    self.atacando = True
                    self.frame_index = 0
                    self.animacao_atual = self.frames_attack
                    self.deu_ataque_nesse_ciclo = False
                    self.som_magia_tocado = False
                    self.ultimo_ataque = tempo_atual

                    if distancia < 160:
                        self.tipo_ataque_mago = 2
                    else:
                        self.tipo_ataque_mago = 1

            if not self.atacando:
                self.animacao_atual = self.frames_idle

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.v_animacao:
            self.tempo_ultimo_frame = tempo_atual
            self.frame_index += 1

            if self.atacando:
                # --- NOVA LÓGICA DE SOM DO NECROMANTE ---
                # Quando o frame chega em 8 e o som ainda não tocou neste ataque:
                if self.frame_index >= 8 and not self.som_magia_tocado:
                    if audio is not None:
                        if self.tipo_ataque_mago == 1:
                            audio.tocar_sfx_player("necroman_fogo")
                        else:
                            audio.tocar_sfx_player("necroman_explosao")
                    self.som_magia_tocado = True  # Ativa a trava para tocar só uma vez

                # --- GERAÇÃO DO ATAQUE FÍSICO/MAGIA ---
                if self.frame_index == 8 and not self.deu_ataque_nesse_ciclo and jogador is not None:
                    if self.tipo_ataque_mago == 1:
                        dx = jogador.rect.centerx - self.rect.centerx
                        dy = (jogador.rect.centery - 10) - self.rect.centery
                        y_spawn = self.rect.top + int(15 * self.escala)
                        ataque_gerado = MagiaNecromante(self.rect.centerx, y_spawn, dx, dy, self.olhando_para_direita,
                                                        self.escala)
                    elif self.tipo_ataque_mago == 2:
                        ataque_gerado = ExplosaoNecromante(jogador.rect.centerx, jogador.rect.bottom, self.escala)

                    self.deu_ataque_nesse_ciclo = True

                # --- FIM DO ATAQUE ---
                if self.frame_index >= len(self.animacao_atual):
                    self.atacando = False
                    self.frame_index = 0
                    self.animacao_atual = self.frames_idle
                    self.som_magia_tocado = False  # <--- LIBERA A TRAVA DO SOM para o próximo ataque!
            else:
                self.frame_index %= len(self.animacao_atual)

        imagem_frame = self.animacao_atual[self.frame_index]
        self.image = imagem_frame if self.olhando_para_direita else pygame.transform.flip(imagem_frame, True, False)

        return ataque_gerado

    def draw_custom(self, tela):
        rect_imagem = self.image.get_rect()
        rect_imagem.centerx = self.rect.centerx
        rect_imagem.bottom = self.rect.bottom + int(12 * self.escala)
        tela.blit(self.image, rect_imagem)

    def tomar_dano(self, audio=None): # <--- Adicionei o argumento audio
        if not self.morrendo:
            self.morrendo = True
            self.frame_index = 0
            self.animacao_atual = self.frames_death
            self.tempo_ultimo_frame = pygame.time.get_ticks()
            if audio is not None:
                audio.tocar_sfx_player("necroman_morte")