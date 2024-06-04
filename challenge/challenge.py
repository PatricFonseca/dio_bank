import re


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


def only_digits(cpf):
    return re.sub(r'[^0-9]', '', cpf)


class Endereco:
    def __init__(self, logradouro, bairro, cidade, uf, cep):
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep

    def endereco_formatado(self):
        return f"{self.logradouro}, {self.bairro}, {self.cidade}/{self.uf}, {self.cep}"


class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco: Endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = only_digits(cpf)
        self.endereco = endereco

    def __str__(self):
        return f"Nome: {self.nome} \nData de nascimento: {self.data_nascimento}\nCPF: {self.cpf}\nEndereço: {self.endereco.endereco_formatado()}"


class Conta_Corrente:
    def __init__(self, cliente: Usuario):
        self.agencia = "0001"
        self.conta = len(contas) + 1
        self.cliente = cliente

    def __str__(self):
        return f"Agência: {self.agencia}\nConta: {self.conta}\nCliente: {self.cliente}\nSaldo: {self.saldo}\nExtrato: {self.extrato}"


def busca_conta_corrente(cpf, conta) -> Conta_Corrente:
    for conta in contas:
        if conta.cliente.cpf == cpf:
            return conta
    return None


usuarios: list[Usuario] = []
contas: list[Conta_Corrente] = []

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques) -> tuple:
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def deposito(saldo, valor, extrato, /) -> tuple:
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def get_extrato(saldo, *, extrato) -> str:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

    return extrato


def encontrar_usuario(cpf):
    return next((usuario for usuario in usuarios if usuario.cpf == cpf), None)


while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        saldo, extrato = deposito(saldo, valor, extrato)
    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite,
                               numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

    elif opcao == "e":

        get_extrato(saldo, extrato=extrato)

    elif opcao == "q":
        break

    elif opcao == "u":
        print("Cadastrando novo usuário...")

        nome = input("Nome: ")
        data_nascimento = input("Data de nascimento: ")
        cpf = input("CPF: ")
        logradouro = input("Logradouro: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        uf = input("UF: ")
        cep = input("CEP: ")

        if only_digits(cpf) in [user.cpf for user in usuarios]:
            print("CPF já existente, por favor tente novamente.")
            continue

        novo_endereco = Endereco(logradouro, bairro, cidade, uf, cep)
        novo_usuario = Usuario(nome, data_nascimento, cpf, novo_endereco)
        usuarios.append(novo_usuario)

    elif opcao == "ul":
        for user in usuarios:
            print(user)

    elif opcao == "c":
        print("Cadastrando nova conta...")
        input_cpf = input("CPF: ")
        usuario = encontrar_usuario(input_cpf)

        if not usuario:
            print("Usuário não encontrado, por favor tente novamente.")
            continue

        conta = Conta_Corrente(usuario)
        contas.append(conta)

        print("Conta criada com sucesso!")
    elif opcao == "cl":
        for conta in contas:
            print('------------------------------')
            print(conta)
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
