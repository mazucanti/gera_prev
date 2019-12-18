#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:39:59 2019

@author: mazucanti
"""

import pandas as pd
from pathlib import Path


def importa_prev():
    local = Path('entradas/prevs/Prevs_VE.prv') # Cria o caminho para o arquivo de prev
    #Importa o arquivo usando o separador como espaço, redefinindo o nome das colunas e ignorando os indices pré existentes usando os postos para isso
    prev = pd.read_csv(local, header=None, names = ['indice','posto','E1','E2','E3','E4','E5','E6'], index_col = 1, delim_whitespace=True)
    prev.drop(['indice'], axis=1, inplace=True) #Tira a coluna de índices do prev que é desnecessária
    return prev


def importa_a0_a1():
    local_a0 = Path("entradas/regressao/Regressão_A0.csv")
    local_a1 = Path("entradas/regressao/Regressão_A1.csv")
    a0 = pd.read_csv(local_a0, index_col=0)
    a1 = pd.read_csv(local_a1, index_col=0)
    return a0, a1


def importa_postos():
    local = Path('entradas/postos_prev.csv')
    postos = pd.read_csv(local, index_col = 0, squeeze = True)
    return postos
    

def arquivos():
    prev = importa_prev()
    a0,a1 = importa_a0_a1()
    postos = importa_postos()
    return prev, a0, a1, postos

    