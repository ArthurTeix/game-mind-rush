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
