import pygame
from game.configuracoes import LARGURA_TELA, ALTURA_TELA


class Botao:
    def __init__(self, imagem_inicial, centro=(0, 0), imagem_hover=None):
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


def centralizar_em_linha(lista_botoes, y, espaco=40):
    """
    Posiciona uma lista de botões em fileira horizontal, centralizada
    como GRUPO na tela (não cada um individualmente), com espaçamento
    igual entre eles. Funciona em qualquer resolução porque usa
    LARGURA_TELA para calcular o ponto de partida.
    """
    largura_total = sum(botao.rect.width for botao in lista_botoes)
    largura_total += espaco * (len(lista_botoes) - 1)

    x_atual = (LARGURA_TELA - largura_total) // 2

    for botao in lista_botoes:
        botao.rect.centerx = x_atual + botao.rect.width // 2
        botao.rect.centery = y
        x_atual += botao.rect.width + espaco


# criação de botões
botao_jogar = Botao("./img/botoes/JOGARMR.png")
botao_modos = Botao("./img/botoes/MODOSMR.png")
botao_config = Botao("./img/botoes/CONFIGMR.png")
botao_ranking = Botao("./img/botoes/RANKINGMR.png")
botao_sair = Botao("./img/botoes/SAIRMR.png")

# posiciona os botões do menu centralizado
Y_BOTOES_MENU = int(ALTURA_TELA * 0.85)
centralizar_em_linha(
    [botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair],
    y=Y_BOTOES_MENU
)

# botão de reiniciar (tela de game over) fica centralizado sozinho por qnquanto que não adicionam os outros
botao_reiniciar = Botao(
    "./img/botoes/REINICIARMR.png",
    centro=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.85))
)
