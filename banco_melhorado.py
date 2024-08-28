import textwrap

def menu():
    return input(textwrap.dedent("""
    [d]\tDepositar
    [e]\tExtrato
    [s]\tSacar
    [q]\tSair
    [nc]\tNova conta
    [nu]\tNovo usuário
    [lc]\tListar contas
    => """))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}\n"
        print("""
        ============DEPÓSITO============
        Operação realizada com sucesso
        ================================""")
        print(saldo, valor, extrato)
        return saldo, extrato
    else:
        print("Operação falhou: O valor informado é inválido")

def sacar(*, saldo, valor, extrato, nsaques, lsaques, limite):
    ex_saldo = valor > saldo
    ex_limite = valor > limite
    ex_saques = nsaques >= lsaques
    if ex_saldo:
        print("Operação falhou: você não tem saldo o suficiente.")
    elif ex_limite:
        print("Operação falhou: o valor de saque excede o limite.")
    elif ex_saques:
        print("Operação falhou: número máximo de saques diários excedidos.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R${valor:.2f}\n"
        nsaques += 1
        print("""
        ==========SAQUE==========
        Operação realizada com sucesso
        =========================""")

    else:
        print("Operação falhou: valor inválido.")
    return saldo, extrato

def get_extrato(saldo, /, *, extrato):
    print("\n================EXTRATO================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=========================================")

def criar_user(l_users: list):
    cpf = input("Informe seu cpf: ")
    if check_user(cpf, l_users):
        print("CPF já em uso!")
        return

    nome = input("Insira nome completo: ")
    nasc = input("Insira data de nascimento (dd-mm-aaaa): ")
    endr = input("Insira endereço (logradouro, nro - bairro - cidade/Sigla do estado")

    l_users.append({'nome':nome, 'nasc':nasc, 'cpf':cpf, 'endr':endr})
    print('\n||||| Usuário criado com sucesso |||||\n')

def check_user(cpf, l_users):
    filtrado = [u for u in l_users if u['cpf'] == cpf]
    return filtrado[0] if filtrado else None

def criar_conta(agencia, n_conta, l_users):
    cpf = input("Informe o cpf do usuário: ")
    if(user := check_user(cpf, l_users)):
        print("\n||||| Conta criada com sucesso |||||")
        return {'agencia':agencia, 'n_conta':n_conta, 'user':user, 'c_cpf': cpf}
    print('\n||||| Usuário não encontrado, fluxo de criação de conta encerrado |||||\n')

def listar_contas(contas):
    if contas:
        for i in contas:
            print(textwrap.dedent(f"""
            ==========CONTAS==========
            Agência: {i['agencia']}
            Número: {i['n_conta']}
            Usuário: {i['user']['nome']}
            =========================="""))
    else:
        print('nenhuma conta encontrada')

def main():
    saldo = 0
    limite = 500
    extrato = ""
    n_saques = 0
    LIM_SAQUES = 3
    AGENCIA = '0001'
    n_conta = 1
    usuarios = []
    contas = []
    while True:
        opcao = menu()
        match opcao:
            case 'd':
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            case 's':
                valor = float(input("Informe o valor do saque: "))
                sacar(saldo=saldo,
                      valor=valor,
                      extrato=extrato,
                      nsaques=n_saques,
                      lsaques=LIM_SAQUES,
                      limite=limite)
            case 'e':
                get_extrato(saldo, extrato=extrato)
            case 'nc':
                n_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, n_conta, usuarios)
                if conta:
                    contas.append(conta)
            case 'nu':
                criar_user(usuarios)
            case 'lc':
                listar_contas(contas)
            case 'q':
                break
            case _:
                print(saldo, extrato)
                print("Operação inválida")
main()