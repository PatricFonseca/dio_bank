from abc import ABC, abstractmethod
# from .models import Cliente, Conta, Conta_Corrente, Endereco, Historico, Usuario, only_digits
import functools
import re
import datetime


class Endereco:
    def __init__(self, logradouro, bairro, cidade, uf, cep):
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep

    def endereco_formatado(self):
        return f"{self.logradouro}, {self.bairro}, {self.cidade}/{self.uf}, {self.cep}"


def only_digits(cpf):
    return re.sub(r'[^0-9]', '', cpf)


def log(funcao):
    @functools.wraps(funcao)
    def wrapper(*args, **kwargs):
        funcao(*args, **kwargs)
        print("==============================")
        print(datetime.datetime.now())
        print(f"Transação: {funcao.__name__}")
        print("==============================")

    return wrapper


class Cliente:
    def __init__(self, endereco: Endereco):
        self.endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class Pessoa_Fisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco: Endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = only_digits(cpf)

    def __str__(self):
        return f"Nome: {self.nome} \nData de nascimento: {self.data_nascimento}\nCPF: {self.cpf}\nEndereço: {self.endereco.endereco_formatado()}"


class Conta:
    def __init__(self, saldo, numero, cliente: Cliente, historico):
        self._saldo = saldo
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = historico

    @property
    def saldo(self):
        return self._saldo

    @log
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(0, numero, cliente, Historico())

    @log
    def sacar(self, valor) -> bool:
        if valor > self._saldo:
            print("Saldo insuficiente!")
            return False
        else:
            self.historico.adicionar_transacao(Saque(valor))
            self._saldo -= valor
            return True

    @log
    def depositar(self, valor) -> bool:
        self._saldo += valor
        self.historico.adicionar_transacao(Deposito(valor))
        return True

    def __str__(self):
        return f"Agência: {self.agencia}\nCliente: {self.cliente}\nSaldo: {self.saldo}\nExtrato: {self.historico}"


class Conta_Corrente(Conta):
    def __init__(self, saldo, numero, cliente: Cliente, historico, limite=500, limite_saques=3):
        super().__init__(saldo, numero, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor) -> bool:
        if valor > self._limite:
            print("Saldo insuficiente!")
            return False
        elif (self._limite_saques <= 0):
            print("Limite de saques excedido")
            return False
        else:
            self._limite -= valor
            self._limite_saques -= 1
            return True


class Transacao(ABC):
    @property
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(Deposito(self._valor))


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(Saque(self._valor))


class Historico:
    def __init__(self):
        self._transacoes = []

    @log
    def adicionar_transacao(self, transacao):
        # extrato = f"{transacao.__class__.__name__}: R$ {transacao.valor:.2f}"
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao['tipo'].lower() == tipo_transacao.lower():
                yield transacao

    def __str__(self):
        return "\n".join([f"Transação {i+1}:\n" + "\n".join([f"  {key} - {value}" for key, value in transaction.items()]) for i, transaction in enumerate(self._transacoes)])


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova Conta
[lc] Lista contas
[nu] Novo usuário
[rel] Relatório
[q] Sair

=> """

clientes: list[Cliente] = [
    Pessoa_Fisica('João', '01/01/2000', '123',
                  Endereco('Rua 1', 'Bairro 1', 'Cidade 1', 'UF 1', 'CEP 1')),
]
contas: list[Conta] = []


def buscar_conta(cpf) -> Conta:
    for conta in contas:
        if conta.cliente.cpf == cpf:
            return conta
    return None


def depositar():
    usuario = encontrar_usuario(input("CPF: "))

    if not usuario:
        print("CPF inválido, por favor tente novamente.")
        return

    valor = float(input("Informe o valor do depósito: "))

    transacao = Deposito(valor)

    conta = buscar_conta(cpf=usuario.cpf)

    if not conta:
        print("Conta inválida, por favor tente novamente.")
        return

    transacao.registrar(conta)


def sacar():
    usuario = encontrar_usuario(input("CPF: "))

    if not usuario:
        print("CPF inválido, por favor tente novamente.")
        return

    valor = float(input("Informe o valor do saque: "))

    transacao = Saque(valor)

    conta = buscar_conta(cpf=usuario.cpf)

    if not conta:
        print("Conta inválida, por favor tente novamente.")
        return

    transacao.registrar(conta)


@log
def cadastrar_novo_usuario():
    print("Cadastrando novo usuário...")

    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento: ")
    cpf = input("CPF: ")
    logradouro = input("Logradouro: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    cep = input("CEP: ")

    novo_cliente = Pessoa_Fisica(nome, data_nascimento, cpf, Endereco(
        logradouro, bairro, cidade, uf, cep))

    if only_digits(cpf) in [cliente.cpf for cliente in clientes]:
        print("CPF já existente, por favor tente novamente.")
        return

    clientes.append(novo_cliente)


@log
def cadastrar_nova_conta():
    print("Cadastrando nova conta...")

    cpf = input("CPF: ")

    cliente = encontrar_usuario(cpf)

    if not cliente:
        print("CPF inválido, por favor tente novamente.")
        return

    saldo = float(input("Saldo inicial: "))
    numero = int(input("Número da conta: "))

    conta = Conta(saldo, numero, cliente, Historico())
    contas.append(conta)


def get_extrato() -> str:
    usuario = encontrar_usuario(input("CPF: "))

    if not usuario:
        print("CPF inválido, por favor tente novamente.")
        return

    conta = buscar_conta(cpf=usuario.cpf)

    if not conta:
        print("Conta inválida, por favor tente novamente.")
        return

    saldo = conta.saldo
    extrato = conta.historico._transacoes

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def encontrar_usuario(cpf):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


while True:

    opcao = input(menu)

    if opcao == "d":
        depositar()

    elif opcao == "s":
        sacar()

    elif opcao == "e":
        get_extrato()

    elif opcao == "q":
        break

    elif opcao == "nu":
        cadastrar_novo_usuario()

    elif opcao == "nc":
        cadastrar_nova_conta()

    elif opcao == "lc":
        for conta in contas:
            print('------------------------------')
            print(conta)

    elif opcao == "rel":
        usuario = encontrar_usuario(input("CPF: "))

        if not usuario:
            print("CPF inválido, por favor tente novamente.")
            continue

        conta = buscar_conta(cpf=usuario.cpf)

        if not conta:
            print("Conta inválida, por favor tente novamente.")
            continue

        for transacao in conta.historico.gerar_relatorio():
            print(
                f'''{transacao['data']}\n{transacao['tipo']}\n \tR$ {transacao['valor']:.2f}''')
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
