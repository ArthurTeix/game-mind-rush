import pygame
from random import randint
from game.util.cores import cores


class Chao:
    LARGURA_OBSTACULO = 110
    ALTURA_OBSTACULO = 50
    MARGEM_INICIO = 140        # distância da ponta esquerda da plataforma
    MARGEM_FIM = 160           # distância da ponta direita da plataforma
    AFUNDAR_OBSTACULO = 2      # quanto a caixa "entra" na plataforma (cola no chão)
    CHANCE_OBSTACULO = 70      # % de chance de nascer um obstáculo em cada bloco
    _imagem_obstaculo = None   # carregada uma vez só e reaproveitada

    def __init__(self, x, y, largura, altura, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade

        self.imagem = pygame.Surface((largura, altura))
        self.imagem.fill(cores['azul-jogo'])

        # obstáculo em cima da plataforma (None = sem obstáculo)
        self.obstaculo = None

    def criar_obstaculo(self):
        largura = Chao.LARGURA_OBSTACULO
        altura = Chao.ALTURA_OBSTACULO

        # faixa em que o obstáculo pode nascer, respeitando as duas margens
        x_min = self.rect.x + Chao.MARGEM_INICIO
        x_max = self.rect.right - Chao.MARGEM_FIM - largura
        if x_max < x_min:
            return  # plataforma curta demais

        if Chao._imagem_obstaculo is None:
            imagem = pygame.image.load('./img/elementos/obstaculo.png').convert()
            imagem.set_colorkey(imagem.get_at((0, 0)))
            imagem = imagem.convert_alpha()
            imagem = imagem.subsurface(imagem.get_bounding_rect()).copy()
            Chao._imagem_obstaculo = pygame.transform.scale(imagem, (largura, altura))

        x = randint(x_min, x_max)
        y = self.rect.top - altura + Chao.AFUNDAR_OBSTACULO
        self.obstaculo = pygame.Rect(x, y, largura, altura)

    def mover(self):
        self.rect.x -= self.velocidade
        if self.obstaculo is not None:
            self.obstaculo.x -= self.velocidade

    def saiu_da_tela(self):
        return self.rect.right <= 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)
        if self.obstaculo is not None:
            tela.blit(Chao._imagem_obstaculo, self.obstaculo)


class GerenciadorChao:
    def __init__(self, largura_tela, altura_tela, velocidade,
                altura_minima=380, altura_maxima=500,
                largura_minima=300, largura_maxima=700,
                espaco_minimo=50, espaco_maximo=150):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade = velocidade

        self.altura_minima = altura_minima
        self.altura_maxima = altura_maxima
        self.largura_minima = largura_minima
        self.largura_maxima = largura_maxima
        self.espaco_minimo = espaco_minimo
        self.espaco_maximo = espaco_maximo

        self.lista_chaos = []

        # o primeiro bloco é fixo e previsível (não sorteado), para
        # garantir uma "zona segura" onde o personagem nasce em pé
        primeiro_chao = self.criar_chao_fixo(x=0, largura=350, altura=self.altura_maxima)
        self.altura_do_chao_inicial = primeiro_chao.rect.height

        # preenche o resto da tela com blocos sorteados normalmente
        x = primeiro_chao.rect.right + randint(self.espaco_minimo, self.espaco_maximo)
        while x < self.largura_tela:
            novo_chao = self.criar_chao(x)
            espaco = randint(self.espaco_minimo, self.espaco_maximo)
            x = novo_chao.rect.right + espaco

    def criar_chao_fixo(self, x, largura, altura):
        y = self.altura_tela - altura
        novo_chao = Chao(x, y, largura, altura, self.velocidade)
        self.lista_chaos.append(novo_chao)
        return novo_chao

    def criar_chao(self, x):
        # sorteia o tamanho deste bloco especificamente
        largura_sorteada = randint(self.largura_minima, self.largura_maxima)
        altura_sorteada = randint(self.altura_minima, self.altura_maxima)

        # a base do bloco fica sempre encostada no fundo da tela;
        # só o topo sobe ou desce, dependendo da altura sorteada
        y = self.altura_tela - altura_sorteada

        novo_chao = Chao(x, y, largura_sorteada, altura_sorteada, self.velocidade)
        self.lista_chaos.append(novo_chao)

        # chance (em %) de nascer um obstáculo em cima deste bloco
        if randint(1, 100) <= Chao.CHANCE_OBSTACULO:
            novo_chao.criar_obstaculo()

        return novo_chao

    def atualizar(self):
        # passo 1: move cada bloco de chão para a esquerda
        for chao in self.lista_chaos:
            chao.mover()

        # passo 2: separa os blocos que ainda estão visíveis,
        # e conta quantos saíram (usado para pontuação)
        chaos_visiveis = []
        quantidade_removida = 0

        for chao in self.lista_chaos:
            if not chao.saiu_da_tela():
                chaos_visiveis.append(chao)
            else:
                quantidade_removida += 1

        self.lista_chaos = chaos_visiveis

        # passo 3: se não sobrou nenhum bloco, cria um novo do zero
        if len(self.lista_chaos) == 0:
            self.criar_chao(self.largura_tela)
            return quantidade_removida

        # passo 4: se o último bloco já apareceu por completo na tela,
        # cria o próximo bloco depois dele, com um espaço aleatório
        ultimo_chao = self.lista_chaos[-1]

        if ultimo_chao.rect.right <= self.largura_tela:
            espaco = randint(self.espaco_minimo, self.espaco_maximo)
            proximo_x = ultimo_chao.rect.right + espaco
            self.criar_chao(proximo_x)

        return quantidade_removida

    def desenhar(self, tela):
        for chao in self.lista_chaos:
            chao.desenhar(tela)
