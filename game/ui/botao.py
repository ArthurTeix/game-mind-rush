import pygame


class Botao:
    def __init__(self, imagem_inicial, centro, imagem_hover=None):
        self.imagem = pygame.image.load(imagem_inicial)
        self.imagem_hover = pygame.image.load(imagem_hover).convert_alpha() if imagem_hover else self.imagem
        self.rect = self.imagem.get_rect(center=centro)

    def desenhar(self, tela):
        tela.blit(self.obter_imagem_atual(), self.rect)

    def obter_imagem_atual(self):
        return self.imagem_hover if self.esta_em_hover() else self.imagem

    def esta_em_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def clicado(self, pos_clique):
        return self.rect.collidepoint(pos_clique)


botao_jogar = Botao("./img/botoes/JOGARMR.png", centro=(60, 840))
botao_modos = Botao("./img/botoes/MODOSMR.png", centro=(424, 840))
botao_config = Botao("./img/botoes/CONFIGMR.png", centro=(788, 840))
botao_ranking = Botao("./img/botoes/RANKINGMR.png", centro=(1152, 840))
botao_sair = Botao("./img/botoes/SAIRMR.png", centro=(1516, 840))
botao_reiniciar = Botao("./img/botoes/REINICIARMR.png", centro=(940, 840))