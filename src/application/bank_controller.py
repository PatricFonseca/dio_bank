from domain.entities.bank import Bank


class BankController:
    def __init__(self, bank: Bank) -> None:
        self.bank = bank

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            print(">>> Valor inválido")
            return

        self.bank.balance += amount
        self.bank.deposits.append(amount)
        self.bank.detailed_statement += f"\nDepósito: R$ {amount:.2f}"

    def withdraw(self, amount: float) -> None:
        self.bank.balance -= amount
        self.bank.withdrawals.append(amount)
        self.bank.detailed_statement += f"\nSaque: R$ {amount:.2f}"

    def validate_withdrawal(self, amount: float) -> bool:
        if (amount > self.bank.balance):
            print(">>> Saldo insuficiente")
            return False
        elif (amount > self.bank.LIMIT):
            print(">>> O valor do saque excede o limite")
            return False
        elif (len(self.bank.withdrawals) >= self.bank.WITHDRAWAL_LIMIT_NUMBER):
            print(">>> Limite de saques excedido")
            return False
        else:
            return True

    # def statement_total(self) -> str:
    #     withdrawals_statement = "\n".join([f"Saques: R$ {a:.2f}" for a in self.bank.withdrawals])
    #     formatted_balance = "R${:.2f}".format(self.bank.balance)

    #     st_formatted = ""
    #     st_formatted += "======= EXTRATO ======\n"
    #     st_formatted += "\n".join(["Depósito: R$ {:.2f}".format(d) for d in self.bank.deposits])
    #     st_formatted += '\n'
    #     st_formatted += withdrawals_statement
    #     st_formatted += "\n\n"
    #     st_formatted += "------ SALDO ------\n"
    #     st_formatted += "Saldo atual: {:>10}\n".format(formatted_balance)

    #     return st_formatted

    def get_statement(self) -> str:
        return f"{self.bank.detailed_statement}\nSALDO: R$ {self.bank.balance:.2f}\n"
