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
FONTE_MENSAGEM = pygame.font.Font('./assets/fontes/aseprite.ttf', 50)
FONTE_PONTOS = pygame.font.Font('./assets/fontes/aseprite.ttf', 60)
FONTE_VIDAS = pygame.font.Font('./assets/fontes/aseprite.ttf', 60)
FONTE_RELOGIO = pygame.font.Font('./assets/fontes/aseprite.ttf', 40)

# taxa de quadros
FPS = 60

# caminho da imagem do menu
CAMINHO_MENU = './assets/img/fundos/MENU.png'
img_menu = pygame.image.load(CAMINHO_MENU)
img_menu = pygame.transform.scale(img_menu, (LARGURA_TELA, ALTURA_TELA))

#  caminho da imagem de fundo do ranking
CAMINHO_BG_RANK = './assets/img/fundos/bg_ranking.png'
img_bg_rank = pygame.image.load(CAMINHO_BG_RANK)
img_bg_rank = pygame.transform.scale(img_bg_rank, (LARGURA_TELA, ALTURA_TELA))

# caminho da imagem do botão de sair do ranking
CAMINHO_SAIR_RANKING = './assets/img/botoes/botoes_menu/sair_ranking.png'
img_sair_rank = pygame.image.load(CAMINHO_SAIR_RANKING)
img_sair_rank = pygame.transform.scale(img_sair_rank, (200, 200))
rect_sair_rank = img_sair_rank.get_rect(topleft=(110, 20))

# caminho da imagem de fundo do jogo
CAMINHO_BG_JOGO = './assets/img/fundos/bg_jogo.png'
img_bg_endless = pygame.image.load(CAMINHO_BG_JOGO)
img_bg_endless = pygame.transform.scale(img_bg_endless, (LARGURA_TELA, ALTURA_TELA))

CAMINHO_IMAGEM_GAMEOVER = './assets/img/fundos/GAMEOVER.png'
img_gameover_endless = pygame.image.load(CAMINHO_IMAGEM_GAMEOVER)
img_gameover_endless = pygame.transform.scale(img_gameover_endless, (LARGURA_TELA, ALTURA_TELA))

CAMINHO_MENSAGEM_GAMEOVER = './assets/img/mensagem/msg_gameover_endless.png'
msg_gameover_endless = pygame.image.load(CAMINHO_MENSAGEM_GAMEOVER)

CAMINHO_ESTRELA = './assets/img/elementos/estrela.png'
img_estrela = pygame.image.load(CAMINHO_ESTRELA)

CAMINHO_CORACAO = './assets/img/elementos/coracao.png'
img_coracao = pygame.image.load(CAMINHO_CORACAO)
