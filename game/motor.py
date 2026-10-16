# Arquivo responsável por administrar o funcionamento do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FULLSCREEN, FPS
from game.database.db import criar_tabelas, salvar_pontuacao, get_top5_pontuacao
from game.elements.personagem import Personagem
from game.elements.chao import GerenciadorChao
from game.elements.obstaculo import GerenciadorObstaculos
from game.render import desenhar_menu, desenhar_jogo, desenhar_gameover, desenhar_ranking, rect_sair_ranking
from game.ui.botao import botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair, botao_reiniciar, botao_sair_gameover, botao_menu
from game.ui.conta import TelaConfig, TelaLogin, TelaCadastro
from game.render import imagem_menu, imagem_gameover, mensagem_gameover

# --- valores da partida (ficam num lugar só: início e reinício usam os mesmos) ---
VELOCIDADE_CHAO = 8.5
ESPACO_MINIMO = 150
ESPACO_MAXIMO = 270
ALTURA_PERSONAGEM = 80
LARGURA_PERSONAGEM = 70
X_PERSONAGEM = 150

ESTADOS_CONTA = ("config", "login", "cadastro")


class Motor:
    def __init__(self):
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), flags)
        pygame.display.set_caption(TITULO_JOGO)

        criar_tabelas()

        self.watch = pygame.time.Clock()
        self.rodando = True
        self.pontos = 0
        self.top5 = []
        self.estado = "menu"

        # jogador logado: None ou {"id": ..., "usuario": ...}
        self.jogador = None
        self.origem_login = "menu"   # para onde o botão "Voltar" do login leva

        # telas de conta
        self.tela_config = TelaConfig()
        self.tela_login = TelaLogin()
        self.tela_cadastro = TelaCadastro()

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

    @property
    def logado(self):
        """True se há um jogador logado. Use para liberar conteúdo exclusivo (ex.: personagem)."""
        return self.jogador is not None

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

        self.gerenciador_obstaculos = GerenciadorObstaculos()
        self.gerenciador_obstaculos.ignorar(self.gerenciador_chao.lista_chaos[0])

        y_inicial = (ALTURA_TELA - self.gerenciador_chao.altura_do_chao_inicial) - ALTURA_PERSONAGEM
        self.personagem.resetar(X_PERSONAGEM, y_inicial)

    def jogo(self):
        while self.rodando:
            self.watch.tick(FPS)

            self.capturar_eventos()

            if self.estado == "menu":
                desenhar_menu(self.tela, self.jogador)

            elif self.estado == "jogar":
                self.atualizar_jogo()
                desenhar_jogo(self.tela, self.personagem, self.gerenciador_chao, self.pontos, self.gerenciador_obstaculos)

            elif self.estado == "gameover":
                desenhar_gameover(self.tela, imagem_gameover, mensagem_gameover)

            elif self.estado == "rank":
                desenhar_ranking(self.tela, self.top5)

            elif self.estado == "config":
                self.tela_config.desenhar(self.tela, self.jogador)

            elif self.estado == "login":
                self.tela_login.desenhar(self.tela)

            elif self.estado == "cadastro":
                self.tela_cadastro.desenhar(self.tela)

            # único update de tela por frame
            pygame.display.update()

    # ------------------------------------------------------------ navegação

    def abrir_login(self, mensagem=None, origem="menu", sucesso=False):
        self.origem_login = origem
        self.tela_login.resetar(mensagem, sucesso)
        self.estado = "login"

    def abrir_cadastro(self):
        self.tela_cadastro.resetar()
        self.estado = "cadastro"

    def tratar_evento_conta(self, evento):
        """Eventos das telas de configuração, login e cadastro."""
        if self.estado == "config":
            acao = self.tela_config.tratar_evento(evento, self.jogador)

            if acao == "login":
                self.abrir_login(origem="config")
            elif acao == "cadastro":
                self.abrir_cadastro()
            elif acao == "logout":
                self.jogador = None
            elif acao == "voltar":
                self.estado = "menu"

        elif self.estado == "login":
            acao = self.tela_login.tratar_evento(evento)

            if acao == "logado":
                self.jogador = self.tela_login.jogador_logado
                self.estado = "menu"
            elif acao == "voltar":
                self.estado = self.origem_login

        elif self.estado == "cadastro":
            acao = self.tela_cadastro.tratar_evento(evento)

            if acao == "cadastrado":
                self.abrir_login("Conta criada com sucesso!", origem="config", sucesso=True)
                # já preenche o usuário e deixa o cursor na senha
                self.tela_login.campo_usuario.texto = self.tela_cadastro.usuario_criado
                self.tela_login.focar_campo(self.tela_login.campo_senha)
            elif acao == "voltar":
                self.estado = "config"

    def capturar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.encerrar_jogo()

            # nas telas de conta, o ESC volta uma tela em vez de fechar o jogo
            if self.estado in ESTADOS_CONTA:
                self.tratar_evento_conta(evento)
                continue

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.encerrar_jogo()

            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP):
                if self.estado == "jogar":
                    self.personagem.pular()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado == "menu":
                    if botao_jogar.clicado(evento.pos):
                        # qualquer pessoa pode jogar, logada ou não
                        self.iniciar_partida()
                        self.estado = "jogar"

                    elif botao_ranking.clicado(evento.pos):
                        # o ranking é individual, então precisa de login
                        if not self.logado:
                            self.abrir_login("Faça login para ver o seu ranking.")
                        else:
                            # consulta o banco uma vez, não a cada frame
                            self.top5 = get_top5_pontuacao(self.jogador["id"])
                            self.estado = "rank"

                    elif botao_config.clicado(evento.pos):
                        self.estado = "config"

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
        self.gerenciador_obstaculos.atualizar(self.gerenciador_chao.lista_chaos, self.gerenciador_chao.velocidade)
        self.pontos += chaos_removidos

        self.personagem.atualizar(self.gerenciador_chao.lista_chaos)
        if any(self.personagem.rect.colliderect(o.rect) for o in self.gerenciador_obstaculos.lista):
            self.personagem.vivo = False
        if not self.personagem.vivo:
            self.estado = "gameover"
            # visitantes jogam normalmente, mas a pontuação só é salva com login
            if self.logado:
                salvar_pontuacao(self.jogador["id"], self.pontos)

    def encerrar_jogo(self):
        self.rodando = False
        pygame.quit()
        quit()
