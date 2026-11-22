#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    FLUXO - Precificador                      ║
║          Calculadora de Precificação para Marketplaces       ║
║                    © 2026 FLUXO                              ║
╚══════════════════════════════════════════════════════════════╝

Este programa é dividido em 4 PARTES:
  PARTE 1 - Utilidades visuais (desenho de bordas, cores, formatação)
  PARTE 2 - Dados e armazenamento (salvar/carregar/excluir produtos)
  PARTE 3 - Lógica de cálculo (precificação por marketplace)
  PARTE 4 - Interface do usuário (menus, navegação, telas)
"""

import os
import csv
import html
import json
import math
import ssl
import unicodedata
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime

# ╔══════════════════════════════════════════════════════════════╗
# ║              PARTE 1 - UTILIDADES VISUAIS                   ║
# ║  Funções para desenhar bordas, colorir textos e formatar    ║
# ║  a apresentação no terminal de forma bonita e legível.      ║
# ╚══════════════════════════════════════════════════════════════╝

# --- Códigos de cores ANSI para o terminal ---

# --- Códigos de cores ANSI para o terminal ---
# Usamos essas cores para destacar informações importantes e pintar os cards
# de cada marketplace com a sua cor real (ex: Shopee laranja/vermelho, Mercado Livre amarelo)
# Cada código muda a cor do texto que vem depois dele.
# RESET volta o texto para a cor normal.

RESET   = "\033[0m"       # Volta ao normal
BOLD    = "\033[1m"       # Texto em negrito
DIM     = "\033[2m"       # Texto esmaecido

# Cores do texto
VERDE   = "\033[92m"      # Verde claro (cor principal do FLUXO)
AZUL    = "\033[94m"      # Azul mais claro
AMARELO = "\033[93m"      # Amarelo
VERMELHO= "\033[91m"      # Vermelho
BRANCO  = "\033[97m"      # Branco
CIANO   = "\033[96m"      # Ciano

# Cores de fundo (usadas nos cards de marketplace)
BG_PRETO     = "\033[40m"  # Fundo preto     (TikTok)
BG_AMARELO   = "\033[43m"  # Fundo amarelo   (Mercado Livre)
BG_AZULESC   = "\033[44m"  # Fundo azul esc. (Amazon)
BG_VERMELHO  = "\033[41m"  # Fundo vermelho  (Shopee)
BG_VERDE     = "\033[42m"  # Fundo verde     (marketplaces cadastrados pelo usuário)

# Largura padrão do terminal (usada para centralizar e desenhar bordas)
LARGURA = 62


def limpar_tela():
    """Limpa a tela do terminal.
    Funciona tanto no Windows (cls) quanto no Linux/Mac (clear)."""
    os.system("cls" if os.name == "nt" else "clear")
# Evita que o terminal fique cheio de texto acumulado.


def linha(caractere="═", cor=AZUL):
    """Desenha uma linha horizontal decorativa.

    Exemplo: ══════════════════════════════════
    """
    print(f"{cor}{'═' * LARGURA}{RESET}")
# Centraliza perfeitamente o texto dentro da caixa verde.


def cabecalho(titulo, cor=VERDE):
    """Desenha um cabeçalho com bordas para destacar seções.

    Exemplo:
    ╔══════════════════════════════════════════╗
    ║          MEU TÍTULO AQUI                 ║
    ╚══════════════════════════════════════════╝
    """
    print(f"{cor}╔{'═' * (LARGURA - 2)}╗{RESET}")
    # Centraliza o título dentro da caixa
    texto = titulo.center(LARGURA - 2)
    print(f"{cor}║{BOLD}{BRANCO}{texto}{RESET}{cor}║{RESET}")
    print(f"{cor}╚{'═' * (LARGURA - 2)}╝{RESET}")


def subcabecalho(titulo, cor=AZUL):
    """Desenha um subtítulo com traços laterais.

    Exemplo: ── Meu Subtítulo ──────────────────
    """
    espacos = LARGURA - len(titulo) - 6
    print(f"\n{cor}── {BOLD}{titulo}{RESET}{cor} {'─' * espacos}{RESET}")

# Criar divisórias visuais na tela, separando o menu 
# dos resultados para a tela não ficar bagunçada.

def exibir_mensagem(texto, cor=AMARELO):
    """Exibe uma mensagem destacada entre colchetes.

    Exemplo: ⚠  Mensagem importante aqui
    """
    print(f"\n{cor}⚠  {texto}{RESET}")
# Dar avisos importantes para o usuário, como produtos não encontrados.
# Usando uma cor chamativa como amarelo para sinalizar.


def exibir_sucesso(texto):
    """Exibe uma mensagem de sucesso em verde.

    Exemplo: ✔  Operação realizada com sucesso!
    """
    print(f"\n{VERDE}✔  {texto}{RESET}")

# Dar retorno positivo ao usuário, quando uma ação for correta.

def exibir_erro(texto):
    """Exibe uma mensagem de erro em vermelho.

    Exemplo: ✖  Algo deu errado!
    """
    print(f"\n{VERMELHO}✖  {texto}{RESET}")
# Alertar o usuário claramente, quando uma ação estiver errada.
# Usando a cor vermelha para ser um sinal de parada dentro do sistema.


def input_estilizado(rotulo):
    """Mostra um campo de entrada estilizado e retorna o que o usuário digitou.

    Exemplo: │ Nome do produto: _
    """
    return input(f"  {CIANO}│ {BRANCO}{rotulo}: {RESET}")
# Substitui aquele visual padrão sem graça do terminal
# por um campo de preenchimento que guia o usuário usando cores diferentes 
# para a pergunta e para o que ele vai digitar.


def formatar_moeda(valor):
    """Formata um número como moeda brasileira.

    Exemplo: 1234.5 → R$ 1.234,50
    """
    # O Python formata como "1,234.50" (padrão americano).
    # Trocamos vírgula e ponto de lugar para ficar no padrão brasileiro.
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"R$ {texto}"

# Padroniza a exibição financeira. Transforma números puros no padrão real R$ (ex: 2,00).


def formatar_percentual(valor):
    """Formata um número decimal como porcentagem brasileira.

    Exemplo: 0.155 → 15,5%
    """
    return f"{valor * 100:.1f}".replace(".", ",") + "%"


def pausar():
    """Pausa a execução e espera o usuário pressionar Enter para continuar."""
    input(f"\n{DIM}  Pressione ENTER para continuar...{RESET}")
# Dar tempo para o usuário ler os resultados na tela 
# antes que o programa limpe tudo e volte para o menu principal.


# ── Leitura e validação de entradas ──
# Funções reutilizáveis que pedem um dado ao usuário e só deixam o
# programa continuar quando o valor é válido. Assim, uma digitação
# errada não derruba o sistema nem faz o usuário perder o que já digitou.

def normalizar_texto(texto):
    """Deixa o texto em minúsculas e sem acentos, para comparar na busca.

    Exemplo: "Fone Bluetooth Ção" → "fone bluetooth cao"
    """
    # NFD separa a letra do acento (ã → a + ~); depois descartamos os acentos.
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acentos = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return sem_acentos.lower().strip()


def cortar(texto, tamanho):
    """Corta o texto para caber numa coluna da tabela, usando '…' se passar."""
    texto = str(texto)
    if len(texto) <= tamanho:
        return texto
    return texto[:tamanho - 1] + "…"


def converter_numero(texto):
    """Converte o que o usuário digitou em número (float).

    Aceita vírgula ou ponto como separador decimal e ignora "R$" e "%".
    Exemplos: "25,90" → 25.9   |   "1.234,56" → 1234.56   |   "15%" → 15.0

    Levanta ValueError se não for um número válido (inclusive "nan" e
    "inf", que o float() do Python aceitaria sem reclamar).
    """
    limpo = texto.strip().replace("R$", "").replace("%", "").replace(" ", "")
    if "," in limpo:
        # Formato brasileiro: o ponto separa os milhares e a vírgula, os decimais
        limpo = limpo.replace(".", "").replace(",", ".")
    valor = float(limpo)
    if math.isnan(valor) or math.isinf(valor):
        raise ValueError("número inválido")
    return valor


def ler_texto(rotulo, atual=None, tamanho_max=40):
    """Pede um texto ao usuário e repete a pergunta até ser válido.

    Args:
        rotulo (str):      Pergunta mostrada na tela.
        atual (str|None):  Valor atual. Se informado, apertar ENTER mantém ele.
        tamanho_max (int): Quantidade máxima de caracteres permitida.

    Retorna:
        texto (str): O texto digitado (sem espaços nas pontas).
    """
    while True:
        if atual is not None:
            texto = input_estilizado(f"{rotulo} (atual: {atual})").strip()
        else:
            texto = input_estilizado(rotulo).strip()

        if not texto and atual is not None:
            return atual  # ENTER = mantém o valor que já existia
        if not texto:
            exibir_erro("Este campo não pode ficar vazio.")
        elif len(texto) > tamanho_max:
            exibir_erro(f"Use no máximo {tamanho_max} caracteres "
                        f"(você digitou {len(texto)}).")
        else:
            return texto


def ler_numero(rotulo, minimo, maximo, atual=None, formatar=str,
               fator=1, minimo_incluso=True):
    """Pede um número ao usuário e repete a pergunta até ser válido.

    Args:
        rotulo (str):          Pergunta mostrada na tela.
        minimo, maximo (num):  Limites permitidos, na unidade que o usuário digita
                               (ex.: 0 a 99 para porcentagem).
        atual (float|None):    Valor atual (já guardado). ENTER mantém ele.
        formatar (função):     Como mostrar o valor atual na tela.
        fator (int):           Divisor entre o que o usuário digita e o que é
                               guardado (100 para porcentagem: digita 15 → 0.15).
        minimo_incluso (bool): False quando o próprio mínimo não vale (ex.: custo > 0).

    Retorna:
        valor (float): O número já convertido para a unidade guardada.
    """
    while True:
        if atual is not None:
            texto = input_estilizado(f"{rotulo} (atual: {formatar(atual)})")
        else:
            texto = input_estilizado(rotulo)

        if not texto.strip() and atual is not None:
            return atual  # ENTER = mantém o valor que já existia

        try:
            valor = converter_numero(texto)
        except ValueError:
            exibir_erro("Digite apenas números (exemplo: 25,90).")
            continue

        abaixo_do_minimo = valor < minimo if minimo_incluso else valor <= minimo
        if abaixo_do_minimo or valor > maximo:
            if minimo_incluso:
                faixa = f"entre {minimo:g} e {maximo:g}"
            else:
                faixa = f"maior que {minimo:g} e até {maximo:g}"
            exibir_erro(f"Valor fora do permitido: use um número {faixa}.")
            continue

        return valor / fator


def confirmar(pergunta):
    """Faz uma pergunta de sim/não e só aceita uma resposta válida.

    Retorna:
        True para S/SIM, False para N/NÃO.
    """
    while True:
        resposta = input(f"  {VERDE}{pergunta} (S/N): {RESET}").strip().upper()
        if resposta in ("S", "SIM"):
            return True
        if resposta in ("N", "NAO", "NÃO"):
            return False
        exibir_erro("Responda com S (sim) ou N (não).")


# ╔══════════════════════════════════════════════════════════════╗
# ║             PARTE 2 - DADOS E ARMAZENAMENTO                 ║
# ║  Funções para salvar, carregar e excluir produtos em um     ║
# ║  arquivo JSON local (equivalente ao localStorage do site).  ║
# ╚══════════════════════════════════════════════════════════════╝
# -m
# Caminho do arquivo onde os produtos são salvos
# O arquivo fica na mesma pasta do programa
# São salvos em formato JSON.
ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "produtos.json")

# Campos que todo produto salvo precisa ter para o sistema funcionar
CAMPOS_OBRIGATORIOS = ("nome", "fornecedor", "custo", "taxa_usuario", "margem")


def _eh_numero(valor):
    """True se o valor é int ou float (bool não conta, apesar de ser int no Python)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def produto_valido(produto):
    """Confere se um item lido do JSON tem a estrutura esperada.

    Protege o sistema de arquivos editados à mão ou danificados:
    sem isso, um campo faltando causaria erro (KeyError) nas telas.
    """
    if not isinstance(produto, dict):
        return False
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in produto:
            return False
    if not isinstance(produto["nome"], str) or not isinstance(produto["fornecedor"], str):
        return False
    if not (_eh_numero(produto["custo"]) and _eh_numero(produto["taxa_usuario"])
            and _eh_numero(produto["margem"])):
        return False

    resultados = produto.get("resultados", {})
    if not isinstance(resultados, dict):
        return False
    for res in resultados.values():
        if not (isinstance(res, dict) and _eh_numero(res.get("preco"))
                and _eh_numero(res.get("lucro"))):
            return False

    historico = produto.get("historico", [])
    if not isinstance(historico, list):
        return False
    for item in historico:
        if not isinstance(item, dict):
            return False
    return True


def _isolar_arquivo_corrompido():
    """Guarda o arquivo de dados ilegível com outro nome.

    Assim ele NÃO é sobrescrito (nenhum dado se perde, dá para recuperar
    à mão) e o sistema consegue recomeçar com uma lista vazia.
    """
    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = ARQUIVO_DADOS.replace(".json", f"_corrompido_{carimbo}.json")
    try:
        os.replace(ARQUIVO_DADOS, destino)
        exibir_mensagem(f"O arquivo de produtos estava danificado e foi guardado "
                        f"como '{os.path.basename(destino)}'. "
                        f"O sistema recomeçou com uma lista vazia.")
    except OSError:
        exibir_mensagem("O arquivo de produtos está danificado e não pôde ser lido.")


# no caso de o usuario querer ver os produtos salvos
def carregar_produtos():
    """Lê todos os produtos salvos no arquivo JSON.

    Retorna:
        lista (list): Lista de dicionários, cada um representando um produto.
                      Se o arquivo não existir, retorna uma lista vazia.
                      Se o arquivo estiver danificado, ele é guardado com outro
                      nome (sem apagar nada) e retorna uma lista vazia.
    """
    if not os.path.exists(ARQUIVO_DADOS):
        return []  # Arquivo não existe ainda, retorna lista vazia

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, UnicodeDecodeError):
        dados = None  # conteúdo ilegível
    except OSError:
        exibir_erro("Não foi possível abrir o arquivo de produtos.")
        return []

    if not isinstance(dados, list):
        _isolar_arquivo_corrompido()
        return []
    for produto in dados:
        if not produto_valido(produto):
            _isolar_arquivo_corrompido()
            return []
    return dados


#salvar os produtos
def salvar_produtos(lista):
    """Grava a lista de produtos no arquivo JSON.

    A gravação é feita em duas etapas: primeiro num arquivo temporário e,
    só depois que terminou, ele substitui o arquivo real. Se o programa
    fechar no meio da gravação, o arquivo antigo continua intacto.

    Args:
        lista (list): Lista de dicionários com os dados dos produtos.
    """
    temporario = ARQUIVO_DADOS + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        # indent=2 deixa o JSON formatado e legível
        # ensure_ascii=False permite acentos (é, ã, ç, etc.)
        json.dump(lista, arquivo, indent=2, ensure_ascii=False)
    os.replace(temporario, ARQUIVO_DADOS)

#adicionar produtos
def adicionar_produto(produto):
    """Adiciona um novo produto à lista e salva no arquivo.

    Args:
        produto (dict): Dicionário com os dados do produto.
                        Exemplo: {"nome": "Fone", "fornecedor": "Ali", ...}
    """
    lista = carregar_produtos()
    lista.append(produto)
    salvar_produtos(lista)

#excluir produtos
def excluir_produto(indice):
    """Remove um produto da lista pelo seu índice (posição).

    Args:
        indice (int): Posição do produto na lista (começa em 0).

    Retorna:
        sucesso (bool): True se excluiu, False se o índice é inválido.
    """
    lista = carregar_produtos()
    if 0 <= indice < len(lista):
        lista.pop(indice)  # Remove o item na posição indicada
        salvar_produtos(lista)
        return True
    return False

#buscar produtos
def buscar_produtos(termo):
    """Procura produtos pelo nome ou pelo fornecedor.

    A busca ignora maiúsculas e acentos, e aceita várias palavras em
    qualquer ordem: "bluetooth fone" encontra "Fone Bluetooth Pro".

    Args:
        termo (str): O que o usuário digitou na busca.

    Retorna:
        encontrados (list): Lista de tuplas (indice, produto). O índice é a
                            posição REAL do produto na lista salva, para
                            conseguir editar/excluir depois.
    """
    palavras = normalizar_texto(termo).split()
    if not palavras:
        return []

    encontrados = []
    for indice, produto in enumerate(carregar_produtos()):
        # Junta nome + fornecedor para procurar tudo de uma vez
        alvo = normalizar_texto(produto["nome"] + " " + produto["fornecedor"])
        if all(palavra in alvo for palavra in palavras):
            encontrados.append((indice, produto))
    return encontrados


# Funções usadas como "chave" para ordenar a lista de produtos.
# Cada item recebido é uma tupla (indice, produto).
def _chave_nome(par):
    return normalizar_texto(par[1]["nome"])


def _chave_custo(par):
    return par[1]["custo"]


def _chave_data(par):
    """Data da última alteração (edição ou cadastro) do produto."""
    produto = par[1]
    texto = produto.get("data_edicao") or produto.get("data") or ""
    try:
        return datetime.strptime(texto, "%d/%m/%Y %H:%M")
    except ValueError:
        return datetime.min  # sem data válida: vai para o fim da lista


def ordenar_produtos(pares, criterio):
    """Ordena uma lista de tuplas (indice, produto).

    Args:
        pares (list):    Lista de tuplas (indice, produto).
        criterio (str):  "cadastro", "nome", "custo" ou "recentes".

    Retorna:
        Uma nova lista ordenada (a original não muda).
    """
    if criterio == "nome":
        return sorted(pares, key=_chave_nome)
    if criterio == "custo":
        return sorted(pares, key=_chave_custo)
    if criterio == "recentes":
        return sorted(pares, key=_chave_data, reverse=True)
    return list(pares)  # "cadastro": mantém a ordem em que foram salvos


def existe_duplicado(nome, fornecedor, ignorar_indice=None):
    """Verifica se já existe outro produto com o mesmo nome E fornecedor.

    Args:
        ignorar_indice (int|None): Posição do produto que está sendo editado
                                   (ele não conta como duplicado de si mesmo).
    """
    nome_norm = normalizar_texto(nome)
    fornecedor_norm = normalizar_texto(fornecedor)
    for indice, produto in enumerate(carregar_produtos()):
        if indice == ignorar_indice:
            continue
        if (normalizar_texto(produto["nome"]) == nome_norm
                and normalizar_texto(produto["fornecedor"]) == fornecedor_norm):
            return True
    return False

#atualizar produtos
def atualizar_produto(indice, produto_novo):
    """Substitui um produto salvo pelos dados atualizados.

    Args:
        indice (int):        Posição do produto na lista (começa em 0).
        produto_novo (dict): Dicionário completo do produto já atualizado.

    Retorna:
        sucesso (bool): True se salvou, False se o índice é inválido
                        ou se não foi possível gravar o arquivo.
    """
    lista = carregar_produtos()
    if not 0 <= indice < len(lista):
        return False
    lista[indice] = produto_novo
    try:
        salvar_produtos(lista)
    except OSError:
        return False
    return True


# ╔══════════════════════════════════════════════════════════════╗
# ║            PARTE 3 - LÓGICA DE CÁLCULO                      ║
# ║  Funções que fazem a precificação dos produtos. Calcula o   ║
# ║  preço ideal de venda com base no custo, taxas fixas do     ║
# ║  marketplace, taxa do vendedor e margem de lucro desejada.  ║
# ╚══════════════════════════════════════════════════════════════╝

# Taxas fixas de cada marketplace (percentual sobre o valor da venda)
# Esses valores são os mesmos usados no site original.
# Estes são os marketplaces que já vêm com o programa.
MARKETPLACES_PADRAO = {
    "TikTok":        {"taxa_fixa": 0.06, "cor_fundo": BG_PRETO,    "cor_texto": BRANCO,  "icone": "♪"},
    "Mercado Livre":  {"taxa_fixa": 0.17, "cor_fundo": BG_AMARELO,  "cor_texto": "\033[34m", "icone": "🤝"},
    "Amazon":         {"taxa_fixa": 0.13, "cor_fundo": BG_AZULESC,  "cor_texto": BRANCO,  "icone": "📦"},
    "Shopee":         {"taxa_fixa": 0.15, "cor_fundo": BG_VERMELHO, "cor_texto": BRANCO,  "icone": "🛒"},
}

# Marketplaces em uso agora: começa com os padrão e muda quando o usuário
# cadastra ou remove algum. É este dicionário que o resto do programa usa.
MARKETPLACES = dict(MARKETPLACES_PADRAO)

# Limites para os marketplaces cadastrados pelo usuário
TAMANHO_MAX_NOME_MKT = 16   # cabe na coluna dos cards e das listas
TAXA_MAX_MKT = 0.99         # taxa fixa máxima: 99%

# Arquivo onde a configuração dos marketplaces fica salva (mesma pasta do programa)
ARQUIVO_MARKETPLACES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "marketplaces.json"
)


def _dados_marketplace_personalizado(taxa_fixa):
    """Monta o dicionário de um marketplace cadastrado pelo usuário.

    O usuário informa só nome e taxa, então a aparência (fundo verde e
    ícone de loja) é a mesma para todos os marketplaces cadastrados.
    """
    return {
        "taxa_fixa": taxa_fixa,
        "cor_fundo": BG_VERDE,
        "cor_texto": BRANCO,
        "icone": "🏪",
    }


def validar_nome_marketplace(nome):
    """Confere se o nome pode ser usado por um novo marketplace.

    Retorna:
        str: mensagem de erro, ou None se o nome é válido.
    """
    nome_norm = normalizar_texto(nome)
    if not nome_norm:
        return "O nome do marketplace é obrigatório."
    if len(nome.strip()) > TAMANHO_MAX_NOME_MKT:
        return f"Use no máximo {TAMANHO_MAX_NOME_MKT} caracteres no nome."
    if nome_norm in {normalizar_texto(n) for n in MARKETPLACES}:
        return f"O marketplace '{nome.strip()}' já existe."
    if nome_norm in {normalizar_texto(n) for n in MARKETPLACES_PADRAO}:
        return ("Esse nome é de um marketplace padrão que foi removido. "
                "Use a opção de restaurar os marketplaces padrão.")
    return None


def validar_taxa_marketplace(taxa_fixa):
    """Confere se a taxa fixa (decimal, ex.: 0.12 = 12%) é aceitável.

    Retorna:
        str: mensagem de erro, ou None se a taxa é válida.
    """
    if not _eh_numero(taxa_fixa) or not 0 <= taxa_fixa <= TAXA_MAX_MKT:
        return "A taxa fixa deve estar entre 0% e 99%."
    return None


def salvar_marketplaces():
    """Grava a configuração atual dos marketplaces no arquivo JSON.

    Só guarda o que difere do padrão: os marketplaces cadastrados
    (nome → taxa), os nomes dos padrão que foram removidos e as taxas
    dos padrão que o usuário alterou.
    A gravação passa por um arquivo temporário, para nunca deixar o
    arquivo real pela metade.

    Retorna:
        bool: True se gravou, False se não foi possível gravar.
    """
    dados = {
        "personalizados": {
            nome: info["taxa_fixa"]
            for nome, info in MARKETPLACES.items()
            if nome not in MARKETPLACES_PADRAO
        },
        "removidos": [nome for nome in MARKETPLACES_PADRAO if nome not in MARKETPLACES],
        "alterados": {
            nome: info["taxa_fixa"]
            for nome, info in MARKETPLACES.items()
            if nome in MARKETPLACES_PADRAO
            and info["taxa_fixa"] != MARKETPLACES_PADRAO[nome]["taxa_fixa"]
        },
    }
    temporario = ARQUIVO_MARKETPLACES + ".tmp"
    try:
        with open(temporario, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        os.replace(temporario, ARQUIVO_MARKETPLACES)
        return True
    except OSError:
        return False


def carregar_marketplaces():
    """Aplica ao MARKETPLACES o que foi salvo no arquivo (se houver).

    Chamada uma vez, quando o programa abre. Se o arquivo não existir,
    o programa segue só com os marketplaces padrão. Se estiver danificado
    ou com valores inválidos, os itens ruins são ignorados.
    """
    if not os.path.exists(ARQUIVO_MARKETPLACES):
        return

    try:
        with open(ARQUIVO_MARKETPLACES, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        dados = None

    if not isinstance(dados, dict):
        exibir_mensagem("O arquivo de marketplaces não pôde ser lido. "
                        "Usando apenas os marketplaces padrão.")
        pausar()
        return

    removidos = dados.get("removidos", [])
    if isinstance(removidos, list):
        for nome in removidos:
            if isinstance(nome, str):
                MARKETPLACES.pop(nome, None)

    personalizados = dados.get("personalizados", {})
    if isinstance(personalizados, dict):
        for nome, taxa in personalizados.items():
            nome_valido = (isinstance(nome, str) and nome.strip() != ""
                           and len(nome) <= TAMANHO_MAX_NOME_MKT
                           and nome not in MARKETPLACES
                           and nome not in MARKETPLACES_PADRAO)
            if nome_valido and validar_taxa_marketplace(taxa) is None:
                MARKETPLACES[nome] = _dados_marketplace_personalizado(taxa)

    # Taxas dos marketplaces padrão que o usuário alterou em sessões anteriores
    alterados = dados.get("alterados", {})
    if isinstance(alterados, dict):
        for nome, taxa in alterados.items():
            if (nome in MARKETPLACES and nome in MARKETPLACES_PADRAO
                    and validar_taxa_marketplace(taxa) is None):
                MARKETPLACES[nome] = dict(MARKETPLACES[nome], taxa_fixa=taxa)

    if not MARKETPLACES:  # arquivo editado à mão e vazio: nunca ficar sem nenhum
        MARKETPLACES.update(MARKETPLACES_PADRAO)


def adicionar_marketplace(nome, taxa_fixa):
    """Cadastra um novo marketplace e salva no arquivo.

    Args:
        nome (str):        Nome do marketplace (até 16 caracteres).
        taxa_fixa (float): Taxa da plataforma em decimal (0.12 = 12%).

    Retorna:
        (bool, str): (deu certo?, mensagem para mostrar ao usuário)
    """
    erro = validar_nome_marketplace(nome) or validar_taxa_marketplace(taxa_fixa)
    if erro:
        return False, erro

    nome = nome.strip()
    MARKETPLACES[nome] = _dados_marketplace_personalizado(taxa_fixa)
    if not salvar_marketplaces():
        del MARKETPLACES[nome]  # desfaz: ou grava tudo, ou não muda nada
        return False, "Não foi possível gravar o arquivo. Verifique se a pasta permite escrita."
    return True, f"Marketplace '{nome}' cadastrado com sucesso!"


def remover_marketplace(nome):
    """Remove um marketplace (padrão ou cadastrado) e salva no arquivo.

    Sempre sobra pelo menos um marketplace, senão não haveria o que calcular.

    Retorna:
        (bool, str): (deu certo?, mensagem para mostrar ao usuário)
    """
    if nome not in MARKETPLACES:
        return False, "Marketplace não encontrado."
    if len(MARKETPLACES) <= 1:
        return False, "É preciso manter pelo menos um marketplace."

    dados = MARKETPLACES.pop(nome)
    if not salvar_marketplaces():
        MARKETPLACES[nome] = dados  # desfaz a remoção
        return False, "Não foi possível gravar o arquivo. Verifique se a pasta permite escrita."
    return True, f"Marketplace '{nome}' removido com sucesso!"


def restaurar_marketplaces_padrao():
    """Traz de volta os marketplaces padrão que foram removidos.

    Os cadastrados pelo usuário continuam como estão.

    Retorna:
        (bool, str): (deu certo?, mensagem para mostrar ao usuário)
    """
    faltando = [nome for nome in MARKETPLACES_PADRAO if nome not in MARKETPLACES]
    if not faltando:
        return False, "Todos os marketplaces padrão já estão ativos."

    personalizados = {nome: info for nome, info in MARKETPLACES.items()
                      if nome not in MARKETPLACES_PADRAO}
    # Guarda os padrão que continuam ativos, para não perder as taxas que o usuário editou
    padroes_atuais = {nome: info for nome, info in MARKETPLACES.items()
                      if nome in MARKETPLACES_PADRAO}
    anterior = dict(MARKETPLACES)
    MARKETPLACES.clear()
    for nome, info in MARKETPLACES_PADRAO.items():  # padrão primeiro, na ordem original
        MARKETPLACES[nome] = padroes_atuais.get(nome, info)
    MARKETPLACES.update(personalizados)

    if not salvar_marketplaces():
        MARKETPLACES.clear()
        MARKETPLACES.update(anterior)  # desfaz
        return False, "Não foi possível gravar o arquivo. Verifique se a pasta permite escrita."
    return True, f"Marketplaces restaurados: {', '.join(faltando)}."


def editar_taxa_marketplace(nome, nova_taxa):
    """Altera a taxa fixa de um marketplace (padrão ou cadastrado) e salva.

    O nome não muda, porque os produtos salvos usam o nome para guardar
    o preço de cada marketplace. Depois de mudar a taxa, os preços
    salvos ficam desatualizados até serem recalculados.

    Args:
        nome (str):        Nome do marketplace que será editado.
        nova_taxa (float): Nova taxa fixa em decimal (0.12 = 12%).

    Retorna:
        (bool, str): (deu certo?, mensagem para mostrar ao usuário)
    """
    if nome not in MARKETPLACES:
        return False, "Marketplace não encontrado."

    erro = validar_taxa_marketplace(nova_taxa)
    if erro:
        return False, erro

    anterior = MARKETPLACES[nome]
    if abs(anterior["taxa_fixa"] - nova_taxa) < 1e-9:
        return False, "A nova taxa é igual à taxa atual. Nada foi alterado."

    # Cria um dicionário NOVO (em vez de mudar o antigo). Assim os valores
    # originais em MARKETPLACES_PADRAO continuam intactos para consulta.
    MARKETPLACES[nome] = dict(anterior, taxa_fixa=nova_taxa)
    if not salvar_marketplaces():
        MARKETPLACES[nome] = anterior  # desfaz: ou grava, ou não muda nada
        return False, "Não foi possível gravar o arquivo. Verifique se a pasta permite escrita."

    return True, (f"Taxa de '{nome}' alterada de {formatar_percentual(anterior['taxa_fixa'])} "
                  f"para {formatar_percentual(nova_taxa)}.")


def calcular_preco(custo, taxa_usuario, margem, taxa_fixa_marketplace):
    """Calcula o preço ideal de venda para um marketplace.

    A fórmula é:
        preço = custo / (1 - taxa_total - margem)

    Onde taxa_total = taxa_fixa_marketplace + taxa_usuario

    Isso garante que, ao vender pelo preço calculado, o vendedor
    receberá exatamente a margem de lucro desejada após descontar
    todas as taxas.

    Args:
        custo (float):                  Custo de aquisição do produto.
        taxa_usuario (float):           Taxa adicional do vendedor (decimal, ex: 0.05 = 5%).
        margem (float):                 Margem de lucro desejada (decimal, ex: 0.20 = 20%).
        taxa_fixa_marketplace (float):  Taxa fixa da plataforma (decimal).

    Retorna:
        resultado (dict): Dicionário com "preco" e "lucro", ou
                          None se margem + taxa >= 100% (impossível calcular).
    """
    taxa_total = taxa_fixa_marketplace + taxa_usuario
    denominador = 1 - taxa_total - margem

    # Se o denominador for zero ou negativo, o cálculo é impossível
    # (significaria que as taxas + margem consomem 100% ou mais do preço)
    if denominador <= 0:
        return None

    preco = custo / denominador
    lucro = preco * margem

    return {
        "preco": round(preco, 2),
        "lucro": round(lucro, 2),
    }


def calcular_todos_marketplaces(custo, taxa_usuario, margem):
    """Calcula o preço ideal para TODOS os marketplaces de uma vez.

    Args:
        custo (float):        Custo de aquisição do produto.
        taxa_usuario (float): Taxa adicional do vendedor (decimal).
        margem (float):       Margem de lucro desejada (decimal).

    Retorna:
        resultados (dict): Dicionário onde cada chave é o nome do marketplace
                           e o valor é o resultado do cálculo (ou None se inválido).
    """
    resultados = {}
    for nome_mkt, dados_mkt in MARKETPLACES.items():
        resultado = calcular_preco(custo, taxa_usuario, margem, dados_mkt["taxa_fixa"])
        resultados[nome_mkt] = resultado
    return resultados


# Campos de um produto que o usuário pode editar.
# chave no dicionário do produto → nome mostrado na tela
CAMPOS_PRODUTO = {
    "nome":         "Nome do produto",
    "fornecedor":   "Fornecedor",
    "custo":        "Custo de aquisição",
    "taxa_usuario": "Taxa adicional",
    "margem":       "Margem de lucro",
}


def formatar_campo(campo, valor):
    """Mostra o valor de um campo do jeito certo (R$, % ou texto)."""
    if campo == "custo":
        return formatar_moeda(valor)
    if campo in ("taxa_usuario", "margem"):
        return formatar_percentual(valor)
    return str(valor)


def calcular_resultados_produto(custo, taxa_usuario, margem):
    """Calcula os preços de todos os marketplaces e guarda só os possíveis.

    Cada resultado traz "preco" (ideal), "lucro" e também "indicado"
    (preço comercial para anunciar, com a margem real dele).

    Retorna:
        resultados (dict): {"Shopee": {"preco": ..., "lucro": ..., "indicado": {...}}, ...}
                           Marketplaces onde o cálculo é impossível
                           (taxa + margem ≥ 100%) não aparecem.
    """
    resultados = {}
    for nome_mkt, resultado in calcular_todos_marketplaces(custo, taxa_usuario, margem).items():
        if resultado:
            resultado = dict(resultado)  # cópia, para acrescentar o indicado
            resultado["indicado"] = calcular_preco_indicado(
                resultado, custo, taxa_usuario, MARKETPLACES[nome_mkt]["taxa_fixa"]
            )
            resultados[nome_mkt] = resultado
    return resultados


def listar_alteracoes(original, rascunho):
    """Compara o produto original com o rascunho editado.

    Retorna:
        alteracoes (list): Lista de tuplas (campo, valor_antes, valor_depois)
                           só com os campos que realmente mudaram.
    """
    alteracoes = []
    for campo in CAMPOS_PRODUTO:
        if original[campo] != rascunho[campo]:
            alteracoes.append((campo, original[campo], rascunho[campo]))
    return alteracoes


def aplicar_alteracoes(original, rascunho, alteracoes):
    """Monta o produto final: novos dados + preços recalculados + histórico.

    O que muda no produto:
      - os campos editados recebem os novos valores;
      - "resultados" é recalculado com o custo/taxa/margem novos;
      - "data_edicao" guarda quando foi a última edição;
      - "historico" ganha uma linha para cada campo alterado
        (guardamos no máximo as últimas 50).

    Retorna:
        produto (dict): Novo dicionário (o original não é modificado).
    """
    produto = dict(original)
    for campo in CAMPOS_PRODUTO:
        produto[campo] = rascunho[campo]

    produto["resultados"] = calcular_resultados_produto(
        produto["custo"], produto["taxa_usuario"], produto["margem"]
    )

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    produto["data_edicao"] = agora

    historico = list(original.get("historico", []))
    for campo, antes, depois in alteracoes:
        historico.append({
            "data": agora,
            "campo": CAMPOS_PRODUTO[campo],
            "de": formatar_campo(campo, antes),
            "para": formatar_campo(campo, depois),
        })
    produto["historico"] = historico[-50:]
    return produto


# ── Preço indicado ──
# O "preço ideal" é o resultado exato da conta (ex.: R$ 87,10). Ninguém anuncia
# assim: o "preço indicado" é o primeiro preço comercial (terminado em ,90)
# que fica igual ou acima do ideal, e mostra a margem REAL que ele entrega.

def calcular_preco_indicado(resultado, custo, taxa_usuario, taxa_mkt):
    """Calcula o preço indicado para anunciar, a partir do preço ideal.

    Regra: sobe para o próximo valor terminado em ,90.
        87,10 → 87,90   |   87,95 → 88,90   |   87,00 → 87,90

    Como o preço indicado é sempre igual ou maior que o ideal,
    a margem real nunca fica abaixo da margem desejada.

    Args:
        resultado (dict|None): Resultado de calcular_preco (com "preco").
        custo (float):         Custo de aquisição do produto.
        taxa_usuario (float):  Taxa adicional do vendedor (decimal).
        taxa_mkt (float):      Taxa fixa do marketplace (decimal).

    Retorna:
        dict com "preco", "lucro" e "margem" (margem real, em decimal),
        ou None se o resultado for None (cálculo impossível).
    """
    if resultado is None:
        return None

    ideal = resultado["preco"]
    indicado = math.floor(ideal) + 0.90
    if indicado < ideal:      # o ,90 do mesmo real ficou abaixo: sobe um real
        indicado += 1
    indicado = round(indicado, 2)

    # Sobra após tirar as taxas e o custo: preço × (1 − taxas) − custo
    lucro = round(indicado * (1 - taxa_mkt - taxa_usuario) - custo, 2)
    return {
        "preco": indicado,
        "lucro": lucro,
        "margem": round(lucro / indicado, 4),
    }


def formatar_indicado(res):
    """Texto curto com o preço indicado de um resultado salvo.

    Retorna "" se o produto foi salvo antes do preço indicado existir.
    """
    indicado = res.get("indicado") if isinstance(res, dict) else None
    if isinstance(indicado, dict) and _eh_numero(indicado.get("preco")):
        return f"  {DIM}indicado:{RESET} {CIANO}{formatar_moeda(indicado['preco'])}{RESET}"
    return ""


# ── Preços salvos desatualizados ──
# Cada produto guarda os preços calculados no dia em que foi salvo. Se o
# usuário muda a taxa de um marketplace (ou cadastra/remove um), esses
# preços ficam velhos. As funções abaixo detectam isso e refazem os cálculos.

def produto_desatualizado(produto, atuais=None):
    """Diz se os preços salvos de um produto não batem com as taxas de hoje.

    Um produto está desatualizado quando, para algum marketplace ATIVO:
      - não tem preço salvo, ou o preço salvo é diferente do atual;
      - foi salvo antes do preço indicado existir;
      - tem preço salvo, mas hoje o cálculo é impossível.

    Args:
        produto (dict):    O produto salvo.
        atuais (dict|None): Resultados já calculados com as taxas de hoje
                            (evita calcular duas vezes). Se None, calcula aqui.
    """
    if atuais is None:
        atuais = calcular_resultados_produto(produto["custo"], produto["taxa_usuario"],
                                             produto["margem"])
    salvos = produto.get("resultados", {})

    for nome_mkt, atual in atuais.items():
        salvo = salvos.get(nome_mkt)
        if not isinstance(salvo, dict) or salvo.get("preco") != atual["preco"]:
            return True
        if "indicado" not in salvo:
            return True

    for nome_mkt in MARKETPLACES:
        if nome_mkt not in atuais and nome_mkt in salvos:
            return True
    return False


def contar_desatualizados():
    """Quantos produtos salvos estão com preços desatualizados."""
    quantidade = 0
    for produto in carregar_produtos():
        if produto_desatualizado(produto):
            quantidade += 1
    return quantidade


def recalcular_produtos():
    """Refaz os preços dos produtos desatualizados, com as taxas atuais.

    O custo, a taxa e a margem de cada produto NÃO mudam: só o campo
    "resultados" é refeito. Cada produto recalculado ganha a data do
    recálculo e uma linha no histórico. Marketplaces que foram removidos
    deixam de aparecer nos preços salvos.

    Retorna:
        (sucesso, quantidade): sucesso=False se não foi possível gravar o arquivo.
    """
    lista = carregar_produtos()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    quantidade = 0

    for posicao, produto in enumerate(lista):
        if not produto_desatualizado(produto):
            continue
        novo = dict(produto)  # cópia: o original só é trocado no final
        novo["resultados"] = calcular_resultados_produto(
            produto["custo"], produto["taxa_usuario"], produto["margem"]
        )
        novo["data_recalculo"] = agora
        historico = list(produto.get("historico", []))
        historico.append({"data": agora, "campo": "Preços",
                          "de": "desatualizados", "para": "recalculados"})
        novo["historico"] = historico[-50:]
        lista[posicao] = novo
        quantidade += 1

    if quantidade == 0:
        return True, 0
    try:
        salvar_produtos(lista)
    except OSError:
        return False, 0
    return True, quantidade


# ── Relatório de todos os produtos ──
# O relatório SEMPRE usa as taxas de hoje (não os preços salvos), então nunca
# sai errado. Ele só avisa quantos produtos salvos estão desatualizados.
# "Mais competitivo" = o marketplace com MENOR preço final para o cliente:
# com a mesma margem em %, quanto menor a taxa, menor o preço.

PASTA_RELATORIOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatorios")


def calcular_linha_relatorio(indice, produto):
    """Monta os dados de UM produto para o relatório.

    Retorna:
        dict com: numero, produto, resultados (taxas de hoje), competitivo
        (nome do marketplace de menor preço ou None), lucro_competitivo,
        retorno (lucro ÷ custo no mais competitivo) e desatualizado (bool).
    """
    resultados = calcular_resultados_produto(produto["custo"], produto["taxa_usuario"],
                                             produto["margem"])
    competitivo = None
    for nome_mkt, res in resultados.items():
        if competitivo is None or res["preco"] < resultados[competitivo]["preco"]:
            competitivo = nome_mkt

    lucro = retorno = None
    if competitivo is not None:
        lucro = resultados[competitivo]["lucro"]
        retorno = lucro / produto["custo"]

    return {
        "numero": indice + 1,
        "produto": produto,
        "resultados": resultados,
        "competitivo": competitivo,
        "lucro_competitivo": lucro,
        "retorno": retorno,
        "desatualizado": produto_desatualizado(produto, resultados),
    }


def _chave_retorno(linha):
    return linha["retorno"]


def montar_relatorio():
    """Reúne todos os produtos salvos e calcula o resumo do relatório.

    Retorna:
        dict com "linhas" (uma por produto) e "resumo" (totais e destaques).
    """
    linhas = []
    for indice, produto in enumerate(carregar_produtos()):
        linhas.append(calcular_linha_relatorio(indice, produto))

    com_retorno = [linha for linha in linhas if linha["retorno"] is not None]

    contagem = {}
    for linha in com_retorno:
        nome_mkt = linha["competitivo"]
        contagem[nome_mkt] = contagem.get(nome_mkt, 0) + 1

    total = len(linhas)
    resumo = {
        "total": total,
        "custo_total": sum(linha["produto"]["custo"] for linha in linhas),
        "margem_media": (sum(linha["produto"]["margem"] for linha in linhas) / total
                         if total else 0),
        "lucro_medio": (sum(linha["lucro_competitivo"] for linha in com_retorno)
                        / len(com_retorno) if com_retorno else None),
        "maior_retorno": max(com_retorno, key=_chave_retorno) if com_retorno else None,
        "menor_retorno": min(com_retorno, key=_chave_retorno) if com_retorno else None,
        "desatualizados": sum(1 for linha in linhas if linha["desatualizado"]),
        "marketplaces": list(MARKETPLACES.keys()),
        "contagem_competitivo": contagem,
    }
    return {"linhas": linhas, "resumo": resumo}


def _numero_br(valor, casas=2):
    """Número com vírgula decimal, como o Excel brasileiro espera. 49.9 → '49,90'."""
    return f"{valor:.{casas}f}".replace(".", ",")


def _texto_seguro_csv(texto):
    """Impede que o Excel trate um texto como fórmula (ex.: nome começando com '=')."""
    texto = str(texto)
    if texto[:1] in ("=", "+", "-", "@"):
        return "'" + texto
    return texto


def exportar_relatorio_csv(relatorio, caminho):
    """Grava o relatório em CSV (separado por ';', abre direto no Excel)."""
    marketplaces = relatorio["resumo"]["marketplaces"]

    cabecalho_csv = ["Nº", "Produto", "Fornecedor", "Custo (R$)",
                     "Taxa adicional (%)", "Margem desejada (%)"]
    for nome_mkt in marketplaces:
        cabecalho_csv += [f"{nome_mkt} - preço ideal (R$)",
                          f"{nome_mkt} - preço indicado (R$)",
                          f"{nome_mkt} - lucro no indicado (R$)"]
    cabecalho_csv += ["Marketplace mais competitivo", "Retorno lucro/custo (%)",
                      "Salvo em", "Preços salvos"]

    # utf-8-sig: o Excel reconhece os acentos; newline="": evita linhas em branco
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(cabecalho_csv)

        for linha in relatorio["linhas"]:
            prod = linha["produto"]
            valores = [linha["numero"], _texto_seguro_csv(prod["nome"]),
                       _texto_seguro_csv(prod["fornecedor"]), _numero_br(prod["custo"]),
                       _numero_br(prod["taxa_usuario"] * 100, 1),
                       _numero_br(prod["margem"] * 100, 1)]
            for nome_mkt in marketplaces:
                res = linha["resultados"].get(nome_mkt)
                if res:
                    valores += [_numero_br(res["preco"]),
                                _numero_br(res["indicado"]["preco"]),
                                _numero_br(res["indicado"]["lucro"])]
                else:
                    valores += ["", "", ""]  # cálculo impossível neste marketplace
            valores += [linha["competitivo"] or "",
                        _numero_br(linha["retorno"] * 100, 1) if linha["retorno"] is not None else "",
                        prod.get("data", ""),
                        "desatualizados" if linha["desatualizado"] else "atualizados"]
            escritor.writerow(valores)


CSS_RELATORIO = """
body { font-family: Segoe UI, Arial, sans-serif; margin: 32px; color: #1c2430; background: #fff; }
h1 { margin: 0 0 4px; color: #0b6b3a; }
h2 { margin-top: 32px; border-bottom: 2px solid #0b6b3a; padding-bottom: 4px; }
.sub { color: #5b6672; margin: 0 0 20px; }
.aviso { background: #fff4d6; border-left: 5px solid #e0a100; padding: 10px 14px; margin: 16px 0; }
.kpis { display: flex; flex-wrap: wrap; gap: 12px; }
.kpi { flex: 1 1 170px; background: #f2f7f4; border-radius: 8px; padding: 12px 16px; }
.kpi b { display: block; font-size: 1.35em; color: #0b6b3a; }
.kpi span { color: #5b6672; font-size: 0.85em; }
.tabela { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 0.9em; }
th { background: #0b6b3a; color: #fff; text-align: left; padding: 8px; }
td { border-bottom: 1px solid #dde3e0; padding: 7px 8px; vertical-align: top; }
tr:nth-child(even) td { background: #f8faf9; }
small { color: #5b6672; }
th small { color: #cfe8d8; font-weight: normal; }
.destaque { color: #0b6b3a; font-weight: bold; }
.velho { color: #b06a00; }
.nota { color: #5b6672; font-size: 0.85em; }
@media print { body { margin: 12px; } }
"""


def exportar_relatorio_html(relatorio, caminho):
    """Grava o relatório como uma página HTML (abre no navegador e pode virar PDF)."""
    esc = html.escape  # protege a página contra textos com < > & digitados pelo usuário
    resumo = relatorio["resumo"]
    marketplaces = resumo["marketplaces"]
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    def cartao(valor, rotulo):
        return f'<div class="kpi"><b>{esc(valor)}</b><span>{esc(rotulo)}</span></div>'

    cartoes = [
        cartao(str(resumo["total"]), "produtos salvos"),
        cartao(formatar_moeda(resumo["custo_total"]), "investimento total (custos)"),
        cartao(formatar_percentual(resumo["margem_media"]), "margem média desejada"),
        cartao(formatar_moeda(resumo["lucro_medio"]) if resumo["lucro_medio"] is not None else "—",
               "lucro médio por unidade"),
    ]
    melhor = resumo["maior_retorno"]
    if melhor:
        cartoes.append(cartao(formatar_percentual(melhor["retorno"]),
                              f"maior retorno: {melhor['produto']['nome']}"))

    aviso = ""
    if resumo["desatualizados"]:
        aviso = (f'<div class="aviso">⚠ {resumo["desatualizados"]} produto(s) têm preços '
                 f'salvos desatualizados no sistema. Os valores deste relatório já usam as '
                 f'taxas atuais. Use "Recalcular preços" no FLUXO para atualizar os salvos.</div>')

    # ── Tabela principal: todos os produtos ──
    cab = ["Nº", "Produto", "Fornecedor", "Custo", "Taxa", "Margem"]
    cabecalho_html = "".join(f"<th>{c}</th>" for c in cab)
    for nome_mkt in marketplaces:
        cabecalho_html += f"<th>{esc(nome_mkt)}<br><small>ideal / indicado</small></th>"
    cabecalho_html += "<th>Mais competitivo</th><th>Retorno</th>"

    corpo = ""
    for linha in relatorio["linhas"]:
        prod = linha["produto"]
        velho = ' <span class="velho" title="Preços salvos desatualizados">⚠</span>' if linha["desatualizado"] else ""
        corpo += (f"<tr><td>{linha['numero']}{velho}</td><td>{esc(prod['nome'])}</td>"
                  f"<td>{esc(prod['fornecedor'])}</td><td>{formatar_moeda(prod['custo'])}</td>"
                  f"<td>{formatar_percentual(prod['taxa_usuario'])}</td>"
                  f"<td>{formatar_percentual(prod['margem'])}</td>")
        for nome_mkt in marketplaces:
            res = linha["resultados"].get(nome_mkt)
            if res:
                corpo += (f"<td>{formatar_moeda(res['preco'])}<br>"
                          f"<b>{formatar_moeda(res['indicado']['preco'])}</b></td>")
            else:
                corpo += "<td>—</td>"
        retorno = formatar_percentual(linha["retorno"]) if linha["retorno"] is not None else "—"
        corpo += f"<td>{esc(linha['competitivo'] or '—')}</td><td>{retorno}</td></tr>"

    # ── Ranking por retorno ──
    ranking = sorted([l for l in relatorio["linhas"] if l["retorno"] is not None],
                     key=_chave_retorno, reverse=True)
    corpo_ranking = ""
    for posicao, linha in enumerate(ranking, 1):
        prod = linha["produto"]
        corpo_ranking += (f"<tr><td>{posicao}º</td><td>{esc(prod['nome'])}</td>"
                          f"<td>{esc(linha['competitivo'])}</td>"
                          f"<td>{formatar_moeda(linha['lucro_competitivo'])}</td>"
                          f'<td class="destaque">{formatar_percentual(linha["retorno"])}</td></tr>')

    pagina = (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Relatório de produtos - FLUXO</title><style>' + CSS_RELATORIO + '</style></head><body>'
        '<h1>Relatório de produtos — FLUXO</h1>'
        f'<p class="sub">Gerado em {agora} • Marketplaces: {esc(", ".join(marketplaces))}</p>'
        + aviso +
        '<div class="kpis">' + "".join(cartoes) + '</div>'
        '<h2>Todos os produtos</h2><div class="tabela"><table>'
        f'<tr>{cabecalho_html}</tr>{corpo}</table></div>'
        '<h2>Ranking por retorno</h2><div class="tabela"><table>'
        '<tr><th>Posição</th><th>Produto</th><th>Marketplace</th><th>Lucro por unidade</th>'
        f'<th>Retorno (lucro ÷ custo)</th></tr>{corpo_ranking}</table></div>'
        '<h2>Como ler este relatório</h2>'
        '<p class="nota"><b>Preço ideal</b>: resultado exato da conta, que garante a margem '
        'desejada depois de descontar as taxas. <b>Preço indicado</b>: o próximo preço '
        'terminado em ,90 igual ou acima do ideal (a margem real fica igual ou maior). '
        '<b>Mais competitivo</b>: marketplace com o menor preço final para o cliente. '
        '<b>Retorno</b>: lucro por unidade dividido pelo custo, no marketplace mais competitivo.</p>'
        '</body></html>'
    )
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(pagina)


def exportar_relatorio(relatorio):
    """Salva o relatório em CSV e HTML na pasta "relatorios".

    Os arquivos ganham data e hora no nome, então relatórios antigos
    nunca são sobrescritos.

    Retorna:
        (caminho_csv, caminho_html)

    Levanta OSError se não for possível gravar (pasta sem permissão, disco cheio...).
    """
    os.makedirs(PASTA_RELATORIOS, exist_ok=True)
    carimbo = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    caminho_csv = os.path.join(PASTA_RELATORIOS, f"relatorio_{carimbo}.csv")
    caminho_html = os.path.join(PASTA_RELATORIOS, f"relatorio_{carimbo}.html")
    exportar_relatorio_csv(relatorio, caminho_csv)
    exportar_relatorio_html(relatorio, caminho_html)
    return caminho_csv, caminho_html


def abrir_arquivo(caminho):
    """Abre um arquivo no programa padrão do computador (navegador, Excel...).

    Retorna True se conseguiu pedir a abertura, False caso contrário.
    """
    try:
        if hasattr(os, "startfile"):      # Windows
            os.startfile(caminho)
            return True
        return webbrowser.open("file://" + os.path.abspath(caminho))
    except OSError:
        return False

# ── Módulo de Feedback (envio via HTTPS e notificação no Windows) ──

# Link do Formspree que encaminha o feedback para o e-mail do grupo
URL_ENVIO_FEEDBACK = os.environ.get(
    "FLUXO_WEBHOOK_URL", "https://formspree.io/f/xqpqdajb"
).strip()

TIMEOUT_FEEDBACK = 15  # Tempo máximo de espera pela resposta do servidor

# Arquivo de segurança para guardar o feedback se o computador estiver sem internet
ARQUIVO_FEEDBACKS_PENDENTES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "feedbacks_pendentes.json"
)


def notificar_windows(titulo, mensagem):
    """Mostra o aviso de sucesso ou falha na barra de tarefas do Windows."""
    if os.name != "nt":
        return False

    try:
        from winotify import Notification
        Notification(
            app_id="FLUXO",
            title=titulo,
            msg=mensagem,
            duration="short",
        ).show()
        return True
    except Exception:
        pass

    try:
        from plyer import notification
        notification.notify(
            title=titulo,
            message=mensagem,
            app_name="FLUXO",
            timeout=5,
        )
        return True
    except Exception:
        return False


def _salvar_feedback_pendente(registro):
    """Guarda o feedback em JSON para o usuário não perder o que escreveu."""
    try:
        pendentes = []
        if os.path.exists(ARQUIVO_FEEDBACKS_PENDENTES):
            try:
                with open(ARQUIVO_FEEDBACKS_PENDENTES, "r", encoding="utf-8") as arq:
                    dados = json.load(arq)
                if isinstance(dados, list):
                    pendentes = dados
            except (json.JSONDecodeError, OSError):
                pendentes = []

        pendentes.append(registro)
        with open(ARQUIVO_FEEDBACKS_PENDENTES, "w", encoding="utf-8") as arq:
            json.dump(pendentes, arq, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def _eh_webhook_discord(url):
    """Verifica se o link configurado é de um Webhook do Discord."""
    return "discord.com/api/webhooks" in url or "discordapp.com/api/webhooks" in url


def _montar_dados_feedback(registro, url):
    """Organiza os dados no formato que o Formspree ou o Discord espera."""
    if _eh_webhook_discord(url):
        return {
            "username": "FLUXO Feedback",
            "embeds": [
                {
                    "title": f"Novo feedback de {registro['nome']}",
                    "description": registro["mensagem"],
                    "color": 3066993,
                    "fields": [
                        {
                            "name": "Contato",
                            "value": registro["contato"] or "Não informado",
                            "inline": True,
                        },
                        {
                            "name": "Data",
                            "value": registro["data"],
                            "inline": True,
                        },
                    ],
                }
            ],
        }

    return {
        "nome": registro["nome"],
        "contato": registro["contato"] or "Não informado",
        "data": registro["data"],
        "mensagem": registro["mensagem"],
        "_subject": f"[FLUXO] Novo feedback de {registro['nome']}",
    }


def _enviar_feedback_https(registro, url):
    """Faz o envio pela porta 443 (HTTPS), evitando bloqueios de rede."""
    payload = _montar_dados_feedback(registro, url)
    dados_bytes = json.dumps(payload).encode("utf-8")

    requisicao = urllib.request.Request(
        url,
        data=dados_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "FLUXO-Precificador/1.0",
        },
    )

    contexto = ssl.create_default_context()
    with urllib.request.urlopen(
        requisicao, timeout=TIMEOUT_FEEDBACK, context=contexto
    ) as resp:
        return 200 <= resp.status < 300


def _tratar_falha_feedback(registro, erro):
    """Salva localmente se der erro e avisa na barra de tarefas."""
    if _salvar_feedback_pendente(registro):
        erro += " Seu feedback foi guardado em feedbacks_pendentes.json."
        notificar_windows(
            "FLUXO - Envio não concluído",
            "Não foi possível enviar agora. O feedback foi guardado no computador.",
        )
    else:
        notificar_windows(
            "FLUXO - Falha no envio",
            "Não foi possível enviar o feedback.",
        )
    return False, erro


def enviar_feedback(mensagem, nome="Anônimo", contato=""):
    """Envia o feedback e dispara a notificação correspondente no Windows."""
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    registro = {
        "nome": nome or "Anônimo",
        "contato": contato,
        "data": data,
        "mensagem": mensagem,
    }

    if not URL_ENVIO_FEEDBACK or "COLE_SUA_URL_AQUI" in URL_ENVIO_FEEDBACK:
        erro = "URL de envio não configurada no código."
        return _tratar_falha_feedback(registro, erro)

    try:
        enviado = _enviar_feedback_https(registro, URL_ENVIO_FEEDBACK)
    except urllib.error.HTTPError as e:
        erro = f"O servidor recusou o envio (HTTP {e.code}). Confira a URL."
    except urllib.error.URLError as e:
        erro = f"Sem conexão com a internet ou servidor indisponível ({e.reason})."
    except OSError as e:
        erro = f"Falha na comunicação: {e}"
    else:
        if enviado:
            notificar_windows(
                "FLUXO - Feedback enviado",
                "Seu feedback foi enviado com sucesso. Obrigado!",
            )
            return True, ""
        erro = "O servidor não confirmou o recebimento."

    return _tratar_falha_feedback(registro, erro)


# ╔══════════════════════════════════════════════════════════════╗
# ║           PARTE 4 - INTERFACE DO USUÁRIO                    ║
# ║  Menus, telas e navegação. Aqui é onde tudo se junta:       ║
# ║  o usuário interage, o programa calcula e exibe resultados. ║
# ╚══════════════════════════════════════════════════════════════╝

def exibir_logo():
    """Exibe a logo ASCII do FLUXO no topo da tela."""
    logo = f"""
{VERDE}{BOLD}
    ███████╗██╗     ██╗   ██╗██╗  ██╗ ██████╗
    ██╔════╝██║     ██║   ██║╚██╗██╔╝██╔═══██╗
    █████╗  ██║     ██║   ██║ ╚███╔╝ ██║   ██║
    ██╔══╝  ██║     ██║   ██║ ██╔██╗ ██║   ██║
    ██║     ███████╗╚██████╔╝██╔╝ ██╗╚██████╔╝
    ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
{RESET}"""
    print(logo)
    print(f"{DIM}{'Precificador de Produtos para Marketplaces'.center(LARGURA)}{RESET}")
    linha()


def exibir_card_marketplace(nome_mkt, nome_produto, fornecedor, resultado, indicado=None):
    """Exibe um card colorido com o resultado de um marketplace.

    Cada marketplace tem sua cor característica, imitando os cards
    do site original (TikTok=preto, Mercado Livre=amarelo, etc.)

    Args:
        nome_mkt (str):       Nome do marketplace.
        nome_produto (str):   Nome do produto.
        fornecedor (str):     Nome do fornecedor.
        resultado (dict):     Dicionário com "preco" e "lucro".
        indicado (dict|None): Preço indicado (de calcular_preco_indicado), se houver.
    """
    dados_mkt = MARKETPLACES[nome_mkt]
    bg   = dados_mkt["cor_fundo"]
    fg   = dados_mkt["cor_texto"]
    icon = dados_mkt["icone"]

    if resultado is None:
        # Margem + taxa inválidas
        print(f"  {bg}{fg} {icon} {nome_mkt:<16} │ Margem + taxa inválidas (≥100%) {RESET}")
        return

    preco_fmt = formatar_moeda(resultado["preco"])
    lucro_fmt = formatar_moeda(resultado["lucro"])

    # Monta o card com cores e informações
    print(f"  {bg}{fg}{'─' * (LARGURA - 4)}{RESET}")
    print(f"  {bg}{fg}  {icon} {BOLD}{nome_mkt}{RESET}{bg}{fg}{''.rjust(LARGURA - len(nome_mkt) - 8)}{RESET}")
    print(f"  {bg}{fg}  {nome_produto} │ {fornecedor}{''.rjust(LARGURA - len(nome_produto) - len(fornecedor) - 9)}{RESET}")
    print(f"  {bg}{fg}  Valor Ideal: {preco_fmt}{''.rjust(LARGURA - len(preco_fmt) - 20)}{RESET}")
    print(f"  {bg}{fg}  Lucro:       {lucro_fmt}{''.rjust(LARGURA - len(lucro_fmt) - 20)}{RESET}")
    if indicado:
        texto = (f"  Preço indicado: {formatar_moeda(indicado['preco'])} "
                 f"(margem real {formatar_percentual(indicado['margem'])})")
        print(f"  {bg}{fg}{BOLD}{texto}{RESET}{bg}{fg}{''.rjust(max(0, LARGURA - 4 - len(texto)))}{RESET}")
    print(f"  {bg}{fg}{'─' * (LARGURA - 4)}{RESET}")
    print()


def selecionar_marketplaces():
    """Permite ao usuário escolher quais marketplaces quer ver.

    Se o usuário digitar algo inválido (número fora da lista, letras),
    o programa explica o erro e pergunta de novo, em vez de ignorar.
    ENTER em branco cancela e devolve uma lista vazia.

    Retorna:
        selecionados (list): Lista com os nomes dos marketplaces escolhidos.
    """
    subcabecalho("Selecione os Marketplaces")
    print()

    nomes = list(MARKETPLACES.keys())
    for i, nome in enumerate(nomes, 1):
        dados = MARKETPLACES[nome]
        taxa_fmt = formatar_percentual(dados["taxa_fixa"])  # mostra casas decimais (ex.: 12,5%)
        print(f"  {CIANO}[{i}]{RESET} {dados['icone']} {nome:<16} {DIM}(taxa fixa: {taxa_fmt}){RESET}")

    print(f"  {CIANO}[A]{RESET} 📊 Todos os marketplaces")
    print()

    while True:
        escolha = input(f"  {BRANCO}Escolha (ex: 1,3 ou A para todos): {RESET}").strip().upper()

        if not escolha:
            return []  # ENTER em branco: cancela
        if escolha == "A":
            return nomes  # Retorna todos

        selecionados = []
        invalidos = []
        for num in escolha.split(","):
            num = num.strip()
            if not num:
                continue
            if num.isdecimal() and 1 <= int(num) <= len(nomes):
                nome = nomes[int(num) - 1]
                if nome not in selecionados:  # "1,1" não repete o marketplace
                    selecionados.append(nome)
            else:
                invalidos.append(num)

        if invalidos:
            exibir_erro(f"Opção inválida: {', '.join(invalidos)}. "
                        f"Use os números da lista (ex.: 1,3) ou A.")
        elif selecionados:
            return selecionados
        else:
            exibir_erro("Escolha pelo menos um marketplace.")


def tela_precificar():
    """Tela principal: preencher dados e calcular preço ideal.

    Fluxo:
    1. Usuário digita nome, fornecedor, custo, taxa e margem
       (cada campo é validado na hora: se errar, só aquele campo é pedido de novo)
    2. Seleciona os marketplaces
    3. O programa calcula e exibe os cards com o preço ideal e o preço indicado
    4. Opção de salvar o produto
    """
    limpar_tela()
    exibir_logo()
    cabecalho("PRECIFICAR PRODUTO")
    print()

    # ── Coleta de dados (cada campo só avança quando está válido) ──
    subcabecalho("Dados do Produto")
    print()
    nome       = ler_texto("Nome do produto", tamanho_max=40)
    fornecedor = ler_texto("Fornecedor", tamanho_max=30)
    print()

    subcabecalho("Dados Financeiros")
    print()
    custo  = ler_numero("Custo de aquisição (R$)", 0, 1000000, minimo_incluso=False)
    taxa   = ler_numero("Sua taxa adicional (%)", 0, 99, fator=100)    # % → decimal
    margem = ler_numero("Margem de lucro desejada (%)", 0, 99, fator=100)  # % → decimal

    # ── Seleção de marketplaces ──
    marketplaces_escolhidos = selecionar_marketplaces()

    if not marketplaces_escolhidos:
        exibir_erro("Nenhum marketplace selecionado!")
        pausar()
        return

    # ── Cálculo ──
    todos_resultados = calcular_todos_marketplaces(custo, taxa, margem)
    # Mesmos resultados + preço indicado (só dos marketplaces onde o cálculo é possível)
    resultados_completos = calcular_resultados_produto(custo, taxa, margem)

    # ── Exibição dos resultados ──
    limpar_tela()
    exibir_logo()
    cabecalho("RESULTADO DA PRECIFICAÇÃO")
    print()
    print(f"  {BOLD}{BRANCO}Produto:{RESET} {nome}  │  {BOLD}{BRANCO}Fornecedor:{RESET} {fornecedor}")
    print(f"  {BOLD}{BRANCO}Custo:{RESET}   {formatar_moeda(custo)}  │  {BOLD}{BRANCO}Taxa:{RESET} {formatar_percentual(taxa)}  │  {BOLD}{BRANCO}Margem:{RESET} {formatar_percentual(margem)}")
    print()
    linha()
    print()

    for mkt in marketplaces_escolhidos:
        indicado = resultados_completos.get(mkt, {}).get("indicado")
        exibir_card_marketplace(mkt, nome, fornecedor, todos_resultados[mkt], indicado)

    # ── Opção de salvar ──
    if confirmar("Deseja salvar este produto?"):
        if existe_duplicado(nome, fornecedor):
            exibir_mensagem("Já existe um produto com esse mesmo nome e fornecedor.")
            if not confirmar("Salvar mesmo assim?"):
                exibir_mensagem("Produto não salvo.")
                pausar()
                return

        produto = {
            "nome": nome,
            "fornecedor": fornecedor,
            "custo": custo,
            "taxa_usuario": taxa,
            "margem": margem,
            # Salva os resultados de TODOS os marketplaces (não só os selecionados)
            "resultados": resultados_completos,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }

        try:
            adicionar_produto(produto)
            exibir_sucesso(f"Produto '{nome}' salvo com sucesso!")
        except OSError:
            exibir_erro("Não foi possível salvar o produto. Verifique se a pasta "
                        "do programa permite escrita.")

    pausar()


def tela_produtos_salvos():
    """Tela que lista todos os produtos salvos e permite excluir.

    Mostra uma tabela formatada com:
    - Nº do produto
    - Nome | Fornecedor
    - Preço ideal em cada marketplace
    - Data de cadastro
    """
    limpar_tela()
    exibir_logo()
    cabecalho("PRODUTOS SALVOS")
    print()

    produtos = carregar_produtos()

    if not produtos:
        exibir_mensagem("Nenhum produto salvo ainda.")
        pausar()
        return

    avisar_desatualizados()

    # ── Exibe cada produto ──
    for i, prod in enumerate(produtos):
        aviso = f"  {AMARELO}⚠ desatualizado{RESET}" if produto_desatualizado(prod) else ""
        print(f"  {AZUL}┌{'─' * (LARGURA - 6)}┐{RESET}")
        print(f"  {AZUL}│{RESET} {BOLD}{CIANO}#{i+1}{RESET}  {BOLD}{BRANCO}{prod['nome']}{RESET} │ {prod['fornecedor']}{aviso}")
        print(f"  {AZUL}│{RESET}  {DIM}Custo: {formatar_moeda(prod['custo'])}  │  "
              f"Taxa: {prod['taxa_usuario']*100:.1f}%  │  "
              f"Margem: {prod['margem']*100:.1f}%{RESET}")

        # Mostra preço para cada marketplace salvo
        if "resultados" in prod:
            for mkt_nome, res in prod["resultados"].items():
                icone = MARKETPLACES.get(mkt_nome, {}).get("icone", "•")
                print(f"  {AZUL}│{RESET}  {icone} {mkt_nome:<16} → "
                      f"{VERDE}{formatar_moeda(res['preco'])}{RESET}  "
                      f"(lucro: {AMARELO}{formatar_moeda(res['lucro'])}{RESET}){formatar_indicado(res)}")

        print(f"  {AZUL}│{RESET}  {DIM}Salvo em: {prod.get('data', 'N/A')}{RESET}")
        print(f"  {AZUL}└{'─' * (LARGURA - 6)}┘{RESET}")
        print()

    # ── Opção de excluir ──
    linha()
    print(f"\n  {BRANCO}Digite o número do produto para excluir, ou 0 para voltar:{RESET}")
    escolha = input(f"  {CIANO}│ Opção: {RESET}").strip()

    if escolha.isdigit() and int(escolha) > 0:
        indice = int(escolha) - 1
        if indice >= len(produtos):
            exibir_erro("Número inválido.")
        elif confirmar(f"Excluir '{produtos[indice]['nome']}' definitivamente?"):
            if excluir_produto(indice):
                exibir_sucesso("Produto excluído com sucesso!")
            else:
                exibir_erro("Não foi possível excluir o produto.")
        else:
            exibir_mensagem("Exclusão cancelada.")
    elif escolha != "0":
        exibir_erro("Opção inválida.")

    pausar()


# ── Busca, detalhes e edição de produtos salvos ──

# Nomes amigáveis dos critérios de ordenação (usados na tela "Listar todos")
NOMES_ORDEM = {
    "cadastro": "ordem de cadastro",
    "nome":     "nome (A-Z)",
    "custo":    "menor custo primeiro",
    "recentes": "mais recentes primeiro",
}


def exibir_tabela_produtos(pares):
    """Mostra uma tabela resumida de produtos.

    Args:
        pares (list): Lista de tuplas (indice, produto). O número mostrado
                      (#) é o mesmo da tela "Produtos salvos".
    """
    print(f"  {DIM}{'Nº':<5}{'Produto':<22}{'Fornecedor':<16}{'Custo':>12}{RESET}")
    print(f"  {AZUL}{'─' * (LARGURA - 6)}{RESET}")
    for indice, prod in pares:
        marca = "*" if prod.get("data_edicao") else " "
        numero = "#" + str(indice + 1)
        print(f"  {CIANO}{numero:<5}{RESET}"
              f"{BRANCO}{cortar(prod['nome'], 21):<22}{RESET}"
              f"{cortar(prod['fornecedor'], 15):<16}"
              f"{VERDE}{formatar_moeda(prod['custo']):>12}{RESET} {AMARELO}{marca}{RESET}")


def escolher_produto(pares, titulo, permite_ordenar=False):
    """Mostra a tabela de produtos e pede qual deles abrir.

    Args:
        pares (list):            Lista de tuplas (indice, produto).
        titulo (str):            Título mostrado acima da tabela.
        permite_ordenar (bool):  Se True, o usuário também pode digitar O
                                 para mudar a ordem da lista.

    Retorna:
        - o índice (int) do produto escolhido;
        - "ordem" se o usuário pediu para mudar a ordenação;
        - None se o usuário quiser voltar.
    """
    subcabecalho(titulo)
    print()
    exibir_tabela_produtos(pares)
    print(f"\n  {DIM}* = produto que já foi editado{RESET}")

    numeros_validos = [indice + 1 for indice, _ in pares]
    pergunta = "Número do produto para abrir"
    pergunta += ", O para mudar a ordem" if permite_ordenar else ""
    pergunta += " (ENTER volta)"

    while True:
        escolha = input(f"\n  {BRANCO}{pergunta}: {RESET}").strip().lstrip("#")
        if not escolha:
            return None
        if permite_ordenar and escolha.upper() == "O":
            return "ordem"
        if escolha.isdigit() and int(escolha) in numeros_validos:
            return int(escolha) - 1
        exibir_erro("Número fora da lista. Digite um dos números da tabela.")


def exibir_ficha_produto(indice, prod):
    """Mostra todos os dados de um produto salvo, incluindo o histórico."""
    print(f"  {AZUL}┌{'─' * (LARGURA - 6)}┐{RESET}")
    print(f"  {AZUL}│{RESET} {BOLD}{CIANO}#{indice + 1}{RESET}  {BOLD}{BRANCO}{prod['nome']}{RESET}")
    print(f"  {AZUL}│{RESET}  {DIM}Fornecedor:{RESET} {prod['fornecedor']}")
    print(f"  {AZUL}│{RESET}  {DIM}Custo:{RESET} {formatar_moeda(prod['custo'])}  │  "
          f"{DIM}Taxa:{RESET} {formatar_percentual(prod['taxa_usuario'])}  │  "
          f"{DIM}Margem:{RESET} {formatar_percentual(prod['margem'])}")

    for mkt_nome, res in prod.get("resultados", {}).items():
        icone = MARKETPLACES.get(mkt_nome, {}).get("icone", "•")
        print(f"  {AZUL}│{RESET}  {icone} {mkt_nome:<16} → "
              f"{VERDE}{formatar_moeda(res['preco'])}{RESET}  "
              f"(lucro: {AMARELO}{formatar_moeda(res['lucro'])}{RESET}){formatar_indicado(res)}")

    if produto_desatualizado(prod):
        print(f"  {AZUL}│{RESET}  {AMARELO}⚠ Preços desatualizados: use \"Recalcular preços\"{RESET}")
    print(f"  {AZUL}│{RESET}  {DIM}Salvo em: {prod.get('data', 'N/A')}{RESET}")
    if prod.get("data_edicao"):
        print(f"  {AZUL}│{RESET}  {DIM}Última edição: {prod['data_edicao']}{RESET}")
    if prod.get("data_recalculo"):
        print(f"  {AZUL}│{RESET}  {DIM}Preços recalculados em: {prod['data_recalculo']}{RESET}")
    print(f"  {AZUL}└{'─' * (LARGURA - 6)}┘{RESET}")

    historico = prod.get("historico", [])
    if historico:
        subcabecalho("Últimas alterações")
        for item in reversed(historico[-5:]):  # as 5 mais recentes, da mais nova para a mais antiga
            print(f"  {DIM}{item.get('data', '')}{RESET}  {item.get('campo', '?')}: "
                  f"{item.get('de', '?')} → {VERDE}{item.get('para', '?')}{RESET}")


def exibir_comparacao_edicao(original, rascunho):
    """Mostra os campos e os preços do produto durante a edição.

    Campos alterados aparecem como "antes → depois" com um *, e os preços
    de cada marketplace são recalculados na hora (prévia), sem salvar nada.
    """
    subcabecalho("Dados do produto")
    print()
    for numero, (campo, rotulo) in enumerate(CAMPOS_PRODUTO.items(), 1):
        antes = formatar_campo(campo, original[campo])
        depois = formatar_campo(campo, rascunho[campo])
        if original[campo] != rascunho[campo]:
            print(f"  {CIANO}[{numero}]{RESET} {rotulo:<20} {DIM}{antes}{RESET} → "
                  f"{AMARELO}{depois}  *{RESET}")
        else:
            print(f"  {CIANO}[{numero}]{RESET} {rotulo:<20} {BRANCO}{depois}{RESET}")

    subcabecalho("Preço ideal por marketplace (prévia)")
    print()
    novos = calcular_resultados_produto(rascunho["custo"], rascunho["taxa_usuario"],
                                        rascunho["margem"])
    for nome_mkt, dados in MARKETPLACES.items():
        antigo = original.get("resultados", {}).get(nome_mkt)
        novo = novos.get(nome_mkt)
        if novo is None:
            print(f"  {dados['icone']} {nome_mkt:<16} {VERMELHO}inviável (taxa + margem ≥ 100%){RESET}")
            continue

        texto_novo = formatar_moeda(novo["preco"])
        texto_antigo = formatar_moeda(antigo["preco"]) if antigo else "—"
        if texto_antigo != texto_novo:
            preco = f"{DIM}{texto_antigo}{RESET} → {AMARELO}{texto_novo}{RESET}"
        else:
            preco = f"{VERDE}{texto_novo}{RESET}"
        print(f"  {dados['icone']} {nome_mkt:<16} {preco}  "
              f"{DIM}(lucro: {formatar_moeda(novo['lucro'])}){RESET}")


def editar_campo(rascunho, campo):
    """Pede o novo valor de UM campo e atualiza o rascunho.

    O rascunho é uma cópia do produto: nada é gravado no arquivo aqui.
    ENTER mantém o valor atual. Valores inválidos são pedidos de novo.
    """
    rotulo = CAMPOS_PRODUTO[campo]
    print(f"\n  {DIM}Digite o novo valor ou apenas ENTER para manter o atual.{RESET}\n")

    if campo == "nome":
        rascunho[campo] = ler_texto(rotulo, rascunho[campo], tamanho_max=40)
    elif campo == "fornecedor":
        rascunho[campo] = ler_texto(rotulo, rascunho[campo], tamanho_max=30)
    elif campo == "custo":
        rascunho[campo] = ler_numero(f"{rotulo} (R$)", 0, 1000000, rascunho[campo],
                                     formatar=formatar_moeda, minimo_incluso=False)
    else:  # taxa_usuario ou margem: digita em %, guarda como decimal
        rascunho[campo] = ler_numero(f"{rotulo} (%)", 0, 99, rascunho[campo],
                                     formatar=formatar_percentual, fator=100)


def salvar_edicao(indice, original, rascunho):
    """Valida, pede confirmação e grava as alterações de um produto.

    Retorna:
        True se as alterações foram salvas (a tela de edição pode fechar),
        False se nada foi salvo (o usuário continua editando).
    """
    alteracoes = listar_alteracoes(original, rascunho)
    if not alteracoes:
        exibir_mensagem("Nenhuma alteração para salvar.")
        pausar()
        return False

    novos = calcular_resultados_produto(rascunho["custo"], rascunho["taxa_usuario"],
                                        rascunho["margem"])
    if not novos:
        exibir_erro("Com esses valores (taxa + margem ≥ 100%) nenhum marketplace "
                    "pode ser calculado. Ajuste a taxa ou a margem.")
        pausar()
        return False

    if existe_duplicado(rascunho["nome"], rascunho["fornecedor"], indice):
        exibir_mensagem("Já existe outro produto com esse mesmo nome e fornecedor.")
        if not confirmar("Salvar mesmo assim?"):
            return False

    subcabecalho("Resumo das alterações")
    print()
    for campo, antes, depois in alteracoes:
        print(f"  • {CAMPOS_PRODUTO[campo]:<20} {DIM}{formatar_campo(campo, antes)}{RESET}"
              f" → {VERDE}{formatar_campo(campo, depois)}{RESET}")
    print()

    if not confirmar("Confirmar e salvar as alterações?"):
        return False

    produto_final = aplicar_alteracoes(original, rascunho, alteracoes)
    if atualizar_produto(indice, produto_final):
        exibir_sucesso("Produto atualizado com sucesso! Os preços foram recalculados.")
        pausar()
        return True

    exibir_erro("Não foi possível gravar as alterações. Verifique se a pasta do "
                "programa permite escrita.")
    pausar()
    return False


def tela_editar_produto(indice):
    """Tela de edição de um produto salvo.

    Fluxo:
    1. O usuário escolhe qual campo alterar (ou edita todos em sequência)
    2. A tela mostra antes → depois e uma prévia dos novos preços
    3. Ao salvar, o sistema pede confirmação, recalcula os preços de
       todos os marketplaces e registra a mudança no histórico
    """
    produtos = carregar_produtos()
    if not 0 <= indice < len(produtos):
        exibir_erro("Produto não encontrado.")
        pausar()
        return

    original = produtos[indice]
    rascunho = dict(original)  # cópia de trabalho: o original só muda ao salvar
    lista_campos = list(CAMPOS_PRODUTO.keys())

    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("EDITAR PRODUTO")
        print()
        exibir_comparacao_edicao(original, rascunho)
        print()
        linha()
        print(f"\n  {DIM}Digite o número do campo que deseja alterar.{RESET}")
        print(f"  {CIANO}[T]{RESET} Editar todos os campos em sequência")
        print(f"  {CIANO}[S]{RESET} Salvar alterações")
        print(f"  {CIANO}[0]{RESET} Cancelar")
        print()

        opcao = input(f"  {BRANCO}Escolha uma opção: {RESET}").strip().upper()

        if opcao.isdigit() and 1 <= int(opcao) <= len(lista_campos):
            editar_campo(rascunho, lista_campos[int(opcao) - 1])
        elif opcao == "T":
            for campo in lista_campos:
                editar_campo(rascunho, campo)
        elif opcao == "S":
            if salvar_edicao(indice, original, rascunho):
                return
        elif opcao == "0":
            if not listar_alteracoes(original, rascunho) or \
                    confirmar("Descartar as alterações feitas?"):
                return
        else:
            exibir_erro("Opção inválida! Tente novamente.")
            pausar()


def tela_detalhe_produto(indice):
    """Mostra a ficha completa de um produto e oferece editar ou excluir."""
    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("DETALHES DO PRODUTO")
        print()

        produtos = carregar_produtos()
        if not 0 <= indice < len(produtos):
            exibir_erro("Produto não encontrado.")
            pausar()
            return

        produto = produtos[indice]
        exibir_ficha_produto(indice, produto)
        print()
        print(f"  {CIANO}[1]{RESET} 📝  Editar dados do produto")
        print(f"  {CIANO}[2]{RESET} 🗑️   Excluir produto")
        print(f"  {CIANO}[0]{RESET} ↩   Voltar")
        print()

        opcao = input(f"  {BRANCO}Escolha uma opção: {RESET}").strip()

        if opcao == "1":
            tela_editar_produto(indice)
        elif opcao == "2":
            print()
            if confirmar(f"Excluir '{produto['nome']}' definitivamente?"):
                if excluir_produto(indice):
                    exibir_sucesso("Produto excluído com sucesso!")
                else:
                    exibir_erro("Não foi possível excluir o produto.")
                pausar()
                return
        elif opcao == "0":
            return
        else:
            exibir_erro("Opção inválida! Tente novamente.")
            pausar()


def tela_busca_produtos():
    """Busca produtos pelo nome ou fornecedor e abre o escolhido."""
    limpar_tela()
    exibir_logo()
    cabecalho("BUSCAR PRODUTO")
    print()
    print(f"  {DIM}Digite parte do nome ou do fornecedor (ex.: fone, ali).")
    print(f"  A busca ignora maiúsculas e acentos.{RESET}\n")

    termo = input_estilizado("Buscar por").strip()
    if not termo:
        exibir_erro("Digite pelo menos uma palavra para buscar.")
        pausar()
        return

    while True:
        # A busca é refeita a cada volta: se o produto foi editado ou
        # excluído, a lista mostrada já aparece atualizada.
        encontrados = buscar_produtos(termo)
        if not encontrados:
            exibir_mensagem(f"Nenhum produto encontrado para '{termo}'.")
            pausar()
            return

        limpar_tela()
        exibir_logo()
        cabecalho("BUSCAR PRODUTO")
        print()
        escolha = escolher_produto(encontrados, f"{len(encontrados)} resultado(s) para '{termo}'")
        if escolha is None:
            return
        tela_detalhe_produto(escolha)


def escolher_ordem(atual):
    """Pergunta como o usuário quer ordenar a lista de produtos.

    Retorna:
        O critério escolhido ("cadastro", "nome", "custo" ou "recentes").
        Se a resposta for inválida, mantém o critério atual.
    """
    opcoes = {"1": "cadastro", "2": "nome", "3": "custo", "4": "recentes"}
    print()
    for numero, criterio in opcoes.items():
        print(f"  {CIANO}[{numero}]{RESET} {NOMES_ORDEM[criterio]}")
    escolha = input(f"\n  {BRANCO}Ordenar por: {RESET}").strip()
    if escolha in opcoes:
        return opcoes[escolha]
    exibir_erro("Opção inválida. A ordem não foi alterada.")
    pausar()
    return atual


def tela_listar_todos():
    """Lista todos os produtos salvos, com opção de ordenar e abrir um deles."""
    criterio = "cadastro"
    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("TODOS OS PRODUTOS")
        print()

        pares = list(enumerate(carregar_produtos()))
        if not pares:
            exibir_mensagem("Nenhum produto salvo.")
            pausar()
            return

        pares = ordenar_produtos(pares, criterio)
        escolha = escolher_produto(pares, f"{len(pares)} produto(s) • ordem: {NOMES_ORDEM[criterio]}",
                                   permite_ordenar=True)
        if escolha is None:
            return
        if escolha == "ordem":
            criterio = escolher_ordem(criterio)
        else:
            tela_detalhe_produto(escolha)


def tela_gerenciar_produtos():
    """Menu de gerenciamento: buscar, listar, abrir, editar e excluir produtos."""
    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("BUSCAR / EDITAR PRODUTOS")
        print()

        total = len(carregar_produtos())
        if total == 0:
            exibir_mensagem("Nenhum produto salvo ainda. "
                            "Precifique e salve um produto primeiro.")
            pausar()
            return

        print(f"  {DIM}{total} produto(s) salvo(s){RESET}\n")
        avisar_desatualizados()
        print(f"  {CIANO}[1]{RESET} 🔎  Buscar por nome ou fornecedor")
        print(f"  {CIANO}[2]{RESET} 📋  Listar todos os produtos")
        print(f"  {CIANO}[3]{RESET} 🔄  Recalcular preços salvos")
        print(f"  {CIANO}[0]{RESET} ↩   Voltar ao menu principal")
        print()
        linha()
        print()

        opcao = input(f"  {BRANCO}Escolha uma opção: {RESET}").strip()

        if opcao == "1":
            tela_busca_produtos()
        elif opcao == "2":
            tela_listar_todos()
        elif opcao == "3":
            tela_recalcular_produtos()
        elif opcao == "0":
            return
        else:
            exibir_erro("Opção inválida! Tente novamente.")
            pausar()


def tela_feedback():
    """Coleta a opinião do usuário no terminal e envia via HTTPS."""
    limpar_tela()
    exibir_logo()
    cabecalho("ENVIE SEU FEEDBACK")
    print(f"\n  {DIM}Sua opinião ajuda a melhorar o FLUXO. Nome e contato são opcionais.{RESET}")

    subcabecalho("Seus Dados")
    print()
    nome = input_estilizado("Seu nome (opcional)").strip() or "Anônimo"
    contato = input_estilizado("E-mail ou WhatsApp para resposta (opcional)").strip()

    subcabecalho("Sua Mensagem")
    print()
    mensagem = ler_texto("Digite seu feedback", tamanho_max=500)
    print()

    if not confirmar("Enviar agora?"):
        exibir_mensagem("Envio cancelado.")
        pausar()
        return

    print(f"\n  {DIM}Enviando...{RESET}")
    ok, erro = enviar_feedback(mensagem, nome=nome, contato=contato)
    if ok:
        exibir_sucesso("Feedback enviado com sucesso! Obrigado pela contribuição.")
    else:
        exibir_erro(erro)

    pausar()


def tela_politica_privacidade():
    """Exibe a Política de Privacidade (texto informativo)."""
    limpar_tela()
    exibir_logo()
    cabecalho("POLÍTICA DE PRIVACIDADE")
    print(f"""
  {BRANCO}A sua privacidade é importante para nós.{RESET}

  {DIM}É política do FLUXO respeitar a sua privacidade em relação
  a qualquer informação sua que possamos coletar.

  • Solicitamos informações pessoais apenas quando realmente
    precisamos delas para lhe fornecer um serviço.

  • Apenas retemos as informações coletadas pelo tempo
    necessário para fornecer o serviço solicitado.

  • Não compartilhamos informações de identificação pessoal
    publicamente ou com terceiros, exceto quando exigido por lei.

  {BOLD}{BRANCO}Compromisso do Usuário:{RESET}{DIM}
  O usuário se compromete a fazer uso adequado dos conteúdos
  e da informação que o FLUXO oferece:
    A) Não se envolver em atividades ilegais;
    B) Não difundir conteúdo prejudicial;
    C) Não causar danos aos sistemas do FLUXO.

  Efetiva a partir de 28 de Abril de 2026.{RESET}
""")
    pausar()


def tela_termos_de_uso():
    """Exibe os Termos de Uso (texto informativo)."""
    limpar_tela()
    exibir_logo()
    cabecalho("TERMOS DE USO")
    print(f"""
  {BRANCO}1. Termos{RESET}
  {DIM}Ao acessar o FLUXO, concorda em cumprir estes termos de
  serviço, todas as leis e regulamentos aplicáveis.{RESET}

  {BRANCO}2. Uso de Licença{RESET}
  {DIM}É concedida permissão para uso pessoal e não comercial.
  Sob esta licença, você NÃO pode:
    1) Modificar ou copiar os materiais;
    2) Usar para finalidade comercial não autorizada;
    3) Fazer engenharia reversa do software;
    4) Remover direitos autorais;
    5) Transferir os materiais para terceiros.{RESET}

  {BRANCO}3. Isenção de responsabilidade{RESET}
  {DIM}Os materiais são fornecidos 'como estão'. O FLUXO não
  oferece garantias expressas ou implícitas.

  O FLUXO pode revisar estes termos a qualquer momento.

  © 2026 FLUXO - Alguns direitos reservados.{RESET}
""")
    pausar()


# ── Gerenciamento de marketplaces (cadastrar, remover, restaurar) ──

def exibir_lista_marketplaces(numerada=False):
    """Mostra os marketplaces atuais, cada um com a sua cor de fundo.

    Args:
        numerada (bool): Se True, mostra [1], [2]... para o usuário escolher um.
    """
    for i, (nome, dados) in enumerate(MARKETPLACES.items(), 1):
        numero = f"{CIANO}[{i}]{RESET} " if numerada else "    "
        origem = "padrão" if nome in MARKETPLACES_PADRAO else "cadastrado"
        if (nome in MARKETPLACES_PADRAO
                and abs(dados["taxa_fixa"] - MARKETPLACES_PADRAO[nome]["taxa_fixa"]) > 1e-9):
            origem += f", taxa original {formatar_percentual(MARKETPLACES_PADRAO[nome]['taxa_fixa'])}"
        print(f"  {numero}{dados['cor_fundo']}{dados['cor_texto']} {dados['icone']} {nome:<16} {RESET} "
              f"{DIM}taxa fixa: {formatar_percentual(dados['taxa_fixa'])} • {origem}{RESET}")


def tela_cadastrar_marketplace():
    """Pede nome e taxa fixa e cadastra um novo marketplace.

    ENTER em branco, em qualquer pergunta, cancela e volta ao menu.
    """
    limpar_tela()
    exibir_logo()
    cabecalho("CADASTRAR MARKETPLACE")

    subcabecalho("Marketplaces atuais")
    print()
    exibir_lista_marketplaces()

    subcabecalho("Novo marketplace")
    print(f"\n  {DIM}ENTER em branco cancela. A taxa fixa é o que a plataforma cobra")
    print(f"  sobre o valor da venda (ex.: 12,5).{RESET}\n")

    while True:
        nome = input_estilizado(f"Nome (até {TAMANHO_MAX_NOME_MKT} caracteres)").strip()
        if not nome:
            return
        erro = validar_nome_marketplace(nome)
        if erro is None:
            break
        exibir_erro(erro)

    while True:
        texto = input_estilizado("Taxa fixa da plataforma (%)")
        if not texto.strip():
            return
        try:
            taxa = converter_numero(texto) / 100  # % → decimal
        except ValueError:
            exibir_erro("Digite apenas números (exemplo: 12,5).")
            continue
        erro = validar_taxa_marketplace(taxa)
        if erro is None:
            break
        exibir_erro(erro)

    print()
    if not confirmar(f"Cadastrar '{nome}' com taxa fixa de {formatar_percentual(taxa)}?"):
        exibir_mensagem("Cadastro cancelado.")
        pausar()
        return

    sucesso, mensagem = adicionar_marketplace(nome, taxa)
    if sucesso:
        exibir_sucesso(mensagem)
    else:
        exibir_erro(mensagem)
    pausar()


def tela_remover_marketplace():
    """Mostra os marketplaces numerados e remove o escolhido (com confirmação)."""
    limpar_tela()
    exibir_logo()
    cabecalho("REMOVER MARKETPLACE")

    nomes = list(MARKETPLACES.keys())
    if len(nomes) <= 1:
        exibir_mensagem("É preciso manter pelo menos um marketplace.")
        pausar()
        return

    subcabecalho("Escolha qual remover")
    print()
    exibir_lista_marketplaces(numerada=True)

    while True:
        escolha = input(f"\n  {BRANCO}Número do marketplace (ENTER volta): {RESET}").strip()
        if not escolha:
            return
        if escolha.isdecimal() and 1 <= int(escolha) <= len(nomes):
            break
        exibir_erro("Número fora da lista. Digite um dos números mostrados.")

    nome = nomes[int(escolha) - 1]
    print(f"\n  {DIM}Os produtos já salvos continuam guardando o preço antigo deste")
    print(f"  marketplace até serem editados. Os novos cálculos não o incluem.{RESET}\n")
    if not confirmar(f"Remover '{nome}'?"):
        exibir_mensagem("Remoção cancelada.")
        pausar()
        return

    sucesso, mensagem = remover_marketplace(nome)
    if sucesso:
        exibir_sucesso(mensagem)
    else:
        exibir_erro(mensagem)
    pausar()


def tela_restaurar_marketplaces():
    """Pede confirmação e traz de volta os marketplaces padrão removidos."""
    print()
    faltando = [nome for nome in MARKETPLACES_PADRAO if nome not in MARKETPLACES]
    if faltando and not confirmar(f"Restaurar {', '.join(faltando)}?"):
        exibir_mensagem("Restauração cancelada.")
        pausar()
        return

    sucesso, mensagem = restaurar_marketplaces_padrao()
    if sucesso:
        exibir_sucesso(mensagem)
    else:
        exibir_mensagem(mensagem)
    pausar()


def tela_marketplaces():
    """Menu de gerenciamento: cadastrar, remover e restaurar marketplaces."""
    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("GERENCIAR MARKETPLACES")

        subcabecalho("Marketplaces atuais")
        print()
        exibir_lista_marketplaces()
        print()
        avisar_desatualizados()
        print(f"  {CIANO}[1]{RESET} ➕  Cadastrar novo marketplace")
        print(f"  {CIANO}[2]{RESET} ➖  Remover marketplace")
        print(f"  {CIANO}[3]{RESET} ♻   Restaurar marketplaces padrão")
        print(f"  {CIANO}[4]{RESET} ✏   Editar taxa de um marketplace")
        print(f"  {CIANO}[5]{RESET} 🔄  Recalcular preços dos produtos salvos")
        print(f"  {CIANO}[0]{RESET} ↩   Voltar ao menu principal")
        print()
        linha()
        print()

        opcao = input(f"  {BRANCO}Escolha uma opção: {RESET}").strip()

        if opcao == "1":
            tela_cadastrar_marketplace()
        elif opcao == "2":
            tela_remover_marketplace()
        elif opcao == "3":
            tela_restaurar_marketplaces()
        elif opcao == "4":
            tela_editar_marketplace()
        elif opcao == "5":
            tela_recalcular_produtos()
        elif opcao == "0":
            return
        else:
            exibir_erro("Opção inválida! Tente novamente.")
            pausar()


# ── Recálculo de preços salvos, edição de marketplace e relatório ──

def avisar_desatualizados():
    """Mostra um aviso se existirem produtos com preços salvos desatualizados."""
    quantidade = contar_desatualizados()
    if quantidade:
        exibir_mensagem(f"{quantidade} produto(s) salvo(s) com preços desatualizados. "
                        f"Use a opção \"Recalcular preços\".")


def executar_recalculo():
    """Recalcula os produtos desatualizados e mostra o resultado na tela."""
    sucesso, quantidade = recalcular_produtos()
    if not sucesso:
        exibir_erro("Não foi possível gravar os produtos. Verifique se a pasta "
                    "do programa permite escrita.")
    elif quantidade == 0:
        exibir_mensagem("Nenhum produto precisava de recálculo.")
    else:
        exibir_sucesso(f"{quantidade} produto(s) recalculado(s) com as taxas atuais!")


def tela_recalcular_produtos():
    """Mostra quais produtos estão desatualizados e recalcula (com confirmação)."""
    limpar_tela()
    exibir_logo()
    cabecalho("RECALCULAR PREÇOS SALVOS")
    print()

    produtos = carregar_produtos()
    if not produtos:
        exibir_mensagem("Nenhum produto salvo ainda.")
        pausar()
        return

    desatualizados = [(indice, produto) for indice, produto in enumerate(produtos)
                      if produto_desatualizado(produto)]
    if not desatualizados:
        exibir_sucesso("Todos os preços salvos já estão atualizados com as taxas atuais.")
        pausar()
        return

    print(f"  {DIM}Estes produtos têm preços calculados com taxas antigas ou foram")
    print(f"  salvos antes do preço indicado existir:{RESET}\n")
    exibir_tabela_produtos(desatualizados)
    print(f"\n  {DIM}Custo, taxa e margem de cada produto não mudam: só os preços são refeitos.{RESET}\n")

    if not confirmar(f"Recalcular {len(desatualizados)} produto(s) agora?"):
        exibir_mensagem("Recálculo cancelado.")
        pausar()
        return

    executar_recalculo()
    pausar()


def tela_editar_marketplace():
    """Escolhe um marketplace e altera a taxa fixa dele.

    ENTER em branco, em qualquer pergunta, cancela e volta ao menu.
    Depois de alterar, oferece recalcular os produtos já salvos.
    """
    limpar_tela()
    exibir_logo()
    cabecalho("EDITAR TAXA DE MARKETPLACE")

    nomes = list(MARKETPLACES.keys())
    subcabecalho("Escolha qual editar")
    print()
    exibir_lista_marketplaces(numerada=True)

    while True:
        escolha = input(f"\n  {BRANCO}Número do marketplace (ENTER volta): {RESET}").strip()
        if not escolha:
            return
        if escolha.isdecimal() and 1 <= int(escolha) <= len(nomes):
            break
        exibir_erro("Número fora da lista. Digite um dos números mostrados.")

    nome = nomes[int(escolha) - 1]
    atual = MARKETPLACES[nome]["taxa_fixa"]

    subcabecalho(f"Nova taxa de {nome}")
    print(f"\n  {DIM}Taxa atual: {formatar_percentual(atual)}", end="")
    if nome in MARKETPLACES_PADRAO:
        print(f"  •  taxa original do programa: "
              f"{formatar_percentual(MARKETPLACES_PADRAO[nome]['taxa_fixa'])}", end="")
    print(f"{RESET}\n")

    while True:
        texto = input_estilizado(f"Nova taxa fixa (%) — atual {formatar_percentual(atual)}")
        if not texto.strip():
            return
        try:
            nova = converter_numero(texto) / 100  # % → decimal
        except ValueError:
            exibir_erro("Digite apenas números (exemplo: 12,5).")
            continue
        erro = validar_taxa_marketplace(nova)
        if erro is None:
            break
        exibir_erro(erro)

    if abs(nova - atual) < 1e-9:
        exibir_mensagem("A nova taxa é igual à atual. Nada foi alterado.")
        pausar()
        return

    # Prévia do efeito: um produto de exemplo (custo R$ 100, margem 20%, sem taxa sua)
    antes = calcular_preco(100, 0, 0.20, atual)
    depois = calcular_preco(100, 0, 0.20, nova)
    texto_antes = formatar_moeda(antes["preco"]) if antes else "inviável"
    texto_depois = formatar_moeda(depois["preco"]) if depois else "inviável"
    print(f"\n  {DIM}Exemplo (custo R$ 100,00 e margem 20%): preço ideal "
          f"{texto_antes} → {texto_depois}{RESET}\n")

    if not confirmar(f"Alterar a taxa de '{nome}' para {formatar_percentual(nova)}?"):
        exibir_mensagem("Alteração cancelada.")
        pausar()
        return

    sucesso, mensagem = editar_taxa_marketplace(nome, nova)
    if not sucesso:
        exibir_erro(mensagem)
        pausar()
        return

    exibir_sucesso(mensagem)

    # A taxa mudou, então os preços já salvos ficaram velhos: oferece refazer.
    quantidade = contar_desatualizados()
    if quantidade:
        print()
        exibir_mensagem(f"{quantidade} produto(s) salvo(s) estão com preços calculados "
                        f"com a taxa antiga.")
        if confirmar("Recalcular agora?"):
            executar_recalculo()
    pausar()


def exibir_resumo_relatorio(relatorio):
    """Mostra na tela o resumo e a tabela do relatório."""
    resumo = relatorio["resumo"]

    subcabecalho("Resumo")
    print()
    print(f"  {BOLD}{BRANCO}Produtos:{RESET} {resumo['total']}  │  "
          f"{BOLD}{BRANCO}Custo total:{RESET} {formatar_moeda(resumo['custo_total'])}")
    lucro_medio = formatar_moeda(resumo["lucro_medio"]) if resumo["lucro_medio"] is not None else "—"
    print(f"  {BOLD}{BRANCO}Margem média:{RESET} {formatar_percentual(resumo['margem_media'])}  │  "
          f"{BOLD}{BRANCO}Lucro médio por unidade:{RESET} {lucro_medio}")

    if resumo["contagem_competitivo"]:
        mais_comum = max(resumo["contagem_competitivo"], key=resumo["contagem_competitivo"].get)
        quantos = resumo["contagem_competitivo"][mais_comum]
        print(f"  {BOLD}{BRANCO}Mais competitivo:{RESET} {mais_comum} "
              f"{DIM}(menor preço em {quantos} de {resumo['total']} produtos){RESET}")
    if resumo["maior_retorno"]:
        melhor = resumo["maior_retorno"]
        print(f"  {BOLD}{BRANCO}Maior retorno:{RESET} {melhor['produto']['nome']} "
              f"{DIM}({formatar_percentual(melhor['retorno'])} sobre o custo){RESET}")

    if resumo["desatualizados"]:
        print()
        exibir_mensagem(f"{resumo['desatualizados']} produto(s) com preços salvos desatualizados "
                        f"(marcados com !). O relatório já usa as taxas atuais.")

    subcabecalho("Todos os produtos (no marketplace de menor preço)")
    print()
    print(f"  {DIM}{'Nº':<6}{'Produto':<19}{'Marketplace':<15}{'Indicado':>12}{'Retorno':>8}{RESET}")
    print(f"  {AZUL}{'─' * (LARGURA - 6)}{RESET}")
    for linha in relatorio["linhas"]:
        marca = "!" if linha["desatualizado"] else " "
        numero = f"#{linha['numero']}{marca}"
        if linha["competitivo"] is None:
            print(f"  {CIANO}{numero:<6}{RESET}{cortar(linha['produto']['nome'], 18):<19}"
                  f"{VERMELHO}cálculo inviável com a taxa e a margem atuais{RESET}")
            continue
        indicado = linha["resultados"][linha["competitivo"]]["indicado"]["preco"]
        print(f"  {CIANO}{numero:<6}{RESET}{BRANCO}{cortar(linha['produto']['nome'], 18):<19}{RESET}"
              f"{cortar(linha['competitivo'], 14):<15}"
              f"{VERDE}{formatar_moeda(indicado):>12}{RESET}"
              f"{formatar_percentual(linha['retorno']):>8}")

    ranking = sorted([l for l in relatorio["linhas"] if l["retorno"] is not None],
                     key=_chave_retorno, reverse=True)
    if len(ranking) > 1:
        subcabecalho("Ranking por retorno (lucro ÷ custo)")
        print()
        for posicao, linha in enumerate(ranking[:3], 1):
            print(f"  {AMARELO}{posicao}º{RESET} {cortar(linha['produto']['nome'], 22):<22} "
                  f"{VERDE}{formatar_percentual(linha['retorno'])}{RESET}  "
                  f"{DIM}({formatar_moeda(linha['lucro_competitivo'])} de lucro por unidade){RESET}")
    print()


def tela_relatorio():
    """Relatório com todos os produtos salvos, com opção de exportar.

    Mostra um resumo na tela e permite gerar um CSV (Excel) e uma
    página HTML (navegador / PDF) na pasta "relatorios".
    """
    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("RELATÓRIO DE PRODUTOS")
        print()

        relatorio = montar_relatorio()
        if relatorio["resumo"]["total"] == 0:
            exibir_mensagem("Nenhum produto salvo ainda. "
                            "Precifique e salve um produto primeiro.")
            pausar()
            return

        exibir_resumo_relatorio(relatorio)
        linha()
        print()
        print(f"  {CIANO}[1]{RESET} 💾  Exportar relatório (CSV para Excel + página HTML)")
        print(f"  {CIANO}[2]{RESET} 🔄  Recalcular preços salvos")
        print(f"  {CIANO}[0]{RESET} ↩   Voltar ao menu principal")
        print()

        opcao = input(f"  {BRANCO}Escolha uma opção: {RESET}").strip()

        if opcao == "1":
            try:
                caminho_csv, caminho_html = exportar_relatorio(relatorio)
            except OSError:
                exibir_erro("Não foi possível salvar o relatório. Verifique se a pasta "
                            "do programa permite escrita.")
                pausar()
                continue
            exibir_sucesso("Relatório exportado na pasta \"relatorios\":")
            print(f"    {DIM}• {os.path.basename(caminho_csv)}   (abra no Excel){RESET}")
            print(f"    {DIM}• {os.path.basename(caminho_html)}  (abra no navegador){RESET}\n")
            if confirmar("Abrir a página HTML agora?"):
                if not abrir_arquivo(caminho_html):
                    exibir_mensagem("Não foi possível abrir automaticamente. "
                                    "Abra o arquivo pela pasta \"relatorios\".")
            pausar()
        elif opcao == "2":
            tela_recalcular_produtos()
        elif opcao == "0":
            return
        else:
            exibir_erro("Opção inválida! Tente novamente.")
            pausar()


def menu_principal():
    """Menu principal do programa. É o ponto de entrada.

    O usuário navega entre as opções digitando o número correspondente.
    O loop continua até o usuário escolher "Sair".
    """
    while True:
        limpar_tela()
        exibir_logo()
        cabecalho("MENU PRINCIPAL")
        print()
        avisar_desatualizados()
        print(f"  {CIANO}[1]{RESET} 📊  Precificar produto")
        print(f"  {CIANO}[2]{RESET} 📁  Produtos salvos")
        print(f"  {CIANO}[3]{RESET} 🔎  Buscar / editar produtos")
        print(f"  {CIANO}[4]{RESET} 🏪  Gerenciar marketplaces")
        print(f"  {CIANO}[5]{RESET} 💬  Enviar feedback")
        print(f"  {CIANO}[6]{RESET} 🔒  Política de Privacidade")
        print(f"  {CIANO}[7]{RESET} 📜  Termos de Uso")
        print(f"  {CIANO}[8]{RESET} 📈  Relatório de produtos")
        print(f"  {CIANO}[0]{RESET} 🚪  Sair")
        print()
        linha()
        print()

        opcao = input(f"  {BRANCO}Escolha uma opção: {RESET}").strip()

        if opcao == "1":
            tela_precificar()
        elif opcao == "2":
            tela_produtos_salvos()
        elif opcao == "3":
            tela_gerenciar_produtos()
        elif opcao == "4":
            tela_marketplaces()
        elif opcao == "5":
            tela_feedback()
        elif opcao == "6":
            tela_politica_privacidade()
        elif opcao == "7":
            tela_termos_de_uso()
        elif opcao == "8":
            tela_relatorio()
        elif opcao == "0":
            limpar_tela()
            print(f"""
{VERDE}{BOLD}
    ╔══════════════════════════════════════════╗
    ║     Obrigado por usar o FLUXO! 👋       ║
    ║       © 2026 FLUXO                       ║
    ╚══════════════════════════════════════════╝
{RESET}""")
            break
        else:
            exibir_erro("Opção inválida! Tente novamente.")
            pausar()


# ── Ponto de entrada do programa ──
# Quando o arquivo é executado diretamente (não importado como módulo),
# Inicia o menu principal.
if __name__ == "__main__":
    carregar_marketplaces()  # aplica marketplaces cadastrados/removidos em sessões anteriores
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C ou Ctrl+D: sai sem mostrar erro técnico
        print(f"\n\n  {DIM}Programa encerrado.{RESET}\n")
