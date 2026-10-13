# Telas de conta: configurações, login e cadastro (feitas só com pygame)

import sqlite3
import pygame

from game.configuracoes import LARGURA_TELA, ALTURA_TELA, FONTE_MENSAGEM
from game.util.cores import cores
from game.util import validacao
from game.database import db

# --- aparência ---
LARGURA_CAMPO = 520
ALTURA_CAMPO = 52
PASSO_CAMPO = 92                 # distância vertical entre um campo e o próximo
COR_FUNDO_CAMPO = (45, 45, 45)
COR_BORDA = (110, 110, 110)
COR_PLACEHOLDER = (110, 110, 110)
COR_BOTAO_NEUTRO = (90, 90, 90)
LARGURA_MAX_MSG = min(int(LARGURA_TELA * 0.8), 900)

FONTE_TITULO_TELA = pygame.font.SysFont('arial', 56)
FONTE_ROTULO = pygame.font.SysFont('arial', 24)
FONTE_CAMPO = pygame.font.SysFont('arial', 30)
FONTE_MSG = pygame.font.SysFont('arial', 26)
FONTE_BOTAO = pygame.font.SysFont('arial', 30, bold=True)
FONTE_PEQUENA = pygame.font.SysFont('arial', 20)


# ------------------------------------------------------------------ helpers

def _permitido_usuario(char):
    return char.isascii() and (char.isalnum() or char == "_")


def _permitido_email(char):
    return not char.isspace()


def _quebrar_linhas(texto, fonte, largura_max):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def _desenhar_mensagem(tela, texto, cor, y_topo):
    for i, linha in enumerate(_quebrar_linhas(texto, FONTE_MSG, LARGURA_MAX_MSG)):
        surf = FONTE_MSG.render(linha, True, cor)
        tela.blit(surf, surf.get_rect(midtop=(LARGURA_TELA // 2, y_topo + i * 30)))


# ------------------------------------------------------------------- campos

class CampoTexto:
    def __init__(self, rotulo, x, y, largura=LARGURA_CAMPO, altura=ALTURA_CAMPO,
                senha=False, max_len=32, permitido=None, mascara_data=False,
                placeholder=""):
        self.rotulo = rotulo
        self.rect = pygame.Rect(x, y, largura, altura)
        self.senha = senha
        self.max_len = max_len
        self.permitido = permitido
        self.mascara_data = mascara_data
        self.placeholder = placeholder

        self.texto = ""
        self.foco = False
        self.mostrar_senha = False

        self.rect_olho = None
        if senha:
            self.rect_olho = pygame.Rect(self.rect.right - 108, self.rect.y + 8, 100, altura - 16)

    def limpar(self):
        self.texto = ""
        self.foco = False
        self.mostrar_senha = False

    # --- entrada ---
    @staticmethod
    def _formatar_data(digitos):
        resultado = digitos[:2]
        if len(digitos) > 2:
            resultado += "/" + digitos[2:4]
        if len(digitos) > 4:
            resultado += "/" + digitos[4:]
        return resultado

    def _inserir(self, char):
        if self.mascara_data:
            if char in "0123456789":
                digitos = self.texto.replace("/", "")
                if len(digitos) < 8:
                    self.texto = self._formatar_data(digitos + char)
            return

        if len(self.texto) >= self.max_len:
            return
        if self.permitido and not self.permitido(char):
            return
        self.texto += char

    def _apagar(self):
        if self.mascara_data:
            self.texto = self._formatar_data(self.texto.replace("/", "")[:-1])
        else:
            self.texto = self.texto[:-1]

    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_olho and self.rect_olho.collidepoint(evento.pos):
                self.mostrar_senha = not self.mostrar_senha
                self.foco = True
            else:
                self.foco = self.rect.collidepoint(evento.pos)

        elif evento.type == pygame.KEYDOWN and self.foco:
            if evento.key == pygame.K_BACKSPACE:
                self._apagar()
            elif evento.unicode and evento.unicode.isprintable():
                self._inserir(evento.unicode)

    # --- desenho ---
    def desenhar(self, tela):
        rotulo = FONTE_ROTULO.render(self.rotulo, True, cores['branco'])
        tela.blit(rotulo, (self.rect.x, self.rect.y - 28))

        pygame.draw.rect(tela, COR_FUNDO_CAMPO, self.rect, border_radius=8)
        borda = cores['azul-jogo'] if self.foco else COR_BORDA
        pygame.draw.rect(tela, borda, self.rect, 2, border_radius=8)

        x_texto = self.rect.x + 10
        area_largura = self.rect.width - 20
        if self.rect_olho:
            area_largura -= self.rect_olho.width + 10

        if self.senha and not self.mostrar_senha:
            exibido = "*" * len(self.texto)
        else:
            exibido = self.texto

        largura_texto = 0
        if exibido:
            surf = FONTE_CAMPO.render(exibido, True, cores['branco'])
            largura_texto = surf.get_width()
            y = self.rect.centery - surf.get_height() // 2

            if largura_texto > area_largura:
                # texto maior que o campo: mostra só o final (onde o cursor está)
                recorte = pygame.Rect(largura_texto - area_largura, 0, area_largura, surf.get_height())
                tela.blit(surf, (x_texto, y), recorte)
                largura_texto = area_largura
            else:
                tela.blit(surf, (x_texto, y))
        elif self.placeholder:
            surf = FONTE_CAMPO.render(self.placeholder, True, COR_PLACEHOLDER)
            tela.blit(surf, (x_texto, self.rect.centery - surf.get_height() // 2))

        # cursor piscando
        if self.foco and (pygame.time.get_ticks() // 500) % 2 == 0:
            x = x_texto + largura_texto + 2
            pygame.draw.line(tela, cores['branco'], (x, self.rect.y + 10), (x, self.rect.bottom - 10), 2)

        # botão "mostrar/ocultar" da senha
        if self.rect_olho:
            pygame.draw.rect(tela, COR_BORDA, self.rect_olho, 1, border_radius=6)
            legenda = "Ocultar" if self.mostrar_senha else "Mostrar"
            surf = FONTE_PEQUENA.render(legenda, True, cores['branco'])
            tela.blit(surf, surf.get_rect(center=self.rect_olho.center))


class BotaoTexto:
    def __init__(self, texto, centro, largura=240, altura=56, cor=None):
        self.texto = texto
        self.cor = cor or cores['azul-jogo']
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.rect.center = centro

    def desenhar(self, tela):
        cor = self.cor
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            cor = tuple(min(255, c + 35) for c in cor)

        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        surf = FONTE_BOTAO.render(self.texto, True, cores['branco'])
        tela.blit(surf, surf.get_rect(center=self.rect.center))

    def clicado(self, pos):
        return self.rect.collidepoint(pos)


# ------------------------------------------------------------------- telas

class TelaConfig:
    """Menu de conta: entrar, cadastrar-se, sair da conta e voltar."""

    def __init__(self):
        cx = LARGURA_TELA // 2
        self.y_inicial = int(ALTURA_TELA * 0.38)
        self.botao_login = BotaoTexto("Entrar", (cx, 0), largura=300)
        self.botao_cadastro = BotaoTexto("Cadastrar-se", (cx, 0), largura=300)
        self.botao_logout = BotaoTexto("Sair da conta", (cx, 0), largura=300)
        self.botao_voltar = BotaoTexto("Voltar", (cx, 0), largura=300, cor=COR_BOTAO_NEUTRO)

    def _botoes_ativos(self, jogador):
        if jogador:
            lista = [("logout", self.botao_logout), ("voltar", self.botao_voltar)]
        else:
            lista = [("login", self.botao_login),
                    ("cadastro", self.botao_cadastro),
                    ("voltar", self.botao_voltar)]

        for i, (_, botao) in enumerate(lista):
            botao.rect.centery = self.y_inicial + i * 80
        return lista

    def tratar_evento(self, evento, jogador):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "voltar"

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for acao, botao in self._botoes_ativos(jogador):
                if botao.clicado(evento.pos):
                    return acao
        return None

    def desenhar(self, tela, jogador):
        tela.fill(cores['cinza-menu'])

        titulo = FONTE_MENSAGEM.render("Conta", True, cores['branco'])
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.15))))

        if jogador:
            status = f"Conectado como {jogador['usuario']}"
        else:
            status = "Você ainda não está conectado"
        surf = FONTE_MSG.render(status, True, cores['azul-jogo'])
        tela.blit(surf, surf.get_rect(center=(LARGURA_TELA // 2, int(ALTURA_TELA * 0.25))))

        for _, botao in self._botoes_ativos(jogador):
            botao.desenhar(tela)


class _TelaFormulario:
    """Base de login e cadastro: campos, Tab/Enter/Esc, mensagem e botões."""
    TITULO = ""

    def __init__(self):
        self.campos = []
        self.mensagem = ""
        self.mensagem_cor = cores['vermelho']
        self.y_titulo = int(ALTURA_TELA * 0.10)
        self.y_mensagem = 0
        self.botao_principal = None
        self.botao_voltar = None

    def _criar_rodape(self, texto_principal):
        """Posiciona mensagem e botões logo abaixo do último campo."""
        cx = LARGURA_TELA // 2
        self.y_mensagem = self.campos[-1].rect.bottom + 14
        y_botoes = self.y_mensagem + 95
        self.botao_principal = BotaoTexto(texto_principal, (cx - 140, y_botoes))
        self.botao_voltar = BotaoTexto("Voltar", (cx + 140, y_botoes), cor=COR_BOTAO_NEUTRO)

    def definir_mensagem(self, texto, erro=True):
        self.mensagem = texto
        self.mensagem_cor = cores['vermelho'] if erro else cores['verde']

    def resetar(self, mensagem=None, sucesso=False):
        for campo in self.campos:
            campo.limpar()
        self.mensagem = ""
        if mensagem:
            self.definir_mensagem(mensagem, erro=not sucesso)
        self._focar(0)

    def _focar(self, indice):
        for i, campo in enumerate(self.campos):
            campo.foco = (i == indice)

    def focar_campo(self, campo):
        self._focar(self.campos.index(campo))

    def _mover_foco(self, passo):
        atual = next((i for i, c in enumerate(self.campos) if c.foco), -1)
        self._focar((atual + passo) % len(self.campos))

    def _erro(self, texto, campo=None):
        self.definir_mensagem(texto, erro=True)
        if campo is not None:
            self._focar(self.campos.index(campo))
        return None

    def enviar(self):
        raise NotImplementedError

    def tratar_evento(self, evento):
        for campo in self.campos:
            campo.tratar_evento(evento)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                self._mover_foco(-1 if evento.mod & pygame.KMOD_SHIFT else 1)
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.enviar()
            elif evento.key == pygame.K_ESCAPE:
                return "voltar"

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_principal.clicado(evento.pos):
                return self.enviar()
            if self.botao_voltar.clicado(evento.pos):
                return "voltar"

        return None

    def desenhar(self, tela):
        tela.fill(cores['cinza-menu'])

        titulo = FONTE_TITULO_TELA.render(self.TITULO, True, cores['branco'])
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, self.y_titulo)))

        for campo in self.campos:
            campo.desenhar(tela)

        if self.mensagem:
            _desenhar_mensagem(tela, self.mensagem, self.mensagem_cor, self.y_mensagem)

        self.botao_principal.desenhar(tela)
        self.botao_voltar.desenhar(tela)


class TelaLogin(_TelaFormulario):
    TITULO = "Entrar"

    def __init__(self):
        super().__init__()
        x = (LARGURA_TELA - LARGURA_CAMPO) // 2
        y0 = int(ALTURA_TELA * 0.30)

        self.campo_usuario = CampoTexto("Nome de usuário", x, y0,
                                        max_len=16, permitido=_permitido_usuario)
        self.campo_senha = CampoTexto("Senha", x, y0 + PASSO_CAMPO, senha=True)
        self.campos = [self.campo_usuario, self.campo_senha]

        self._criar_rodape("Entrar")
        self.jogador_logado = None

    def enviar(self):
        usuario = self.campo_usuario.texto.strip()
        senha = self.campo_senha.texto

        if not usuario or not senha:
            return self._erro("Preencha o usuário e a senha.")

        jogador = db.autenticar(usuario, senha)
        if jogador is None:
            return self._erro("Usuário ou senha incorretos.", self.campo_usuario)

        self.jogador_logado = jogador
        return "logado"


class TelaCadastro(_TelaFormulario):
    TITULO = "Cadastro"

    def __init__(self):
        super().__init__()
        self.y_titulo = int(ALTURA_TELA * 0.08)
        x = (LARGURA_TELA - LARGURA_CAMPO) // 2
        y0 = int(ALTURA_TELA * 0.19)

        self.campo_usuario = CampoTexto("Nome de usuário", x, y0,
                                        max_len=16, permitido=_permitido_usuario)
        self.campo_email = CampoTexto("E-mail", x, y0 + PASSO_CAMPO,
                                        max_len=60, permitido=_permitido_email)
        self.campo_senha = CampoTexto("Senha", x, y0 + 2 * PASSO_CAMPO, senha=True)
        self.campo_nascimento = CampoTexto("Data de nascimento", x, y0 + 3 * PASSO_CAMPO,
                                            mascara_data=True, placeholder="DD/MM/AAAA")
        self.campos = [self.campo_usuario, self.campo_email,
                        self.campo_senha, self.campo_nascimento]

        self._criar_rodape("Cadastrar")
        self.usuario_criado = ""

    def enviar(self):
        usuario = self.campo_usuario.texto.strip()
        email = self.campo_email.texto.strip()
        senha = self.campo_senha.texto
        nascimento = self.campo_nascimento.texto

        erro = validacao.validar_usuario(usuario)
        if erro:
            return self._erro(erro, self.campo_usuario)
        if db.usuario_existe(usuario):
            return self._erro("Nome de usuário já existe. Escolha outro.", self.campo_usuario)

        erro = validacao.validar_email(email)
        if erro:
            return self._erro(erro, self.campo_email)
        if db.email_existe(email):
            return self._erro("E-mail já cadastrado. Tente entrar com a sua conta.", self.campo_email)

        erro = validacao.validar_senha(senha)
        if erro:
            return self._erro(erro, self.campo_senha)

        erro, nascimento_iso = validacao.validar_data_nascimento(nascimento)
        if erro:
            return self._erro(erro, self.campo_nascimento)

        try:
            db.inserir_jogador(usuario, email, senha, nascimento_iso)
        except sqlite3.IntegrityError:
            return self._erro("Usuário ou e-mail já cadastrado. Tente outros dados.", self.campo_usuario)

        self.usuario_criado = usuario
        return "cadastrado"
