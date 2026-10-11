import pygame

pygame.init()
pygame.font.init()

# --- Configurações de tela ---
FULLSCREEN = True

info_tela = pygame.display.Info()
LARGURA_TELA = info_tela.current_w
ALTURA_TELA = info_tela.current_h

# título do jogo
TITULO_JOGO = "Mind Rush"

# fontes
FONTE_TITULO = pygame.font.SysFont('arial', 60)
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

# taxa de quadros
FPS = 60

# caminho da imagem do menu
CAMINHO_MENU = './img/fundos/MENU.png'
imagem_menu = pygame.image.load(CAMINHO_MENU)
imagem_menu = pygame.transform.scale(imagem_menu, (LARGURA_TELA, ALTURA_TELA))

#  caminho da imagem de fundo do ranking
CAMINHO_BG_RANK = './img/fundos/bg_ranking.png'
imagem_bg_rank = pygame.image.load(CAMINHO_BG_RANK)
imagem_bg_rank = pygame.transform.scale(imagem_bg_rank, (LARGURA_TELA, ALTURA_TELA))

# caminho da imagem do botão de sair do ranking
CAMINHO_SAIR_RANKING = './img/botoes/sair_ranking.png'
imagem_sair_ranking = pygame.image.load(CAMINHO_SAIR_RANKING)
imagem_sair_ranking = pygame.transform.scale(imagem_sair_ranking, (200, 200))
rect_sair_ranking = imagem_sair_ranking.get_rect(topleft=(110, 20))

# caminho da imagem de fundo do jogo
CAMINHO_BG_JOGO = './img/fundos/bg_jogo.png'
imagem_bg_jogo = pygame.image.load(CAMINHO_BG_JOGO)
imagem_bg_jogo = pygame.transform.scale(imagem_bg_jogo, (LARGURA_TELA, ALTURA_TELA))
