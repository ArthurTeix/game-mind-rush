# Arquivo responsável por desenhar e renderizar as telas do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_TITULO, FONTE_PONTOS, TITULO_JOGO
from game.util.cores import cores

def desenhar_menu(tela):
    tela.fill((30, 30, 30))

    texto = FONTE_TITULO.render(TITULO_JOGO, True, cores['branco'])
    rect_texto = texto.get_rect(center=(LARGURA_TELA // 2, (ALTURA_TELA // 2 - 90)))
    tela.blit(texto, rect_texto)

    dica = FONTE_PONTOS.render("Clique para jogar | ESPAÇO para pular | ESC para sair", True, (200, 200, 200))
    rect_dica = dica.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    tela.blit(dica, rect_dica)

    pygame.display.update()


def desenhar_jogo(tela, personagem, gerenciador_chao, pontos):
    tela.fill((135, 206, 235))  # azul céu, só para não ficar tela preta

    gerenciador_chao.desenhar(tela)
    personagem.desenhar(tela)

    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", True, cores['amarelo'])
    tela.blit(texto_pontos, (20, 20))

    pygame.display.update()
