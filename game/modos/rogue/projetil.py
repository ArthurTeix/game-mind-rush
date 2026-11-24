import pygame
import math

class Projetil(pygame.sprite.Sprite):
    VELOCIDADE = 700          # pixels por segundo
    COR = (255, 220, 60)

    def __init__(self, pos, direcao, grupos, limite, dano=1, velocidade=None):
        super().__init__(grupos)

        self.direcao = pygame.Vector2(direcao)
        self.limite = limite
        self.dano = dano
        self.velocidade = velocidade or self.VELOCIDADE

        imagem = pygame.image.load("./assets/img/elementos/projetil_python.png").convert_alpha()
        angulo = -math.degrees(math.atan2(self.direcao.y, self.direcao.x))

        self.image = pygame.transform.rotate(imagem, angulo)
        self.rect = self.image.get_rect(center=pos)
        self.posicao = pygame.Vector2(self.rect.center)

    def update(self, dt):
        self.posicao += self.direcao * self.VELOCIDADE * dt
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))

        if not self.limite.colliderect(self.rect):
            self.kill()
