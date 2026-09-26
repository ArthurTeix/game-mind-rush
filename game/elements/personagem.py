import pygame


class Personagem:
    def __init__(self, largura_tela, altura_tela, x, y, largura, altura, caminhos_imagens):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.largura = largura
        self.altura = altura

        self.rect = pygame.Rect(x, y, largura, altura)

        # --- física vertical ---
        self.velocidade_y = 0
        self.gravidade = 0.6
        self.forca_salto = -16

        # --- controle de estado ---
        self.no_chao = False
        self.vivo = True

        # --- animação (corrida) ---
        self.imagens = []
        for caminho in caminhos_imagens:
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem, (largura, altura))
            self.imagens.append(imagem)

        self.frame_atual = 0
        self.contador_frames = 0
        self.intervalo_troca = 6

    def pular(self):
        if self.no_chao:
            self.velocidade_y = self.forca_salto
            self.no_chao = False

    def aplicar_gravidade(self):
        self.velocidade_y += self.gravidade
        self.rect.y += self.velocidade_y

    def verificar_colisao_com_chao(self, lista_de_chaos):
        self.no_chao = False

        for chao in lista_de_chaos:
            if self.rect.colliderect(chao.rect) and self.velocidade_y >= 0:
                # posição que o personagem tinha ANTES de mover neste frame
                bottom_anterior = self.rect.bottom - self.velocidade_y

                # só conta como "pousar em cima" se ele estava acima do
                # topo do bloco no frame passado (10px de tolerância)
                if bottom_anterior <= chao.rect.top + 10:
                    self.rect.bottom = chao.rect.top
                    self.velocidade_y = 0
                    self.no_chao = True

    def verificar_queda_fatal(self):
        if self.rect.y > self.altura_tela:
            self.vivo = False

    def animar(self):
        self.contador_frames += 1

        if self.contador_frames >= self.intervalo_troca:
            self.frame_atual = (self.frame_atual + 1) % len(self.imagens)
            self.contador_frames = 0

    def atualizar(self, lista_de_chaos):
        self.aplicar_gravidade()
        self.verificar_colisao_com_chao(lista_de_chaos)
        self.animar()
        self.verificar_queda_fatal()

    def desenhar(self, tela):
        tela.blit(self.imagens[self.frame_atual], self.rect)
