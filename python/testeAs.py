from provenance import Provenance

# Exemplo de uso da função
nome_arquivo = r'C:\Users\win10\algoritmo\rdf-ccfpq-master\experimentosAntoniza\olimpic\results.txt'
json = r'C:\Users\win10\algoritmo\rdf-ccfpq-master\experimentosAntoniza\olimpic\resultsProvenence.json'
string_procurada = 'location'

#resultado = Provenance.encontrarTriplas(nome_arquivo, string_procurada, json)
#print(resultado)

testerequisitos = Provenance.requisitos()
print(testerequisitos)