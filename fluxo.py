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
import json
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
AZUL    = "\033[94m"      # Azul claro
AMARELO = "\033[93m"      # Amarelo
VERMELHO= "\033[91m"      # Vermelho
BRANCO  = "\033[97m"      # Branco
CIANO   = "\033[96m"      # Ciano/Turquesa

# Cores de fundo (usadas nos cards de marketplace)
BG_PRETO     = "\033[40m"  # Fundo preto     (TikTok)
BG_AMARELO   = "\033[43m"  # Fundo amarelo   (Mercado Livre)
BG_AZULESC   = "\033[44m"  # Fundo azul esc. (Amazon)
BG_VERMELHO  = "\033[41m"  # Fundo vermelho  (Shopee)

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

    Exemplo: 49.90 → R$ 49.90
    """
    return f"R$ {valor:.2f}"

# Padroniza a exibição financeira. Transforma números puros no padrão real R$ (ex:2.00).

def pausar():
    """Pausa a execução e espera o usuário pressionar Enter para continuar."""
    input(f"\n{DIM}  Pressione ENTER para continuar...{RESET}")
# Dar tempo para o usuário ler os resultados na tela 
# antes que o programa limpe tudo e volte para o menu principal.


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

# no caso de o usuario querer ver os produtos salvos
def carregar_produtos():
    """Lê todos os produtos salvos no arquivo JSON.

    Retorna:
        lista (list): Lista de dicionários, cada um representando um produto.
                      Se o arquivo não existir, retorna uma lista vazia.
    """
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []  # Arquivo não existe ainda, retorna lista vazia


def salvar_produtos(lista):
    """Grava a lista de produtos no arquivo JSON.

    Args:
        lista (list): Lista de dicionários com os dados dos produtos.
    """
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        # indent=2 deixa o JSON formatado e legível
        # ensure_ascii=False permite acentos (é, ã, ç, etc.)
        json.dump(lista, arquivo, indent=2, ensure_ascii=False)


def adicionar_produto(produto):
    """Adiciona um novo produto à lista e salva no arquivo.

    Args:
        produto (dict): Dicionário com os dados do produto.
                        Exemplo: {"nome": "Fone", "fornecedor": "Ali", ...}
    """
    lista = carregar_produtos()
    lista.append(produto)
    salvar_produtos(lista)


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


# ╔══════════════════════════════════════════════════════════════╗
# ║            PARTE 3 - LÓGICA DE CÁLCULO                      ║
# ║  Funções que fazem a precificação dos produtos. Calcula o   ║
# ║  preço ideal de venda com base no custo, taxas fixas do     ║
# ║  marketplace, taxa do vendedor e margem de lucro desejada.  ║
# ╚══════════════════════════════════════════════════════════════╝

# Taxas fixas de cada marketplace (percentual sobre o valor da venda)
# Esses valores são os mesmos usados no site original
MARKETPLACES = {
    "TikTok":        {"taxa_fixa": 0.06, "cor_fundo": BG_PRETO,    "cor_texto": BRANCO,  "icone": "♪"},
    "Mercado Livre":  {"taxa_fixa": 0.17, "cor_fundo": BG_AMARELO,  "cor_texto": "\033[34m", "icone": "🤝"},
    "Amazon":         {"taxa_fixa": 0.13, "cor_fundo": BG_AZULESC,  "cor_texto": BRANCO,  "icone": "📦"},
    "Shopee":         {"taxa_fixa": 0.15, "cor_fundo": BG_VERMELHO, "cor_texto": BRANCO,  "icone": "🛒"},
}


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


def exibir_card_marketplace(nome_mkt, nome_produto, fornecedor, resultado):
    """Exibe um card colorido com o resultado de um marketplace.

    Cada marketplace tem sua cor característica, imitando os cards
    do site original (TikTok=preto, Mercado Livre=amarelo, etc.)

    Args:
        nome_mkt (str):       Nome do marketplace.
        nome_produto (str):   Nome do produto.
        fornecedor (str):     Nome do fornecedor.
        resultado (dict):     Dicionário com "preco" e "lucro".
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
    print(f"  {bg}{fg}{'─' * (LARGURA - 4)}{RESET}")
    print()


def selecionar_marketplaces():
    """Permite ao usuário escolher quais marketplaces quer ver.

    Retorna:
        selecionados (list): Lista com os nomes dos marketplaces escolhidos.
    """
    subcabecalho("Selecione os Marketplaces")
    print()

    nomes = list(MARKETPLACES.keys())
    for i, nome in enumerate(nomes, 1):
        dados = MARKETPLACES[nome]
        taxa_pct = dados["taxa_fixa"] * 100
        print(f"  {CIANO}[{i}]{RESET} {dados['icone']} {nome:<16} {DIM}(taxa fixa: {taxa_pct:.0f}%){RESET}")

    print(f"  {CIANO}[A]{RESET} 📊 Todos os marketplaces")
    print()

    escolha = input(f"  {BRANCO}Escolha (ex: 1,3 ou A para todos): {RESET}").strip().upper()

    if escolha == "A":
        return nomes  # Retorna todos

    selecionados = []
    for num in escolha.split(","):
        num = num.strip()
        if num.isdigit():
            idx = int(num) - 1
            if 0 <= idx < len(nomes):
                selecionados.append(nomes[idx])

    return selecionados


def tela_precificar():
    """Tela principal: preencher dados e calcular preço ideal.

    Fluxo:
    1. Usuário digita nome, fornecedor, custo, taxa e margem
    2. Seleciona os marketplaces
    3. O programa calcula e exibe os cards com resultados
    4. Opção de salvar o produto
    """
    limpar_tela()
    exibir_logo()
    cabecalho("PRECIFICAR PRODUTO")
    print()

    # ── Coleta de dados ──
    subcabecalho("Dados do Produto")
    print()
    nome       = input_estilizado("Nome do produto")
    fornecedor = input_estilizado("Fornecedor")
    print()

    subcabecalho("Dados Financeiros")
    print()
    custo_str  = input_estilizado("Custo de aquisição (R$)")
    taxa_str   = input_estilizado("Sua taxa adicional (%)")
    margem_str = input_estilizado("Margem de lucro desejada (%)")

    # ── Validação ──
    try:
        custo  = float(custo_str.replace(",", "."))
        taxa   = float(taxa_str.replace(",", ".")) / 100    # Converte % para decimal
        margem = float(margem_str.replace(",", ".")) / 100  # Converte % para decimal
    except ValueError:
        exibir_erro("Valores numéricos inválidos! Use apenas números.")
        pausar()
        return

    if not nome.strip() or not fornecedor.strip():
        exibir_erro("Nome do produto e fornecedor são obrigatórios!")
        pausar()
        return

    if custo <= 0:
        exibir_erro("O custo deve ser maior que zero!")
        pausar()
        return

    # ── Seleção de marketplaces ──
    marketplaces_escolhidos = selecionar_marketplaces()

    if not marketplaces_escolhidos:
        exibir_erro("Nenhum marketplace selecionado!")
        pausar()
        return

    # ── Cálculo ──
    todos_resultados = calcular_todos_marketplaces(custo, taxa, margem)

    # ── Exibição dos resultados ──
    limpar_tela()
    exibir_logo()
    cabecalho("RESULTADO DA PRECIFICAÇÃO")
    print()
    print(f"  {BOLD}{BRANCO}Produto:{RESET} {nome}  │  {BOLD}{BRANCO}Fornecedor:{RESET} {fornecedor}")
    print(f"  {BOLD}{BRANCO}Custo:{RESET}   {formatar_moeda(custo)}  │  {BOLD}{BRANCO}Taxa:{RESET} {taxa*100:.1f}%  │  {BOLD}{BRANCO}Margem:{RESET} {margem*100:.1f}%")
    print()
    linha()
    print()

    for mkt in marketplaces_escolhidos:
        exibir_card_marketplace(mkt, nome, fornecedor, todos_resultados[mkt])

    # ── Opção de salvar ──
    salvar = input(f"  {VERDE}Deseja salvar este produto? (S/N): {RESET}").strip().upper()
    if salvar == "S":
        produto = {
            "nome": nome,
            "fornecedor": fornecedor,
            "custo": custo,
            "taxa_usuario": taxa,
            "margem": margem,
            "resultados": {},
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
        # Salva os resultados de TODOS os marketplaces (não só os selecionados)
        for mkt_nome, resultado in todos_resultados.items():
            if resultado:
                produto["resultados"][mkt_nome] = resultado

        adicionar_produto(produto)
        exibir_sucesso(f"Produto '{nome}' salvo com sucesso!")

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

    # ── Exibe cada produto ──
    for i, prod in enumerate(produtos):
        print(f"  {AZUL}┌{'─' * (LARGURA - 6)}┐{RESET}")
        print(f"  {AZUL}│{RESET} {BOLD}{CIANO}#{i+1}{RESET}  {BOLD}{BRANCO}{prod['nome']}{RESET} │ {prod['fornecedor']}")
        print(f"  {AZUL}│{RESET}  {DIM}Custo: {formatar_moeda(prod['custo'])}  │  "
              f"Taxa: {prod['taxa_usuario']*100:.1f}%  │  "
              f"Margem: {prod['margem']*100:.1f}%{RESET}")

        # Mostra preço para cada marketplace salvo
        if "resultados" in prod:
            for mkt_nome, res in prod["resultados"].items():
                icone = MARKETPLACES.get(mkt_nome, {}).get("icone", "•")
                print(f"  {AZUL}│{RESET}  {icone} {mkt_nome:<16} → "
                      f"{VERDE}{formatar_moeda(res['preco'])}{RESET}  "
                      f"(lucro: {AMARELO}{formatar_moeda(res['lucro'])}{RESET})")

        print(f"  {AZUL}│{RESET}  {DIM}Salvo em: {prod.get('data', 'N/A')}{RESET}")
        print(f"  {AZUL}└{'─' * (LARGURA - 6)}┘{RESET}")
        print()

    # ── Opção de excluir ──
    linha()
    print(f"\n  {BRANCO}Digite o número do produto para excluir, ou 0 para voltar:{RESET}")
    escolha = input(f"  {CIANO}│ Opção: {RESET}").strip()

    if escolha.isdigit() and int(escolha) > 0:
        indice = int(escolha) - 1
        if excluir_produto(indice):
            exibir_sucesso("Produto excluído com sucesso!")
        else:
            exibir_erro("Número inválido.")

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
        print(f"  {CIANO}[1]{RESET} 📊  Precificar produto")
        print(f"  {CIANO}[2]{RESET} 📁  Produtos salvos")
        print(f"  {CIANO}[3]{RESET} 🔒  Política de Privacidade")
        print(f"  {CIANO}[4]{RESET} 📜  Termos de Uso")
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
            tela_politica_privacidade()
        elif opcao == "4":
            tela_termos_de_uso()
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
# ele inicia o menu principal.
if __name__ == "__main__":
    menu_principal()
