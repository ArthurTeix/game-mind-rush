# 🧠 Mind Rush

## 📖 Sobre o projeto

**Mind Rush** é um jogo educacional no estilo *endless runner*, desenvolvido como projeto interdisciplinar da **Universidade Federal Rural de Pernambuco (UFRPE)**. A proposta é transformar o estudo e a revisão de conteúdos em uma experiência dinâmica e divertida: enquanto o jogador corre e desvia de obstáculos, ele coleta moedas que abrem perguntas relacionadas a diferentes cursos da universidade, unindo diversão e aprendizado em uma única jogada.

Cada personagem do jogo representa um curso (como Computação, Veterinária, Letras e História), e responder corretamente às perguntas garante vidas extras, enquanto errar torna a partida mais desafiadora. O jogo também contará com um modo de estudo personalizado (estilo flashcards), onde o próprio jogador pode cadastrar suas perguntas e respostas para revisar qualquer conteúdo de forma mais leve e engajante.

## 🎯 Público-alvo

Estudantes em geral e aspirantes a universitários que buscam uma forma mais dinâmica, leve e envolvente de estudar e revisar conteúdos.

## ✅ Funcionalidades atuais

- 🏃 Boneco esquivando de obstáculos (gameplay básico de *endless runner*)

## 🛠️ Funcionalidades a incrementar

- ❓ Sistema de perguntas e respostas vinculado a moedas coletadas durante a corrida
- ❤️ Sistema de vidas: acertos recuperam vida, erros reduzem a velocidade/dificultam o jogo
- 🏆 Sistema de pontuação baseado em acertos, desvios de obstáculos e perguntas respondidas
- ⚡ Power-ups especiais (super velocidade, intangibilidade, entre outros)
- 🎴 Modo Anki: cadastro de perguntas e respostas personalizadas para estudo livre
- 🧑‍🎓 Personagens temáticos por curso (Computação, Veterinária, Letras, História)
- 🌟 Personagens e conquistas especiais desbloqueáveis
- 👤 Sistema de cadastro e login de usuário

## 🚀 Como executar

1. Clone o repositório:
```bash
git clone https://github.com/ArthurTeix/game-mind-rush.git
cd game-mind-rush
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o jogo:
```bash
python main.py
```

## 🚀 Release 1.0

| Funcionalidade | Descrição |
|---|---|
| Menu / Navegação | Menu principal e navegação entre as funcionalidades do jogo. |
| Cadastro de Jogador | Cadastro de novos jogadores no sistema. |
| Login | Autenticação do jogador para acesso ao sistema. |
| Sistema de Jogo | Execução da partida com movimentação e desvio de obstáculos. |
| Sistema de Pontuação | Pontuação atribuída ao jogador ao esquivar dos obstáculos durante a partida. |
| Ranking | Armazena as 5 melhores pontuações conquistadas pelo jogador. |

---

## 🚀 Release 2.0

| Funcionalidade | Descrição |
|---|---|
| Seleção de Personagens | Permite ao jogador a escolher um personagem referente a um curso em específico antes de começar o modo Endless Runner. |
| Moeda de Pergunta | Permite ao jogador coletar moedas durante a partida e responder às perguntas. |
| Perguntas e Respostas em Múltipla Escolha | Ao coletar a Moeda de Pergunta, o sistema exibe uma pergunta de uma área de conhecimento específica e o jogador precisa responder para avançar. Se o usuário acertar a resposta, ele ganha uma vida (respeitando o limite de 3 vidas), caso contrário ele perde uma vida. |
| Banco de Questões | Armazena e disponibiliza questões utilizadas durante o jogo. |
| Power-up: Fantasma | Adiciona um recurso especial que pode deixar o personagem intangível por 5 segundos durante a partida. |
| Modo Rogue-Like | O jogador precisa enfrentar Ondas/Hordas. A cada fim de uma Onda, o usuário pode escolher um benefício para prosseguir no jogo. |

---

## Fluxogramas
<a href="https://drive.google.com/file/d/1fE1Pq1ITFS5ljT3zZ30k4zELO8ufPyjS/view?usp=drive_link">Para acessar os fluxogramas, clique aqui.<a>

Os Fluxogramas contidos no link acima mostra todos os tratamentos de Fluxo Principal, Alternativos e de Erros. Sendo Esses:

1. Menu e Seleção de Personagens;
2. Jogo;
3. Cadastro;
4. Power-up;
5. Login;
6. Alterar Nome de Usuário/Senha;
7. Apagar Conta;
8. Banco de Questões;
9. Modo Flashcard;

## 👥 Integrantes

Arthur Teixeira - Desenvolvimento | Organização do Projeto | Design <br>
Esthefany Vitória - Design | Desenvolvimento | Organização do Projeto <br>
Richardson - Organização do Projeto | Desenvolvimento do Artigo
