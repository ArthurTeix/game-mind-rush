# Arquivo responsável por desenhar e renderizar as telas do jogo

import pygame
from game.ui.botao import botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair, botao_reiniciar
from game.ui.logo import logo_menu
from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_TITULO, FONTE_PONTOS


def desenhar_menu(tela):
    tela.fill((30, 30, 30))
    logo_menu.desenhar(tela)
    botao_jogar.desenhar(tela)
    botao_modos.desenhar(tela)
    botao_config.desenhar(tela)
    botao_ranking.desenhar(tela)
    botao_sair.desenhar(tela)
    pygame.display.update()


def desenhar_jogo(tela, personagem, gerenciador_chao, pontos):
    tela.fill((135, 206, 235))  # azul céu, só para não ficar tela preta

    gerenciador_chao.desenhar(tela)
    personagem.desenhar(tela)

    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", True, cores['amarelo'])
    tela.blit(texto_pontos, (20, 20))

    pygame.display.update()

def desenhar_gameover(tela, imagem_gameover):
    tela.fill((255, 105, 180))

    rect_imagem = imagem_gameover.get_rect(center=(960, 337))
    tela.blit(imagem_gameover, rect_imagem)

    botao_reiniciar.desenhar(tela)

    pygame.display.update()
