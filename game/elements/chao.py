import pygame
from random import randint
from game.util.cores import cores


class Chao:
    def __init__(self, x, y, largura, altura, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade

        self.imagem = pygame.Surface((largura, altura))
        self.imagem.fill(cores['rosa'])

        # APENAS QUANDO TIVER IMG
        # self.imagem = pygame.image.load('./img/elementos/chao.png').convert_alpha()
        # self.imagem = pygame.transform.scale(self.imagem, (largura, altura))

    def mover(self):
        self.rect.x -= self.velocidade

    def saiu_da_tela(self):
        return self.rect.right <= 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


class GerenciadorChao:
    def __init__(self, largura_tela, altura_tela, velocidade,
                altura_minima=400, altura_maxima=500,
                largura_minima=400, largura_maxima=500,
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
