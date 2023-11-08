import json
import re

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

    def encontrarTriplas(arquivotxt, name, arquivojson):
        # Crie uma lista para armazenar objetos JSON
        conteudos_json = []
        #Abrir o arquivo json
        with open(arquivojson, encoding='utf-8') as meu_json:
            dados = json.load(meu_json)
        # Abra o arquivo para leitura
        with open(arquivotxt, 'r') as arquivo:
        # Itere pelas linhas do arquivo em busca das aresta rotulada por name
            for numero_linha, linha in enumerate(arquivo, start=1):
            # Quando encontrar a aresta na linha
                if name in linha:
                    # Use uma expressão regular para encontrar todas as palavras na linha
                    # Assim identificar vértices de origem e destino
                    palavras = re.findall(r'\w+', linha)
                    for palavra in palavras:
                     
                        #Verificar se a aresta ou vértice tem propriedade
                        if palavra in dados:
                            prov = dados[palavra]

                            #adicionar as propredades a lista
                            conteudos_json.append(prov)
                        else:
                            pass
        r = json.dumps(conteudos_json, indent=2)
        return r

    # Função que recebe os requisitos do usuário
 
    def requisitos():

        verticeOrigem = {}
        aresta = {}
        verticeDestino = {}

        key1 = input("digite a chave para o requisito do vértice de origem: ")
        if not key1:
            key1 = None
            verticeOrigem[key1] = None
        else:
            valor1 = input("digite o valor para o requisito do vértice de origem: ")
            if not valor1:
                verticeOrigem[key1] = None
            else:
                verticeOrigem[key1] = valor1
        
        key2 = input("digite a chave para o requisito da aresta: ")
        if not key2:
            key2 = None
            aresta[key2] = None
        else:
            valor2 = input("digite o valor para o requisito da aresta: ")
            if not valor2:
                aresta[key2] = None
            else:
                aresta[key2] = valor2
        
        
        key3 = input("digite a chave para o requisito do vértice de destino: ")
        if not key3:
            key3 = None
            verticeDestino[key3] = None
        else:
            valor3 = input("digite o valor para o requisito do vértice de destino: ")
            if not valor3:
                verticeDestino[key3] = None
            else:
                verticeDestino[key3] = valor3
        
        
        return verticeOrigem, aresta, verticeDestino
       
        


