import Pyro4
import json
import requests
import binascii
import hashlib

from messenger import register
from random import randint

@Pyro4.expose
class TransactionManager(object):
    _GAME = 'testnet'
    _ENDPOINT = "https://gameathon.mifiel.com/api/v1/games/{}/pool" \
                .format(_GAME)
    _TRANS_VERSION = 1

    def init(self):
        self._pool = {}
        # Fill pool with current transactions.
        pool_response = requests.get(self._ENDPOINT)
        raw_pool = json.loads(pool_response.content)
        print(raw_pool)
        for transaction in raw_pool:
            self.new_transaction(transaction)

    def _get_hash(transaction):
        return transaction['hash']

    def block_found(self, block):
        for transaction in block.transactions:
            self.remove_transaction(transaction)

    def new_transaction(self, transaction):
        transaction_hash = TransactionManager._get_hash(transaction)
        self._pool[transaction_hash] = transaction

    def remove_transaction(self, transaction):
        transaction_hash = TransactionManager._get_hash(transaction)
        del self._pool[transaction_hash]

    def _is_hex(s):
      try:
          if len(s) % 2 != 0: return False
          if int(s, 16): return True
      except ValueError:
          return False

    def _to_binary(value):
        print(value)
        return binascii.unhexlify(str(value))

    def _int_to_binary(i):
        return str(i).encode('ascii')

    def _reverse_double_sha256(value):
        d = hashlib.sha256(value)
        d2 = hashlib.sha256()
        d2.update(d.digest())
        return d2.hexdigest()[::-1]

    def _hash_transaction(transaction, lock_time=0):
        # Fixme: support more than one input/output.
        input_ = transaction['inputs'][0]
        input_payload = b''.join([
            TransactionManager._to_binary(input_['prev_hash']),
            TransactionManager._to_binary(input_['script_sig']),
            TransactionManager._int_to_binary(input_['vout'])
            ])

        output_ = transaction['outputs'][0]
        output_payload = b''.join([
            TransactionManager._int_to_binary(output_['value']),
            TransactionManager._int_to_binary(len(TransactionManager._to_binary(output_['script']))),
            TransactionManager._to_binary(output_['script'])
            ])

        transaction = b''.join([
            TransactionManager._int_to_binary(TransactionManager._TRANS_VERSION),
            TransactionManager._int_to_binary(len(transaction['inputs'])),
            input_payload,
            TransactionManager._int_to_binary(len(transaction['outputs'])),
            output_payload,
            TransactionManager._int_to_binary(lock_time)
            ])

        return TransactionManager._reverse_double_sha256(transaction)

    def _generate_coinbase():
        n = 'TeamZero_basura_'+str(randint(0,10000000000))
        input_ = { 'prev_hash': '0000000000000000000000000000000000000000000000000000000000000000',
                   'vout': -1,
                   'script_sig': binascii.hexlify(n.encode('ascii')).decode()}

        output_ = {'script': '257db1167953557378c179e7ceeaa572a1bad464',
                   'value': 5000000000 }

        inputs = [input_]
        outputs = [output_]
        confirmations = 0
        transaction = {'hash': None,
                       'inputs': inputs,
                       'outputs': outputs,
                       'size': 0,
                       'confirmations': confirmations}
        hash_ = TransactionManager._hash_transaction(transaction)
        transaction['hash'] = hash_
        return transaction


    def _select_transactions(self):
        coinbase = TransactionManager._generate_coinbase()
        transactions = [coinbase]
        # For now return all transactions plus coinbase
        # for transaction in self._pool.values():
        #     transactions.append(transaction)
        return transactions

    def _hash_pair(h1, h2):
        # TODO
        return '0'*64

    def _compute_merkle_hash(transaction_hashes):
        if len(transaction_hashes) == 1:
            return transaction_hashes[0]

        # Ensure we have even number of transactions
        if len(transaction_hashes) % 2 != 0:
            transaction_hashes.append(transaction_hashes[-1])

        new_hashes = []
        for i in range(0, len(transaction_hashes), 2):
            h1 = transaction_hashes[i]
            h2 = transaction_hashes[i + 1]
            new_hashes.append(TransactionManager._hash_pair(h1, h2))
            return TransactionManager._compute_merkle_hash(new_hashes)



    def build_block(self, prev_block):
        prev_block_hash = prev_block['hash']
        hash_ = '#'*64
        height = prev_block['height'] + 1
        message = binascii.hexlify(b'TeamZero Rules!').decode()
        transactions = self._select_transactions()
        transaction_hashes = [TransactionManager._get_hash(t) for t in transactions]
        merkle_hash = TransactionManager._compute_merkle_hash(transaction_hashes)
        reward = 50
        nonce = None
        user = 'TeamZero Miner!'
        target = None
        created_at = None
        return {'prev_block_hash': prev_block_hash,
                'hash': hash_,
                'height': height,
                'message': message,
                'merkle_hash': merkle_hash,
                'transactions': transactions,
                'reward': reward,
                'nonce': nonce,
                'user': user,
                'target': target,
                'created_at': created_at,
                'version_': '1'}

    def new_transaction(self, transaction):
        transaction_hash = TransactionManager._get_hash(transaction)
        self._pool[transaction_hash] = transaction

    def remove_transaction(self, transaction):
        transaction_hash = TransactionManager._get_hash(transaction)
        del self._pool[transaction_hash]


if __name__ == '__main__':
    transaction_manager = register(TransactionManager, 'transaction_manager')
    print("Transaction Manager: {}".format(transaction_manager))
    transaction_manager.requestLoop()
