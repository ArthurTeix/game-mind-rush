# Arquivo responsável por administrar o funcionamento do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FULLSCREEN, FPS
from game.elements.personagem import Personagem
from game.elements.chao import GerenciadorChao
from game.render import desenhar_menu, desenhar_jogo, desenhar_gameover
from game.ui.botao import botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair, botao_reiniciar, botao_sair_gameover

class Motor:
    def __init__(self):
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), flags)
        pygame.display.set_caption(TITULO_JOGO)

        self.watch = pygame.time.Clock()
        self.rodando = True
        self.pontos = 0
        self.estado = "menu"
        self.imagem_gameover = pygame.image.load("./img/mensagem/MORREUMR.png").convert_alpha()

        # cria o gerenciador de chão primeiro, porque o personagem
        # precisa nascer em cima de um bloco de chão já existente
        self.gerenciador_chao = GerenciadorChao(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            velocidade=5,
            espaco_minimo=150,
            espaco_maximo=270
        )

        # posiciona o personagem exatamente em cima do primeiro bloco de chão,
        # em vez de usar um valor fixo que pode não bater com a altura real do bloco
        altura_personagem = 50
        y_inicial = (ALTURA_TELA - self.gerenciador_chao.altura_do_chao_inicial) - altura_personagem

        self.personagem = Personagem(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            x=150, y=y_inicial,
            largura=57, altura=altura_personagem,
            caminhos_imagens=[
                "./img/personagem-teste.png",
                "./img/personagem-teste.png",
                "./img/personagem-teste.png",
            ]
        )

    def jogo(self):
        while self.rodando:
            self.watch.tick(FPS)

            self.capturar_eventos()

            if self.estado == "menu":
                desenhar_menu(self.tela)

            elif self.estado == "jogar":
                self.atualizar_jogo()
                desenhar_jogo(self.tela, self.personagem, self.gerenciador_chao, self.pontos)

            elif self.estado == "gameover":
                desenhar_gameover(self.tela, self.imagem_gameover)

            pygame.display.update()


    def reiniciar_jogo(self):
        self.pontos = 0

        self.gerenciador_chao = GerenciadorChao(
        largura_tela=LARGURA_TELA,
        altura_tela=ALTURA_TELA,
        velocidade=5,
        espaco_minimo=150,
        espaco_maximo=270
        )
        
        altura_personagem = 50
        y_inicial = (ALTURA_TELA - self.gerenciador_chao.altura_do_chao_inicial) - altura_personagem

        self.personagem.rect.x = 150
        self.personagem.rect.y = y_inicial
        self.personagem.vivo = True
        self.personagem.vidas = 3

    def capturar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.encerrar_jogo()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.encerrar_jogo()

            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP):
                if self.estado == "jogar":
                    self.personagem.pular()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado == "menu" and botao_jogar.clicado(evento.pos):
                    self.estado = "jogar"

                elif self.estado == "menu" and botao_sair.clicado(evento.pos):
                    self.rodando = False

                elif self.estado == "gameover":
                    if botao_reiniciar.clicado(evento.pos):
                        self.reiniciar_jogo()
                        self.estado = "jogar"
                    elif botao_sair_gameover.clicado(evento.pos):
                        self.rodando = False

    def atualizar_jogo(self):
        chaos_removidos = self.gerenciador_chao.atualizar()
        self.pontos += chaos_removidos

        self.personagem.atualizar(self.gerenciador_chao.lista_chaos)

        if not self.personagem.vivo:
            self.estado = "gameover"

    def encerrar_jogo(self):
        self.rodando = False
        pygame.quit()
        quit()
