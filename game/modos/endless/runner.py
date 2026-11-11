
import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA
from game.database.db import salvar_pontuacao

from game.modos.endless.personagem import Personagem
from game.modos.endless.chao import GerenciadorChao
from game.modos.endless.obstaculo import GerenciadorObstaculos
from game.modos.endless.moeda import GerenciadorMoeda
from game.modos.endless.powerup import GerenciadorPowerUp

from game.render import desenhar_endless


# Configurações exclusivas do Endless Run
VELOCIDADE_CHAO = 8.5
ESPACO_MINIMO = 150
ESPACO_MAXIMO = 270

ALTURA_PERSONAGEM = 80
LARGURA_PERSONAGEM = 70
X_PERSONAGEM = 150

class EndlessRunner:

    def __init__(self):

        self.pontos = 0
        self.pontuacao_salva = False

# o personagem é criado uma única vez (carrega as imagens);
# a posição real é definida em iniciar_partida()
        self.personagem = Personagem(
            largura_tela=LARGURA_TELA,
            altura_tela=ALTURA_TELA,
            x=X_PERSONAGEM,
            y=0,
            largura=LARGURA_PERSONAGEM,
            altura=ALTURA_PERSONAGEM,
            caminhos_imagens=[
                "./assets/img/personagens/computacao/robo_pos0.png",
                "./assets/img/personagens/computacao/robo_pos1.png",
                "./assets/img/personagens/computacao/robo_pos2.png"
            ]
        )

        self.iniciar_partida()

    def iniciar_partida(self):

        self.pontuacao_salva = False

        self.pontos = 0

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

    def eventos(self, evento):

        if evento.type == pygame.KEYDOWN:

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

    def atualizar(self, jogador=None):

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

        if not self.personagem.vivo:

            if jogador is not None and not self.pontuacao_salva:
                salvar_pontuacao(jogador["id"], self.pontos)
                self.pontuacao_salva = True     

            return False   

        return True

    def desenhar(self, tela):

        desenhar_endless(
            tela,
            self.personagem,
            self.gerenciador_chao,
            self.pontos,
            self.gerenciador_obstaculos,
            self.gerenciador_moeda,
            self.gerenciador_powerup
        )
