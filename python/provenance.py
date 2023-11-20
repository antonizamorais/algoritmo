import json
import re
import ast

class Provenance:

    #função para abrir os dados de proveniência em formato json
    def load(provenanceFile):
        with open(provenanceFile, encoding='utf-8') as meu_json:
            P = json.load(meu_json)
        return P
    
    #função que retorna as propriedades de um determinado vértice ou aresta x do grafo de proveniência
    def propriedadesPROV(fileProv, x):
        with open(fileProv, encoding='utf-8') as meu_json:
            dados = json.load(meu_json)
        return dados[x]

    #função para encontrar as propriedades da tripla a partir da aresta

    def encontrarPropriedades(grafo, aresta, propriedades):
        resultados_grafo = []     
        
        for partes in grafo:
            #verificar se a aresta esta presente na linha
            if aresta in partes:
                partes = partes[:-1]
                resultados_grafo.append(partes)

        resultados_com_propriedades = []

        # Buscar propriedades no arquivo JSON
        for resultado_grafo in resultados_grafo:
            resultado_com_propriedades = {}

            for v in resultado_grafo:
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
    
    # Função para converter um dicionário em string
    def converteDic(dic):
        # Converter dicionários em strings
        return [f"{key}: {value}" for key, value in dic.items()]

   
    # Função para verificar se a lista de requisitos esta presente na lista de propriedades
    def verificarListas(list_req, list_prov):
        for sublist in list_req:
            # Verifica se qualquer sublista está presente
            if any(all(
                (item is None or str(item) in str(dic.values())) for item in sublist
            ) for dic in list_prov):
                return True
        return False
            


