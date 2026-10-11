# Arquivo responsável por desenhar e renderizar as telas do jogo
# (o pygame.display.update() é chamado uma única vez por frame, no motor.py)

import pygame
from game.util.cores import cores
from game.ui.logo import logo_menu
from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_TITULO, FONTE_PONTOS
from game.ui.botao import botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair, botao_reiniciar, botao_sair_gameover, botao_menu

CAMINHO_BG_RANK = './img/fundos/bg_ranking.png'
imagem_bg_rank = pygame.image.load(CAMINHO_BG_RANK)
imagem_bg_rank = pygame.transform.scale(imagem_bg_rank, (LARGURA_TELA, ALTURA_TELA))

CAMINHO_SAIR_RANKING = './img/botoes/sair_ranking.png'
imagem_sair_ranking = pygame.image.load(CAMINHO_SAIR_RANKING)
imagem_sair_ranking = pygame.transform.scale(imagem_sair_ranking, (200, 200))
rect_sair_ranking = imagem_sair_ranking.get_rect(topleft=(110, 20))

CAMINHO_BG_JOGO = './img/fundos/bg_jogo.png'
imagem_bg_jogo = pygame.image.load(CAMINHO_BG_JOGO)
imagem_bg_jogo = pygame.transform.scale(imagem_bg_jogo, (LARGURA_TELA, ALTURA_TELA))

CAMINHO_MENU = './img/fundos/MENU.png'
imagem_menu = pygame.image.load(CAMINHO_MENU)
imagem_menu = pygame.transform.scale(imagem_menu, (LARGURA_TELA, ALTURA_TELA))

def desenhar_menu(tela, imagem_menu, jogador=None):
    tela.blit(imagem_menu, (0, 0))

    if jogador:
        saudacao = FONTE_TITULO.render(f"Olá, {jogador['usuario']}", True, cores['azul-jogo'])
        tela.blit(saudacao, saudacao.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.07))))

    logo_menu.desenhar(tela)
    botao_jogar.desenhar(tela)
    botao_modos.desenhar(tela)
    botao_config.desenhar(tela)
    botao_ranking.desenhar(tela)
    botao_sair.desenhar(tela)


def desenhar_jogo(tela, personagem, gerenciador_chao, pontos):
    tela.blit(imagem_bg_jogo, (0, 0))

    gerenciador_chao.desenhar(tela)
    personagem.desenhar(tela)

    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", True, cores['azul-jogo'])
    tela.blit(texto_pontos, (20, 20))


def desenhar_gameover(tela, imagem_menu):
    tela.blit(imagem_menu, (0, 0))

    rect_imagem = imagem_menu.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    tela.blit(imagem_menu, rect_imagem)

    botao_reiniciar.desenhar(tela)
    botao_menu.desenhar(tela)
    botao_sair_gameover.desenhar(tela)


def desenhar_ranking(tela, top5):
    tela.blit(imagem_bg_rank, (0, 0))

    x_caixa = int(LARGURA_TELA * 0.521)
    y_primeira = int(ALTURA_TELA * 0.393)
    espacamento_ranking = int(ALTURA_TELA * 0.0943)

    for i, pontos in enumerate(top5):
        ranking = FONTE_TITULO.render(f'{pontos}', 1, cores['rosa'])
        rect_rank_text = ranking.get_rect(
            center=(x_caixa, y_primeira + espacamento_ranking * i)
        )
        tela.blit(ranking, rect_rank_text)

    tela.blit(imagem_sair_ranking, rect_sair_ranking)
