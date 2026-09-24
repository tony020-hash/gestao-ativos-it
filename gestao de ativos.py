from enum import Enum
import json
import os

class TipoAtivo(Enum):
    SERVIDORES = 1
    COMPUTADORES = 2
    BANCO_DE_DADOS = 3
    ROTEADOR = 4

ativos = {}

# Pega o caminho exato da pasta do seu projeto
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
NOME_ARQUIVO = os.path.join(DIRETORIO_ATUAL, "ativos.json")

def salvar_dados():
    with open(NOME_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(ativos, arquivo, indent=4, ensure_ascii=False)

def carregar_dados():
    global ativos
    if os.path.exists(NOME_ARQUIVO):
        with open(NOME_ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados_carregados = json.load(arquivo)
            ativos = {int(k): v for k, v in dados_carregados.items()}

def ler_inteiro(mensagem):
    """
    Lê um número inteiro do usuário com tratamento de exceção.
    Evita que o programa feche caso o usuário digite letras ou caracteres inválidos.
    """
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("\n[ERRO] Entrada inválida! Por favor, digite apenas um número inteiro.")

def cadastrar_ativo():
    id_do_ativo = ler_inteiro("Digite o ID do ativo: ")
    nome_ativo = input("Digite o nome do ativo: ")
    responsavel = input("Digite o nome do responsável: ")
    localizacao = input("Digite a localização do ativo: ")

    opcao_tipo = ler_inteiro("Escolha o tipo (1-Servidor, 2-PC, 3-BD, 4-Roteador): ")
    tipo_escolhido = TipoAtivo(opcao_tipo).name

    ativos[id_do_ativo] = {
        "nome": nome_ativo,
        "responsavel": responsavel,
        "localizacao": localizacao,
        "tipo": tipo_escolhido,
        "vulnerabilidades": []
    }
    salvar_dados()
    print(f"\nAtivo '{nome_ativo}' cadastrado e salvo com sucesso!")

def listar_ativos():
    if not ativos:
        print("\nNenhum ativo cadastrado.")
        return
    
    print("\n--- MENU DE LISTAGEM / BUSCA ---")
    print("1 - Listar todos os ativos")
    print("2 - Busca especifica")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        for id_ativo, dados in ativos.items():
            print(f"\nID: {id_ativo} | Nome: {dados['nome']} | Tipo: {dados['tipo']} | Resp: {dados['responsavel']} | Local: {dados['localizacao']}")
    
    elif opcao == "2":
        print("\n--- BUSCA POR CRITÉRIO ---")
        print("1 - Buscar por ID")
        print("2 - Buscar por Nome")
        print("3 - Buscar por Responsável")
        print("4 - Buscar por Localização")
        
        criterio = input("Escolha uma opção: ")

        # 1. Busca por ID
        if criterio == "1":
            id_busca = ler_inteiro("Digite o ID do ativo: ")
            if id_busca in ativos:
                dados = ativos[id_busca]
                print(f"\nID: {id_busca} | Nome: {dados['nome']} | Tipo: {dados['tipo']} | Resp: {dados['responsavel']} | Local: {dados['localizacao']}")
            else:
                print("\nID não encontrado.")

        # 2. Busca por Nome
        elif criterio == "2":
            nome_busca = input("Digite o nome do ativo: ")
            encontrados = [dados for dados in ativos.values() if dados['nome'] == nome_busca]
            if encontrados:
                for dados in encontrados:
                    print(f"\nNome: {dados['nome']} | Tipo: {dados['tipo']} | Resp: {dados['responsavel']} | Local: {dados['localizacao']}")
            else:
                print("\nNenhum ativo encontrado com esse nome.")    
        
        # 3. Busca por Responsável
        elif criterio == "3":
            resp_busca = input("Digite o nome do responsável: ")
            encontrados = [dados for dados in ativos.values() if dados['responsavel'] == resp_busca]
            if encontrados:
                for dados in encontrados:
                    print(f"\nNome: {dados['nome']} | Tipo: {dados['tipo']} | Resp: {dados['responsavel']} | Local: {dados['localizacao']}")
            else:
                print("\nNenhum ativo encontrado com esse responsável.")
        
        # 4. Busca por Localização
        elif criterio == "4":
            local_busca = input("Digite a localização do ativo: ")
            encontrados = [dados for dados in ativos.values() if dados['localizacao'] == local_busca]
            if encontrados:
                for dados in encontrados:
                    print(f"\nNome: {dados['nome']} | Tipo: {dados['tipo']} | Resp: {dados['responsavel']} | Local: {dados['localizacao']}")
            else:
                print("\nNenhum ativo encontrado com essa localização.")

def atualizar_ativo():
    id_busca = ler_inteiro("Digite o ID do ativo que deseja atualizar: ")
    if id_busca in ativos:
        novo_resp = input("Digite o novo responsável: ")
        nova_local = input("Digite a nova localização: ")
        ativos[id_busca]["responsavel"] = novo_resp
        ativos[id_busca]["localizacao"] = nova_local
        salvar_dados()
        print("\nAtivo atualizado e salvo com sucesso!")
    else:
        print("\nID não encontrado.")

def excluir_ativo():
    id_busca = ler_inteiro("Digite o ID do ativo que deseja excluir: ")
    if id_busca in ativos:
        del ativos[id_busca]
        salvar_dados()
        print("\nAtivo removido com sucesso!")
    else:
        print("\nID não encontrado.")

# Início do programa
carregar_dados()

def gerenciar_vulnerabilidades():
    if not ativos:
        print("\nNenhum ativo cadastrado.")
        return

    id_busca = ler_inteiro("Digite o ID do ativo para gerenciar vulnerabilidades: ")

    if id_busca in ativos:
        print(f"\n--- VULNERABILIDADES DO ATIVO: {ativos[id_busca]['nome']} ---")
        print("1 - Adicionar Vulnerabilidade")
        print("2 - Listar Vulnerabilidades")
        print("3 - Remover Vulnerabilidade")
        
        opcao = input("Escolha uma opção: ")

        # 1. Adicionar Vulnerabilidade
        if opcao == "1":
            nova_vuln = input("Digite a descrição da vulnerabilidade: ")
            ativos[id_busca]["vulnerabilidades"].append(nova_vuln)
            salvar_dados()
            print("\nVulnerabilidade adicionada com sucesso!")

        # 2. Listar Vulnerabilidades
        elif opcao == "2":
            vulns = ativos[id_busca]["vulnerabilidades"]
            if vulns:
                print("\nLista de Vulnerabilidades:")
                for i, v in enumerate(vulns, start=1):
                    print(f"{i}. {v}")
            else:
                print("\nNenhuma vulnerabilidade registrada para este ativo.")

        # 3. Remover Vulnerabilidade
        elif opcao == "3":
            vulns = ativos[id_busca]["vulnerabilidades"]
            if not vulns:
                print("\nNão há vulnerabilidades para remover.")
            else:
                print("\nEscolha a vulnerabilidade para remover:")
                for i, v in enumerate(vulns, start=1):
                    print(f"{i}. {v}")
                
                idx = ler_inteiro("Digite o número da vulnerabilidade a remover: ") - 1
                if 0 <= idx < len(vulns):
                    removida = vulns.pop(idx)
                    salvar_dados()
                    print(f"\nVulnerabilidade '{removida}' removida com sucesso!")
                else:
                    print("\nNúmero inválido.")
    else:
        print("\nID não encontrado.")

while True:
    print("\n--- SISTEMA DE GESTÃO DE ATIVOS ---")
    print("1 - Cadastrar Ativo")
    print("2 - Listar Ativos")
    print("3 - Atualizar Ativo")
    print("4 - Excluir Ativo")
    print("5 - Gerenciar vulnerabilidades")
    print("6 - Sair do Sistema")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_ativo()
    elif opcao == "2":
        listar_ativos()
    elif opcao == "3":
        atualizar_ativo()
    elif opcao == "4":
        excluir_ativo()
    elif opcao == "5":
        gerenciar_vulnerabilidades()
    elif opcao == "6":
        salvar_dados()
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida!") 