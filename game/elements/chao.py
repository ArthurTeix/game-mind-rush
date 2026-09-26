import pygame
from random import randint
from game.util.cores import cores

class Chao:
    def __init__(self, x, y, largura, altura, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade

        self.imagem = pygame.Surface((largura, altura))
        self.imagem.fill(cores['verde'])

        # APENAS QUNADO TIVER IMG
        # self.imagem = pygame.image.load('./img/elementos/chao.png').convert_alpha()
        # self.imagem = pygame.transform.scale(self.imagem, (largura, altura))

    def mover(self):
        """
        TODO:
        - o chão anda para a ESQUERDA, então self.rect.x deve DIMINUIR
        a cada chamada, na velocidade definida em self.velocidade
        """
        self.rect.x -= self.velocidade

    def saiu_da_tela(self):
        return self.rect.right <= 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)
