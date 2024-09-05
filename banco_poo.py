import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from stat import FILE_ATTRIBUTE_ARCHIVE


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def transacionar(self, conta, transacao):
        transacao.registrar(conta)

    def add_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nasc
        self.cpf = cpf


class Conta:
    def __init__(self, num, cliente):
        self._saldo = 0
        self._num = num
        self._agencia = '0001'
        self._cliente = cliente
        self._extrato = Extrato()

    @classmethod
    def nova_conta(cls, num, cliente):
        return cls(num, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def num(self):
        return self._num

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def extrato(self):
        return self._extrato

    def sacar(self, valor):
        saldo = self.saldo
        exced_saldo = valor > saldo

        if exced_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! Valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, num, cliente, lim=500, lim_saq=3):
        super().__init__(num, cliente)
        self._lim = lim
        self._lim_saq = lim_saq

    def sacar(self, valor):
        n_saq = len(
            [transacao for transacao in self.extrato.transacoes if transacao["tipo"] == Saque.__name__]
        )

        exc_lim = valor > self._lim
        exc_saq = n_saq >= self._lim_saq

        if exc_lim:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif exc_saq:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
                    Agência:\t{self.agencia}
                    C/C:\t\t{self.num}
                    Titular:\t{self.cliente.nome}
                """


class Extrato:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.extrato.add_transacao(self)


class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.extrato.add_transacao(self)


def menu():
    return input(textwrap.dedent("""\n
================ MENU ================
[d]\tDepositar
[e]\tExtrato
[s]\tSacar
[nc] Nova conta
[nu] Novo usuário
[lc] Listar contas
[q]\tSair
=> """))


def filtrar_cliente(cpf, clientes):
    filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return filtrados[0] if filtrados else None


def get_conta(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe seu CPF: ")
    filtrado = filtrar_cliente(cpf, clientes)

    if not filtrado:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Depositar(valor)

    conta = get_conta(filtrado)

    if not conta:
        return

    filtrado.transacionar(conta, transacao)


def sacar(clientes):
    cpf = input("Informe seu CPF: ")
    filtrado = filtrar_cliente(cpf, clientes)

    if not filtrado:
        print("Cliente não encontrado")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = get_conta(filtrado)
    if not conta:
        return

    filtrado.transacionar(conta, transacao)


def get_extrato(clientes):
    cpf = input("Informe o CPF: ")

    if not (filtrado := filtrar_cliente(cpf, clientes)):
        print("Cliente não encontrado")
        return

    if (conta := get_conta(filtrado)):
        return

    print("==========EXTRATO==========")
    transacoes = conta.extrato.transacoes

    ext = ""
    if not transacoes:
        ext = "Não foram realizadas transações"
    else:
        for t in transacoes:
            ext += f"{t["tipo"]}:\n\tR$ {t["valor"]:.2f}"

    print(ext)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("===========================")


def set_cliente(clientes):
    cpf = input("Insira o CPF:")
    filtrado = filtrar_cliente(cpf, clientes)

    if filtrado:
        print("Já existe um cliente")
        return

    nome = input("Insira nome completo: ")
    nasc = input("Insira data de nascimento (dd - mm - aaaa): ")
    endr = input("Informe seu endereço (Logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, nasc=nasc, endereco=endr, cpf=cpf)

    clientes.append(cliente)

    print("Cliente registrado com sucesso")


def set_conta(num, clis, contas):
    cpf = input("Insira o CPF:")
    filtrado = filtrar_cliente(cpf, clis)

    if not filtrado:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado")
        return

    conta = ContaCorrente.nova_conta(cliente=filtrado, num=num)
    contas.append(conta)
    filtrado.contas.append(conta)

    print("\nConta criada com sucesso!")


def list_contas(contas):
    for conta in contas:
        print("=" * 20)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        match opcao:
            case 'd':
                depositar(clientes)
            case 'e':
                get_extrato(clientes)
            case 's':
                sacar(clientes)
            case 'nc':
                n_conta = len(contas) + 1
                set_conta(n_conta, clientes, contas)
            case 'nu':
                set_cliente(clientes)
            case 'lc':
                list_contas(contas)
            case 'q':
                break
            case _:
                print("Operação inválida! Tente novamente")


main()