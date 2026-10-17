import pygame
from game.elements.obstaculo import GerenciadorObstaculos
from game.elements.moeda import Moeda, GerenciadorMoeda


class Personagem:
    def __init__(self, largura_tela, altura_tela, x, y, largura, altura, caminhos_imagens):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.largura = largura
        self.altura = altura

        self.rect = pygame.Rect(x, y, largura, altura)

        # --- física vertical ---
        # pos_y guarda a posição como float: o Rect só aceita inteiros, e
        # somar 0.6 direto no rect.y fazia o personagem "piscar" no chão
        # (no_chao alternava True/False e o pulo falhava a cada 2 frames)
        self.pos_y = float(y)
        self.bottom_anterior = self.rect.bottom
        self.velocidade_y = 0
        self.gravidade = 1
        self.forca_salto = -20

        # --- controle de estado ---
        self.no_chao = False
        self.vivo = True

        self.vidas_max = 3
        self.vidas = 3

        self.x_inicial = x
        self.y_inicial = y

        self.invulnerabilidade = 0

        # --- animação (corrida) ---
        self.imagens = []
        for caminho in caminhos_imagens:
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem, (largura, altura))
            self.imagens.append(imagem)

        self.frame_atual = 0
        self.contador_frames = 0
        self.intervalo_troca = 6

    def resetar(self, x, y):
        """Volta o personagem ao estado inicial de uma partida."""
        self.rect.x = x
        self.rect.y = y
        self.pos_y = float(y)
        self.bottom_anterior = self.rect.bottom
        self.velocidade_y = 0
        self.no_chao = False
        self.vivo = True
        self.frame_atual = 0
        self.contador_frames = 0
        self.vidas = self.vidas_max
        self.invulnerabilidade = 0

    def pular(self):
        if self.no_chao:
            self.velocidade_y = self.forca_salto
            self.no_chao = False

    def aplicar_gravidade(self):
        # guarda onde os pés estavam ANTES de mover neste frame
        self.bottom_anterior = self.rect.bottom

        self.velocidade_y += self.gravidade
        self.pos_y += self.velocidade_y
        self.rect.y = round(self.pos_y)

    def verificar_colisao_com_chao(self, lista_de_chaos):
        self.no_chao = False

        # hitbox um pouco menor que a imagem, para não ser injusto
        hitbox = self.rect.inflate(-20, -10)

        for chao in lista_de_chaos:
            if not self.rect.colliderect(chao.rect):
                continue

            # pousar em cima: está descendo e os pés estavam acima do
            # topo do bloco no frame passado (10px de tolerância)
            if self.velocidade_y >= 0 and self.bottom_anterior <= chao.rect.top + 10:
                self.rect.bottom = chao.rect.top
                self.pos_y = float(self.rect.y)
                self.velocidade_y = 0
                self.no_chao = True
                break

            # qualquer outra batida (lateral ou por baixo) é fatal
            if hitbox.colliderect(chao.rect):
                self.vivo = False

    def perder_vida(self):
        if self.invulnerabilidade > 0 or not self.vivo:
            return

        self.vidas -= 1

        if self.vidas <= 0:
            self.vidas = 0
            self.vivo = False
        else:
            self.invulnerabilidade = 60

    def ganhar_vida(self):
        if not self.vivo:
            return

        self.vidas += 1
        self.vidas = min(self.vidas + 1, self.vidas_max)

    def verificar_queda_fatal(self):
        if self.rect.y > self.altura_tela:
            self.vivo = False

    def verificar_colisao_obstaculo(self, gerenciador_obstaculos):
        hitbox = self.rect.inflate(-20, -10)
        
        for obstaculo in gerenciador_obstaculos.lista_obstaculos:
            if hitbox.colliderect(obstaculo.rect):
                self.perder_vida()
                gerenciador_obstaculos.remover(obstaculo)
                break

    def verificar_colisao_moeda(self, gerenciador_moeda):
        hitbox = self.rect.inflate(-20, -10)

        for moeda in gerenciador_moeda.lista_moeda:
            if hitbox.colliderect(moeda.rect):
                self.ganhar_vida()
                gerenciador_moeda.remover(moeda)
                break

    def animar(self):
        self.contador_frames += 1

        if self.contador_frames >= self.intervalo_troca:
            self.frame_atual = (self.frame_atual + 1) % len(self.imagens)
            self.contador_frames = 0

    def atualizar(self, lista_de_chaos, gerenciador_obstaculos, gerenciador_moeda):
        self.aplicar_gravidade()
        self.verificar_colisao_com_chao(lista_de_chaos)
        self.verificar_colisao_obstaculo(gerenciador_obstaculos)
        self.verificar_colisao_moeda(gerenciador_moeda)
        self.animar()
        self.verificar_queda_fatal()

        if self.invulnerabilidade > 0:
            self.invulnerabilidade -= 1

    def desenhar(self, tela):
        tela.blit(self.imagens[self.frame_atual], self.rect)
