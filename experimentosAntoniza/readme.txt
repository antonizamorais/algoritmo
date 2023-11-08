-> Gramática: restringe as arestas da consulta
-> Requisitos: define quais propriedades da aresta ou dos vértices são relevantes para a consulta.
	requisitos da aresta (ra)
	requisitos do vértice de origem (rvo)
	requisitos do vértice de destino (rvd)

Perguntas sobre o grafo Olimpic 

Quais pessoas receberam a medalha de ouro na maratona masculina de 1000 metros?
-> G: location results
-> R: ra = nulo, rvo = "name": "10000M Men", rvd = "medal": "G"

Quais pessoas receberam a medalha de prata na maratona masculina de 1000 metros?
-> G: location results
-> R: ra = nulo, rvo = "name": "10000M Men", rvd = "medal": "S"

Quais pessoas receberam a medalha de bronze na maratona masculina de 1000 metros?
-> G: location results
-> R: ra = nulo, rvo = "name": "10000M Men", rvd = "medal": "B"

Quais pessoas receberam a medalha de ouro com nacionalidade estadunidense na maratona masculina de 1000 metros?
-> G: location results
-> R: ra = nulo, rvo = "name": "10000M Men", rvd = "medal": "G” and "nationality": "USA"

Quais os resultados da maratona masculina de 100 metros que ocorreram no Rio?
-> G: location results
-> R: ra = nulo, rvo = "name": "10000M Men", rvd = "location": "Rio"

Perguntas sobre o grafo countriesStatesCities

Quais os países da região asiática com fuso horário em Ásia/Kabul
-> G: timezones
-> R: ra = nulo, rvo = "region": "Asia" , rvd = "zoneName": "Asia\/Kabul"

OBS: Algumas regiões têm vários fusos horários como a região Polar
Quais os fusos horários da região Polar?
-> G: timezones
-> R: ra = nulo, rvo = "region": "Polar" , rvd = nulo

Cidades do estado Badakhshan
-> G: states cities
-> R: ra = nulo, rvo =  "name": "Badakhshan", rvd = nulo

OBS: definindo a região 
Cidades do estado Badakhshan da região asiática
-> G: states cities
-> R: ra = nulo, rvo =  "region": "Asia", rvd = "name": "Badakhshan

Cidades da Europa
-> G: states cities
-> R: ra = nulo, rvo =  "region": "Europe", rvd = nulo
