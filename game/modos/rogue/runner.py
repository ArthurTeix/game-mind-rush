import pygame
import math
from game.modos.rogue.habilidades import sortear_habilidades, HABILIDADES_POR_ID, quebrar_texto
from game.modos.rogue.jogador import Jogador
from game.modos.rogue.horda import GerenciadorHordas

class RogueLike:
    CURA_POR_HORDA = 20                  
    QUANTIDADE_OPCOES = 3
    ATRASO_ESCOLHA = 0.3
 
    def __init__(self, tela):
        self.tela = tela
        self.limite = tela.get_rect()
        self.fonte = pygame.font.Font(None, 30)

        self.fonte_pequena = pygame.font.Font('./assets/fontes/aseprite.ttf', 20)
        self.fonte_media = pygame.font.Font('./assets/fontes/aseprite.ttf', 30)
        self.fonte_grande = pygame.font.Font('./assets/fontes/aseprite.ttf', 72)

        self.fundo = pygame.image.load("./assets/img/fundos/mapa_rogue.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, self.limite.size)

        self.reiniciar()

    def iniciar_partida(self):
        self.reiniciar()

    def eventos(self, evento):
        self.tratar_evento(evento)

    def atualizar(self, dt):
        self.atualizar_jogo(dt)

        return self.estado != "gameover"

    def desenhar(self):
        self.desenhar_jogo()
 
    def reiniciar(self):
        self.todos = pygame.sprite.Group()
        self.projeteis = pygame.sprite.Group()
        self.jogador = Jogador(
            (self.limite.centerx - 24, self.limite.centery - 24),
            self.todos, self.projeteis, self.limite,
        )
        self.hordas = GerenciadorHordas(self.jogador, self.limite)
        self.obtidas = {}
        self.opcoes = []
        self.tempo_escolha = 0.0
        self.estado = "jogando"        

    def abrir_escolha(self):  
        self.opcoes = sortear_habilidades(self.obtidas, self.QUANTIDADE_OPCOES) 
        self.tempo_escolha = 0.0  
        if self.opcoes:  
            self.estado = "escolha"  
 
    def escolher(self, indice): 
        habilidade = self.opcoes[indice]  
        habilidade.aplicar(self.jogador) 
        self.obtidas[habilidade.id] = self.obtidas.get(habilidade.id, 0) + 1 
        self.opcoes = []  
        self.estado = "jogando"  

    def retangulos_cartas(self): 
        quantidade = len(self.opcoes)  
        largura, altura, espaco = 300, 340, 40  
        total = quantidade * largura + (quantidade - 1) * espaco
        x0 = self.limite.centerx - total // 2  
        y = self.limite.centery - altura // 2 + 30  
        return [pygame.Rect(x0 + i * (largura + espaco), y, largura, altura) 
                for i in range(quantidade)] 

    def tratar_evento(self, evento):  
        if self.estado == "escolha": 
            if self.tempo_escolha < self.ATRASO_ESCOLHA: 
                return 
            indice = None  
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_1, pygame.K_2, pygame.K_3): 
                indice = evento.key - pygame.K_1 
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  
                for i, carta in enumerate(self.retangulos_cartas()):
                    if carta.collidepoint(evento.pos):  
                        indice = i 
            if indice is not None and indice < len(self.opcoes): 
                self.escolher(indice) 
        elif self.estado == "gameover": 
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:  
                self.reiniciar() 
 
    def atualizar_jogo(self, dt):
        if self.estado == "escolha":  
            self.tempo_escolha += dt
        if self.estado != "jogando":
            return
 
        self.todos.update(dt)
        self.projeteis.update(dt)

        for ponto in self.hordas.pontos:
            ponto.colisao(self.jogador)

        if self.hordas.update(dt):
            self.jogador.curar(self.CURA_POR_HORDA)
            self.abrir_escolha()
            return
 
        
        acertos = pygame.sprite.groupcollide(self.projeteis, self.hordas.grupo, True, False)
        for projetil, viloes in acertos.items():
            if viloes[0].levar_dano(projetil.dano):
                pass
        
        tocando = pygame.sprite.spritecollide(
            self.jogador, self.hordas.grupo, False,
            collided=pygame.sprite.collide_rect_ratio(0.7),
        )

        if tocando and self.jogador.invulnerabilidade <= 0:
            self.jogador.levar_dano(max(v.dano for v in tocando))
         
        if not self.jogador.vivo:
            self.estado = "gameover"

    def texto(self, conteudo, pos, cor=(255, 255, 255), fonte=None, centro=False):
        imagem = (fonte or self.fonte).render(conteudo, True, cor)
        rect = imagem.get_rect(center=pos) if centro else imagem.get_rect(topleft=pos)
        self.tela.blit(imagem, rect)
 
    def desenhar_hud(self):
        
        barra = pygame.Rect(1600, 20, 300, 24)
        proporcao = self.jogador.vida / self.jogador.vida_maxima
        cor = (80, 200, 100) if proporcao > 0.5 else (230, 190, 50) if proporcao > 0.25 else (220, 60, 60)
        pygame.draw.rect(self.tela, (40, 40, 50), barra)
        pygame.draw.rect(self.tela, cor, (barra.x, barra.y, round(barra.width * proporcao), barra.height))
        pygame.draw.rect(self.tela, (230, 230, 230), barra, 2)
        self.texto(f"HP {self.jogador.vida}/{self.jogador.vida_maxima}", (barra.x + 8, barra.y + 4), (20, 20, 20), fonte=self.fonte_pequena)
 
        self.texto(f"Pontos: {self.jogador.pontos}", (1600, 54), fonte=self.fonte_pequena)

        if self.estado == "escolha":  
            return
 
        centro_x = self.limite.centerx
        if self.hordas.estado == "ativa":
            self.texto(f"Horda {self.hordas.horda}", (centro_x, 40), fonte=self.fonte_grande, centro=True)
        else:
            proxima = self.hordas.horda + 1
            segundos = max(0, math.ceil(self.hordas.tempo_pausa))
            if self.hordas.horda > 0:
                self.texto(f"Horda {self.hordas.horda} vencida!", (centro_x, 40), (120, 230, 140),
                           self.fonte_grande, centro=True)
            self.texto(f"Horda {proxima} em {segundos}s", (centro_x, 90), fonte=self.fonte_pequena, centro=True)

    def desenhar_habilidades_obtidas(self):  
        for i, (id_habilidade, nivel) in enumerate(self.obtidas.items()):  
            nome = HABILIDADES_POR_ID[id_habilidade].nome  
            y = self.limite.bottom - 24 - 24 * (len(self.obtidas) - 1 - i)  
            self.texto(f"{nome} x{nivel}", (20, y), (200, 200, 200), self.fonte_pequena)  

    def desenhar_escolha(self):  
        veu = pygame.Surface(self.limite.size, pygame.SRCALPHA)  
        veu.fill((0, 0, 0, 190))  
        self.tela.blit(veu, (0, 0))  
 
        cx = self.limite.centerx  
        self.texto(f"Horda {self.hordas.horda} vencida!", (cx, 90), (120, 230, 140), self.fonte_grande, centro=True)  
        self.texto("Escolha uma habilidade", (cx, 150), fonte=self.fonte_pequena, centro=True)
 
        posicao_mouse = pygame.mouse.get_pos()  
        for i, (carta, habilidade) in enumerate(zip(self.retangulos_cartas(), self.opcoes)):  
            sobre = carta.collidepoint(posicao_mouse)  
            pygame.draw.rect(self.tela, (60, 66, 92) if sobre else (42, 46, 66), carta, border_radius=12)  
            pygame.draw.rect(self.tela, (255, 220, 60) if sobre else (110, 116, 150), carta, 3, border_radius=12)  
            self.texto(str(i + 1), (carta.x + 20, carta.y + 14), (255, 220, 60), self.fonte_media)  
            self.texto(habilidade.nome, (carta.centerx, carta.y + 70), (255, 255, 255), self.fonte_media, centro=True)  
            nivel = self.obtidas.get(habilidade.id, 0) + 1  
            texto_nivel = f"Nivel {nivel}" + (f"/{habilidade.maximo}" if habilidade.maximo else "")  
            self.texto(texto_nivel, (carta.centerx, carta.y + 108), (150, 200, 255), self.fonte_pequena, centro=True)  
            linhas = quebrar_texto(habilidade.descricao, self.fonte, carta.width - 40)  
            for k, linha in enumerate(linhas):  
                self.texto(linha, (carta.centerx, carta.y + 160 + 30 * k), (220, 220, 220), centro=True)  
            self.texto(f"Clique", (carta.centerx, carta.bottom - 28), (160, 160, 160), self.fonte_pequena, centro=True)  
    
    def desenhar_jogo(self):
        self.tela.blit(self.fundo, (0,0))
        self.hordas.pontos.draw(self.tela)
        self.todos.draw(self.tela)
        self.projeteis.draw(self.tela)
        self.hordas.desenhar(self.tela)
        self.desenhar_hud()
        self.desenhar_habilidades_obtidas()

        if self.estado == "escolha":  
            self.desenhar_escolha()
 
        if self.estado == "gameover":
            veu = pygame.Surface(self.limite.size, pygame.SRCALPHA)
            veu.fill((0, 0, 0, 170))
            self.tela.blit(veu, (0, 0))
            cx, cy = self.limite.center
            self.texto("GAME OVER", (cx, cy - 60), (230, 70, 70), self.fonte_grande, centro=True)
            self.texto(f"Você chegou até a horda {self.hordas.horda}", (cx, cy), centro=True)
            self.texto(f"Pontos: {self.jogador.pontos}",(1600, 54))
            self.texto("Pressione R para reiniciar", (cx, cy + 80), (200, 200, 200), centro=True)
