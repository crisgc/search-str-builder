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

AND_KEY = '__and__'
OR_KEY = '__or__'
GROUP_KEY = '__group__'
GROUPS_KEY = '__groups__'
DEFAULT_MAP = { AND_KEY: 'AND', OR_KEY: 'OR'}

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

def build_search_str(ast, groups, map_dict, groups_join_oprt=None): 

    if groups_join_oprt is None:
        groups_join_oprt = OR_KEY

    def is_oprt(oprt):
        """
        Testa se a ast é um operador lógico

        Args:
            oprt: O operador a ser testado
        """
        return_value = isinstance(ast, dict) and (oprt in ast)
        return return_value

    def is_group():
        return GROUP_KEY in ast

    def build_oprt(oprt, terms=None):
        """
        Monta uma string com operadores lógicos
        """
        if terms is None:
            terms = ast[oprt]

        children = [build_search_str(term, groups, map_dict) for term in
                terms ]
        join_str = round_str(map_dict[oprt], ' ')
        return join_str.join(children)

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
            if is_oprt(join_oprt): 
                search_str = round_brackets(build_oprt(join_oprt))

        if is_group():
            search_str = build_oprt(groups_join_oprt, groups[ast[GROUP_KEY]])
            search_str = round_brackets(search_str)

    return search_str
    # Caso em que é um operador

def build_search_strings(search_dict, map_dict=None):
    # TODO essa função deve separar as strings e os grupos
    """
    Monta as strings de pesquisa

    Args:
        syntax_tree: a string de pesquisa
    """
    if map_dict is None:
        map_dict = DEFAULT_MAP

    trees = [ value for (key,value) in search_dict.iteritems() if type(key)
            == int ]
    groups = search_dict['__groups__'];
    
    # TODO remover esses print no final   
    print trees
    print groups

    search_strings = [build_search_str(tree, groups, map_dict) for tree in
            trees]
    return search_strings

def main():

    ast = {'__groups__': 
            { 
                'group1': ['group1member1', 'group1member2']
                }, 
            1 : { AND_KEY: [ {GROUP_KEY: 'group1'}, 'test2' , 'test3' ] } # {'__group__': 'group1'}
            }
    print build_search_strings(ast)

# TODO criar a função para ler de arquivo

if __name__ == '__main__':
    # TODO transformar esse teste em um teste unitário
    main()
