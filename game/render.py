# Arquivo responsável por desenhar e renderizar as telas do jogo
# (o pygame.display.update() é chamado uma única vez por frame, no motor.py)

from game.util.cores import cores
from game.ui.logo import logo_menu
from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_TITULO, FONTE_PONTOS, imagem_menu, imagem_bg_rank, imagem_sair_ranking, imagem_bg_jogo, rect_sair_ranking, mensagem_gameover, imagem_gameover
from game.ui.botao import botao_jogar, botao_modos, botao_config, botao_ranking, botao_sair, botao_reiniciar, botao_sair_gameover, botao_menu

def desenhar_menu(tela, jogador=None):
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


def desenhar_gameover(tela, imagem_menu, mensagem_gameover):
    tela.fill((255, 0, 0))
    tela.blit(imagem_menu, (0, 0))

    rect = mensagem_gameover.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2.5))
    tela.blit(mensagem_gameover, rect)

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
