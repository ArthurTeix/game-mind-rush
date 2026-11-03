import math
import pygame
from random import randint

from game.configuracoes import FPS


class PowerUp:
    """Power-up "Fantasma": ao ser coletado, deixa o personagem intangível
    por 5 segundos. Enquanto estiver intangível, o personagem atravessa
    obstáculos sem perder vida, mas continua pegando moedas (e continua
    precisando de chão: cair no vazio ainda é fatal).

    O item aparece flutuando sobre as plataformas, igual às moedas.
    O tempo restante do efeito fica guardado no Personagem (tempo_intangivel)
    e é mostrado no relógio do canto superior direito (ver render.py).
    """
    LARGURA = 55
    ALTURA = 55
    ALTURA_ACIMA = 20
    CHANCE = 60                    # % de chance por plataforma

    DURACAO_SEGUNDOS = 5
    DURACAO_FRAMES = DURACAO_SEGUNDOS * FPS
    AVISO_FRAMES = FPS               # no último segundo o personagem pisca

    _imagem = None

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.LARGURA, self.ALTURA)

    @classmethod
    def criar_sobre_plataforma(cls, rect_chao, evitar=()):
        """Sorteia se nasce um power-up sobre a plataforma.
        'evitar' é uma lista de Rects (moedas, obstáculos) que não podem ficar
        em cima do power-up."""
        if randint(1, 100) > cls.CHANCE:
            return None

        x_min = rect_chao.x
        x_max = rect_chao.right - cls.LARGURA
        if x_min > x_max:
            return None

        x = randint(x_min, x_max)
        y = rect_chao.top - cls.ALTURA - cls.ALTURA_ACIMA
        candidato = cls(x, y)

        area = candidato.rect.inflate(40, 40)
        if any(area.colliderect(r) for r in evitar):
            return None
        return candidato

    @classmethod
    def carregar_imagem(cls):
        """Desenha o fantasminha por código (ainda não existe imagem pronta)."""
        w, h = cls.LARGURA, cls.ALTURA
        imagem = pygame.Surface((w, h), pygame.SRCALPHA)

        def corpo(cor, g):
            # g = quanto o desenho "cresce" (usado para fazer o contorno)
            pygame.draw.circle(imagem, cor, (w // 2, 24), 22 + g)
            pygame.draw.rect(imagem, cor, (5 - g, 24, 44 + 2 * g, 24))
            for cx in (12, w // 2, w - 13):
                pygame.draw.circle(imagem, cor, (cx, 48), 7 + g)

        corpo((90, 190, 240), 2)        # contorno
        corpo((235, 245, 255), 0)       # corpo

        pygame.draw.circle(imagem, (30, 30, 60), (19, 26), 4)   # olhos
        pygame.draw.circle(imagem, (30, 30, 60), (35, 26), 4)
        pygame.draw.circle(imagem, (30, 30, 60), (w // 2, 37), 3)  # boca

        cls._imagem = imagem

    def mover(self, velocidade):
        self.rect.x -= velocidade

    def desenhar(self, tela):
        if PowerUp._imagem is None:
            PowerUp.carregar_imagem()
        # só visual: sobe e desce de leve (a colisão usa o rect parado)
        balanco = int(math.sin(pygame.time.get_ticks() / 200) * 5)
        tela.blit(PowerUp._imagem, (self.rect.x, self.rect.y + balanco))


class GerenciadorPowerUp:
    def __init__(self):
        self._por_chao = {}

    def ignorar(self, chao):
        self._por_chao[chao] = None

    @property
    def lista_powerups(self):
        return [p for p in self._por_chao.values() if p is not None]

    def atualizar(self, lista_chaos, velocidade, evitar=()):
        for item in self.lista_powerups:
            item.mover(velocidade)

        self._por_chao = {c: p for c, p in self._por_chao.items() if c in lista_chaos}

        for chao in lista_chaos:
            if chao not in self._por_chao:
                self._por_chao[chao] = PowerUp.criar_sobre_plataforma(chao.rect, evitar)

    def desenhar(self, tela):
        for item in self.lista_powerups:
            item.desenhar(tela)

    def remover(self, item):
        for chao, atual in self._por_chao.items():
            if atual is item:
                self._por_chao[chao] = None
                break
