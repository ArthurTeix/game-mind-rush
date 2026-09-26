# Arquivo responsável por desenhar e renderizar as telas do jogo

import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_TITULO, FONTE_PONTOS


def desenhar_menu(tela):
    tela.fill((30, 30, 30))

    texto = FONTE_TITULO.render("Mind Rush", True, (255, 255, 255))
    tela.blit(
        texto,
        (500, 300)
    )

    dica = FONTE_PONTOS.render("Clique para jogar | ESPAÇO para pular | ESC para sair", True, (200, 200, 200))
    tela.blit(
        dica,
        (150, 600)
    )

    pygame.display.update()


def desenhar_jogo(tela, personagem, gerenciador_chao, pontos):
    tela.fill((135, 206, 235))  # azul céu, só para não ficar tela preta

    gerenciador_chao.desenhar(tela)
    personagem.desenhar(tela)

    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", True, (255, 255, 0))
    tela.blit(texto_pontos, (20, 20))

    pygame.display.update()
