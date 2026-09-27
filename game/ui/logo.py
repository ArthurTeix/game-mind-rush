import pygame
from game.configuracoes import LARGURA_TELA, ALTURA_TELA


class Logo:
    def __init__(self, caminho_imagem, centro):
        self.imagem = pygame.image.load(caminho_imagem)
        self.rect = self.imagem.get_rect(center=centro)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


logo_menu = Logo(
    "./img/logo/LOGOMR.png",
    centro=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.35))
)
