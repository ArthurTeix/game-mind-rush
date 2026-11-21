import pygame
from game.modos.rogue.pontos import Pontos

class Inimigos(pygame.sprite.Sprite):
    LARGURA = 64
    ALTURA = 64

    IMAGEM = None
    CAMINHO_IMAGEM = None

    VIDA = 1
    VELOCIDADE = 100
    DANO = 10
 
    def __init__(self, pos, alvo, grupos, grupo_pontos, vida=1, velocidade=100, dano=10):
        super().__init__(grupos)

        self.grupo_pontos = grupo_pontos
        self.alvo = alvo
 
        self.vida_max = vida if vida is not None else self.VIDA
        self.vida = self.vida_max

        self.velocidade = (velocidade if velocidade is not None else self.VELOCIDADE)

        self.dano = dano

        self.image = self.carregar_imagem()
        self.rect = self.image.get_rect(topleft=pos)

        self.imagem_original = self.image

        self.imagem_morte = self.carregar_imagem_morte()
        self.morrendo = False
        self.tempo_morte = 0.1
        self.timer_morte = 0

        self.posicao = pygame.Vector2(self.rect.topleft)
        self.direcao = pygame.Vector2()
 
    def carregar_imagem(self):
        if self.__class__.IMAGEM is None:
            try:
                imagem = pygame.image.load(self.CAMINHO_IMAGEM).convert_alpha()

                self.__class__.IMAGEM = pygame.transform.scale(imagem, (self.LARGURA, self.ALTURA))

            except (FileNotFoundError, pygame.error, TypeError):
                imagem = pygame.Surface((self.LARGURA, self.ALTURA),pygame.SRCALPHA)

                imagem.fill(self.COR)

                pygame.draw.rect(imagem, (30, 30, 30), imagem.get_rect(), 3)

                self.__class__.IMAGEM = imagem

        return self.__class__.IMAGEM

    def carregar_imagem_morte(self):
        try:
            imagem = pygame.image.load(self.CAMINHO_IMAGEM_MORTE).convert_alpha()

            return pygame.transform.scale(imagem, (self.LARGURA, self.ALTURA))

        except (FileNotFoundError, pygame.error, TypeError):
            return self.imagem_original

    def perseguir(self):
            ate_o_alvo = pygame.Vector2(self.alvo.rect.center) - pygame.Vector2(self.rect.center)
            if ate_o_alvo.length_squared() > 0:
                self.direcao = ate_o_alvo.normalize()
            else:
                self.direcao = pygame.Vector2()

    def movimentar(self, dt):
            self.posicao += self.direcao * self.velocidade * dt
            self.rect.topleft = (round(self.posicao.x), round(self.posicao.y))  

    def update(self, dt):

        if self.morrendo:
            self.timer_morte -= dt

            if self.timer_morte <= 0:
                Pontos(self.rect.center, self.grupo_pontos)
                self.kill()

        if self.morrendo:
            self.timer_morte -= dt

            if self.timer_morte <= 0:
                Pontos(self.rect.center, self.grupo_pontos)
                self.kill()

            return
    
        self.perseguir()
        self.movimentar(dt)

 
    def levar_dano(self, quantidade=1):
        """Devolve True se o vilão morreu com esse golpe."""
        if self.morrendo:
            return False
    
        self.vida -= quantidade
        if self.vida <= 0:
            self.morrendo = True
            self.image = self.imagem_morte
            self.timer_morte = self.tempo_morte

            return True
        
        return False
 
    def desenhar_barra_de_vida(self, tela):
        if self.vida_max <= 1:
            return
        
        largura = self.rect.width

        barra = pygame.Rect(self.rect.x, self.rect.y - 8, largura, 5)
        pygame.draw.rect(tela, (60, 20, 20), barra)

        cheio = barra.copy()
        cheio.width = round(largura * max(self.vida, 0) / self.vida_max)

        pygame.draw.rect(tela, (230, 70, 70), cheio)

class Bug(Inimigos):
    LARGURA = 54
    ALTURA = 54

    CAMINHO_IMAGEM = "./assets/img/personagens/inimigos/bug_estatico.png"
    CAMINHO_IMAGEM_MORTE = "./assets/img/personagens/inimigos/bug_morto.png"

    VIDA = 1
    VELOCIDADE = 100
    DANO = 10

    COR = (50, 0, 50)


class Erro(Inimigos):
    LARGURA = 54
    ALTURA = 54

    CAMINHO_IMAGEM = "./assets/img/personagens/inimigos/erro_estatico.png"
    CAMINHO_IMAGEM_MORTE = "./assets/img/personagens/inimigos/erro_morto.png"
    
    VIDA = 1
    VELOCIDADE = 200
    DANO = 10

    COR = (50, 0, 50)

class Firewall(Inimigos):
    LARGURA = 64
    ALTURA = 64
    
    CAMINHO_IMAGEM = "./assets/img/personagens/inimigos/firewall_estatico.png"
    CAMINHO_IMAGEM_MORTE = "./assets/img/personagens/inimigos/firewall_morto.png"
        
    VIDA = 2
    VELOCIDADE = 70
    DANO = 20
    
    COR = (50, 0, 50)