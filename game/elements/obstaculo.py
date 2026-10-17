import pygame
from random import randint

class Obstaculo:
    LARGURA = 110
    ALTURA = 50
    MARGEM_INICIO = 140
    MARGEM_FIM = 160
    AFUNDAR = 2
    CHANCE = 75
    _imagem_obstaculo = None

    def __init__ (self, x, y):
        self.rect = pygame.Rect(x, y, self.LARGURA, self.ALTURA)

    @classmethod
    def criar_sobre_plataforma (cls, rect_chao):
        if randint(1,100) > cls.CHANCE:
            return None

        x_min = rect_chao.x + cls.MARGEM_INICIO
        x_max = rect_chao.right - cls.MARGEM_FIM - cls.LARGURA

        if x_max < x_min:
            return None

        x = randint(x_min, x_max)
        y = rect_chao.top - cls.ALTURA + cls.AFUNDAR
        return cls(x,y)

    @classmethod
    def carregar_imagem(cls):
        imagem_obstaculo = pygame.image.load('./img/elementos/obstaculo.png').convert()
        imagem_obstaculo.set_colorkey(imagem_obstaculo.get_at((0, 0)))
        imagem_obstaculo = imagem_obstaculo.convert_alpha()
        imagem_obstaculo = imagem_obstaculo.subsurface(imagem_obstaculo.get_bounding_rect()).copy()
        cls._imagem_obstaculo = pygame.transform.scale(imagem_obstaculo, (cls.LARGURA, cls.ALTURA))

    def mover(self, velocidade):
        self.rect.x -= velocidade

    def desenhar(self, tela):
        if Obstaculo._imagem_obstaculo is None:
            Obstaculo.carregar_imagem()
        tela.blit(Obstaculo._imagem_obstaculo, self.rect)

class GerenciadorObstaculos:
    def __init__(self):
        self._por_chao = {}

    # indica se um chão ainda não possui um obstáculo
    def ignorar(self, chao):
        self._por_chao[chao] = None

    @property
    def lista_obstaculos(self):
        return [o for o in self._por_chao.values() if o is not None]    

    
    def atualizar(self, lista_chaos, velocidade):
        for obstaculo in self.lista_obstaculos:
            obstaculo.mover(velocidade)

        self._por_chao = {
            c: o for c, o in self._por_chao.items()
            if c in lista_chaos
        }

        for chao in lista_chaos:
            if chao not in self._por_chao:
                self._por_chao[chao] = Obstaculo.criar_sobre_plataforma(
                    chao.rect
                )


    def desenhar(self, tela):
        for obstaculo in self.lista_obstaculos:
            obstaculo.desenhar(tela)


    def remover(self, obstaculo):
        for chao, atual in self._por_chao.items():
            if atual is obstaculo:
                self._por_chao[chao] = None
                break