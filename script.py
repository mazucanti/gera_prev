#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:46:20 2019

@author: mazucanti
"""


from src import ena_prev as ena
from src import importa as imp



mes = int(input('Digite o mês do PREV a ser calculado: '))
ano = int(input('Digite o ano do PREV a ser calculado: '))

try:
    ena_geral = ena.calc_ena(mes, ano)
    postos = imp.importa_postos()
    ena_submercado = ena.ena_mercados(ena_geral, postos)
    ena_bacias = ena.ena_bacia(ena_geral, postos)
    ena_ree = ena.ena_ree(ena_geral, postos)
except FileNotFoundError:
    print("O arquivo de prev não foi encontrado!")
except:
    print("Alguma outra coisa deu errado com a ENA.\nVerifique se não houve alteração no código!")
else:
    for i in range(len(ena_submercado)):
        ena_submercado[i].sort_index(ascending = False, inplace = True)
        
    nomes, rv = imp.get_nomes(ano, mes)
    mlt = imp.importa_mlt(mes, ano)
    dias, total = ena.dias_semana(ano, mes)
    medias, enas = ena.media_mes(dias, total, ena_submercado, ena_ree, ena_bacias)
    ena.exporta_ena(ano, mes, nomes, rv, medias, mlt, enas)

    print('ENA calculada com sucesso!')

