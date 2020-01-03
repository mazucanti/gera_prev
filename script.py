#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:46:20 2019

@author: mazucanti
"""


from prevs import ena_prev as ena



mes = input('Digite o mês do PREV a ser calculado: ')
ano = input('Digite o ano do PREV a ser calculado: ')

try:
    ena_geral = ena.calc_ena(mes, ano)
    ena_submercado = ena.ena_mercados(ena_geral)
    ena_bacias = ena.ena_bacia(ena_geral)
    ena_ree = ena.ena_ree(ena_geral)
except FileNotFoundError:
    print("O arquivo de prev não foi encontrado!")
except:
    print("Alguma outra coisa deu errado com a ENA.\nVerifique se não houve alteração no código!")
else:
    ena_submercado.sort_index(ascending = False, inplace = True)
    
    ena.exporta_ena(0, ena_submercado, ena_ree, ena_bacias)

    print('ENA calculada com sucesso!')
    
    