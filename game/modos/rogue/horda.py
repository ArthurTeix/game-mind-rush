import pygame
import random
from game.modos.rogue.inimigos import Bug, Erro, Firewall

class GerenciadorHordas:
    PAUSA_ENTRE_HORDAS = 3.0             
    PAUSA_INICIAL = 2.0
    HORDAS_POR_NOVO_VILAO = 2            
    TEMPO_AVISO = 3.0                    
    
    TIPOS = [
        {"classe": Bug, "vida": 1, "velocidade": 100, "dano": 10},
        {"classe": Erro, "vida": 1, "velocidade": 200, "dano": 10},
        {"classe": Firewall, "vida": 2, "velocidade": 70, "dano": 20},   
    ]

    def __init__(self, alvo, area_tela):
        self.alvo = alvo
        self.area = area_tela
        self.grupo = pygame.sprite.Group()

        self.horda = 0                   
        self.estado = "pausa"            
        self.tempo_pausa = self.PAUSA_INICIAL
        self.para_criar = 0              
        self.tempo_spawn = 0.0
        self.config = self.dificuldade(1)
        self.pontos = pygame.sprite.Group()

        self.novo_vilao = None           
        self.aviso_tempo = 0.0           

        self.fonte_horda = pygame.font.Font(None, 28)

        
        self.largura_barra = 800
        self.altura_barra = 24
        self.y_barra = 80

    def dificuldade(self, n):
        """O que cresce a cada horda: quantidade, ritmo de surgimento e vilões na tela."""
        return {
            "quantidade": 10 + 10 * (n - 1),                       
            "intervalo": max(0.10, 0.5 * (0.92 ** (n - 1))),     
            "simultaneos": min(60, 30 + 2 * (n - 1)),             
        }

    @property
    def restantes(self):
        return len(self.grupo) + self.para_criar

    def tipos_disponiveis(self):
        """Tipos liberados na horda atual: 1 até a horda 5, 2 até a 10, 3 até a 15..."""
        quantos = (self.horda - 1) // self.HORDAS_POR_NOVO_VILAO + 1
        return self.TIPOS[:max(1, quantos)]

    def sortear_tipo(self):
        tipos = self.tipos_disponiveis()
        
        pesos = [1] * (len(tipos) - 1) + [2]
        return random.choices(tipos, weights=pesos)[0]

    def iniciar_horda(self):
        self.horda += 1
        self.config = self.dificuldade(self.horda)
        self.para_criar = self.config["quantidade"]
        self.tempo_spawn = 0.0
        self.estado = "ativa"

        
        indice = (self.horda - 1) // self.HORDAS_POR_NOVO_VILAO
        if (self.horda - 1) % self.HORDAS_POR_NOVO_VILAO == 0 and 0 < indice < len(self.TIPOS):
            self.novo_vilao = self.TIPOS[indice]["classe"]
            self.aviso_tempo = self.TEMPO_AVISO
        else:
            self.novo_vilao = None

    def posicao_fora_da_tela(self, classe=Bug):
        margem = 20
        lado = random.choice(("cima", "baixo", "esquerda", "direita"))
        if lado == "cima":
            return (random.randint(-classe.LARGURA, self.area.width), -classe.ALTURA - margem)
        if lado == "baixo":
            return (random.randint(-classe.LARGURA, self.area.width), self.area.height + margem)
        if lado == "esquerda":
            return (-classe.LARGURA - margem, random.randint(-classe.ALTURA, self.area.height))
        return (self.area.width + margem, random.randint(-classe.ALTURA, self.area.height))

    def criar_vilao(self):
        tipo = self.sortear_tipo()
        classe = tipo["classe"]
        classe(
            self.posicao_fora_da_tela(classe), self.alvo, self.grupo, self.pontos,
            vida=tipo["vida"],
            velocidade=tipo["velocidade"] * random.uniform(0.85, 1.15),
            dano=tipo["dano"],
        )

    def update(self, dt):
        """Devolve True no frame em que uma horda termina."""
        horda_concluida = False
        self.aviso_tempo = max(0.0, self.aviso_tempo - dt)

        if self.estado == "pausa":
            self.tempo_pausa -= dt
            if self.tempo_pausa <= 0:
                self.iniciar_horda()
        else:
            self.tempo_spawn -= dt
            pode_criar = (self.para_criar > 0
                          and self.tempo_spawn <= 0
                          and len(self.grupo) < self.config["simultaneos"])
            if pode_criar:
                self.criar_vilao()
                self.para_criar -= 1
                self.tempo_spawn = self.config["intervalo"]

            if self.para_criar == 0 and len(self.grupo) == 0:
                self.estado = "pausa"
                self.tempo_pausa = self.PAUSA_ENTRE_HORDAS
                horda_concluida = True

        self.grupo.update(dt)
        return horda_concluida

    def desenhar(self, tela):
        self.grupo.draw(tela)
        for vilao in self.grupo:
            vilao.desenhar_barra_de_vida(tela)
        self.desenhar_barra_horda(tela)
        self.desenhar_aviso(tela)

    def desenhar_aviso(self, tela):
        if self.aviso_tempo <= 0 or self.novo_vilao is None:
            return
        nome = getattr(self.novo_vilao, "NOME", self.novo_vilao.__name__)
        imagem = self.fonte_horda.render(f"Novo vilão: {nome}!", True, (255, 220, 60))
        y = self.y_barra + self.altura_barra + 28
        tela.blit(imagem, imagem.get_rect(center=(tela.get_width() // 2, y)))

    def desenhar_barra_horda(self, tela):

        
        if self.horda == 0 or self.estado != "ativa":
            return

        restantes = self.restantes
        total = self.config["quantidade"]

        
        progresso = restantes / total if total > 0 else 0

        largura_preenchida = int(self.largura_barra * progresso)

        
        x = (tela.get_width() - self.largura_barra) // 2

        
        pygame.draw.rect(
            tela,
            (50, 50, 50),
            (x, self.y_barra, self.largura_barra, self.altura_barra),
        )

        
        if largura_preenchida > 0:
            pygame.draw.rect(
                tela,
                (60, 200, 100),
                (x, self.y_barra, largura_preenchida, self.altura_barra),
            )

        
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (x, self.y_barra, self.largura_barra, self.altura_barra),
            width=2,
        )