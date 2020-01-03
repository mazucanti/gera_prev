#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:40:50 2019

@author: mazucanti
"""

import pandas as pd
from prevs import importa as imp
from pathlib import Path
from prevs import prev_tipo3


def trata_vazoes_base(prev, a1):
    vazoes_base = prev.loc[a1.iloc[:,0], :] # pega no prev as vazões base do arquivo a1
    vazoes_base.reset_index(inplace=True)  #tira os postos base dos índices 
    base = a1.reset_index() # recebe os índices de regressão sem os índices dos postos regredidos
    indice = base.loc[:,'posto'] # Pega os valores dos postos em uma série para usar de índice
    vazoes_base.insert(0, "ind", indice, allow_duplicates=True) #Adiciona os índices na coluna 0
    vazoes_base.drop('posto', axis=1, inplace=True) # Remove a coluna de postos original
    vazoes_base.rename(columns={'ind':'posto'}, inplace=True) #A coluna de índices se chama 'posto' agora
    vazoes_base.set_index('posto', inplace=True) #posto é usada como novos índices
    return vazoes_base


def vazoes_tipo0(prev, postos): #Faz as vazões tipo 0
    # vazoes0 = prev.join(postos.query('tipo==0'), on = 'posto', how = 'inner') #faz um join com os postos de tipo 0 identificados na tabela postos
    vazoes0 = prev.join(postos.query('tipo==0 or tipo == 1'), on = 'posto', how = 'inner') #faz um join com os postos que já possuem vazão calculada
    vazoes0.drop(['nome','ree','tipo','sub_mer','bacia'],axis = 1, inplace = True) #Remove as colunas desnecessárias vindas do join
    return vazoes0


#Calcula as regressões lineares das vazões do tipo 1
def regressao_tipo_1(prev, a0, a1, postos, mes):
    vazoes_base = trata_vazoes_base(prev, a1) #recebe a planilha de vazões base devidamente identificadas com os postos regredidos
    vazoes_base = vazoes_base.join(postos.query('tipo == 1'), on = 'posto', how = 'inner') # join para filtrar somente os postos tipo 1
    vazoes_base.drop(['nome','tipo','sub_mer','bacia','ree'], axis=1, inplace = True) #Remove as colunas desnecessárias
    ind = vazoes_base.head(70).index #Salva os números de postos presentes nas vazões de tipo 1
    col = vazoes_base.T.head(70).index # Salva os estagios do prev
    vazoes_tipo1 = pd.DataFrame(0,index = ind, columns = col) #Cria um df preenchido com 0 identificados por postos e dias
    for i in range(6): #Itera os estagios do prev
        A0 = a0.loc[:,mes] #Armazena todos os A0 do mês operativo atual de todos os postos tipo 1
        A1 = a1.loc[:,mes] #Armazena todos os A1 do mês operativo atual de todos os postos tipo 1
        X = vazoes_base.iloc[:,i] # Armazena todas as vazões base de todos os postos
        Y = A0 + (A1*X) #Calcula a regressão linear
        vazoes_tipo1.iloc[:,i] += Y #Soma o resultado da regressão à coluna do dia apropriado
    return vazoes_tipo1


#A função cria um dicionário com todas as vazões de tipo 3 e as organiza em uma tabela
def regressao_tipo_3(mes):
    data_postos_tipo3 = {126: prev_tipo3.posto_126(), 127: prev_tipo3.posto_127(), 131: prev_tipo3.posto_131(), 132: prev_tipo3.posto_132(),
                         176: prev_tipo3.posto_176(), 285: prev_tipo3.posto_285(), 292: prev_tipo3.posto_292(mes), 298: prev_tipo3.posto_298(), 
                         299: prev_tipo3.posto_299(), 302: prev_tipo3.posto_302(mes), 303: prev_tipo3.posto_303(), 304: prev_tipo3.posto_304(),
                         306: prev_tipo3.posto_306(), 315: prev_tipo3.posto_315(), 316: prev_tipo3.posto_316(), 317: prev_tipo3.posto_317(),
                         318: prev_tipo3.posto_318(), 37: prev_tipo3.posto_37(), 38: prev_tipo3.posto_38(), 39: prev_tipo3.posto_39(), 
                         40: prev_tipo3.posto_40(), 42: prev_tipo3.posto_42(), 43: prev_tipo3.posto_43(), 45: prev_tipo3.posto_45(), 
                         46: prev_tipo3.posto_46(), 66: prev_tipo3.posto_66(), 75: prev_tipo3.posto_75()}
    
    postos_tipo3 = pd.DataFrame(data=data_postos_tipo3)
    return postos_tipo3.T


# Monta a tabela final de vazões
def vazoes_finais(mes, ano):
    prevs, a0, a1, postos = imp.arquivos(ano, mes) #Recebe os postos, vazões e coeficientes de regressão tipo 1
    vazoes = [None] * len(prevs) #Cria vetor de vazões tratadas e regredidas para cada prev
    for i, prev in enumerate(prevs):
        tipo0 = vazoes_tipo0(prev, postos) #Recebe as vazões dos postos tipo 0
        # tipo1 = regressao_tipo_1(prev, a0, a1, postos, mes) #Recebe as vazoes dos postos tipo 1
        vazoes[i] = tipo0
        # vazoes[i] = pd.concat([tipo0,tipo1]) #Junta as vazoes tipo 1 e 0 em uma tabela
        vazoes[i].sort_index(inplace = True) # Orgazina a tabela por ordem crescente de código de posto
        vazoes[i].dropna(inplace=True) #Retira os postos que não têm vazão
        local = Path('saídas/vazoes/vazões_para_tipo3.csv') #Cria o diretório para a tabela calculada
        vazoes[i].to_csv(local) #Função que exporta para referência nas regressões de tipo 3
        tipo3 = regressao_tipo_3(mes) #Recebe uma tabela com todas as vazões de postos tipo 3
        vazoes[i] = pd.concat([vazoes[i], tipo3],) #Adiciona os postos à tabela
        vazoes[i].sort_index(inplace = True) #Organiza a tabela por ordem crescente de código de posto
    return vazoes


