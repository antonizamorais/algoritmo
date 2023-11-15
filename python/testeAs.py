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

# Exemplo de uso
arquivo = input("arquivo txt: ")
resultados = _read_graph_file(arquivo)
print(resultados)
