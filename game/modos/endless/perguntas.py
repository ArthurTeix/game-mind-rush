import random

AREAS = {
    "computacao": [
        {"pergunta": "Qual estrutura de dados segue a regra LIFO (o último a entrar é o primeiro a sair)?",
        "correta": "Pilha", "erradas": ["Fila", "Árvore", "Grafo"]},
        {"pergunta": "O que significa a sigla CPU?",
        "correta": "Unidade Central de Processamento",
        "erradas": ["Unidade Central de Programas", "Controle Principal de Usuário", "Computador Pessoal Universal"]},
        {"pergunta": "Quantos bits tem um byte?",
        "correta": "8", "erradas": ["4", "16", "32"]},
        {"pergunta": "Qual linguagem é usada para estilizar páginas web?",
        "correta": "CSS", "erradas": ["SQL", "Python", "C"]},
        {"pergunta": "Em Python, qual função exibe um texto na tela?",
        "correta": "print()", "erradas": ["echo()", "write()", "show()"]},
    ],
    "consumo": [
        {"pergunta": "O Código de Defesa do Consumidor é a Lei nº:",
        "correta": "8.078/1990", "erradas": ["9.394/1996", "12.965/2014", "13.709/2018"]},
        {"pergunta": "Em compras feitas pela internet, em quantos dias o consumidor pode desistir da compra (direito de arrependimento)?",
        "correta": "7 dias", "erradas": ["2 dias", "15 dias", "30 dias"]},
        {"pergunta": "Qual órgão é conhecido por atender e orientar o consumidor em reclamações?",
        "correta": "Procon", "erradas": ["Detran", "Receita Federal", "INSS"]},
        {"pergunta": "Como se chama o aumento generalizado e contínuo dos preços?",
        "correta": "Inflação", "erradas": ["Deflação", "Recessão", "Superávit"]},
        {"pergunta": "Segundo o Código de Defesa do Consumidor, quem compra um produto tem direito a:",
        "correta": "Informação clara sobre o produto",
        "erradas": ["Desconto em toda compra", "Troca sem nenhum motivo em qualquer loja", "Frete grátis sempre"]},
    ],
    "letras": [
        {"pergunta": "Quem escreveu o romance \"Dom Casmurro\"?",
        "correta": "Machado de Assis", "erradas": ["José de Alencar", "Clarice Lispector", "Graciliano Ramos"]},
        {"pergunta": "Qual é o plural de \"cidadão\"?",
        "correta": "cidadãos", "erradas": ["cidadões", "cidadães", "cidadans"]},
        {"pergunta": "Qual figura de linguagem aparece em \"Seus olhos são duas estrelas\"?",
        "correta": "Metáfora", "erradas": ["Comparação", "Hipérbole", "Ironia"]},
        {"pergunta": "Quem é o autor de \"Os Lusíadas\"?",
        "correta": "Luís de Camões", "erradas": ["Fernando Pessoa", "Eça de Queirós", "Gil Vicente"]},
        {"pergunta": "Qual é a classe gramatical da palavra \"rapidamente\"?",
        "correta": "Advérbio", "erradas": ["Adjetivo", "Substantivo", "Verbo"]},
    ],
    "historia": [
        {"pergunta": "Em que ano o Brasil declarou sua independência de Portugal?",
        "correta": "1822", "erradas": ["1500", "1889", "1930"]},
        {"pergunta": "Quem proclamou a República no Brasil, em 1889?",
        "correta": "Marechal Deodoro da Fonseca",
        "erradas": ["Dom Pedro II", "Getúlio Vargas", "Tiradentes"]},
        {"pergunta": "Em que ano foi assinada a Lei Áurea, que aboliu a escravidão no Brasil?",
        "correta": "1888", "erradas": ["1822", "1871", "1900"]},
        {"pergunta": "Em que ano a frota de Pedro Álvares Cabral chegou ao Brasil?",
        "correta": "1500", "erradas": ["1492", "1530", "1580"]},
        {"pergunta": "Em que ano começou a Primeira Guerra Mundial?",
        "correta": "1914", "erradas": ["1905", "1939", "1945"]},
    ],
    "pokemon": [
        {"pergunta": "Qual é o tipo do Pikachu?",
        "correta": "Elétrico", "erradas": ["Fogo", "Água", "Planta"]},
        {"pergunta": "Qual é o Pokémon inicial do tipo Fogo da primeira geração?",
        "correta": "Charmander", "erradas": ["Bulbasaur", "Squirtle", "Pidgey"]},
        {"pergunta": "Quantos Pokémon existem na primeira geração (região de Kanto)?",
        "correta": "151", "erradas": ["100", "251", "386"]},
        {"pergunta": "Em qual cidade o Ash nasceu?",
        "correta": "Pallet Town", "erradas": ["Pewter City", "Viridian City", "Cerulean City"]},
        {"pergunta": "Para qual Pokémon o Pikachu evolui?",
        "correta": "Raichu", "erradas": ["Pichu", "Pidgeot", "Jolteon"]},
    ],
}


class SorteadorPerguntas:
    """Sorteia perguntas de uma área sem repetir até acabarem todas
    (depois embaralha de novo). Também embaralha as alternativas."""

    def __init__(self, area):
        self.area = area
        self._restantes = []

    def proxima(self):
        if not self._restantes:
            self._restantes = list(AREAS[self.area])
            random.shuffle(self._restantes)

        base = self._restantes.pop()
        alternativas = [base["correta"]] + list(base["erradas"][:3])
        random.shuffle(alternativas)

        return {
            "pergunta": base["pergunta"],
            "alternativas": alternativas,
            "correta": alternativas.index(base["correta"]),
        }
