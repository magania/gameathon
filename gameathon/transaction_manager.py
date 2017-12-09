class TransactionManager(object):
    def __init__(self):
        self.pool = []
        pass

    def block_found(self, block):
        pass

    def build_block(self):
        pass
        block = None
        return block

    def new_transaction(self, transaction):
        pass

    def listen(self):
        pass


if __name__ == '__main__':
    print("Transaction Manager running ...")
    transaction_manager = TransactionManager()
    transaction_manager.listen()
