import pygame
from game.configuracoes import LARGURA_TELA, ALTURA_TELA


class Botao:
    def __init__(self, imagem_inicial, centro=(0, 0), imagem_hover=None):
        self.imagem = pygame.image.load(imagem_inicial)
        self.imagem_hover = pygame.image.load(imagem_hover) if imagem_hover else self.imagem
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

def centralizar_em_coluna(lista_botoes, x, espaco=40):
    altura_total = sum(botao.rect.height for botao in lista_botoes)
    altura_total += espaco * (len(lista_botoes) - 1)

    y_atual = (ALTURA_TELA - altura_total) // 2

    for botao in lista_botoes:
        botao.rect.centerx = x
        botao.rect.centery = y_atual + botao.rect.height // 2
        y_atual += botao.rect.height + espaco


# criação de botões
botao_jogar = Botao("./assets/img/botoes/botoes_menu/jogar.png", imagem_hover="./assets/img/botoes/botoes_menu/jogar_hover.png")
botao_modos = Botao("./assets/img/botoes/botoes_menu/modos.png", imagem_hover="./assets/img/botoes/botoes_menu/modos_hover.png")
botao_conta = Botao("./assets/img/botoes/botoes_menu/conta.png", imagem_hover="./assets/img/botoes/botoes_menu/conta_hover.png")
botao_ranking = Botao("./assets/img/botoes/botoes_menu/ranking.png", imagem_hover="./assets/img/botoes/botoes_menu/ranking_hover.png")
botao_sair = Botao("./assets/img/botoes/botoes_menu/sair.png", imagem_hover="./assets/img/botoes/botoes_menu/sair_hover.png")
botao_reiniciar_endless = Botao("./assets/img/botoes/botoes_menu/jnovamente.png", imagem_hover="./assets/img/botoes/botoes_menu/jnovamente_hover.png")
botao_sair_gameover_endless = Botao("./assets/img/botoes/botoes_menu/sair_go.png", imagem_hover="./assets/img/botoes/botoes_menu/sair_go_hover.png")
botao_menu_endless = Botao("./assets/img/botoes/botoes_menu/menu.png", imagem_hover="./assets/img/botoes/botoes_menu/menu_hover.png")

botao_modo1 = Botao("./assets/img/botoes/botoes_modos/modo1.png", imagem_hover="./assets/img/botoes/botoes_modos/modo1_hover.png")
botao_modo2 = Botao("./assets/img/botoes/botoes_modos/modo2.png", imagem_hover="./assets/img/botoes/botoes_modos/modo2_hover.png")

# posiciona os botões do menu centralizado
Y_BOTOES_MENU = int(ALTURA_TELA * 0.85)
centralizar_em_linha(
    [botao_jogar, botao_conta, botao_ranking, botao_sair],
    y=Y_BOTOES_MENU
)

# posiciona os botões do game over centralizado
Y_BOTOES_GAMEOVER = int(ALTURA_TELA * 0.85)
centralizar_em_linha(
    [botao_reiniciar_endless, botao_menu_endless, botao_sair_gameover_endless],
    y=Y_BOTOES_GAMEOVER
)

# posiciona os botões da tela modos centralizado verticalmente
X_BOTOES_MODOS = int(LARGURA_TELA // 2)
centralizar_em_coluna(
    [botao_modo1, botao_modo2],
    x=X_BOTOES_MODOS
)