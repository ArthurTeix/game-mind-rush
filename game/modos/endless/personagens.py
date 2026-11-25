import pygame

# Personagens disponíveis na tela de escolha.
#   id            -> também é a chave das perguntas em perguntas.py (AREAS)
#   cor           -> cor do retângulo (enquanto não existem as imagens)
#   imagens       -> quando tiver as imagens, troque None pela lista de caminhos
#                    (os frames da animação de corrida), por exemplo:
#                    ["./assets/img/personagens/letras/pos0.png",
#                     "./assets/img/personagens/letras/pos1.png",
#                     "./assets/img/personagens/letras/pos2.png"]
#   requer_login  -> True = só fica liberado para quem fez login
PERSONAGENS = [
    {
        "id": "computacao",
        "nome": "Computação",
        "cor": (12, 183, 242),
        "imagens": ["./assets/img/personagens/computacao/pc_pos0.png",
        "./assets/img/personagens/computacao/pc_pos1.png"],
        "requer_login": False,
    },
    {
        "id": "consumo",
        "nome": "Ciências do Consumo",
        "cor": (46, 204, 113),
        "imagens": ["./assets/img/personagens/computacao/papelao_pos0.png",
        "./assets/img/personagens/computacao/papelao_pos1.png"],
        "requer_login": False,
    },
    {
        "id": "letras",
        "nome": "Letras",
        "cor": (255, 105, 180),
        "imagens": ["./assets/img/personagens/computacao/livro_pos0.png",
        "./assets/img/personagens/computacao/livro_pos1.png"],
        "requer_login": False,
    },
    {
        "id": "historia",
        "nome": "História",
        "cor": (233, 147, 0),
        "imagens": ["./assets/img/personagens/computacao/historia_pos0.png",
        "./assets/img/personagens/computacao/historia_pos1.png"],
        "requer_login": False,
    },
    {
        "id": "pokemon",
        "nome": "Pokémon",
        "cor": (230, 50, 50),
        "imagens": ["./assets/img/personagens/computacao/cleyton_pos0.png",
        "./assets/img/personagens/computacao/cleyton_pos1.png"],
        "requer_login": True,
    },
]


def criar_sprite_cor(cor, largura, altura):
    """Retângulo arredondado com um olho (mostra que ele olha para a direita).
    Serve de personagem até as imagens ficarem prontas."""
    sprite = pygame.Surface((largura, altura), pygame.SRCALPHA)
    corpo = pygame.Rect(0, 0, largura, altura)
    escura = tuple(max(c - 70, 0) for c in cor)
    raio = max(4, largura // 6)

    pygame.draw.rect(sprite, cor, corpo, border_radius=raio)
    pygame.draw.rect(sprite, escura, corpo, width=max(2, largura // 20), border_radius=raio)

    olho = max(3, largura // 9)
    cx, cy = int(largura * 0.68), int(altura * 0.28)
    pygame.draw.circle(sprite, (255, 255, 255), (cx, cy), olho)
    pygame.draw.circle(sprite, (20, 20, 20), (cx + olho // 3, cy), max(2, olho // 2))
    return sprite


_cache_previews = {}

def obter_preview(personagem, largura, altura):
    """Imagem do personagem para a tela de escolha (guardada em cache)."""
    chave = (personagem["id"], largura, altura)
    if chave not in _cache_previews:
        if personagem["imagens"]:
            imagem = pygame.image.load(personagem["imagens"][0]).convert_alpha()
            _cache_previews[chave] = pygame.transform.scale(imagem, (largura, altura))
        else:
            _cache_previews[chave] = criar_sprite_cor(personagem["cor"], largura, altura)
    return _cache_previews[chave]
