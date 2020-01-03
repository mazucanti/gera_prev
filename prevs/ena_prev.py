#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:38:59 2019

@author: mazucanti
"""


from prevs import vazoes_prev as reg
import pandas as pd
from pathlib import Path


# %%


# Função cria o DataFrame (df) com as linhas e colunas apropriadas
def cria_ena(mes, ano):
    ena = []  #Vetor que armazenará a tabela de ENA relativa a cada PREV
    vazoes = reg.vazoes_finais(mes, ano) #Recebe as vazões regredidas 
    for vazao in vazoes: #Itera todas as vazões dos prevs carregados
        ind = vazao.head(200).index #Pega o número dos postos
        col = vazao.T.head(7).index #Pega os meses do arquivo
        ena.append(pd.DataFrame(0, index = ind, columns = col)) #Cria a tabela e a preenche com 0
    return ena, vazoes


# In[62]:


# Importa o arquivo de produtibilidades
def get_prod():
    loc = Path('entradas/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0) 
    for i,row in prod.head(180).iterrows(): #For substitui as vírgulas por pontos
        row['prod'] = row['prod'].replace(",",".") # Se isso não for feito, o df age como se fosse string
        row['prod'] = float(row['prod']) # Converte as strings para float
    return prod



# %%
    

# Função transforma as vazões em energia
def calc_ena(mes, ano):
    produtibilidades = get_prod() # Armazena todas as produtibilidades
    ena, vazoes = cria_ena(mes, ano) #armazena a tabela vazia e as vazões
    for j in len(vazoes):
        for i in range(6): #For itera cada dia do mês
            energia = vazoes[j].iloc[:,i].multiply(produtibilidades.iloc[:,0]) #Multiplica todas as vazões de postos com suas respectivas produtibilidades
            ena[j].iloc[:,i] = energia # Atualiza a tabela de ENA com as ENAs calculadas
        ena[j].fillna(0, inplace = True) # Troca os valores inválidos por 0
        ena[j].index.rename('posto', inplace = True) # Troca o nome dos índices para "posto"
        ena[j].sort_index(inplace=True) #Organiza os índices por ordem crescente
    return ena


# %%

    
#Exporta o df para um arquivo xls
def exporta_ena(nomes, *enas):
    local = Path('saídas/ENA/ENA.xls')
    formato = [0,6,20]
    with pd.ExcelWriter(local) as writer:
        for i, ena in enumerate(enas):
            for j, item in enumerate(ena):
                item.to_excel(writer, sheet_name = nomes[j], startrow = formato[i], startcol=0)
    
    
    
# %%


# Faz um recorte na ENA e reorganiza por submercado
def ena_mercados(ena):
    local = Path('entradas/postos_prev.csv') #Importa a importantíssima planilha de postos
    postos = pd.read_csv(local, index_col = 0) #Armazena a planilha nessa variável
    ena_por_mercado = pd.concat([ena,postos], axis=1) #Junta os DF para ter as características a serem filtradas
    ena_por_mercado.drop(['nome','ree','tipo','bacia'], axis=1, inplace=True) #Remove os atributos desnecessários
    ena_m = ena_por_mercado.groupby(['sub_mer']).sum() #Agrupa a ENA por submercado e soma os valores de cada grupo
    return ena_m


# %%
    

# Faz um recorte na ENA e reorganiza por REE
def ena_ree(ena):
    local = Path('entradas/postos_prev.csv') #Importa a importantíssima planilha de postos
    postos = pd.read_csv(local, index_col = 0) #Armazena a planilha nessa variável
    ena_por_ree = pd.concat([ena,postos], axis=1) #Junta os DF para ter as características a serem filtradas
    ena_por_ree.drop(['nome','tipo','bacia','sub_mer'], axis=1, inplace=True) #Remove os atributos desnecessários
    ena_r = ena_por_ree.groupby(['ree']).sum() #Agrupa a ENA por REE e soma os valores de cada grupo
    return ena_r


# %%
    
#Faz um recorte na ENA e reorganiza por bacia
def ena_bacia(ena):
    local = Path('entradas/postos_prev.csv') #Importa a importantíssima planilha de postos
    postos = pd.read_csv(local, index_col = 0) #Armazena a planilha nessa variável
    ena_por_bacia = pd.concat([ena, postos], axis=1) #Junta os DF para ter as características a serem filtradas
    ena_por_bacia.drop(['nome','ree','tipo','sub_mer'], axis=1, inplace = True) #Remove os atributos desnecessários
    ena_b = ena_por_bacia.groupby(['bacia']).sum() #Agrupa a ENA por bacia e soma os valores de cada grupo
    return ena_b


# %%
    

