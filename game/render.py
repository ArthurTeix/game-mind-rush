# Arquivo responsável por desenhar e renderizar as telas do jogo
# (o pygame.display.update() é chamado uma única vez por frame, no motor.py)

import math
import pygame

from game.util.cores import cores
from game.modos.endless.powerup import PowerUp
from game.ui.logo import logo_menu
from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_PONTOS, FONTE_MENSAGEM, FONTE_RELOGIO, FPS, img_menu, img_bg_rank, img_sair_rank, img_bg_endless, rect_sair_rank, msg_gameover_endless, img_gameover_endless, img_estrela, img_coracao
from game.ui.botao import botao_jogar, botao_conta, botao_ranking, botao_sair, botao_reiniciar_endless, botao_sair_gameover_endless, botao_menu_endless, botao_modo1, botao_modo2

def desenhar_menu(tela, jogador=None):
    tela.blit(img_menu, (0, 0))

    if jogador:
        saudacao = FONTE_MENSAGEM.render(f"Oi, {jogador['usuario']}", True, cores['verde-logo'])
        tela.blit(saudacao, saudacao.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.265))))

    logo_menu.desenhar(tela)
    botao_jogar.desenhar(tela)
    botao_conta.desenhar(tela)
    botao_ranking.desenhar(tela)
    botao_sair.desenhar(tela)


def desenhar_relogio_intangibilidade(tela, frames_restantes):
    """Relógio do power-up fantasma, no canto superior direito:
    um anel que vai esvaziando e o número de segundos que faltam."""
    raio = 55
    centro = (LARGURA_TELA - raio - 30, raio + 25)

    fracao = max(0.0, min(1.0, frames_restantes / PowerUp.DURACAO_FRAMES))
    segundos = math.ceil(frames_restantes / FPS)
    ultimo_segundo = frames_restantes < PowerUp.AVISO_FRAMES
    cor = cores['vermelho'] if ultimo_segundo else cores['azul-ceu']

    pygame.draw.circle(tela, cores['cinza-menu'], centro, raio)

    # fatia que representa o tempo restante (começa no topo, sentido horário)
    if fracao > 0:
        passos = max(2, int(60 * fracao))
        pontos = [centro]
        for i in range(passos + 1):
            angulo = -math.pi / 2 + 2 * math.pi * fracao * i / passos
            pontos.append((centro[0] + raio * math.cos(angulo),
                           centro[1] + raio * math.sin(angulo)))
        pygame.draw.polygon(tela, cor, pontos)

    # miolo escuro (transforma a fatia em anel) e borda
    pygame.draw.circle(tela, cores['cinza-menu'], centro, raio - 12)
    pygame.draw.circle(tela, cores['branco'], centro, raio, 4)

    texto = FONTE_RELOGIO.render(str(segundos), True, cores['branco'])
    tela.blit(texto, texto.get_rect(center=centro))


def desenhar_endless(tela, personagem, gerenciador_chao, pontos, gerenciador_obstaculos, gerenciador_moeda, gerenciador_powerup=None):
    tela.blit(img_bg_endless, (0, 0))

    gerenciador_chao.desenhar(tela)
    gerenciador_obstaculos.desenhar(tela)
    gerenciador_moeda.desenhar(tela)
    if gerenciador_powerup is not None:
        gerenciador_powerup.desenhar(tela)
    personagem.desenhar(tela)

    tela.blit(img_estrela, (20, 20))
    texto_pontos = FONTE_PONTOS.render(f"{pontos}", True, cores['amarelo'])
    tela.blit(texto_pontos, (110, 30))

    for i in range(max(personagem.vidas, 0)):
        tela.blit(img_coracao, (20 + i * 40, 100))

    if personagem.intangivel:
        desenhar_relogio_intangibilidade(tela, personagem.tempo_intangivel)

def desenhar_gameover_endless(tela, img_gameover_endless, msg_gameover_endless):
    tela.fill((255, 0, 0))
    tela.blit(img_gameover_endless, (0, 0))

    rect = msg_gameover_endless.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2.5))
    tela.blit(msg_gameover_endless, rect)

    botao_reiniciar_endless.desenhar(tela)
    botao_menu_endless.desenhar(tela)
    botao_sair_gameover_endless.desenhar(tela)

def desenhar_ranking(tela, top5):
    tela.blit(img_bg_rank, (0, 0))

    x_caixa = int(LARGURA_TELA * 0.521)
    y_primeira = int(ALTURA_TELA * 0.393)
    espacamento_ranking = int(ALTURA_TELA * 0.0943)

    for i, pontos in enumerate(top5):
        ranking = FONTE_MENSAGEM.render(f'{pontos}', 1, cores['verde-logo'])
        rect_rank_text = ranking.get_rect(
            center=(x_caixa, y_primeira + espacamento_ranking * i)
        )
        tela.blit(ranking, rect_rank_text)

    tela.blit(img_sair_rank, rect_sair_rank)

def desenhar_modos(tela):
    tela.fill((0, 255, 0))

    botao_modo1.desenhar(tela)
    botao_modo2.desenhar(tela)

def desenhar_rogue(tela):
    tela.fill((255, 0, 0))