class Bank:
    def __init__(self) -> None:
        self.LIMIT = 500
        self.WITHDRAWAL_LIMIT_NUMBER = 3

        self.balance = 0
        self.deposits = []
        self.withdrawals = []
        self.detailed_statement = "====== EXTRATO ======\n"
