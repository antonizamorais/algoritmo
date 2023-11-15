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

    def encontrarPropriedades(arquivo_txt, rotulo, propriedades):
        resultados_txt = []     
        
        linhas = arquivo_txt.split('\n')

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

    # Função que recebe os requisitos do usuário
    def requisitos():
        verticeOrigem = {}
        aresta = {}
        verticeDestino = {}

        localarquivo = input("requisito: ")
        with open(localarquivo, 'r') as arquivo:
            # Lê as linhas em grupos de 3 (assumindo que o arquivo sempre tem múltiplos de 3 linhas)
            for linha1, linha2, linha3 in zip(arquivo, arquivo, arquivo):
                # Processa cada linha individualmente
                nome1, valor1 = linha1.strip().split('=')
                nome2, valor2 = linha2.strip().split('=')
                nome3, valor3 = linha3.strip().split('=')

                # Adiciona os valores aos dicionários
                verticeOrigem[nome1] = valor1
                aresta[nome2] = valor2
                verticeDestino[nome3] = valor3

        return verticeOrigem, aresta, verticeDestino
    
    # Função para converter uma string do formato 'chave = valor' em um par chave-valor
    def parse_line(line):
        match = re.match(r'\s*([^=]+)\s*=\s*(.*)\s*', line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            return key, value
        else:
            return None, None

   

    
        


