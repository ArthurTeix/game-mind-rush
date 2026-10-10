# Arquivo responsável por administrar o funcionamento do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FULLSCREEN, FPS
from game.database.db import criar_tabela_pontuacao, salvar_pontuacao, get_top5_pontuacao
from game.elements.personagem import Personagem
from game.elements.chao import GerenciadorChao
from game.render import desenhar_menu, desenhar_jogo, desenhar_gameover, desenhar_ranking, rect_sair_ranking
from game.ui.botao import botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair, botao_reiniciar, botao_sair_gameover, botao_menu

# --- valores da partida (ficam num lugar só: início e reinício usam os mesmos) ---
VELOCIDADE_CHAO = 6
ESPACO_MINIMO = 150
ESPACO_MAXIMO = 270
ALTURA_PERSONAGEM = 80
LARGURA_PERSONAGEM = 70
X_PERSONAGEM = 150


class Motor:
    def __init__(self):
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), flags)
        pygame.display.set_caption(TITULO_JOGO)

        criar_tabela_pontuacao()

        self.watch = pygame.time.Clock()
        self.rodando = True
        self.pontos = 0
        self.top5 = []
        self.estado = "menu"
        self.imagem_gameover = pygame.image.load("./img/mensagem/MORREUMR.png").convert_alpha()

        # o personagem é criado uma única vez (carrega as imagens);
        # a posição real é definida em iniciar_partida()
        self.personagem = Personagem(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            x=X_PERSONAGEM, y=0,
            largura=LARGURA_PERSONAGEM, altura=ALTURA_PERSONAGEM,
            caminhos_imagens=[
                "./img/personagens/computacao/robo_pos0.png",
                "./img/personagens/computacao/robo_pos1.png",
                "./img/personagens/computacao/robo_pos2.png",
            ]
        )

        self.iniciar_partida()

    def iniciar_partida(self):
        """Prepara uma partida nova do zero (usada no início, no reinício e ao jogar pelo menu)."""
        self.pontos = 0

        # o chão é criado primeiro, porque o personagem
        # precisa nascer em cima de um bloco já existente
        self.gerenciador_chao = GerenciadorChao(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            velocidade=VELOCIDADE_CHAO,
            espaco_minimo=ESPACO_MINIMO,
            espaco_maximo=ESPACO_MAXIMO
        )

        y_inicial = (ALTURA_TELA - self.gerenciador_chao.altura_do_chao_inicial) - ALTURA_PERSONAGEM
        self.personagem.resetar(X_PERSONAGEM, y_inicial)

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

            elif self.estado == "rank":
                desenhar_ranking(self.tela, self.top5)

            # único update de tela por frame
            pygame.display.update()

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
                if self.estado == "menu":
                    if botao_jogar.clicado(evento.pos):
                        self.iniciar_partida()
                        self.estado = "jogar"
                    elif botao_ranking.clicado(evento.pos):
                        self.top5 = get_top5_pontuacao()  # consulta o banco uma vez, não a cada frame
                        self.estado = "rank"
                    elif botao_sair.clicado(evento.pos):
                        self.rodando = False

                elif self.estado == "rank":
                    if rect_sair_ranking.collidepoint(evento.pos):
                        self.estado = "menu"

                elif self.estado == "gameover":
                    if botao_reiniciar.clicado(evento.pos):
                        self.iniciar_partida()
                        self.estado = "jogar"
                    elif botao_menu.clicado(evento.pos):
                        self.estado = "menu"
                    elif botao_sair_gameover.clicado(evento.pos):
                        self.rodando = False

    def atualizar_jogo(self):
        chaos_removidos = self.gerenciador_chao.atualizar()
        self.pontos += chaos_removidos

        self.personagem.atualizar(self.gerenciador_chao.lista_chaos)

        if not self.personagem.vivo:
            self.estado = "gameover"
            salvar_pontuacao(self.pontos)

    def encerrar_jogo(self):
        self.rodando = False
        pygame.quit()
        quit()
