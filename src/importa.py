 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:39:59 2019

@author: mazucanti
"""

import pandas as pd
import datetime as dt
import calendar as cl
from pathlib import Path


def get_datas(ano,mes):
    datas = [] #Vetor que armazenará as datas dos primeiros dias de todas as semanas operativas do prev
    calendario_obj = cl.Calendar(firstweekday=5)
    cal_mes = calendario_obj.monthdatescalendar(ano, mes)
    for semana in cal_mes:
        datas.append(semana[0])
    if len(datas)<6:
        for i in range(6 - len(datas)):
            datas.append(datas[len(datas)-1] + dt.timedelta(weeks = i+1))
    
    datas = ['indice', 'posto'] + datas #Adiciona elementos auxiliares para a criação do DF
    return datas

def importa_prevs(ano, mes):
    arquivos = Path('entradas/prevs/%s/%s' % (str(ano), str(mes))).glob('**/*') # Cria o caminho para todos os prevs de um mês e ano específico
    prevs = [] #Vetor que armazenará todos os prevs de uma pasta
    datas = get_datas(ano,mes)
    files = [arquivo for arquivo in arquivos if arquivo.is_file()] #Organiza os arquivos válidos em um vetor
    for file in files:
        prevs.append(pd.read_csv(file, header=None, names = datas, index_col = 1, delim_whitespace=True))
    #Importa cada arquivo usando o separador como espaço, redefinindo o nome das colunas e ignorando os indices pré existentes usando os postos para isso
    for i, prev in enumerate(prevs): #itera todos os arquivos carregados
        prevs[i] = prev.drop(['indice'], axis=1) #Tira a coluna de índices do prev que é desnecessária
    return prevs


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
    

def arquivos(ano, mes):
    prevs = importa_prevs(ano, mes)
    a0,a1 = importa_a0_a1()
    postos = importa_postos()
    return prevs, a0, a1, postos


def get_nomes(ano,mes):
    nomes = []
    rv = []
    arquivos = Path('entradas/prevs/%s/%s' % (str(ano), str(mes))).glob('**/*') # Cria o caminho para todos os prevs de um mês e ano específico
    files = [arquivo for arquivo in arquivos if arquivo.is_file()] #Organiza os arquivos válidos em um vetor
    for i, file in enumerate(files):
        nomes.append(file.stem)
        rv.append(file.suffix)
        rv[i] = rv[i].replace(".", "")
        rv[i] = rv[i].upper() 
    nomes = formata_nomes(nomes,ano,mes)
    return nomes, rv


def importa_mlt(mes, ano):
    postos = importa_postos()
    bacia = postos['bacia']
    ree = postos['ree']
    sub_mer = postos['sub_mer']
    nomes = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
    local = Path('entradas/mlt/GeraPrevs.xlsm')
    mlt = pd.read_excel(local, sheet_name= 'MLT', header = 0, index_col = 0)
    mlt = mlt.iloc[:,17:29]
    mlt.columns = nomes
    mlt = mlt.loc[:,nomes[mes-1]]
    mlt.name = 'MLT'
    bacia = pd.concat([mlt,bacia], axis=1)
    bacia = bacia.groupby('bacia').sum()
    ree = pd.concat([mlt,ree], axis=1)
    ree = ree.groupby('ree').sum()
    sub_mer = pd.concat([mlt,sub_mer], axis=1)
    sub_mer = sub_mer.groupby('sub_mer').sum()
    sub_mer.sort_index(ascending = False, inplace = True)
    mlt = [sub_mer,ree,bacia]
    return mlt
    

def formata_nomes(nomes, ano, mes):
    if mes < 10: mes = '0' + str(mes)
    prefixo = str(ano)+str(mes)+"-prevs-"
    for i in range(len(nomes)):
        nomes[i] = nomes[i].replace(prefixo, "")
        nomes[i] = nomes[i].replace(str(ano)+"-","")
        nomes[i] = nomes[i].replace("Diaria-","")
        nomes[i] = nomes[i].replace("INAR","")
        nomes[i] = nomes[i].replace("+", "")
    return nomes
    
