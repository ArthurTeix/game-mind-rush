import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA
from game.database.db import salvar_pontuacao
from game.util.cores import cores

from game.modos.endless.personagem import Personagem
from game.modos.endless.chao import GerenciadorChao
from game.modos.endless.obstaculo import GerenciadorObstaculos
from game.modos.endless.moeda import GerenciadorMoeda
from game.modos.endless.powerup import GerenciadorPowerUp
from game.modos.endless.personagens import PERSONAGENS
from game.modos.endless.perguntas import SorteadorPerguntas

from game.render import (
    desenhar_endless,
    desenhar_selecao_personagem,
    desenhar_pergunta,
    retangulos_selecao,
    layout_pergunta,
)


# Configurações exclusivas do Endless Run
VELOCIDADE_CHAO = 8.5
ESPACO_MINIMO = 150
ESPACO_MAXIMO = 270

ALTURA_PERSONAGEM = 80
LARGURA_PERSONAGEM = 70
X_PERSONAGEM = 150

FRAMES_FEEDBACK = 75        # quanto tempo o resultado da pergunta fica na tela
FRAMES_MENSAGEM = 180       # quanto tempo o aviso "faça login" fica na tela

TECLAS_ALTERNATIVAS = {
    pygame.K_1: 0, pygame.K_KP1: 0,
    pygame.K_2: 1, pygame.K_KP2: 1,
    pygame.K_3: 2, pygame.K_KP3: 2,
    pygame.K_4: 3, pygame.K_KP4: 3,
}


class EndlessRunner:
    """Estados internos do modo:
        "selecao"  -> tela de escolha do personagem (antes de cada partida)
        "jogando"  -> a corrida
        "pergunta" -> corrida pausada, com a pergunta da moeda na tela
    Para quem usa o runner nada muda: continua chamando eventos(),
    atualizar(jogador) e desenhar(tela); atualizar() devolve False quando
    o personagem morre (game over)."""

    def __init__(self):

        self.pontos = 0
        self.pontuacao_salva = False

        self.estado = "selecao"
        self._jogador = None            # guardado a cada atualizar()
        self.voltar_menu = False        # vira True se o jogador apertar Esc na seleção

        # --- seleção de personagem ---
        self.indice_selecao = 0
        self.personagem_escolhido = PERSONAGENS[0]
        self._rects_selecao = retangulos_selecao(len(PERSONAGENS))
        self._mouse_anterior = pygame.mouse.get_pos()
        self.mensagem_selecao = ""
        self.timer_mensagem = 0

        # --- perguntas ---
        self.sorteador = SorteadorPerguntas(self.personagem_escolhido["id"])
        self.pergunta = None
        self.layout_pergunta = None
        self.resposta = None            # índice da alternativa escolhida
        self.timer_feedback = 0
        self.feedback = None            # (texto, cor)

# o personagem é criado uma única vez; a aparência (cor/imagens) é
# definida quando o jogador escolhe, e a posição em iniciar_partida()
        self.personagem = Personagem(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            x=X_PERSONAGEM,
            y=0,
            largura=LARGURA_PERSONAGEM,
            altura=ALTURA_PERSONAGEM,
            caminhos_imagens=self.personagem_escolhido["imagens"],
            cor=self.personagem_escolhido["cor"]
        )

        self.iniciar_partida()

    def iniciar_partida(self):
        """Prepara uma partida nova. O jogo começa na tela de escolha do
        personagem; a corrida só começa depois que o jogador escolher."""

        self.pontuacao_salva = False

        self.pontos = 0

        self.estado = "selecao"
        self.voltar_menu = False
        self.mensagem_selecao = ""
        self.timer_mensagem = 0
        self.pergunta = None
        self.layout_pergunta = None
        self.resposta = None
        self.feedback = None

        self.gerenciador_chao = GerenciadorChao(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            velocidade=VELOCIDADE_CHAO,
            espaco_minimo=ESPACO_MINIMO,
            espaco_maximo=ESPACO_MAXIMO
        )

        self.gerenciador_obstaculos = GerenciadorObstaculos()
        self.gerenciador_obstaculos.ignorar(
            self.gerenciador_chao.lista_chaos[0]
        )

        self.gerenciador_moeda = GerenciadorMoeda()
        self.gerenciador_moeda.ignorar(
            self.gerenciador_chao.lista_chaos[0]
        )

        self.gerenciador_powerup = GerenciadorPowerUp()
        self.gerenciador_powerup.ignorar(
            self.gerenciador_chao.lista_chaos[0]
        )

        y_inicial = (
            ALTURA_TELA
            - self.gerenciador_chao.altura_do_chao_inicial
            - ALTURA_PERSONAGEM
        )

        self.personagem.resetar(X_PERSONAGEM, y_inicial)

    # ------------------------------------------------------------------
    # seleção de personagem
    # ------------------------------------------------------------------
    def _bloqueado(self, personagem):
        return personagem["requer_login"] and self._jogador is None

    def escolher_personagem(self, indice):
        personagem = PERSONAGENS[indice]

        if self._bloqueado(personagem):
            self.mensagem_selecao = "Faça login para desbloquear este personagem"
            self.timer_mensagem = FRAMES_MENSAGEM
            return

        self.personagem_escolhido = personagem
        self.personagem.trocar_aparencia(personagem["imagens"], personagem["cor"])
        self.sorteador = SorteadorPerguntas(personagem["id"])
        self.estado = "jogando"

    def _eventos_selecao(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.indice_selecao = (self.indice_selecao - 1) % len(PERSONAGENS)

            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.indice_selecao = (self.indice_selecao + 1) % len(PERSONAGENS)

            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.escolher_personagem(self.indice_selecao)

            elif evento.key == pygame.K_ESCAPE:
                self.voltar_menu = True

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, rect in enumerate(self._rects_selecao):
                if rect.collidepoint(evento.pos):
                    self.indice_selecao = i
                    self.escolher_personagem(i)
                    break

    def _atualizar_selecao(self):
        if self.timer_mensagem > 0:
            self.timer_mensagem -= 1
            if self.timer_mensagem == 0:
                self.mensagem_selecao = ""

        # o mouse sobre um cartão também o seleciona
        pos = pygame.mouse.get_pos()
        if pos != self._mouse_anterior:
            self._mouse_anterior = pos
            for i, rect in enumerate(self._rects_selecao):
                if rect.collidepoint(pos):
                    self.indice_selecao = i
                    break

    # ------------------------------------------------------------------
    # perguntas
    # ------------------------------------------------------------------
    def _abrir_pergunta(self):
        self.pergunta = self.sorteador.proxima()
        self.layout_pergunta = layout_pergunta(self.pergunta)
        self.resposta = None
        self.feedback = None
        self.estado = "pergunta"

    def responder(self, indice):
        if self.resposta is not None or indice >= len(self.pergunta["alternativas"]):
            return

        self.resposta = indice

        if indice == self.pergunta["correta"]:
            if self.personagem.vidas < self.personagem.vidas_max:
                self.feedback = ("Correto! +1 vida", cores['verde'])
            else:
                self.feedback = ("Correto! (suas vidas já estão cheias)", cores['verde'])
            self.personagem.ganhar_vida()
        else:
            self.feedback = ("Errou! -1 vida", cores['vermelho'])
            self.personagem.perder_vida(forcar=True)

        self.timer_feedback = FRAMES_FEEDBACK

    def _eventos_pergunta(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in TECLAS_ALTERNATIVAS:
            self.responder(TECLAS_ALTERNATIVAS[evento.key])

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, rect in enumerate(self.layout_pergunta["rects"]):
                if rect.collidepoint(evento.pos):
                    self.responder(i)
                    break

    # ------------------------------------------------------------------
    # laço do jogo
    # ------------------------------------------------------------------
    def eventos(self, evento):

        if self.estado == "selecao":
            self._eventos_selecao(evento)

        elif self.estado == "pergunta":
            self._eventos_pergunta(evento)

        elif evento.type == pygame.KEYDOWN:

            if evento.key in (
                pygame.K_SPACE,
                pygame.K_UP,
                pygame.K_w
            ):
                self.personagem.pular()

            elif evento.key in (
                pygame.K_s,
                pygame.K_DOWN
            ):
                self.personagem.descer()

    def _verificar_fim(self, jogador):
        if not self.personagem.vivo:

            if jogador is not None and not self.pontuacao_salva:
                salvar_pontuacao(jogador["id"], self.pontos)
                self.pontuacao_salva = True

            return False

        return True

    def atualizar(self, jogador=None):

        self._jogador = jogador

        if self.estado == "selecao":
            self._atualizar_selecao()
            return True

        if self.estado == "pergunta":
            # corrida pausada: só conta o tempo do resultado da resposta
            if self.resposta is not None:
                self.timer_feedback -= 1

                if self.timer_feedback <= 0:
                    self.estado = "jogando"
                    self.pergunta = None
                    self.resposta = None
                    return self._verificar_fim(jogador)

            return True

        chaos_removidos = self.gerenciador_chao.atualizar()

        self.gerenciador_obstaculos.atualizar(
            self.gerenciador_chao.lista_chaos,
            self.gerenciador_chao.velocidade
        )

        self.gerenciador_moeda.atualizar(
            self.gerenciador_chao.lista_chaos,
            self.gerenciador_chao.velocidade
        )

        ocupados = [
            o.rect for o in self.gerenciador_obstaculos.lista_obstaculos
        ]

        ocupados += [
            m.rect for m in self.gerenciador_moeda.lista_moeda
        ]

        self.gerenciador_powerup.atualizar(
            self.gerenciador_chao.lista_chaos,
            self.gerenciador_chao.velocidade,
            ocupados
        )

        self.pontos += chaos_removidos

        self.personagem.atualizar(
            self.gerenciador_chao.lista_chaos,
            self.gerenciador_obstaculos,
            self.gerenciador_moeda,
            self.gerenciador_powerup
        )

        # pegou uma moeda: pausa a corrida e faz a pergunta da área escolhida
        # (se morreu neste mesmo frame, não pergunta nada)
        if self.personagem.moeda_coletada:
            self.personagem.moeda_coletada = False

            if self.personagem.vivo:
                self._abrir_pergunta()

        return self._verificar_fim(jogador)

    def desenhar(self, tela):

        if self.estado == "selecao":
            desenhar_selecao_personagem(
                tela,
                PERSONAGENS,
                self.indice_selecao,
                self._jogador,
                self.mensagem_selecao
            )
            return

        desenhar_endless(
            tela,
            self.personagem,
            self.gerenciador_chao,
            self.pontos,
            self.gerenciador_obstaculos,
            self.gerenciador_moeda,
            self.gerenciador_powerup
        )

        if self.estado == "pergunta":
            desenhar_pergunta(
                tela,
                self.pergunta,
                self.layout_pergunta,
                self.personagem_escolhido["nome"],
                self.personagem_escolhido["cor"],
                self.resposta,
                self.feedback
            )
