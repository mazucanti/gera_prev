#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:38:59 2019

@author: mazucanti
"""


from src import vazoes_prev as reg
import pandas as pd
import calendar as cal
from pathlib import Path


# %%


# Função cria o DataFrame (df) com as linhas e colunas apropriadas
def cria_ena(mes, ano):
    ena = []  #Vetor que armazenará a tabela de ENA relativa a cada PREV
    vazoes = reg.vazoes_finais(mes, ano) #Recebe as vazões regredidas 
    for vazao in vazoes: #Itera todas as vazões dos prevs carregados
        ind = vazao.head(200).index #Pega o número dos postos
        col = vazao.T.head(6).index #Pega os meses do arquivo
        ena.append(pd.DataFrame(0, index = ind, columns = col)) #Cria a tabela e a preenche com 0
    return ena, vazoes


# In[62]:


# Importa o arquivo de produtibilidades
def get_prod():
    loc = Path('entradas/produtibilidades/prod.csv')
    prod = pd.read_csv(loc, index_col=0) 
    for i,row in prod.head(200).iterrows(): #For substitui as vírgulas por pontos
        row['prod'] = row['prod'].replace(",",".") # Se isso não for feito, o df age como se fosse string
        row['prod'] = float(row['prod']) # Converte as strings para float
    return prod



# %%
    

# Função transforma as vazões em energia
def calc_ena(mes, ano):
    produtibilidades = get_prod() # Armazena todas as produtibilidades
    ena, vazoes = cria_ena(mes, ano) #armazena a tabela vazia e as vazões
    for j in range(len(vazoes)):
        for i in range(6): #For itera cada dia do mês
            energia = vazoes[j].iloc[:,i].multiply(produtibilidades.iloc[:,0]) #Multiplica todas as vazões de postos com suas respectivas produtibilidades
            ena[j].iloc[:,i] = energia # Atualiza a tabela de ENA com as ENAs calculadas
        ena[j].fillna(0, inplace = True) # Troca os valores inválidos por 0
        ena[j].index.rename('posto', inplace = True) # Troca o nome dos índices para "posto"
        ena[j].sort_index(inplace=True) #Organiza os índices por ordem crescente
    return ena


# %%

    
#Exporta o df para um arquivo xls
def exporta_ena(ano,mes, nomes, rv, medias, enas):
    if mes<10: mes = '0' + str(mes)
    local = Path('saídas/ENA/'+str(ano)+str(mes)+'-ENA.xls') #Cria o caminho para o arquivo a ser exportado
    formato = [1,7,21] #Números das linhas apropriadas para a escrita na tabela do excel
    with pd.ExcelWriter(local) as writer: #Cria o objeto que escreve os DF no arquivo
        for i, ena in enumerate(enas): #Itera as enas entradas como parâmetro
            for j, item in enumerate(ena):
                item.to_excel(writer, sheet_name = nomes[j], startrow = formato[i], startcol = 0)
                medias[j+len(ena)*i].to_excel(writer, sheet_name = nomes[j], startrow = formato[i], startcol = 8)
                worksheet = writer.sheets[nomes[j]]
                worksheet.write(0, 0, rv[j])
    
    
    
# %%


# Faz um recorte na ENA e reorganiza por submercado
def ena_mercados(ena, postos):
    ena_m = []
    for item in ena:
        ena_por_mercado = pd.concat([item,postos], axis=1) #Junta os DF para ter as características a serem filtradas
        ena_por_mercado.drop(['nome','ree','tipo','bacia'], axis=1, inplace=True) #Remove os atributos desnecessários
        ena_m.append(ena_por_mercado.groupby(['sub_mer']).sum()) #Agrupa a ENA por submercado e soma os valores de cada grupo
    return ena_m


# %%
    

# Faz um recorte na ENA e reorganiza por REE
def ena_ree(ena, postos):
    ena_r = []
    for item in ena:
        ena_por_ree = pd.concat([item,postos], axis=1) #Junta os DF para ter as características a serem filtradas
        ena_por_ree.drop(['nome','tipo','bacia','sub_mer'], axis=1, inplace=True) #Remove os atributos desnecessários
        ena_r.append(ena_por_ree.groupby(['ree']).sum()) #Agrupa a ENA por REE e soma os valores de cada grupo
    return ena_r


# %%
    
#Faz um recorte na ENA e reorganiza por bacia
def ena_bacia(ena, postos):
    ena_b = []
    for item in ena:
        ena_por_bacia = pd.concat([item, postos], axis=1) #Junta os DF para ter as características a serem filtradas
        ena_por_bacia.drop(['nome','ree','tipo','sub_mer'], axis=1, inplace = True) #Remove os atributos desnecessários
        ena_b.append(ena_por_bacia.groupby(['bacia']).sum()) #Agrupa a ENA por bacia e soma os valores de cada grupo
    return ena_b


# %%
   

def media_mes(dias, total, *enas):
    ponderadas = []
    j = 0
    for item in enas: #Itera cada recorte de ENA
        for ena in item: #Itera as tabelas de cada recorte
            num_poderada = 0 #Variável que armazenará ena * dias de cada estágio somados
            for i, no_dias in enumerate(dias): #Itera o vetor de dias operativos
                num_poderada += ena.iloc[:,i] * no_dias #Multiplica todas as enas pelo número de dias do mês operativo no estágio
            ponderadas.append(num_poderada / total) #Divide a soma dos produtos pelo total de dias do mês operativo
            ponderadas[j].name = "Média"
            j += 1
    return ponderadas, enas

    
def dias_semana(ano,mes):
    obj_cal_mes = cal.Calendar(firstweekday = 5) #Cria o objeto de calendário e define sábado como primeiro dia da semana
    cal_mes_atual = obj_cal_mes.monthdatescalendar(ano, mes) #Cria o calendário do mês e ano passado como parâmetro
    dias_por_semana = [0] * 6 #Cria um vetor com um item pra cada estágio
    total = 0 #Armazena o total de dias do mês
    for i, semana in enumerate(cal_mes_atual): #Itera as semanas operativas do mês
        contador = 0 #Contador de dias do mês atual por semana
        for dia in semana: #Itera os dias da semana
            if dia.month == mes: #Checa se o dia faz parte do mês em questão
                contador += 1 #Caso seja, um contador é incrementado
        dias_por_semana[i] = contador #É registrado o número de dias do mês operativo naquele estágio
        total += contador #O total é atualizado
    return dias_por_semana, total 

