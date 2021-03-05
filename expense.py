class Expense:
    def __init__(self, id, amount, reason, timestamp):
        self.id = id
        self.amount = amount
        self.reason = reason
        self.timestamp = timestamp

    def to_string(self):
        return f"{self.id} {self.amount} € {self.reason} {self.timestamp}"