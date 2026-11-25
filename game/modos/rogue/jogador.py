import pygame
from game.modos.rogue.projetil import Projetil

pygame.init()

class Jogador(pygame.sprite.Sprite):
    VIDA_MAXIMA = 100
    TEMPO_INVULNERAVEL = 1.0
    ESPALHAMENTO_TIRO = 14

    def __init__(self, pos, grupos, projeteis, limite):
        super().__init__(grupos)

        self.animacoes = self.carregar_animacoes()
        self.direcao_animacao = "baixo"
        self.quadro_atual = 0
        self.tempo_animacao = 0
        self.VELOCIDADE_ANIMACAO = 0.12

        self.image = self.animacoes["baixo"][0]

        self.rect = self.image.get_rect(topleft=pos)

        # movimentação
        self.posicao = pygame.Vector2(self.rect.topleft)
        self.direcao = pygame.Vector2()
        self.velocidade = 300

        # tiro
        self.projeteis = projeteis
        self.limite = limite
        self.intervalo_tiro = 0.35
        self.espera_tiro = 0.0
        self.dano_tiro = 1
        self.velocidade_tiro = Projetil.VELOCIDADE

        self.projeteis_por_tiro = 1

        # vida
        self.vida_maxima = self.VIDA_MAXIMA
        self.vida = self.vida_maxima
        self.invulnerabilidade = 0.0
        self.tempo_invulneravel = self.TEMPO_INVULNERAVEL

        self.multiplicador_dano = 1.0
        self.regeneracao = 0.0
        self.acumulo_regeneracao = 0.0

        self.multiplicador_pontos = 1.0
        self.pontos = 0

    def carregar_imagem(self):
        try:
            return pygame.image.load('./assets/img/personagens/generico/jogador_estatico.png').convert_alpha()
        except (FileNotFoundError, pygame.error):
            imagem = pygame.Surface((48, 48))
            imagem.fill((60, 120, 220))
            pygame.draw.rect(imagem, (140, 190, 255), imagem.get_rect().inflate(-20, -20))

            return imagem

    def carregar_animacoes(self):

        direcoes = ["baixo", "cima", "esquerda", "direita"]
        animacoes = {}

        for direcao in direcoes:
            quadros = []

            for i in range(3):
                imagem = pygame.image.load(f"./assets/img/personagens/generico/{direcao}_{i}.png").convert_alpha()

                imagem = pygame.transform.scale(imagem, (64, 64))
                quadros.append(imagem)

            animacoes[direcao] = quadros

        return animacoes

    def animar(self, dt):

        if self.direcao.length_squared() == 0:
            self.quadro_atual = 0
            self.tempo_animacao = 0
            self.image = self.carregar_imagem()
            return

        if abs(self.direcao.x) > abs(self.direcao.y):
            nova_direcao = (
                "direita" if self.direcao.x > 0 else "esquerda"
            )
        else:
            nova_direcao = (
                "baixo" if self.direcao.y > 0 else "cima"
            )

        if nova_direcao != self.direcao_animacao:
            self.direcao_animacao = nova_direcao
            self.quadro_atual = 0
            self.tempo_animacao = 0

        quadros = self.animacoes[self.direcao_animacao]

        self.tempo_animacao += dt

        while self.tempo_animacao >= self.VELOCIDADE_ANIMACAO:
            self.tempo_animacao -= self.VELOCIDADE_ANIMACAO

            self.quadro_atual = (
                self.quadro_atual + 1
            ) % len(quadros)

        self.image = quadros[self.quadro_atual]

    # ---- vida

    @property
    def vivo(self):
        return self.vida > 0

    def levar_dano(self, quantidade):
        """Devolve True se o golpe valeu (fora do tempo de invulnerabilidade)."""
        if self.invulnerabilidade > 0 or not self.vivo:
            return False

        dano_final = quantidade * self.multiplicador_dano

        self.vida = max(0, self.vida - dano_final)
        self.invulnerabilidade = self.tempo_invulneravel
        return True

    def curar(self, quantidade):
        if self.vivo:
            self.vida = min(self.vida_maxima, self.vida + quantidade)

    def regenerar(self, dt):
        if self.regeneracao <= 0 or not self.vivo:
            return

        self.acumulo_regeneracao += self.regeneracao * dt

        cura = int(self.acumulo_regeneracao)

        if cura > 0:
            self.curar(cura)
            self.acumulo_regeneracao -= cura

    # ---- controles

    def entrada(self):
        tecla = pygame.key.get_pressed()          # movimento: WASD
        self.direcao.x = int(tecla[pygame.K_d]) - int(tecla[pygame.K_a])
        self.direcao.y = int(tecla[pygame.K_s]) - int(tecla[pygame.K_w])
        if self.direcao.length_squared() > 0:
            self.direcao = self.direcao.normalize()

    def atirar(self):
        tecla = pygame.key.get_pressed()          # tiro: setas
        alvo = pygame.Vector2(
            int(tecla[pygame.K_RIGHT]) - int(tecla[pygame.K_LEFT]),
            int(tecla[pygame.K_DOWN]) - int(tecla[pygame.K_UP]),
        )
        if alvo.length_squared() == 0 or self.espera_tiro > 0:
            return
        Projetil(self.rect.center, alvo.normalize(), self.projeteis, self.limite)
        self.espera_tiro = self.intervalo_tiro

    def movimentar(self, dt):
        self.posicao += self.direcao * self.velocidade * dt
        self.rect.topleft = (round(self.posicao.x), round(self.posicao.y))
        self.rect.clamp_ip(self.limite)               # não sai da tela
        self.posicao.update(self.rect.topleft)

    def piscar(self):
        if self.invulnerabilidade > 0:
            if int(self.invulnerabilidade * 10) % 2 == 0:
                self.image.set_alpha(80)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def adicionar_pontos(self, quantidade):
        self.pontos += quantidade

    def update(self, dt):
        self.espera_tiro = max(0.0, self.espera_tiro - dt)
        self.invulnerabilidade = max(0.0, self.invulnerabilidade - dt)

        if not self.vivo:
            return

        self.regenerar(dt)
        self.entrada()
        self.movimentar(dt)
        self.animar(dt)
        self.atirar()
        self.piscar()
