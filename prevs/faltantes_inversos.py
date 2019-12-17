#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import importa

 
# %%
    

def posto_119(mes):
    prev, a0, a1, postos = importa.arquivos()
    regressao = prev.loc[118,:]
    for i in range(6):
        estagio = ['E1','E2','E3','E4','E5','E6']
        estagio = str(estagio)
        mes = str(mes)
        regressao.iloc[i] = (prev.loc[118,estagio[i]] - a1.loc[118,mes]) / a1.loc[118,mes]
    regressao = regressao.rename(119)  
    return regressao


# %%


def posto_301(mes):
    prev, a0, a1, postos = importa.arquivos()
    regressao = posto_119()
    base = posto_119()
    for i in range(6):
        regressao.iloc[i] = a0.loc[301,mes] + (a1.loc[301,mes] * base.iloc[i])
    regressao = regressao.rename(301)
    return regressao


# %%
    

def posto_320(mes):
    prev, a0, a1, postos = importa.arquivos()
    regressao = posto_119()
    base = posto_119()
    for i in range(6):
        regressao.iloc[i] = a0.loc[320,mes] + (a1.loc[320,mes] * base.iloc[i])
    regressao = regressao.rename(320)
    return regressao


# %%
    

def cria_tabela(mes):
    prev, a0, a1, postos = importa.arquivos()
    p118 = prev.loc[118,:]
    p119 = posto_119(mes)
    p301 = posto_301(mes)
    p320 = posto_320(mes)
    postos = {119: p119, 118: p118, 301: p301, 320: p320}
    tabela = pd.DataFrame(data=postos)
    tabela = tabela.T
    return tabela

