(*
 * Search builder
 * crisgc
 *)

(* 
 * ----------------------------------------
 * DEFINIÇÃO DO MÓDULO
 * ----------------------------------------
 *)


(* Define o tipo árvore e os operadores lógicos associados *)
type logicOprt =
    | AndOperator
    | OrOperator

(* Função que retorna a string do operador a partir da string requerida *)
let map_logic_2_str_scopus = 
    function
    | AndOperator -> "AND" 
    | OrOperator -> "OR"

type t_search_str_ast =
    | TerminalOprt of string
    | LogicOprt of (logicOprt * t_search_str_ast list)

(* Funções para adição de prefixo e sufixo *)
let roundStr prefix suffix str = prefix ^ str ^ suffix
let roundStr1 preffix = roundStr preffix preffix
let parenthise = roundStr "(" ")"
let addSpace = roundStr1 " "

(* Cria os bullets para o latex *)
let latexGroup lst =
    let buildBullets lst =
        let print_item key values = Printf.sprintf "\\item[%s] %s " key
        (String.concat ", " values) in
        let bullets = 
            List.map (fun (key, values) -> (print_item key values) ) lst
        in
        String.concat "\n" bullets
    in
    roundStr "\\begin{description}\n" "\n\\end{description}" (buildBullets lst);;

(* Funções para a construção da AST *)
let buildTerminal str_list = List.map (fun e -> TerminalOprt e) str_list;;
let buildJoin str_list_1 str_list_2 = 
    let cartesian_product list1 list2 = 
        List.concat (List.map (fun x -> List.map (fun x' -> (x, x'))
        list2) list1)
    in
    let concat_pairs list_pairs =
        List.map (fun (x, x') -> x ^ " " ^ x') list_pairs
    in
    let str_list = concat_pairs (cartesian_product str_list_1 str_list_2) in
    buildTerminal str_list
;;
let buildOr ast = LogicOprt (OrOperator, ast);;
let buildAnd ast = LogicOprt (AndOperator, ast);;

(** Monta a questão a partir de um grupo *)
(* TODO minimizar o uso de parênteses levando em consideração a precedência de
 * operadores
 *)
let buildSearchStr ast logic_2_str = 
    let rec buildSearchList ast =
        match ast with
        | TerminalOprt str -> 
                (* Criar função para adicionar aspas em string compostas *)
                let addApostrofeIfNecessary str =
                    let apostrofe = "\"" in
                    let complex_word str = String.contains str ' ' in
                    if complex_word str then
                        roundStr1 apostrofe str
                    else
                        str in
                addApostrofeIfNecessary str
        | LogicOprt (logic, list_of_ast) ->
                let str_list = List.map buildSearchList list_of_ast in (* Monta
                a string *)
                let oprt_str = logic_2_str logic in (* Operator *)
                let createOprtStr oprt_str group = parenthise (String.concat
                (addSpace oprt_str) group) in
                createOprtStr oprt_str str_list
    in
    buildSearchList ast;;

(* Monta a impressão da pesquisa em Latex *)
let latexSearchStrPrint ast logic_2_str = 
    let round_itemize = roundStr "\\begin{itemize}\n" "\n\\end{itemize}\n" in
    let latexItem = "\\item " in
    let rec buildLatexPrint ast =
        match ast with
        | TerminalOprt str -> latexItem ^ str
        | LogicOprt (logic, list_of_ast) ->
                let str_list = List.map buildLatexPrint list_of_ast in
                let sub_items = round_itemize (String.concat "\n" str_list) in
                let oprt_str = logic_2_str logic in
                let oprt_item = latexItem ^ oprt_str ^ "\n" in
                oprt_item ^ sub_items
    in
    round_itemize (buildLatexPrint ast);;

