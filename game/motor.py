# Arquivo responsável por administrar o funcionamento do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FULLSCREEN, FPS
from game.database.db import criar_tabelas, get_top5_pontuacao
from game.render import desenhar_menu, desenhar_gameover_endless, desenhar_ranking, desenhar_modos, rect_sair_rank
from game.ui.botao import botao_jogar, botao_conta, botao_ranking, botao_sair, botao_reiniciar_endless, botao_sair_gameover_endless, botao_menu_endless, botao_modo1, botao_modo2
from game.ui.conta import TelaConfig, TelaLogin, TelaCadastro, TelaAlterar, TelaExcluir  
from game.render import img_gameover_endless, msg_gameover_endless
from game.modos.endless.runner import EndlessRunner
from game.modos.rogue.runner import RogueLike

ESTADOS_CONTA = ("conta", "login", "cadastro", "alterar", "excluir")

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

        self.jogador = None
        self.endless = EndlessRunner()
        self.rogue = RogueLike(self.tela)
        self.origem_login = "menu"   

        # telas de conta
        self.tela_config = TelaConfig()
        self.tela_login = TelaLogin()
        self.tela_cadastro = TelaCadastro()
        self.tela_alterar = None
        self.tela_excluir = None

    @property
    def logado(self):
        """True se há um jogador logado. Use para liberar conteúdo exclusivo (ex.: personagem)."""
        return self.jogador is not None


    def jogo(self):
        while self.rodando:
            dt = min(self.watch.tick(FPS) / 1000, 0.05)

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

            elif self.estado == "alterar":
                self.tela_alterar.desenhar(self.tela)

            elif self.estado == "excluir":
                self.tela_excluir.desenhar(self.tela)

            elif self.estado == "endlessrun":
               
                vivo = self.endless.atualizar(self.jogador)

                if not vivo:
                    self.estado = "gameover_endless"

                self.endless.desenhar(self.tela)

            elif self.estado == "rogue":

                vivo = self.rogue.atualizar(dt)

                if not vivo:
                    self.estado = "gameover_rogue"

                self.rogue.desenhar()

            elif self.estado == "gameover_rogue":
                self.rogue.desenhar()

            pygame.display.flip()

    # ------------------------------------------------------------ navegação

    def abrir_login(self, mensagem=None, origem="menu", sucesso=False):
        self.origem_login = origem
        self.tela_login.resetar(mensagem, sucesso)
        self.estado = "login"

    def abrir_cadastro(self):
        self.tela_cadastro.resetar()
        self.estado = "cadastro"

    def abrir_alterar(self):
        """Cria uma tela de alteração limpa para o jogador logado e abre."""
        self.tela_alterar = TelaAlterar(self.jogador)
        self.estado = "alterar"

    def abrir_excluir(self):
        """Cria uma tela de exclusão limpa para o jogador logado e abre."""
        self.tela_excluir = TelaExcluir(self.jogador)
        self.estado = "excluir"

    def tratar_evento_conta(self, evento):
        """Eventos das telas de configuração, login, cadastro, alteração e exclusão."""
        if self.estado == "conta":
            acao = self.tela_config.tratar_evento(evento, self.jogador)

            if acao == "login":
                self.abrir_login(origem="conta")
            elif acao == "cadastro":
                self.abrir_cadastro()
            elif acao == "alterar":          
                self.abrir_alterar()
            elif acao == "excluir":          
                self.abrir_excluir()
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
                self.tela_login.campo_usuario.texto = self.tela_cadastro.usuario_criado
                self.tela_login.focar_campo(self.tela_login.campo_senha)
            elif acao == "voltar":
                self.estado = "conta"

        elif self.estado == "alterar":
            acao = self.tela_alterar.tratar_evento(evento)

            if acao in ("alterado", "voltar"):
                self.estado = "conta"

        elif self.estado == "excluir":
            acao = self.tela_excluir.tratar_evento(evento)

            if acao == "excluida":
                self.jogador = None          
                self.estado = "menu"
            elif acao == "voltar":
                self.estado = "conta"

    def capturar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.encerrar_jogo()

            if self.estado in ESTADOS_CONTA:
                self.tratar_evento_conta(evento)
                continue

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.encerrar_jogo()

            if self.estado == "endlessrun":
                 self.endless.eventos(evento)

            if self.estado == "rogue":
                 self.rogue.eventos(evento)

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
                        self.rogue.iniciar_partida()
                        self.estado = "rogue"

                elif self.estado == "gameover_endless":
                    if botao_reiniciar_endless.clicado(evento.pos):
                        self.endless.iniciar_partida()
                        self.estado = "endlessrun"
                    elif botao_menu_endless.clicado(evento.pos):
                        self.estado = "menu"
                    elif botao_sair_gameover_endless.clicado(evento.pos):
                        self.rodando = False

                if self.estado == "rogue":
                    self.rogue.eventos(evento)

            elif self.estado == "gameover_rogue":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        self.rogue.iniciar_partida()
                        self.estado = "rogue"

    def encerrar_jogo(self):
        self.rodando = False
        pygame.quit()
        quit()
