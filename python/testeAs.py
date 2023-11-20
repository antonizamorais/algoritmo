import re
import json
from graphs import _read_graph_file

def abrirArquivo(caminho):
    try:
        with open(caminho, 'r') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo {caminho} não encontrado.")
        return None

def encontrarTriplas(arquivotxt, name):
    triplas_encontradas = []

    # Separe as linhas do arquivo de texto
    linhas = arquivotxt.split('\n')

    # Itere pelas linhas do arquivo em busca das arestas rotuladas por name
    for linha in linhas:
        if name in linha:
            # Encontrar todas as palavras na linha
            palavras = re.findall(r'\S+', linha)  # Use \S+ para pegar palavras que contêm caracteres especiais
            
            # Depuração: imprima informações
            print("Linha:", linha)
            print("Palavras:", palavras)

            # Abra o arquivo referenciado e obtenha o conteúdo
            caminho_arquivo = palavras[-1]  # Última palavra na linha é o caminho do arquivo
            conteudo_arquivo = abrirArquivo(caminho_arquivo)

            if conteudo_arquivo is not None:
                # Adicione a tripla à lista
                tripla = palavras + [conteudo_arquivo]
                triplas_encontradas.append(tripla)

    return triplas_encontradas

# Exemplo de uso

def buscar_rotulo(arquivo_txt, rotulo, arquivo_json):
    resultados_txt = []

    # Carregar o arquivo JSON com as propriedades
    with open(arquivo_json, 'r') as json_file:
        propriedades = json.load(json_file)

    with open(arquivo_txt, 'r') as f:
        linhas = f.readlines()

        for linha in linhas:
            # Divide a linha nas triplas
            partes = linha.split()

            # Verifica se o rótulo está presente na linha
            if rotulo in partes:
                resultados_txt.append(partes)
    print(resultados_txt)
    resultados_com_propriedades = []

    # Buscar propriedades no arquivo JSON
    for resultado_txt in resultados_txt:
        resultado_com_propriedades = {}

        for v in resultado_txt:
            if v in propriedades:
                resultado_com_propriedades[v] = propriedades[v]

        resultados_com_propriedades.append(resultado_com_propriedades)

    return resultados_com_propriedades

def requisitos():
    # Inicializa listas para armazenar dados
    verticesOrigem = []
    arestas = []
    verticesDestino = []

    # Obtém o caminho do arquivo do usuário
    localarquivo = input("requisito: ")

    # Abre o arquivo em modo de leitura
    with open(localarquivo, 'r') as arquivo:
        # Lê o arquivo em grupos de três linhas
        for linha1, linha2, linha3 in zip(arquivo, arquivo, arquivo):
            # Processa a primeira linha no grupo
            if "None" in linha1:
                verticesOrigem.append(None)
            else:
                nome1, valor1 = map(str.strip, linha1.split('='))
                verticesOrigem.append(f"{nome1}:{valor1}")

            # Processa a segunda linha no grupo
            if "None" in linha2:
                arestas.append(None)
            else:
                nome2, valor2 = map(str.strip, linha2.split('='))
                arestas.append(f"{nome2}:{valor2}")

            # Processa a terceira linha no grupo
            if "None" in linha3:
                verticesDestino.append(None)
            else:
                nome3, valor3 = map(str.strip, linha3.split('='))
                verticesDestino.append(f"{nome3}:{valor3}")

    # Retorna as listas
    return verticesOrigem, arestas, verticesDestino



v, o, d = requisitos()
print(v)
print(o)
print(d)