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

# O tipo de um objeto pode ser testado através da função type:  ("K!=goo.gl/8Mh2W0)


# TODO verificar como pode ser lido argumentos da linha de

"""
Programa para gerar uma string de pesquisa a partir de grupos e conectores
logicos
"""

DEFAULT_MAP = dict(__and__='and', __or__='or')

def is_complex_string(string_to_test):
    """
    Testa se uma string é complexa. Isto é se contém um espaço
    """
    return (' ' in string_to_test)


def round_str(base, prefix, suffix=None):
    """
    Put a preffix and a suffix around a base string

    Args:
        base: the base string
        prefix: the prefix to append
        suffix: the suffix to append

    Return:
        the new string

    """
    if suffix == None:
        suffix = prefix

    result = prefix + base + suffix
    return result

def round_brackets(base):
    return round_str(base, '(', ')')

def round_appostrofe(base):
    return round_str(base, '\"')


        
def build_search_str(string_ast, groups, map_dict):
    """
    Monta um string de pesquisa
    """
    # Base case
    if isinstance(string_ast, basestring):
        if is_complex_string(string_ast):
            return round_appostrofe

def build_search_string(search_dict, map_dict=None):
    # TODO essa função deve separar as strings e os grupos
    """
    Monta as strings de pesquisa

    Args:
        syntax_tree: a string de pesquisa
    """
    if map_dict is None:
        map_dict = DEFAULT_MAP

    string_trees = [ value for (key,value) in search_dict.iteritems() if type(key)
            == int ]


def main():
    ast = {'__groups__': 
            { 
                'group1': ['test']
                }, 
            1 : 'test' # {'__group__': 'group1'}
            }
    print build_search_string(ast)

if __name__ == '__main__':
    # TODO transformar esse teste em um teste unitário

    main()
