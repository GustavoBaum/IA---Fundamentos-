# Feito por Gustavo Baum
# 18/09/2026 - 9:42

import random

# Constantes / valores da matriz
LIMPO = 0
SUJO = 1
ROBO = 2
PAREDE = 3

ACOES_MOVIMENTO = {
    'acima':    (-1, 0),
    'abaixo':   (1, 0),
    'esquerda': (0, -1),
    'direita':  (0, 1),
}

SIMBOLOS = {LIMPO: '0', SUJO: '2', ROBO: 'R', PAREDE: '1'}


# Ambiente: criacao aleatoria da sala e do robo
def criar_ambiente(n=4, prob_sujeira=None):

    if prob_sujeira is None:
        prob_sujeira = random.uniform(0.2, 0.8) 

    tamanho = n + 2
    estado = [[PAREDE] * tamanho for _ in range(tamanho)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            estado[i][j] = SUJO if random.random() < prob_sujeira else LIMPO

    # garante pelo menos uma sujeira (senao o teste fica trivial)
    if not any(SUJO in linha for linha in estado):
        i, j = random.randint(1, n), random.randint(1, n)
        estado[i][j] = SUJO

    posicao_robo = (random.randint(1, n), random.randint(1, n))
    return estado, posicao_robo


# Funcao de mapeamento: traduz a matriz bruta em informacoes uteis
def funcaoMapear(matriz):
    
    posicao_robo = None
    proxima_sujeira = None

    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor == ROBO and posicao_robo is None:
                posicao_robo = (i, j)
            elif valor == SUJO and proxima_sujeira is None:
                proxima_sujeira = (i, j)

    return {'posicao_robo': posicao_robo, 'proxima_sujeira': proxima_sujeira}


# O AGENTE REATIVO SIMPLES  
def agenteReativoSimples(percepcao):
    
    matriz = percepcao['matriz']
    sujo_aqui = percepcao['sujo_aqui']

    if sujo_aqui:
        return 'aspirar'

    mapa = funcaoMapear(matriz)
    linha, coluna = mapa['posicao_robo']
    alvo = mapa['proxima_sujeira']

    if alvo is None:
        return 'aspirar'  # sala inteira limpa, acao sem efeito

    linha_alvo, coluna_alvo = alvo
    if linha < linha_alvo:
        return 'abaixo'
    if linha > linha_alvo:
        return 'acima'
    if coluna < coluna_alvo:
        return 'direita'
    if coluna > coluna_alvo:
        return 'esquerda'
    return 'aspirar'  # nao deveria acontecer (cairia na regra 1 antes)


# Simulador: aplica as acoes do agente sobre o ambiente
def mover(posicao, acao):
    dl, dc = ACOES_MOVIMENTO.get(acao, (0, 0))
    return (posicao[0] + dl, posicao[1] + dc)


def sujeiras_restantes(estado):
    return sum(linha.count(SUJO) for linha in estado)


def imprimir_matriz(matriz, titulo=None):
    if titulo:
        print(titulo)
    for linha in matriz:
        print(' '.join(SIMBOLOS[v] for v in linha))
    print()


def executar_simulacao(n=4, prob_sujeira=None, seed=None, max_passos=None,
                        mostrar_passos=False):
    estado, posicao = criar_ambiente(n, prob_sujeira)
    sujeiras_iniciais = sujeiras_restantes(estado)
    if max_passos is None:
        max_passos = 20 * n * n + 100  # margem confortavel p/ qualquer N

    if mostrar_passos:
        imprimir_matriz(
            [[ROBO if (i, j) == posicao else estado[i][j]
              for j in range(len(estado[0]))] for i in range(len(estado))],
            titulo=f"Estado inicial (robo em {posicao}, {sujeiras_iniciais} sujeiras):"
        )

    passos = 0
    while passos < max_passos and sujeiras_restantes(estado) > 0:
        linha, coluna = posicao
        sujo_aqui = (estado[linha][coluna] == SUJO)

        matriz_percebida = [l[:] for l in estado]
        matriz_percebida[linha][coluna] = ROBO

        percepcao = {'matriz': matriz_percebida, 'sujo_aqui': sujo_aqui}
        acao = agenteReativoSimples(percepcao)

        if mostrar_passos:
            print(f"  passo {passos:3d}: robo em {posicao}, sujo_aqui={sujo_aqui!s:5} -> {acao}")

        if acao == 'aspirar':
            if sujo_aqui:
                estado[linha][coluna] = LIMPO
        else:
            nova_posicao = mover(posicao, acao)
            nl, nc = nova_posicao
            if estado[nl][nc] != PAREDE:      # bater na parede nao tem efeito
                posicao = nova_posicao

        passos += 1

    if mostrar_passos:
        imprimir_matriz(estado, titulo=f"Estado final apos {passos} passos:")

    return {
        'limpou_tudo': sujeiras_restantes(estado) == 0,
        'passos': passos,
        'sujeiras_iniciais': sujeiras_iniciais,
        'n': n,
    }


# Demonstracao e testes
if __name__ == '__main__':
    print("=" * 70)
    print("DEMONSTRACAO DETALHADA - sala 4x4, uma execucao com passos")
    print("=" * 70)
    resultado = executar_simulacao(n=4, seed=42, mostrar_passos=True)
    print(f"-> limpou tudo? {resultado['limpou_tudo']}  "
          f"(sujeiras iniciais: {resultado['sujeiras_iniciais']}, "
          f"passos usados: {resultado['passos']})")

