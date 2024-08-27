ops = """
    [d] Depositar
    [e] Extrato
    [s] Sacar
    [q] Sair
    
=>
"""

saldo = 0
limite = 500
extrato = ""
n_saques = 0
LIM_SAQUES = 3

while True:
    opcao = input(ops)
    match opcao:
        case 'd':
            valor = float(input("Informe o valor do depósito: "))
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R${valor:.2f}\n"
            else:
                print("Operação falhou: O valor informado é inválido")
        case 's':
            valor = float(input("Informe o valor do saque: "))
            ex_saldo = valor > saldo
            ex_limite = valor > limite
            ex_saques = n_saques >= LIM_SAQUES
            if ex_saldo:
                print("Operação falhou: você não tem saldo o suficiente.")
            elif ex_limite:
                print("Operação falhou: o valor de saque excede o limite.")
            elif ex_saques:
                print("Operação falhou: número máximo de saques diários excedidos.")
            elif valor > 0:
                saldo -= valor
                extrato += f"Saque: R${valor:.2f}\n"
                n_saques += 1
            else:
                print("Operação falhou: valor inválido.")
        case 'e':
            print("\n==========EXTRATO==========")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")
        case 'q':
            break
        case _:
            print("Operação inválida")