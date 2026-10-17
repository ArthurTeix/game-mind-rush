import pygame
from random import randint

class Moeda:
    LARGURA = 50
    ALTURA = 50
    ALTURA_ACIMA = 20 
    CHANCE = 70
    _imagem_moeda = None

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.LARGURA, self.ALTURA)

    @classmethod
    def criar_sobre_plataforma(cls, rect_chao):
        if randint(1, 100) > cls.CHANCE:
            return None

        x_min = rect_chao.x
        x_max = rect_chao.right - cls.LARGURA
        if x_min > x_max:
            return None

        x = randint(x_min, x_max)
        y = rect_chao.top - cls.ALTURA - cls.ALTURA_ACIMA
        return cls(x, y)

    @classmethod
    def carregar_imagem(cls):
        imagem = pygame.image.load('./img/elementos/moeda.png').convert_alpha()
        cls._imagem_moeda = pygame.transform.scale(imagem, (cls.LARGURA, cls.ALTURA))

    def mover(self, velocidade):
        self.rect.x -= velocidade

    def desenhar(self, tela):
        if Moeda._imagem_moeda is None:
            Moeda.carregar_imagem()
        tela.blit(Moeda._imagem_moeda, self.rect)

class GerenciadorMoeda:
    def __init__(self):
        self._por_chao = {}

    def ignorar(self, chao):
        self._por_chao[chao] = None

    @property
    def lista_moeda(self):
        return [c for c in self._por_chao.values() if c is not None]

    def atualizar(self, lista_chaos, velocidade):
        for item in self.lista_moeda:
            item.mover(velocidade)

        self._por_chao = {c: i for c, i in self._por_chao.items() if c in lista_chaos}

        for chao in lista_chaos:
            if chao not in self._por_chao:
                self._por_chao[chao] = Moeda.criar_sobre_plataforma(chao.rect)

    def desenhar(self, tela):
        for item in self.lista_moeda:
            item.desenhar(tela)

    def remover(self, item):
        for chao, atual in self._por_chao.items():
            if atual is item:
                self._por_chao[chao] = None
                break