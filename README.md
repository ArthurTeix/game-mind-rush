# 🧠 Mind Rush

**Mind Rush** é um jogo educacional desenvolvido como projeto das matérias de "Projeto Interdisciplinar de Sistemas de Informação" e "Princípios de Programação" da **Universidade Federal Rural de Pernambuco (UFRPE)**. Seu objetivo é transformar o conhecimento, estudo e a revisão de conteúdos acadêmicos em uma experiência dinâmica e interativa, combinando elementos de jogos de ação, progressão e aprendizagem.

O jogo combina os gêneros **Endless Runner** e **Rogue-Like**, permitindo que os jogadores enfrentem obstáculos, coletem moedas, respondam perguntas e enfrentem hordas de inimigos. Cada personagem representa um curso universitário, relacionando a experiência de jogo a diferentes áreas do conhecimento (e um personagem temático em homenagem ao professor que ministra as cadeiras).

---

## 🎯 Público-alvo

Estudantes em geral e aspirantes a universitários que buscam uma maneira mais dinâmica, acessível e divertida de  conhecer, estudar, revisar conteúdos acadêmicos.

---

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento do jogo.
- **Pygame:** biblioteca utilizada para desenvolvimento de jogos e recursos gráficos, conforme as dependências do projeto.
- **Git e GitHub:** ferramentas de versionamento e gerenciamento do código-fonte.

---

## 📁 Estrutura do projeto

O projeto está organizado em diretórios e módulos que separam os recursos visuais, as funcionalidades do jogo, os modos de gameplay e os arquivos responsáveis pela inicialização e funcionamento da aplicação.

```text
Mind-Rush/
│
├── assets/
│   ├── fontes/
│   └── img/
│
├── game/
│   ├── database/
│   ├── modos/
│   │   ├── endless/
│   │   └── rogue/
│   ├── ui/
│   ├── util/
│   ├── configuracoes.py
│   ├── motor.py
│   └── render.py
│
├── .editorconfig
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

### Descrição dos diretórios

| Diretório | Descrição |
|---|---|
| `assets/` | Armazena os recursos externos utilizados pelo jogo, como imagens e fontes. Centraliza os arquivos necessários para a composição visual da aplicação. |
| `assets/fontes/` | Armazena os arquivos de fontes tipográficas utilizados na interface e nos elementos visuais do jogo. |
| `assets/img/` | Armazena as imagens e demais recursos gráficos utilizados nos menus, personagens, cenários e elementos da gameplay. |
| `game/` | Diretório principal da lógica do jogo. Reúne os módulos responsáveis pelos sistemas, modos de jogo, interfaces, dados e funcionalidades auxiliares. |
| `game/database/` | Destinado ao gerenciamento e armazenamento dos dados utilizados pelo jogo, incluindo informações relacionadas aos jogadores e banco de questões. |
| `game/elements/` | Reúne os elementos que compõem a gameplay, como objetos, componentes e entidades utilizados durante as partidas. |
| `game/modos/` | Organiza os diferentes modos de jogo, mantendo suas implementações separadas. |
| `game/modos/endless/` | Reúne os módulos e funcionalidades específicos do modo Endless Runner, como mecânicas de corrida, movimentação, obstáculos e coleta de moedas. |
| `game/modos/rogue/` | Reúne os módulos e funcionalidades específicos do modo Rogue-Like, incluindo ondas de inimigos, combate e sistema de melhorias. |
| `game/ui/` | Centraliza os componentes de interface gráfica, telas, menus e elementos de interação com o jogador. |
| `game/util/` | Armazena funções auxiliares e recursos utilitários utilizados por diferentes módulos do projeto. |

### Descrição dos arquivos principais

| Arquivo | Descrição |
|---|---|
| `game/configuracoes.py` | Centraliza as configurações utilizadas pelo jogo, permitindo organizar parâmetros e definições gerais da aplicação. |
| `game/motor.py` | Responsável pelo motor do jogo, concentrando funcionalidades relacionadas à execução e ao gerenciamento da lógica principal. |
| `game/render.py` | Responsável pelos processos de renderização, organizando a apresentação visual dos elementos na tela. |
| `.editorconfig` | Define padrões de configuração para editores de código, ajudando a manter a consistência de formatação entre os integrantes da equipe. |
| `.gitignore` | Especifica arquivos e diretórios que devem ser ignorados pelo Git durante o versionamento do projeto. |
| `main.py` | Arquivo principal e ponto de entrada da aplicação, responsável por iniciar a execução do jogo. |
| `README.md` | Documento de apresentação e documentação do projeto, contendo informações sobre funcionalidades, estrutura, instalação e histórico de versões. |
| `requirements.txt` | Lista as bibliotecas e dependências Python necessárias para a instalação e execução do projeto. |

---

## 🎮 Modos de jogo

### 🏃 Endless Runner — Modo Clássico

O Endless Runner é o modo de corrida contínua, no qual o jogador precisa desviar de obstáculos e coletar moedas para aumentar sua pontuação e interagir com o sistema de perguntas (Utilizando as teclas W ou ⬆️ para pular e S ou ⬇️ para descer).

**Características:**

- Movimentação e desvio de obstáculos.
- Seleção de personagens relacionados a cursos universitários.
- Coleta de moedas durante a partida.
- Perguntas de múltipla escolha vinculadas às moedas coletadas.
- Sistema de vidas associado ao desempenho nas perguntas.
- Pontuação baseada no desempenho do jogador.
- Power-ups que concedem habilidades especiais.
- Sistema de Ranking baseado nas melhores pontuações.

### ⚔️ Rogue-Like

O modo Rogue-Like apresenta uma experiência baseada em ondas (hordas) de inimigos. O jogador precisa sobreviver aos confrontos e escolher melhorias para fortalecer seu personagem durante a progressão (Utilizando as teclas W, S, D e A para movimentação e ⬆️, ⬇️, ➡️ e ⬅️ para disparar projéteis).

**Características:**

- Carregamento do personagem e da primeira horda de inimigos.
- Combate por meio de disparos para derrotar os inimigos.
- Progressão por ondas.
- Disponibilização de três benefícios ao final de cada onda.
- Escolha de apenas um benefício para continuar a partida.
- Aumento progressivo da dificuldade e da quantidade de inimigos.
- Encerramento da partida quando a vida do personagem chega a zero.
- Exibição da última onda sobrevivida e retorno ao menu.

---

## ⚙️ Sistemas e funcionalidades

### 👤 Sistema de usuários

O jogo possui funcionalidades de cadastro e autenticação de jogadores, permitindo o acesso às funcionalidades disponíveis.

### 🧑‍🎓 Sistema de personagens

Os personagens representam diferentes cursos universitários, como Computação, Ciência do Consumo, Letras e História.

O sistema permite selecionar um personagem antes de iniciar o modo Endless Runner. Também contempla a possibilidade de personagens bloqueados, que apresentam requisitos para desbloqueio (Login).

### ❓ Banco de questões

O banco de questões disponibiliza perguntas utilizadas durante as partidas.

Ao coletar uma moeda de pergunta, o sistema seleciona aleatoriamente uma questão do banco padrão associado ao personagem e apresenta suas alternativas para o jogador.

### ❤️ Sistema de vidas e perguntas

As respostas influenciam diretamente a condição do jogador durante a partida.

No fluxo especificado para a coleta de moedas:

- **Resposta correta:** recuperação de 1 coração de vida.
- **Resposta incorreta:** redução de 1 coração de vida.

### 🪙 Sistema de moedas

As moedas de pergunta são coletadas durante a partida. Ao ocorrer a colisão com uma delas, o sistema abre uma pergunta com alternativas.

### ⚡ Power-ups

Os power-ups são recursos especiais que concedem habilidades temporárias ao personagem.

Entre os poderes descritos no projeto está o **Fantasma**, que permite ao personagem ficar intangível durante 5 segundos contra obstáculos.

### 🏆 Sistema de pontuação e ranking

O sistema de pontuação considera o desempenho do jogador durante as partidas, incluindo os obstáculos desviados.

O projeto também contempla um ranking com as cinco melhores pontuações conquistadas pelo jogador.

---

## 🚀 Instalação e execução

### Pré-requisitos

- Python instalado.
- Git instalado.
- Gerenciador de pacotes pip.

### 1. Clone o repositório

```bash
git clone https://github.com/ArthurTeix/game-mind-rush.git
```

### 2. Acesse o diretório do projeto

```bash
cd game-mind-rush
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o jogo

```bash
python main.py
```

---

## 📦 Histórico de versões e releases

### 🚀 Release 1.0 — Versão inicial

A primeira release estabeleceu a estrutura inicial do jogo e seus principais sistemas de navegação e gameplay.

| Funcionalidade | Descrição |
|---|---|
| Menu e navegação | Menu principal e navegação entre as funcionalidades do jogo. |
| Cadastro de jogador | Cadastro de novos jogadores. |
| Login | Autenticação dos jogadores. |
| Sistema de jogo | Movimentação do personagem e desvio de obstáculos. |
| Sistema de pontuação | Atribuição de pontos ao desviar dos obstáculos. |
| Ranking | Armazenamento das cinco melhores pontuações conquistadas pelo jogador. |

### 🚀 Release 2.0 — Expansão da gameplay

A segunda release ampliou as possibilidades de interação, adicionando sistemas educacionais, novos personagens e um novo modo de jogo.

| Requisito | Funcionalidade | Descrição |
|---|---|---|
| RF006 | Seleção de personagens | Permite selecionar personagens relacionados aos cursos universitários antes de iniciar o Endless Runner. |
| RF007 | Banco de questões padrão | Disponibiliza perguntas selecionadas aleatoriamente para utilização durante as partidas. |
| RF009 | Power-ups | Permite obter habilidades especiais ao colidir com os respectivos objetos. |
| RF010 | Moedas e perguntas | Abre perguntas com alternativas e temporizador de 50 segundos após a coleta de moedas. |
| RF011 | Modo Rogue-Like | Introduz batalhas por ondas, combate contra inimigos e seleção de melhorias entre as ondas. |

**Destaques da Release 2.0:**

- Integração entre coleta de moedas e perguntas educacionais.
- Recuperação e redução de vida conforme as respostas.
- Implementação do Power-up Fantasma.
- Introdução do modo Rogue-Like.
- Progressão por ondas com seleção de benefícios.

### 🚀 Release 3.0 — Melhorias e expansão educacional

A terceira release está planejada para ampliar as funcionalidades de gerenciamento de usuários e introduzir uma nova experiência de aprendizagem personalizada.

As funcionalidades abaixo estão planejadas e não devem ser consideradas implementadas.

| Requisito | Funcionalidade | Descrição |
|---|---|---|
| RF012 | Alterar nome de usuário | Permite modificar o nome de usuário pelo perfil, verificando a disponibilidade do novo nome. |
| RF013 | Alterar senha | Permite atualizar a senha do jogador por meio do perfil. |
| RF014 | Apagar conta | Permite excluir permanentemente a conta do jogador mediante confirmação. |
| RF015 | Modo Flashcard | Introduz um sistema de estudo personalizado com perguntas e respostas cadastradas pelo próprio jogador. |
| RF016 | Tesouros no Rogue | Introduz um sistema de prêmios no modo rogue-like. |

---

## 📊 Requisitos funcionais

Os requisitos funcionais do projeto estão organizados por identificação:

| Identificação | Requisito |
|---|---|
| RF006 | Selecionar personagem |
| RF007 | Banco de questões do jogo / padrão |
| RF009 | Power-ups |
| RF010 | Pegar moeda e exibir pergunta |
| RF011 | Modo Rogue-Like |
| RF012 | Trocar nome de usuário |
| RF013 | Trocar senha |
| RF014 | Apagar conta |
| RF015 | Modo Flashcard |

---

## 📑 Documentação e fluxogramas

Os fluxogramas do projeto documentam os fluxos principais, alternativos e de validação das funcionalidades do sistema, permitindo visualizar o comportamento esperado das operações e as interações entre jogador e aplicação.

**[📄 Acessar os fluxogramas do Mind Rush no Google Drive](https://drive.google.com/file/d/1fE1Pq1ITFS5ljT3zZ30k4zELO8ufPyjS/view?usp=drive_link)**

Os fluxogramas contemplam:

1. Menu e seleção de personagens.
2. Jogo.
3. Cadastro.
4. Power-ups.
5. Login.
6. Alteração de nome de usuário e senha.
7. Exclusão de conta.
8. Banco de questões.
9. Modo Flashcard.

---

## 👥 Equipe de desenvolvimento

| Integrante | Responsabilidades |
|---|---|
| Arthur Teixeira | Desenvolvimento do jogo, organização do projeto, desenvolvimento do artigo e design. |
| Esthefany Vitória | Design, desenvolvimento do jogo, desenvolvimento do artigo e organização do projeto. |
| Richardson Barbosa | Organização do projeto, desenvolvimento do artigo e desenvolvimento do jogo. |
