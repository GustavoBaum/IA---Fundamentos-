from copy import deepcopy 
import time
import random

"""
Turma: IA - Ciências da Computação - 6º Semestre
Nome Integrantes: Eugênio, Guilherme Bez, Gustavo Baum e Rembrandt
23/10/2026 - 08:53

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

def solicitarCPU1():
    print("Vez da CPU1 (X), pensando...")

    time.sleep(1.5)

    melhor_valor = float("-inf")
    melhores_movimentos = []

    for i in range(3):
        for j in range(3):
            if matriz[i][j] == 0:
                matriz[i][j] = "X"
                valor = miniMax(matriz, maximizing=False)
                matriz[i][j] = 0

                if valor > melhor_valor:
                  melhor_valor = valor 
                  melhores_movimentos = [(i ,j)]
                elif valor == melhor_valor:
                    melhores_movimentos.append((i, j))

    if melhores_movimentos:
        escolha = random.choice(melhores_movimentos)
        matriz[escolha[0]][escolha[1]] = "X"
    
def solicitarCPU2():
    print("Vez da CPU (O), pensando...")

    time.sleep(1.5) # Pequeno delay para a jogada da CPU
    
    melhor_valor = float("inf")
    melhores_movimentos = []

    for i in range(3):
        for j in range(3):
            if matriz[i][j] == 0:
                matriz[i][j] = "O"
                valor = miniMax(matriz, maximizing=True)
                matriz[i][j] = 0

                if valor < melhor_valor:
                    melhor_valor = valor
                    melhores_movimentos = [(i, j)]
                elif valor == melhor_valor:
                    melhores_movimentos.append([i, j])

    if melhores_movimentos:
        escolha = random.choice(melhores_movimentos)
        matriz[escolha[0]][escolha[1]] = "O"

def mostrarMatriz():
    for linha in matriz:
        for elemento in linha:
            print(elemento, end=" ")
        print()

def matrizes_candidatas(matriz, player):
    mc = []

    for i in range(len(matriz)):
        for j in range(len(matriz)):
           if matriz[i][j] != ' ':
               continue
           candidatos = deepcopy(matriz)
           candidatos[i][j] = player

           mc.append(candidatos)

    return mc 

def is_win(matriz, jogador):
    # Verifica linhas
    for linha in matriz:
        if all(cell == jogador for cell in linha):
            return True

    # Verifica colunas
    for col in range(3):
        if all(matriz[row][col] == jogador for row in range(3)):
            return True

    # Verifica diagonais
    if all(matriz[i][i] == jogador for i in range(3)) or all(matriz[i][2-i] == jogador for i in range(3)):
        return True;

    return False
 
def is_terminal(matriz):
    return (
        is_win(matriz, "X")
        or is_win(matriz, "O")
        or all(cell != 0 for linha in matriz for cell in linha)
    )

def avaliar(matriz):
    if is_win(matriz, "X"):
        return 1
    if is_win(matriz, "O"):
        return -1
    return 0

def miniMax(matriz, maximizing=False):
    if is_terminal(matriz):
        return avaliar(matriz)

    if maximizing:
        value = float("-inf")
        for child in matrizes_candidatas(matriz, "X"):
            value = max(value, miniMax(child, False))
        return value
    else:
        value = float("+inf")
        for child in matrizes_candidatas(matriz, "O"):
            value = min*value, miniMax(child, True)
        return value       

def verificarVencedor():
    if is_win(matriz, "X"):
        print("CPU1 (X) venceu!")
        return True
    elif is_win(matriz, "O"):
        print("CPU2 (O) venceu!")
        return True
        
    elif all(cell != 0 for linha in matriz for cell in linha):
        print("Empate!")
        return True
    return False

def jogar():
    while (True):
        mostrarMatriz()

        solicitarCPU1()

        if verificarVencedor():
            mostrarMatriz()
            print("Fim do Jogo!")
            break

        solicitarCPU2()

        if verificarVencedor():
            mostrarMatriz()
            print("Fim do Jogo!")
            break 

if __name__ == "__main__":
  jogar()