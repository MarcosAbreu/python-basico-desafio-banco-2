import datetime

# MENU
menu =["""
========================
MENU
------------------------
Escolha uma das operações abaixo:
------------------------
1) Acessar conta
2) Adicionar usuário
3) Adicionar conta
--- 4) Listar Clientes (Admin)
--- 5) Listar Contas (Admin)
0) Sair
------------------------""",
"""
========================
MENU
------------------------
Escolha uma das operações abaixo:
------------------------
1) Depositar
2) Sacar
3) Extrato
0) Voltar
------------------------"""]

# Pre-set para teste
lista_clientes: list = [{'nome': 'John Doe', 'data_nascimento': '01/01/1327', 'cpf': '00000000000', 'endereco': {'logradouro': 'Rua Qualquer', 'nro': '99', 'bairro': 'Algum lugar', 'cidade': 'Cidade Grande', 'estado': 'AM'}}, {'nome': 'Jane Doe', 'data_nascimento': '31/12/1327', 'cpf': '11111111111', 'endereco': {'logradouro': 'Rua Nova', 'nro': '98', 'bairro': 'Bairro Velho', 'cidade': 'Cidade Pequena', 'estado': 'RS'}}]
lista_contas: list = [{'agencia': '0001', 'numero_conta': 1, 'usuario': '00000000000', 'saldo': 0, 'extrato': []}, {'agencia': '0001', 'numero_conta': 2, 'usuario': '11111111111', 'saldo': 0, 'extrato': []}]

#Constantes de Regra de Negócio
AGENCIA = "0001"
LIMITE_SAQUE = 500
MAX_SAQUE = 3

#Funções Auxiliares

def inserir_valor():
    valor_inserido = input("Digite o valor: ")
    try:
        valor = float(valor_inserido)
        if valor >= 0:
            return valor
        else:
            print("------------------------")
            print("\nNão é permitido valor negativo, tente novamente.")
            return False
    except ValueError:
        print("------------------------")
        print("\nO Valor digitado não é um número.")
        return False

def formata_cpf(cpf:str):
    cpf_temp = cpf.replace('.','')
    cpf_temp = cpf_temp.replace('-','')
    return  cpf_temp

def verifica_cpf(*,lista_clientes,cpf):
    
    for cliente in lista_clientes:
        if cliente['cpf'] in cpf:
            return True
    return False

def truncar_endereco(endereco:str):
    logradouro = endereco[:endereco.find(",")]
    nro = endereco[endereco.find(",")+1:endereco.find("-")]
    temp = endereco[endereco.find("-")+1:]
    bairro = temp[:temp.find("-")]
    cidade = temp[temp.find("-")+1:temp.find("/")]
    estado = temp[temp.find("/")+1:]
    return logradouro,nro,bairro,cidade,estado

def novo_numero_conta(lista_contas:list):
    maior = 0
    for conta in lista_contas:
        if int(conta['numero_conta']) > maior:
            maior = int(conta['numero_conta'])
    return maior+1

def verifica_conta(numero_conta,*,lista_contas):
    for conta in lista_contas:
        if numero_conta is conta["numero_conta"]:
            return False
    return True

# Funções Criar Usuário e Conta

def criar_usuario(*,lista_clientes:list,nome,data_nascimento,cpf:str,endereco:str):
    if verifica_cpf(lista_clientes=lista_clientes,cpf=cpf) is False:
        endereco_truncado = truncar_endereco(endereco)
        cliente:dict = {
            'nome': nome,
            'data_nascimento':data_nascimento,
            'cpf': cpf,
            'endereco': {
                'logradouro': endereco_truncado[0],
                'nro': endereco_truncado[1],
                'bairro': endereco_truncado[2],
                'cidade': endereco_truncado[3],
                'estado': endereco_truncado[4]
            }
        }
        lista_clientes.append(cliente)
        
    else:
        print("Este CPF já esta cadastrado")

    return lista_clientes

def criar_conta(*,lista_contas:list,lista_clientes,agencia,numero_conta,usuario:str):
    print("------------------------")
    if verifica_cpf(lista_clientes=lista_clientes,cpf=usuario) is True:
        conta:dict = {
            'agencia': agencia,
            'numero_conta':numero_conta,
            'usuario': usuario,
            'saldo': 0,
            'extrato': []
        }
        
        if verifica_conta(numero_conta,lista_contas=lista_contas) is True:
            lista_contas.append(conta)
            print("\nConta criada com sucesso!")
        else:
            print("\nEsta conta já esta vinculada a outro usuario.")
    else:
        print("\nEste usuário não esta cadastrado")

    return lista_contas

def cadastrar_usuario(*,lista_clientes):
    print("------------------------")
    print("\nPara cadastrar Novo Usuário, preencha os campos com as informações do usuário.\n")
    usuario_nome = input("Nome: ")
    usuario_data_nascimento = input("Data de Nascimento: ")
    usuario_cpf = input("CPF: ")
    usuario_cpf = formata_cpf(usuario_cpf)
    print("Endereço:")
    usuario_endereco = input("-- Logradouro: ") + "," + input("-- Número: ") + "-" + input("-- Bairro: ") + "-" + input("-- Cidade: ") + "/" + input("-- Estado(Sigla): ")

    try:
        lista_clientes = criar_usuario(lista_clientes=lista_clientes,nome=usuario_nome,data_nascimento=usuario_data_nascimento,cpf=usuario_cpf,endereco=usuario_endereco)
    except ValueError:
        print("------------------------")
        print("\nNão foi possível criar este usuário. Tente novamente.")

    return lista_clientes

def cadastrar_conta(*,lista_contas,lista_clientes):
    print("------------------------")
    print("\nPara cadastrar Nova Conta, é necessário vincular um usuário já cadastrado.\n")
    usuario_cpf = input("Digite o CPF do usuário já cadastrado: ")
    usuario_cpf = formata_cpf(usuario_cpf)

    criar_conta(lista_contas=lista_contas,lista_clientes=lista_clientes,agencia=AGENCIA,numero_conta=novo_numero_conta(lista_contas),usuario=usuario_cpf)
    return lista_contas

# Funções de transação bancária

def depositar(lista_contas,numero_conta,valor,/):
    print("------------------------")
    for conta in lista_contas:
        if conta['numero_conta'] == int(numero_conta):
            conta['saldo'] += valor
            conta['extrato'].append(["Deposito", str(datetime.datetime.now()),valor])
            print("\nO valor foi depositado com sucesso!")
    return lista_contas
 
def sacar(*,lista_contas,numero_conta,valor,LIMITE_SAQUE,MAX_SAQUE):
    print("------------------------")
    temp_indice = 0
    if valor:
        hoje = str(datetime.date.today())
        saques_diarios = 0
        for indice,conta in enumerate(lista_contas):
            if conta['numero_conta'] == int(numero_conta):
                temp_indice = indice
                for extrato_item in conta['extrato']:
                    if hoje in extrato_item[1] and "Saque" in extrato_item[0]:
                        saques_diarios += 1

        if saques_diarios < int(MAX_SAQUE):
            if valor <= LIMITE_SAQUE:
                if valor <= lista_contas[temp_indice]['saldo']:
                    lista_contas[temp_indice]['saldo'] -= valor
                    print(f"\nO valor de {valor} foi sacado com sucesso!")
                    lista_contas[temp_indice]['extrato'].append(["Saque", str(datetime.datetime.now()),"-"+str(valor)])
                else:
                    print(f"\nSaldo insuficiente para o valor {valor}. Verifique saldo disponivel.")
            else:
                print(f"\nO valor solicitado esta acima do limite (R$ {LIMITE_SAQUE}) permitido por transação.")
        else:
            print(f"\nLimites de {MAX_SAQUE} saques diários atingido!")
        return lista_contas

def ver_extrato(numero_conta,/,*,lista_contas):
    saldo = 0
    print(f"""
========================
EXTRATO
------------------------
Detalhes:""")
    for conta in lista_contas:
        if conta['numero_conta'] == int(numero_conta):
            saldo = conta['saldo']
            for extrato in conta['extrato']:
                print(extrato)
    print("------------------------")
    print(f"Seu saldo atual é {saldo}")
    print("========================")

# Funções de Listar clientes e Listar contas

def listar_clientes(*,lista_clientes):
    print(f"""
========================
CLIENTES
------------------------""")
    for cliente in lista_clientes:
        print(f"Nome: {cliente['nome']}")
        print(f"Data Nascimento: {cliente['data_nascimento']}")
        print(f"CPF: {cliente['cpf']}")
        print(f"Endereço: {cliente['endereco']['logradouro']}, {cliente['endereco']['nro']} - {cliente['endereco']['bairro']} - {cliente['endereco']['cidade']}/{cliente['endereco']['estado']}")
        print("------------------------")
    print("========================")

def listar_contas(*,lista_contas):
    print(f"""
========================
CONTAS
------------------------""")
    for conta in lista_contas:
        print(f"Agencia: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print(f"Usuario: {conta['usuario']}")
        print(f"Saldo: {conta['saldo']}")
        print(f"Extrato: {conta['extrato']}")
        print("------------------------")
    print("========================")

# Main

while True:
    print(menu[0])
    operacao = input("Digite a operação desejada: ")
    if operacao == '1': # Acessar conta
        cpf_inserido = input("Digite o cpf cadastrado: ")
        cpf_inserido = formata_cpf(cpf_inserido)
        for conta in lista_contas:
            if conta['usuario'] == cpf_inserido:
                conta_inserida = input("Digite o número da conta: ")
                for conta in lista_contas:
                    temp_break = False
                    if conta['numero_conta'] == int(conta_inserida):
                        while True:
                            print(menu[1])
                            sub_operacao = input("Digite a operação desejada: ")
                            if sub_operacao == '1':
                                valor_inserido = inserir_valor()
                                if valor_inserido != False:
                                    lista_contas = depositar(lista_contas,conta_inserida,valor_inserido)
                            elif sub_operacao == '2':
                                valor_inserido = inserir_valor()
                                if valor_inserido != False:
                                    lista_contas = sacar(lista_contas=lista_contas,numero_conta=conta_inserida,valor=valor_inserido,LIMITE_SAQUE=LIMITE_SAQUE,MAX_SAQUE=MAX_SAQUE)
                            elif sub_operacao == '3':
                                ver_extrato(conta_inserida,lista_contas=lista_contas)
                            else:
                                temp_break = True
                                break
                    elif temp_break == True:
                        break;
        print("------------------------")
        print("\nUsuario não encontrado, tente novamente.")
    elif operacao == '2': # Adicionar Usuário
        lista_clientes = cadastrar_usuario(lista_clientes=lista_clientes)
    elif operacao == '3': # Adicionar Conta
        lista_contas = cadastrar_conta(lista_clientes=lista_clientes,lista_contas=lista_contas)
    elif operacao == '4': # Listar Clientes
        listar_clientes(lista_clientes=lista_clientes)
    elif operacao == '5': # Listar Contas
        listar_contas(lista_contas=lista_contas)
    else: # Sair
        break