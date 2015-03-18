#!/usr/bin/env python
# coding=utf-8

"""
Possui funções para montar strings de pesquisa Para uma determinada plataforma.

Serão tranformadas em string de pesquisa estruturas de dados do tipo JSON:
    Exemplo:
    {
        groups: {
            group1: [term1, term2, term3]
        }
        1: {
            __and__: {
                group: group1
            }
                
        }
    }

Os operadores lógicos permitidos na montagem da linha serão __and__ e __or__.
Esses operadores serão transformados
"""

# A biblioterca JSON pode ser lida utilizando a biblioteca padrão JSON
# (goo.gl/32pvde)

# O tipo de um objeto pode ser testado através da função type:  (goo.gl/8Mh2W0)


# TODO verificar como pode ser lido argumentos da linha de

"""
Programa para gerar uma string de pesquisa a partir de grupos e conectores
logicos
"""

def build_search_string(syntax_tree, map_function):
    """
    Monta
    """
    pass    

def main():
    pass

if __name__ == '__main__':
    main()
