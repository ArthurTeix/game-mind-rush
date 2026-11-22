# Arquivo responsável por desenhar e renderizar as telas do jogo
# (o pygame.display.update() é chamado uma única vez por frame, no motor.py)

import math
import pygame

from game.util.cores import cores
from game.modos.endless.powerup import PowerUp
from game.modos.endless.personagens import obter_preview
from game.ui.logo import logo_menu
from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_PONTOS, FONTE_MENSAGEM, FONTE_RELOGIO, FONTE_TEXTO, FONTE_TEXTO_GRANDE, FONTE_TEXTO_PEQUENA, FPS, img_menu, img_bg_rank, img_sair_rank, img_bg_endless, rect_sair_rank, msg_gameover_endless, img_gameover_endless, img_estrela, img_coracao
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

# ----------------------------------------------------------------------
# escolha de personagem
# ----------------------------------------------------------------------
def _quebrar_linhas(texto, fonte, largura_max):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def retangulos_selecao(quantidade):
    """Posição dos cartões da tela de escolha (usada para desenhar e para os cliques)."""
    margem = int(LARGURA_TELA * 0.05)
    espaco = int(LARGURA_TELA * 0.02)
    largura = (LARGURA_TELA - 2 * margem - espaco * (quantidade - 1)) // quantidade
    largura = min(largura, 260)
    altura = min(int(largura * 1.55), int(ALTURA_TELA * 0.6))

    total = largura * quantidade + espaco * (quantidade - 1)
    x0 = (LARGURA_TELA - total) // 2
    y = int(ALTURA_TELA * 0.27)

    return [pygame.Rect(x0 + i * (largura + espaco), y, largura, altura) for i in range(quantidade)]


def _desenhar_cadeado(tela, centro, tamanho):
    cx, cy = centro
    largura = tamanho
    altura = int(tamanho * 0.75)
    corpo = pygame.Rect(0, 0, largura, altura)
    corpo.center = (cx, cy + int(tamanho * 0.15))
    argola = pygame.Rect(0, 0, int(largura * 0.65), int(largura * 0.7))
    argola.midbottom = (cx, corpo.top + 4)

    pygame.draw.arc(tela, (200, 200, 200), argola, 0, math.pi, max(4, tamanho // 8))
    pygame.draw.rect(tela, (200, 200, 200), corpo, border_radius=6)
    pygame.draw.circle(tela, (50, 50, 50), corpo.center, max(3, tamanho // 9))


def desenhar_selecao_personagem(tela, personagens, indice, jogador=None, mensagem=""):
    tela.blit(img_bg_endless, (0, 0))

    escurecer = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    escurecer.fill((0, 0, 0, 160))
    tela.blit(escurecer, (0, 0))

    titulo = FONTE_MENSAGEM.render("Escolha seu personagem", True, cores['branco'])
    tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.13))))

    subtitulo = FONTE_TEXTO.render("As perguntas da partida serão da área do personagem escolhido", True, (200, 200, 200))
    tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.20))))

    for i, (personagem, rect) in enumerate(zip(personagens, retangulos_selecao(len(personagens)))):
        bloqueado = personagem["requer_login"] and jogador is None
        selecionado = (i == indice)

        pygame.draw.rect(tela, (35, 35, 35) if bloqueado else (45, 45, 45), rect, border_radius=14)
        borda = cores['azul-jogo'] if selecionado else (110, 110, 110)
        pygame.draw.rect(tela, borda, rect, 5 if selecionado else 2, border_radius=14)

        # imagem do personagem (silhueta cinza se estiver bloqueado)
        largura_prev = int(rect.width * 0.45)
        altura_prev = int(largura_prev * 80 / 70)
        preview = obter_preview(personagem, largura_prev, altura_prev)
        if bloqueado:
            preview = pygame.mask.from_surface(preview).to_surface(setcolor=(70, 70, 70, 255), unsetcolor=(0, 0, 0, 0))
        pos_prev = preview.get_rect(midtop=(rect.centerx, rect.y + 30))
        tela.blit(preview, pos_prev)

        if bloqueado:
            _desenhar_cadeado(tela, pos_prev.center, max(24, largura_prev // 2))

        # nome
        cor_nome = (150, 150, 150) if bloqueado else cores['branco']
        y_nome = pos_prev.bottom + 22
        for linha in _quebrar_linhas(personagem["nome"], FONTE_TEXTO, rect.width - 20):
            surf = FONTE_TEXTO.render(linha, True, cor_nome)
            tela.blit(surf, surf.get_rect(midtop=(rect.centerx, y_nome)))
            y_nome += FONTE_TEXTO.get_linesize()

        # aviso no rodapé do cartão
        if bloqueado:
            linhas = _quebrar_linhas("Requer login", FONTE_TEXTO_PEQUENA, rect.width - 20)
            y_aviso = rect.bottom - 14 - len(linhas) * FONTE_TEXTO_PEQUENA.get_linesize()
            for linha in linhas:
                surf = FONTE_TEXTO_PEQUENA.render(linha, True, cores['amarelo'])
                tela.blit(surf, surf.get_rect(midtop=(rect.centerx, y_aviso)))
                y_aviso += FONTE_TEXTO_PEQUENA.get_linesize()

    if mensagem:
        surf = FONTE_TEXTO.render(mensagem, True, cores['amarelo'])
        tela.blit(surf, surf.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.86))))

    dica = FONTE_TEXTO_PEQUENA.render("← → escolhem   |   Enter ou clique confirmam   |   Esc volta", True, (170, 170, 170))
    tela.blit(dica, dica.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.93))))

# ----------------------------------------------------------------------
# pergunta (aparece quando o personagem pega uma moeda)
# ----------------------------------------------------------------------
def layout_pergunta(pergunta):
    """Calcula onde fica cada elemento da pergunta (usado para desenhar e para os cliques)."""
    largura_painel = min(int(LARGURA_TELA * 0.8), 1100)
    pad = 36
    largura_texto = largura_painel - 2 * pad
    largura_num = 50

    linhas_pergunta = _quebrar_linhas(pergunta["pergunta"], FONTE_TEXTO_GRANDE, largura_texto)
    alt_linha_p = FONTE_TEXTO_GRANDE.get_linesize()
    alt_linha_a = FONTE_TEXTO.get_linesize()

    linhas_alt, alturas = [], []
    for alternativa in pergunta["alternativas"]:
        linhas = _quebrar_linhas(alternativa, FONTE_TEXTO, largura_texto - largura_num - 20)
        linhas_alt.append(linhas)
        alturas.append(max(56, len(linhas) * alt_linha_a + 24))

    espaco = 14
    altura_cabecalho = 44
    altura_feedback = 46

    total = (pad + altura_cabecalho + len(linhas_pergunta) * alt_linha_p + 24
             + sum(alturas) + espaco * (len(alturas) - 1) + 16 + altura_feedback + pad)
    topo = max(10, (ALTURA_TELA - total) // 2)
    painel = pygame.Rect((LARGURA_TELA - largura_painel) // 2, topo, largura_painel, total)

    y = painel.y + pad + altura_cabecalho
    pos_pergunta = (painel.x + pad, y)
    y += len(linhas_pergunta) * alt_linha_p + 24

    rects = []
    for altura in alturas:
        rects.append(pygame.Rect(painel.x + pad, y, largura_texto, altura))
        y += altura + espaco

    return {
        "painel": painel,
        "pad": pad,
        "linhas_pergunta": linhas_pergunta,
        "pos_pergunta": pos_pergunta,
        "rects": rects,
        "linhas_alternativas": linhas_alt,
        "largura_num": largura_num,
        "y_feedback": y - espaco + 16 + altura_feedback // 2,
    }


def desenhar_pergunta(tela, pergunta, layout, nome_area, cor_area, resposta=None, feedback=None):
    escurecer = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    escurecer.fill((0, 0, 0, 170))
    tela.blit(escurecer, (0, 0))

    painel = layout["painel"]
    pygame.draw.rect(tela, (30, 30, 30), painel, border_radius=16)
    pygame.draw.rect(tela, cor_area, painel, 4, border_radius=16)

    cabecalho = FONTE_TEXTO.render(f"Pergunta de {nome_area}", True, cor_area)
    tela.blit(cabecalho, (painel.x + layout["pad"], painel.y + layout["pad"]))

    x, y = layout["pos_pergunta"]
    for linha in layout["linhas_pergunta"]:
        tela.blit(FONTE_TEXTO_GRANDE.render(linha, True, cores['branco']), (x, y))
        y += FONTE_TEXTO_GRANDE.get_linesize()

    mouse = pygame.mouse.get_pos()
    for i, rect in enumerate(layout["rects"]):
        if resposta is None:
            sobre = rect.collidepoint(mouse)
            fundo = (70, 70, 70) if sobre else (50, 50, 50)
            borda = cores['azul-jogo'] if sobre else (110, 110, 110)
        elif i == pergunta["correta"]:
            fundo, borda = (25, 110, 55), cores['verde']
        elif i == resposta:
            fundo, borda = (130, 35, 35), cores['vermelho']
        else:
            fundo, borda = (40, 40, 40), (80, 80, 80)

        pygame.draw.rect(tela, fundo, rect, border_radius=10)
        pygame.draw.rect(tela, borda, rect, 2, border_radius=10)

        numero = FONTE_TEXTO_GRANDE.render(str(i + 1), True, cor_area)
        tela.blit(numero, numero.get_rect(center=(rect.x + layout["largura_num"] // 2, rect.centery)))

        linhas = layout["linhas_alternativas"][i]
        altura_texto = len(linhas) * FONTE_TEXTO.get_linesize()
        y_linha = rect.centery - altura_texto // 2
        for linha in linhas:
            tela.blit(FONTE_TEXTO.render(linha, True, cores['branco']), (rect.x + layout["largura_num"] + 10, y_linha))
            y_linha += FONTE_TEXTO.get_linesize()

    if feedback:
        texto, cor = feedback
        surf = FONTE_TEXTO_GRANDE.render(texto, True, cor)
        tela.blit(surf, surf.get_rect(center=(LARGURA_TELA // 2, layout["y_feedback"])))
    else:
        dica = FONTE_TEXTO_PEQUENA.render("Clique na resposta ou aperte 1, 2, 3 ou 4", True, (170, 170, 170))
        tela.blit(dica, dica.get_rect(center=(LARGURA_TELA // 2, layout["y_feedback"])))

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
    tela.fill((12, 183, 242))

    botao_modo1.desenhar(tela)
    botao_modo2.desenhar(tela)

def desenhar_rogue(tela):
    tela.fill((255, 0, 0))
