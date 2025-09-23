import logging

class AccountManager:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_id, initial_balance=0):
        if account_id in self.accounts:
            raise ValueError(f"Account {account_id} already exists")
        self.accounts[account_id] = initial_balance
        return True

    def get_balance(self, account_id):
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        return self.accounts[account_id]

    def deduct(self, account_id, amount):
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        balance = self.accounts[account_id]
        if balance < amount:
            raise ValueError(f"Insufficient funds in account {account_id}")
        self.accounts[account_id] = balance - amount
        return True

    def credit(self, account_id, amount):
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        self.accounts[account_id] += amount
        return True

    def rollback_deduct(self, account_id, amount):
        if account_id in self.accounts:
            self.accounts[account_id] += amount

class TransactionLogger:
    def __init__(self):
        self.logger = logging.getLogger('BankingLogger')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def log_success(self, message):
        self.logger.info(f"SUCCESS: {message}")

    def log_failure(self, message):
        self.logger.error(f"FAILURE: {message}")

class NotificationService:
    def __init__(self):
        self.threshold = 1000

    def send_sms(self, account_id, message):
        print(f"SMS to {account_id}: {message}")

    def notify_if_needed(self, account_id, amount, action):
        if amount > self.threshold:
            self.send_sms(account_id, f"{action} of ${amount} processed")

class BankingInterface:
    def __init__(self):
        self.account_manager = AccountManager()
        self.logger = TransactionLogger()
        self.notifier = NotificationService()

    def create_account(self, account_id, initial_balance=0):
        try:
            success = self.account_manager.create_account(account_id, initial_balance)
            if success:
                self.logger.log_success(f"Account {account_id} created with balance ${initial_balance}")
            return success
        except ValueError as e:
            self.logger.log_failure(str(e))
            return False

    def get_balance(self, account_id):
        try:
            balance = self.account_manager.get_balance(account_id)
            self.logger.log_success(f"Balance for {account_id}: ${balance}")
            return balance
        except ValueError as e:
            self.logger.log_failure(str(e))
            return None

    def transfer(self, from_account, to_account, amount):
        if amount <= 0:
            self.logger.log_failure("Transfer amount must be positive")
            return False

        deducted = False
        try:
            # Validate accounts
            self.account_manager.get_balance(from_account)
            self.account_manager.get_balance(to_account)

            # Check balance
            balance = self.account_manager.get_balance(from_account)
            if balance < amount:
                raise ValueError(f"Insufficient funds in {from_account}")

            # Deduct
            self.account_manager.deduct(from_account, amount)
            deducted = True

            # Credit
            self.account_manager.credit(to_account, amount)

            # Commit: Log and notify
            self.logger.log_success(f"Transfer ${amount} from {from_account} to {to_account}")
            self.notifier.notify_if_needed(from_account, amount, "Transfer out")
            self.notifier.notify_if_needed(to_account, amount, "Transfer in")

            return True

        except ValueError as e:
            self.logger.log_failure(f"Transfer failed: {str(e)}")
            if deducted:
                # Rollback
                self.account_manager.rollback_deduct(from_account, amount)
                self.logger.log_success(f"Rolled back deduction from {from_account}")
            return False

if __name__ == "__main__":
    interface = BankingInterface()

    # Create accounts
    interface.create_account("A001", 2000)
    interface.create_account("A002", 500)

    # Successful transfer
    interface.transfer("A001", "A002", 300)

    # Check balances
    interface.get_balance("A001")
    interface.get_balance("A002")

    # Insufficient funds
    interface.transfer("A002", "A001", 600)

    # Invalid account
    interface.transfer("A001", "A999", 100)
    interface.get_balance("A999")