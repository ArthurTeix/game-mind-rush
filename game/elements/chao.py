import pygame
from random import randint
from game.util.cores import cores
from game.elements.obstaculo import Obstaculo

class Chao:

    def __init__(self, x, y, largura, altura, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade

        self.imagem = pygame.Surface((largura, altura))
        self.imagem.fill(cores['azul-jogo'])

        self.obstaculo = None

    def mover(self):
        self.rect.x -= self.velocidade

    def saiu_da_tela(self):
        return self.rect.right <= 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)
        if self.obstaculo is not None:
            tela.blit(Chao._imagem_obstaculo, self.obstaculo)


class GerenciadorChao:
    DEBUG_MEDIDAS = False
    ARQUIVO_LOG = './debug_chao.log'
    _fonte_debug = None
    _frame_debug = 0

    def __init__(self, largura_tela, altura_tela, velocidade,
                altura_minima=400, altura_maxima=500,
                largura_minima=400, largura_maxima=900, # 400 | 625 | 750 | 900
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

        largura_inicial = max(350, int(self.largura_tela * 0.6))
        primeiro_chao = self.criar_chao_fixo(x=0, largura=largura_inicial, altura=self.altura_maxima)
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
        if GerenciadorChao.DEBUG_MEDIDAS:
            antes = [(c.rect.x, c.rect.width) for c in self.lista_chaos]

        for chao in self.lista_chaos:
            chao.mover()

        if GerenciadorChao.DEBUG_MEDIDAS:
            self._conferir_movimento(antes)

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

        if GerenciadorChao.DEBUG_MEDIDAS:
            self._desenhar_medidas(tela)

    @staticmethod
    def _registrar(mensagem):
        """Escreve no terminal e no arquivo debug_chao.log (na pasta de onde o jogo foi iniciado)."""
        linha = f"[frame {GerenciadorChao._frame_debug}] {mensagem}"
        print("[DEBUG]", linha)
        try:
            with open(GerenciadorChao.ARQUIVO_LOG, 'a', encoding='utf-8') as arq:
                arq.write(linha + "\n")
        except OSError:
            pass

    def _conferir_movimento(self, antes):
        """Registra se algum bloco andar diferente, mudar de largura ou se algum vão mudar."""
        GerenciadorChao._frame_debug += 1

        for i, (chao, (x0, w0)) in enumerate(zip(self.lista_chaos, antes)):
            if x0 - chao.rect.x != self.velocidade:
                self._registrar(f"bloco {i} andou {x0 - chao.rect.x}px (esperado {self.velocidade}px)")
            if chao.rect.width != w0:
                self._registrar(f"bloco {i} mudou de largura: {w0} -> {chao.rect.width}")

        for i in range(len(self.lista_chaos) - 1):
            vao_antes = antes[i + 1][0] - (antes[i][0] + antes[i][1])
            vao_depois = self.lista_chaos[i + 1].rect.left - self.lista_chaos[i].rect.right
            if vao_antes != vao_depois:
                self._registrar(f"vão entre blocos {i} e {i + 1} mudou: {vao_antes} -> {vao_depois}")

    def _desenhar_medidas(self, tela):
        """Mostra L = largura real de cada bloco e vão = distância até o próximo bloco (em pixels)."""
        if GerenciadorChao._fonte_debug is None:
            GerenciadorChao._fonte_debug = pygame.font.SysFont('arial', 22, bold=True)
        fonte = GerenciadorChao._fonte_debug

        for i, chao in enumerate(self.lista_chaos):
            texto = fonte.render(f"L={chao.rect.width}", True, cores['amarelo'])
            tela.blit(texto, (max(chao.rect.x, 0) + 8, chao.rect.y + 60))

            if i + 1 < len(self.lista_chaos):
                proximo = self.lista_chaos[i + 1]
                vao = proximo.rect.left - chao.rect.right
                texto = fonte.render(f"vão={vao}", True, cores['vermelho'])
                tela.blit(texto, (chao.rect.right + 4, self.altura_tela - 40))
