
# sys.path.append('/src')
from application.bank_controller import BankController
from domain.entities.bank import Bank

bank = Bank()
bankController = BankController(bank)

while True:
    print("Digite a opção desejada:")
    print("1. Depósito")
    print("2. Saque")
    print("3. Extrato")
    print("4. Sair")
    choice = input(">: ")

    if choice == "1":
        print("Depósito")
        amount = float(input("Digite o valor: "))
        bankController.deposit(amount)
    elif choice == "2":
        print("Saque".center(10))
        amount = float(input("Digite o valor: "))
        if bankController.validate_withdrawal(amount):
            bankController.withdraw(amount)
    elif choice == "3":
        print(bankController.get_statement())
    elif choice == "4":
        break
    else:
        print("Opção inválida. Tente novamente.")
