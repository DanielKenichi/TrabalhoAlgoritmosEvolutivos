
"""
# O Problema do Caixeiro Viajante
Daniel Kenichi Tiago Tateishi - 790837 - Bacharelado em Ciência da Computação

# o Problema:
Suponha que um caixeiro viajante tenha que visitar n cidades diferentes, iniciando e 
encerrando sua viagem na primeira cidade. Suponha, também, que não importa a 
ordem com que as cidades são visitadas e que de cada uma delas o caixeiro pode ir 
diretamente para qualquer outra. O problema do caixeiro viajante consiste em descobrir 
a rota que torna mínima a viagem total.

# Exercício:
Implemente em Python um Algoritmo Evolutivo para a resolução do problema do 
Caixeiro viajante considerando 6 (seis) cidades. Em seu código, gere as distâncias entre 
as cidades de maneira aleatória. Seu programa deve encontrar a melhor rota partindo 
da cidade 0, passando por todas as cidades e retornando à cidade 0. A Tabela 1 
apresenta um exemplo de distâncias geradas aleatoriamente. Defina a melhor maneira 
de modelar seus indivíduos que representam as soluções do problema, e também a 
função de fitness. Faça suas próprias escolhas sobre os operadores de seleção, 
cruzamento, mutação e elitismo. Não é permitido utilizar bibliotecas prontas.
"""

import random

#Definindo uma função fitness para avaliar os individuos (rotas) 
#Critério de avaliação: Distância total percorrida
def fitness(indv):
  dist_total = 0
  partida = 0
  destino = 1
  while destino <= num_cidades:
    try:
      dist_total += distancias[indv[partida]][indv[destino]]
    except:
      dist_total += distancias[indv[destino]][indv[partida]]
    partida += 1 
    destino += 1

  return dist_total

#Definindo Função de Seleção do tipo torneio
#Critério de comparação: menor distância percorrida

def selecao_torneio(populacao):
  ind1 = -1
  ind2 = -1

  while ind1 == ind2:
    # Torneio 1
    sorteados = random.sample(range(0, len(populacao)), 2)
    if fitness(populacao[sorteados[0]]) < fitness(populacao[sorteados[1]]):
      ind1 = sorteados[0]
    else:
      ind1 = sorteados[1]

    # Torneio 2
    sorteados = random.sample(range(0, len(populacao)), 2)
    if fitness(populacao[sorteados[0]]) < fitness(populacao[sorteados[1]]):
      ind2 = sorteados[0]
    else:
      ind2 = sorteados[1]
        
  return ind1,ind2

def gera_filho(pai1, pai2, key, tam_seq):
  filho = []
  seq = []
  i = 0
  
  filho.append(0)
  if key == 0:
    #Coloca a sequencia do pai1 à esquerda do vetor
    while i < tam_seq:
      filho.append(pai1[i])
      i += 1
    #Coloca o restante das cidades no vetor na sequência em que aparecem no pai2
    for j in pai2:
      if j not in filho:
        filho.append(j)
  
  elif key == 1:
    seq = pai1[:tam_seq]
    #Coloca as cidades que não pertencerem a sequência selecionada do pai1 na sequência em que aparecem no pai2
    for j in pai2:
      if j not in seq:
        filho.append(j)
    #Coloca a sequencia do pai1 à direita do vetor
    while i < tam_seq:
      filho.append(pai1[i])
      i += 1
  filho.append(0)

  return filho

def cruzamento(ids, populacao):
  #tamanho da sequencia de um dos pais a ser copiado
  tam_seq = random.randrange(2, num_cidades - 1, 1) 
  #key = 0 sequencia copiada para a esquerda do vetor | key = 1 '' '' direita
  key1 = random.randrange(0,2,1)
  key2 = random.randrange(0,2,1)

  pai1 = populacao[ids[0]].copy()
  pai1.pop(0)
  pai1.pop(num_cidades - 1)

  pai2 = populacao[ids[1]].copy()
  pai2.pop(0)
  pai2.pop(num_cidades - 1)

  #cruzamento 1
  filho1 = gera_filho(pai1, pai2, key1, tam_seq)

  #cruzamento 2
  filho2 = gera_filho(pai2, pai1, key2, tam_seq)

  return filho1, filho2


def elitismo(populacao):

  dists = [fitness(i) for i in populacao]
  id1 = dists.index(min(dists))
  dists.pop(id1)
  id2 = dists.index(min(dists)) + 1
  
  return id1,id2


def mutacao(indvs, prob):
  idx1 = -1
  idx2 = -1 
  for indv in indvs:
    if random.random() < prob:
      while idx1 == idx2:
        idx1 = random.randint(1, len(indv) - 2)
        idx2 = random.randint(1, len(indv) - 2)
      aux = indv[idx1]
      indv[idx1] = indv[idx2]
      indv[idx2] = aux 

  return indvs


def exibe_tabela(distancias, num_cidades):
  for i in range(num_cidades):
    print("  ", i, end='')
  aux = 0
  print()
  for dist in distancias:
    print(aux, dist)
    aux += 1


#inicializando tabela de distâncias e numero de cidades
distancias = []
num_cidades = 6
tam_pop = 10

for i in range(num_cidades):
  j = 0
  row = []
  while j <= i:
    if i != j:
      dist = random.randrange(10, 10000, 1)
      row.append(dist)
    else:
      row.append(0)
    j += 1
  distancias.append(row)

#exibindo tabela
exibe_tabela(distancias, num_cidades)

populacao_inicial = []

for i in range(tam_pop):
  individuo = []
  cidades = [c for c in range(num_cidades)]
  j = 0

  for j in range(num_cidades + 1):
    if j == 0 or j == num_cidades:
      individuo.append(0)
    else:
      index = random.randrange(1, len(cidades), 1)
      individuo.append(cidades[index])
      cidades.pop(index)
      
  populacao_inicial.append(individuo)

#printando população inicial
for indv in populacao_inicial:
  print(indv)

#definindo numero de gerações máxima
num_gens = 100

#definindo probabilidade de mutacao
prob = 0.3

#calculando distancias da populacao
dists = [fitness(i) for i in populacao_inicial]

#selecionando melhor individuo da populacao
melhor_rota_historica = populacao_inicial[dists.index(min(dists))]
melhor_distancia_historica = min(dists)

for gen in range(num_gens):
  nova_pop = []

  #definindo elite da populacao antiga
  elite = elitismo(populacao_inicial.copy())
  nova_pop.append(populacao_inicial[elite[0]])
  nova_pop.append(populacao_inicial[elite[1]])

  # Gera os filhos restantes para completar a população
  num_filhos = 2
  while num_filhos < tam_pop:

    # Seleção por torneio
    ids_vencedores = selecao_torneio(populacao_inicial)
    
    # Cruzamento
    filhos = cruzamento(ids_vencedores, populacao_inicial.copy())
    # Coloca os filhos na nova população
    nova_pop.append(filhos[0])
    nova_pop.append(filhos[1])

    num_filhos = num_filhos + 2
  
  #Populacao sujeita a mutacao
  nova_pop = mutacao(nova_pop, prob)

  #Verificando melhores resultados dessa geracao
  novas_dists = [fitness(i) for i in nova_pop]
  melhor_rota_geracao = nova_pop[novas_dists.index(min(novas_dists))]
  melhor_distancia_geracao = min(novas_dists)


  #Imprime o resultado dessa geracao e o resultado historico
  print("Melhor rota Geracao: {} com distância {}".format(melhor_rota_geracao, melhor_distancia_geracao))
  print("Melhor rota histórica: {} com distância {}".format(melhor_rota_historica, melhor_distancia_historica))
  print()

  #Verificando se a geracao supera os resultados historicos
  if melhor_distancia_geracao < melhor_distancia_historica:
    melhor_distancia_historica = melhor_distancia_geracao
    melhor_rota_historica = melhor_rota_geracao
  
  # Substitui a populacao antiga pela atual
  populacao_inicial = nova_pop.copy()