#!/usr/bin/env python
# coding=utf-8

import argparse
import json
import logging as log

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

AND_KEY = '__and__'
OR_KEY = '__or__'
GROUP_KEY = '__group__'
GROUPS_KEY = '__groups__'
DEFAULT_MAP = { AND_KEY: 'AND', OR_KEY: 'OR'}

def is_complex_string(string_to_test,chars='- _'):
    """
    Testa se uma string é complexa. Isto é se contém um espaço
    """
    for char in chars:
        if char in string_to_test:
            return True
    return False

def round_str(base, prefix, suffix=None):
    """
    Put a preffix and a suffix around a base string

    Args:
        :base: the base string
        :prefix: the prefix to append
        :suffix: the suffix to append

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

def is_oprt(ast, oprt):
    """
    Testa se a ast é um operador lógico

    Args:
        :oprt: O operador a ser testado

    Returns:
        True se é o a string é o operador lógico em questão
    """
    return_value = isinstance(ast, dict) and (oprt in ast)
    return return_value
    
def is_group(ast):
    return GROUP_KEY in ast
    
def build_oprt(oprt, terms, map_dict):
    """
    Monta uma string com operadores lógicos
    """
    join_str = round_str(map_dict[oprt], ' ')
    return join_str.join(terms)

def build_search_str(ast, groups, map_dict, groups_join_oprt=None): 

    if groups_join_oprt is None:
        groups_join_oprt = OR_KEY

    """
    Monta um string de pesquisa
    """
    if isinstance(ast, basestring):
        # Caso base
        if is_complex_string(ast):
            search_str = round_appostrofe(ast)
        else:
            search_str = ast
    elif isinstance(ast, dict):
        # Casos recursivos             
        for join_oprt in [AND_KEY, OR_KEY]:
            if is_oprt(ast, join_oprt): 
                children = [build_search_str(term, groups, map_dict) for term in
                        ast[join_oprt]]
                search_str = round_brackets(build_oprt(join_oprt, children,
                    map_dict))

        if is_group(ast):
            children = [build_search_str(term, groups, map_dict) for term in groups[ast[GROUP_KEY]]]
            search_str = build_oprt(groups_join_oprt, children, map_dict)
            search_str = round_brackets(search_str)

    return search_str
    # Caso em que é um operador

def build_search_string(search_dict):
    """
    Monta a string de pesquisa através do dicionário contendo os grupos de
    pesquisa e as árvores definindo as strings de pesquisa
    """
    (groups, trees, logic_oprt_mapping) = parse_groups_and_ast(search_dict)
    search_strings = [build_search_str(tree, groups, logic_oprt_mapping) for tree in
            trees]
    return search_strings

def parse_groups_and_ast(search_dict, map_dict=None):
    # TODO essa função deve separar as strings e os grupos
    # TODO fazer essa função tratar diferentes mapeamentos de operadores
    # lógicos
    """
    Separa os grupos de pesquisa das strings

    Args:
        :search_dict: um dicionário no formato esperado de definição dos grupos
            e das strings de pesquisa
        :map_dict: o mapeamento entre os operadores lógicos do json e os
            operadores lógicos das ferramentas de pesquisa.

    Returns:
        Uma tupla de três elementos na seguinte ordem:

        :groups: Os grupos de pesquisa
        :trees: As árvores de pesquisa
        :logic_oprt_mapping: O mapeamento entre os 
    """
    if map_dict is None:
        map_dict = DEFAULT_MAP

    trees = sorted([ (key, value) for (key,value) in search_dict.iteritems() if
        key.isdigit() ], key=lambda x: x[0])
    trees = [value for (key, value) in trees]
    groups = search_dict[GROUPS_KEY];
    return (groups, trees, map_dict) 

def main():
   
    # Fazendo o parse na linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The file name')
    parser.add_argument('--out')
    args = parser.parse_args()

    log.basicConfig(level=log.DEBUG)

    log.debug(args.filename)
    ast = read_file(args.filename)

    # Imprime
    result = build_search_string(ast)
    result = '\n'.join(result)
    if args.out:
        out_file = open(args.out, mode = 'w')
        out_file.write(result)
        out_file.close()
    else:
        print parse_groups_and_ast(ast)

# TODO criar a função para ler de arquivo
def read_file(filename):
    """
    Lê o arquivo JSON

    Args:
        filename=O arquivo a ser lido
    """

    with file(filename, mode='r') as f:
        structure = json.load(f)
        log.debug(structure)
        return structure

if __name__ == '__main__':
    # TODO transformar esse teste em um teste unitário
    main()
