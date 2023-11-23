import json
import re
import ast
from itertools import islice

class Provenance:

    #função para abrir os dados de proveniência em formato json
    def load(provenanceFile):
        with open(provenanceFile, encoding='utf-8') as meu_json:
            P = json.load(meu_json)
        return P
    
    #Função para lê arquivo de requisitos
    def loadReq(requisitoFile):
        with open(requisitoFile, 'r') as arquivo:
            R = arquivo.read()
        return R

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

    def requisitos(arquivo):
    # Inicializa listas para armazenar dados
        verticesOrigem = []
        arestas = []
        verticesDestino = []

        # Use islice para criar uma "janela deslizante" de tamanho 3
        for grupo_linhas in zip(*(islice(arquivo, i, None) for i in range(3))):
            # Processa cada linha no grupo
            for i, linha in enumerate(grupo_linhas):
                if "=" in linha:
                    nome, valor = map(str.strip, linha.split('='))
                    valor = f"{nome}:{valor}"
                else:
                    # Lidar com o caso em que a linha não tem o formato esperado
                    valor = None

                # Adiciona o valor à lista apropriada (verticesOrigem, arestas, verticesDestino)
                if i == 0:
                    verticesOrigem.append(valor)
                elif i == 1:
                    arestas.append(valor)
                elif i == 2:
                    verticesDestino.append(valor)

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
            


