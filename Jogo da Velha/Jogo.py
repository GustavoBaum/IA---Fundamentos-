"""
Turma: IA - Ciências da Computação - 6º Semestre
Nome Integrantes: Douglas, Eugênio, Guilherme Bez, Gustavo Baum e Rembrandt
16/10/2026 - 08:06

Jogo escolhido: Qual jogo o grupo escolheu? Quais são suas regras?
R: Jogo da Velha

Estado inicial: Como o jogo começa? Como esse estado pode ser representado? 
R: O jogo começa com um tabuleiro vazio, representado por uma matriz 3x3, onde cada célula pode estar vazia, conter um "X" (jogador MAX) ou um "O" (jogador MIN).

Jogadores: Quantos jogadores participam? Quem são MAX e MIN?
R: O jogo é jogado por dois jogadores. O jogador MAX é representado pelo "X" e o jogador MIN é representado pelo "O".

Ações possíveis: Quais ações cada jogador pode executar? Existem restrições? 
R: Cada jogador pode colocar seu símbolo ("X" ou "O", respectivamente) em qualquer célula vazia do tabuleiro(matriz 3x3). A restrição é que uma célula já ocupada não pode ser escolhida novamente.

Função de transição: Como oestado do jogo miuda após cada ação? 
R: Após cada ação, o estado do jogo muda ao atualizar a célula escolhida pelo jogador com seu símbolo correspondente. O tabuleiro é atualizado para refletir a nova configuração.

Estado terminal: Em quais situações o jogo termina? Como identificar vitória, derrota ou empate?
R: O jogo termina quando um jogador consegue alinhar três de seus símbolos em uma linha, coluna ou diagonal, resultando em vitória para esse jogador. 
   Se todas as células do tabuleiro estiverem preenchidas e nenhum jogador tiver vencido, o jogo termina em empate.

Função de utilidade: Como serão atribuídas pontuações aos resultados do jogo?
R: A função de utilidade atribui pontuações da seguinte forma: vitória do jogador MAX (X) recebe uma pontuação de +1, vitória do jogador MIN (O) 
   recebe uma pontuação de -1, e empate recebe uma pontuação de 0.

Tipo de jogo: O jogo é determinístico ou estocástico? Por quê?
R: O jogo é determinístico, pois não há elementos de sorte ou aleatoriedade envolvidos. O resultado do jogo depende exclusivamente das ações dos jogadores e das regras estabelecidas.
"""

matriz = [ 
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

matriz = [[0 for _ in range(3)] for _ in range(3)]; 
semVencedor = 0

def solicitarJogador1(jogador):
    linha1, coluna1 = map(int, jogador.split())
    linha1 = int(linha1)-1
    coluna1 = int(coluna1)-1
    
    if (linha1 > 2 or linha1 < 0) or (coluna1 > 2 or coluna1 < 0):
        print("Posição inválida. Tente novamente.")
        jogador = input("Vez do Jogador 1 (X), digite a linha e a coluna: ")
        return solicitarJogador1(jogador)
    
    if (matriz[linha1][coluna1] == "X" or matriz[linha1][coluna1] == "O"):
        print("Posição ocupada. Tente novamente")
        jogador = input("Vez do Jogador 1 (X), digite a linha e a coluna: ")
        return solicitarJogador1(jogador)

    matriz[linha1][coluna1] = "X"

def solicitarJogador2(jogador):
     linha2, coluna2 = map(int, jogador.split())
     linha2 = int(linha2)-1
     coluna2 = int(coluna2)-1

     if (linha2 > 2 or linha2 < 0) or (coluna2 > 2 or coluna2 < 0):
        print("Posição Inválida. Tente novamente.")
        jogador = input("Vez do Jogador 2 (O), digite a linha e a coluna: ")
        return solicitarJogador2(jogador)
     
     if (matriz[linha2][coluna2] == "X" or matriz[linha2][coluna2] == "O"):
         print("Posição ocupada. Tente novamente.")
         jogador = input("Vez do Jogador 2 (O), digite a linha e a coluna: ")
         return solicitarJogador2(jogador)

     matriz[linha2][coluna2] = "O"

def mostrarMatriz():
    for linha in matriz:
        for elemento in linha:
            print(elemento, end=" ")
        print()

def verificarVencedor():
    # Verificar linhas
    for linha in matriz:
        if linha.count("X") == 3:
            print("Jogador 1 (X) venceu!")
            return +1
        elif linha.count("O") == 3:
            print("Jogador 2 (O) venceu!")
            return +1

    # Verificar colunas
    for coluna in range(3):
        if [matriz[linha][coluna] for linha in range(3)].count("X") == 3:
            print("Jogador 1 (X) venceu!")
            return +1
        elif [matriz[linha][coluna] for linha in range(3)].count("O") == 3:
            print("Jogador 2 (O) venceu!")
            return +1

    # Verificar diagonais
    if [matriz[i][i] for i in range(3)].count("X") == 3 or [matriz[i][2 - i] for i in range(3)].count("X") == 3:
        print("Jogador 1 (X) venceu!")
        return +1
    elif [matriz[i][i] for i in range(3)].count("O") == 3 or [matriz[i][2 - i] for i in range(3)].count("O") == 3:
        print("Jogador 2 (O) venceu!")
        return +1

    # Verificar empate
    if all(elemento != 0 for linha in matriz for elemento in linha):
        print("Empate!")
        return +1

    return 0

def jogar():
    mostrarMatriz()
    semVencedor = verificarVencedor()

    while semVencedor == 0:
        jogador1 = input("Vez do Jogador 1 (X), digite a linha e a coluna: ")
        solicitarJogador1(jogador1)
        # Atualizar a matriz com a jogada do jogador 1
        semVencedor += verificarVencedor()
        if semVencedor == 0:
            jogador2 = input("Vez do Jogador 2 (O), digite a linha e a coluna: ")
            solicitarJogador2(jogador2)
            # Atualizar a matriz com a jogada do jogador 2
            semVencedor += verificarVencedor()
            jogar()
        elif semVencedor == 1:
            mostrarMatriz()
            print("Fim do jogo!")
        break

jogar()
