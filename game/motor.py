# Arquivo responsável por administrar o funcionamento do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FULLSCREEN, FPS
from game.database.db import criar_tabelas, get_top5_pontuacao
from game.render import desenhar_menu, desenhar_gameover_endless, desenhar_ranking, desenhar_modos, desenhar_rogue, rect_sair_rank
from game.ui.botao import botao_jogar, botao_conta, botao_ranking, botao_sair, botao_reiniciar_endless, botao_sair_gameover_endless, botao_menu_endless, botao_modo1, botao_modo2
from game.ui.conta import TelaConfig, TelaLogin, TelaCadastro
from game.render import img_gameover_endless, msg_gameover_endless
from game.modos.endless.runner import EndlessRunner

ESTADOS_CONTA = ("conta", "login", "cadastro")

class Motor:
    def __init__(self):
        pygame.init()
        
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
        self.endless = EndlessRunner()
        self.origem_login = "menu"   # para onde o botão "Voltar" do login leva

        # telas de conta
        self.tela_config = TelaConfig()
        self.tela_login = TelaLogin()
        self.tela_cadastro = TelaCadastro()

    @property
    def logado(self):
        """True se há um jogador logado. Use para liberar conteúdo exclusivo (ex.: personagem)."""
        return self.jogador is not None


    def jogo(self):
        while self.rodando:
            self.watch.tick(FPS)

            self.capturar_eventos()

            if self.estado == "menu":
                desenhar_menu(self.tela, self.jogador)

            elif self.estado == "jogar":
                desenhar_modos(self.tela)

            elif self.estado == "gameover_endless":
                desenhar_gameover_endless(self.tela, img_gameover_endless, msg_gameover_endless)

            elif self.estado == "rank":
                desenhar_ranking(self.tela, self.top5)

            elif self.estado == "conta":
                self.tela_config.desenhar(self.tela, self.jogador)

            elif self.estado == "login":
                self.tela_login.desenhar(self.tela)

            elif self.estado == "cadastro":
                self.tela_cadastro.desenhar(self.tela)

            elif self.estado == "rogue":
                desenhar_rogue(self.tela)

            elif self.estado == "endlessrun":
               
                vivo = self.endless.atualizar(self.jogador)

                if not vivo:
                    self.estado = "gameover_endless"

                self.endless.desenhar(self.tela)

            pygame.display.flip()

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
        if self.estado == "conta":
            acao = self.tela_config.tratar_evento(evento, self.jogador)

            if acao == "login":
                self.abrir_login(origem="conta")
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
                self.abrir_login("Conta criada com sucesso!", origem="conta", sucesso=True)
                # já preenche o usuário e deixa o cursor na senha
                self.tela_login.campo_usuario.texto = self.tela_cadastro.usuario_criado
                self.tela_login.focar_campo(self.tela_login.campo_senha)
            elif acao == "voltar":
                self.estado = "conta"

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

            if self.estado == "endlessrun":
                 self.endless.eventos(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado == "menu":
                    if botao_jogar.clicado(evento.pos):
                        # qualquer pessoa pode jogar, logada ou não
                       self.estado = "jogar"

                    elif botao_ranking.clicado(evento.pos):
                        # o ranking é individual, então precisa de login
                        if not self.logado:
                            self.abrir_login("Faça login para ver o seu ranking.")
                        else:
                            # consulta o banco uma vez, não a cada frame
                            self.top5 = get_top5_pontuacao(self.jogador["id"])
                            self.estado = "rank"

                    elif botao_conta.clicado(evento.pos):
                        self.estado = "conta"

                    elif botao_sair.clicado(evento.pos):
                        self.rodando = False

                elif self.estado == "rank":
                    if rect_sair_rank.collidepoint(evento.pos):
                        self.estado = "menu"

                elif self.estado == "jogar":
                    if botao_modo1.clicado(evento.pos):
                        self.endless.iniciar_partida()
                        self.estado = "endlessrun"
                    elif botao_modo2.clicado(evento.pos):
                        self.estado = "rogue"

                elif self.estado == "gameover_endless":
                    if botao_reiniciar_endless.clicado(evento.pos):
                        self.endless.iniciar_partida()
                        self.estado = "endlessrun"
                    elif botao_menu_endless.clicado(evento.pos):
                        self.estado = "menu"
                    elif botao_sair_gameover_endless.clicado(evento.pos):
                        self.rodando = False

    def encerrar_jogo(self):
        self.rodando = False
        pygame.quit()
        quit()
