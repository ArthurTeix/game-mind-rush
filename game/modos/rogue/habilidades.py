import random

class Habilidade:
    def __init__(self, id, nome, descricao, efeito, maximo=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.efeito = efeito
        self.maximo = maximo

    def aplicar(self, jogador):
        self.efeito(jogador)


def efeito_vida_extra(jogador):
    jogador.vida_maxima += 20
    jogador.curar(20)

def efeito_velocidade(jogador):
    jogador.velocidade *= 1.15

def efeito_gatilho_rapido(jogador):
    jogador.intervalo_tiro = max(0.08, jogador.intervalo_tiro * 0.8)

def efeito_escudo(jogador):
    jogador.tempo_invulneravel += 0.3

def efeito_regenerar(jogador):
    jogador.regeneracao += 0.25

HABILIDADES = [
    Habilidade("vida_extra", "Vida extra", "+20 de vida max.", efeito_vida_extra),
    Habilidade("velocidade", "Velocidade", "+15% de velocidade de movimento.", efeito_velocidade),
    Habilidade("gatilho_veloz", "Gatilho veloz", "Atira 20% mais veloz.", efeito_gatilho_rapido),
    Habilidade("escudo", "Escudo", "+0,3 s de invulnerabilidade depois de um golpe.", efeito_escudo),
    Habilidade("regenerar", "Regenerar", "Recupera 1 de vida a cada 4 segundos.", efeito_regenerar),
]

HABILIDADES_POR_ID = {h.id: h for h in HABILIDADES}

def sortear_habilidades(obtidas, quantidade=3):
    disponiveis = [h for h in HABILIDADES if h.maximo is None or obtidas.get(h.id, 0) < h.maximo]
    return random.sample(disponiveis, min(quantidade, len(disponiveis)))

def quebrar_texto(texto, fonte, largura):
    linhas = []
    atual = ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas
