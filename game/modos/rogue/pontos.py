import pygame

class Pontos(pygame.sprite.Sprite):

    def __init__(self, pos, *grupos):
        super().__init__(*grupos)

        self.image = pygame.image.load(
            "./assets/img/elementos/pontos.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(center=pos)

        self.image = pygame.transform.scale(self.image, (55, 35))

    def colisao(self, jogador):
        if self.rect.colliderect(jogador.rect):
            jogador.adicionar_pontos(10)
            self.kill()
            return True

        return False
