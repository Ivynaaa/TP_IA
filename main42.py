import heapq
import itertools

class No:
    def __init__(self, posicao, g, h, pai=None):
        self.posicao = posicao
        self.g = g
        self.h = h
        self.f = g + h
        self.pai = pai

    def __lt__(self, outro):
        return self.f < outro.f

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def busca_a_estrela(mapa, inicio, fim):
    lista_aberta = []
    lista_fechada = set()
    no_inicio = No(inicio, 0, heuristica(inicio, fim))
    heapq.heappush(lista_aberta, no_inicio)

    while lista_aberta:
        no_atual = heapq.heappop(lista_aberta)
        lista_fechada.add(no_atual.posicao)

        if no_atual.posicao == fim:
            caminho = []
            while no_atual:
                caminho.append(no_atual.posicao)
                no_atual = no_atual.pai
            return caminho[::-1]

        vizinhos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for movimento in vizinhos:
            posicao_vizinha = (no_atual.posicao[0] + movimento[0], no_atual.posicao[1] + movimento[1])

            if (0 <= posicao_vizinha[0] < len(mapa)) and (0 <= posicao_vizinha[1] < len(mapa[0])):
                if posicao_vizinha in lista_fechada:
                    continue

                # Verificar se a posição vizinha é um obstáculo
                if mapa[posicao_vizinha[0]][posicao_vizinha[1]] == 'E':
                    continue

                custo_terreno = custo_terreno_map.get(mapa[posicao_vizinha[0]][posicao_vizinha[1]], float('inf'))
                custo_g = no_atual.g + custo_terreno
                custo_h = heuristica(posicao_vizinha, fim)
                no_vizinho = No(posicao_vizinha, custo_g, custo_h, no_atual)

                if all(no_vizinho.posicao != n.posicao or no_vizinho.f < n.f for n in lista_aberta):
                    heapq.heappush(lista_aberta, no_vizinho)

    return None

def calcular_custo_total(mapa, inicio, caminho):
    custo_total = 0
    caminho_total = []
    inicio_atual = inicio

    custos = []
    mapas_intermediarios = []

    for parada in caminho:
        segmento_caminho = busca_a_estrela(mapa, inicio_atual, parada)
        if segmento_caminho is None:
            return float('inf'), [], [], []
        
        # Debug: verificar o custo de cada terreno
        for x, y in segmento_caminho:
            print(f"Terreno: {mapa[x][y]}, Custo: {custo_terreno_map.get(mapa[x][y], float('inf'))}")
        
        custo_segmento = sum(custo_terreno_map.get(mapa[x][y], float('inf')) for x, y in segmento_caminho)
        print(f"Custo do segmento de {inicio_atual} para {parada}: {custo_segmento}")
        custo_total += custo_segmento
        custos.append(custo_segmento)
        caminho_total += segmento_caminho[:-1]
        caminho_total.append(parada)
        inicio_atual = parada

        # Criar um mapa intermediário para esta parada
        mapa_intermediario = desenhar_mapa(mapa, caminho_total, inicio, parada, mostrar=False)
        mapas_intermediarios.append(mapa_intermediario)

    return custo_total, caminho_total, custos, mapas_intermediarios

def forca_bruta_com_a_estrela(mapa, inicio, paradas):
    melhor_custo = float('inf')
    melhor_caminho = []
    melhor_custos = []
    melhor_mapas = []

    for permutacao in itertools.permutations(paradas):
        print("Processando permutação:", list(permutacao) + [fim]) #ver quais rotas estão sendo processadas
        custo, caminho, custos, mapas_intermediarios = calcular_custo_total(mapa, inicio, list(permutacao) + [fim])
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_caminho = caminho
            melhor_custos = custos
            melhor_mapas = mapas_intermediarios

    return melhor_custo, melhor_caminho, melhor_custos, melhor_mapas

def desenhar_mapa(mapa, caminho, inicio, fim, mostrar=True):
    simbolo_cima = '.'
    simbolo_baixo = '.'
    simbolo_esquerda = '.'
    simbolo_direita = '.'

    simbolo_livre_asfalto = 'A'
    simbolo_obstaculo = '■'
    simbolo_livre_terra = 'T'
    simbolo_livre_grama = 'G'
    simbolo_livre_paralelepipedo = 'P'
    simbolo_inicio = '*'
    simbolo_final = 'x'

    simbolos_terreno = {
        'A': simbolo_livre_asfalto,
        'E': simbolo_obstaculo,
        'T': simbolo_livre_terra,
        'G': simbolo_livre_grama,
        'P': simbolo_livre_paralelepipedo
    }

    mapa_visual = [[simbolos_terreno.get(celula, ' ') for celula in linha] for linha in mapa]

    for i in range(len(caminho) - 1):
        x1, y1 = caminho[i]
        x2, y2 = caminho[i + 1]

        if x2 == x1 - 1 and y2 == y1:
            mapa_visual[x2][y2] = simbolo_cima
        elif x2 == x1 + 1 and y2 == y1:
            mapa_visual[x2][y2] = simbolo_baixo
        elif x2 == x1 and y2 == y1 - 1:
            mapa_visual[x2][y2] = simbolo_esquerda
        elif x2 == x1 and y2 == y1 + 1:
            mapa_visual[x2][y2] = simbolo_direita

    ix, iy = inicio
    fx, fy = fim
    mapa_visual[ix][iy] = simbolo_inicio
    mapa_visual[fx][fy] = simbolo_final

    if mostrar:
        for linha in mapa_visual:
            print(' '.join(linha))

    return mapa_visual

def ler_mapa_arquivo(nome_arquivo):
    with open('mapa42.txt') as arquivo:
        mapa = [linha.strip().split() for linha in arquivo]
    return mapa

# Definição do mapa de custos
custo_terreno_map = {
    'A': 1,
    'E': float('inf'),  # Obstáculos não têm custo de passagem
    'T': 3,
    'G': 5,
    'P': 10
}

# Uso:
mapa = ler_mapa_arquivo('mapa42.txt')
inicio = (20, 12)#(20, 12)  # Ponto inicial pode ser ajustado conforme necessário
paradas = [(5, 32),(13, 31), (32, 8), (35, 35)]# , ]
fim = (41,21)#(9, 4)  # Ponto final ajustado

melhor_custo, melhor_caminho, custos, mapas_intermediarios = forca_bruta_com_a_estrela(mapa, inicio, paradas)

print("Melhor custo encontrado:", melhor_custo)
print("Custo das paradas:", custos)
print("Melhor caminho encontrado:", melhor_caminho)

# Mostrar o mapa para cada parada
for i, mapa_intermediario in enumerate(mapas_intermediarios):
    print(f"\nMapa após parada {i + 1} (Custo: {custos[i]}):")
    for linha in mapa_intermediario:
        print(' '.join(linha))
