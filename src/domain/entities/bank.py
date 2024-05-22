class Bank:
    def __init__(self) -> None:
        self.LIMIT = 500
        self.WITHDRAWAL_LIMIT_NUMBER = 3

        self.balance = 0
        self.deposits = []
        self.withdrawals = []
        self.detailed_statement = "====== EXTRATO ======\n"

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            print(">>> Valor inválido")
            return
        
        self.balance += amount
        self.deposits.append(amount)
        self.detailed_statement += f"\nDepósito: R$ {amount:.2f}" 

    def withdraw(self, amount: float) -> None:
        self.balance -= amount
        self.withdrawals.append(amount)
        self.detailed_statement += f"\nSaque: R$ {amount:.2f}"

    def validate_withdrawal(self, amount: float) -> bool:
        if (amount > self.balance) :
            print(">>> Saldo insuficiente")
            return False
        elif (amount > self.LIMIT):
            print(">>> O valor do saque excede o limite")
            return False
        elif (self.WITHDRAWAL_LIMIT_NUMBER <= len(self.withdrawals)):
            print(">>> Limite de saques excedido")
            return False
        else:
            return True

    # def statement_total(self) -> str:
    #     withdrawals_statement = "\n".join([f"Saques: R$ {a:.2f}" for a in self.withdrawals])
    #     formatted_balance = "R${:.2f}".format(self.balance)

    #     st_formatted = ""
    #     st_formatted += "======= EXTRATO ======\n"
    #     st_formatted += "\n".join(["Depósito: R$ {:.2f}".format(d) for d in self.deposits])
    #     st_formatted += '\n'
    #     st_formatted += withdrawals_statement
    #     st_formatted += "\n\n"
    #     st_formatted += "------ SALDO ------\n"
    #     st_formatted += "Saldo atual: {:>10}\n".format(formatted_balance)

    #     return st_formatted

    def get_statement(self) -> str:
        return f"{self.detailed_statement}\nSALDO: R$ {self.balance:.2f}"