from transaction_manager import TransactionManager

tm = TransactionManager()
hash_esperado = 'eb103aecd49c3c943614eecfa0ad53db265b38dac33892ef4a502e7d944eb43e'
transaction = {'inputs': [{'amount': 5035000448,
   'prev_hash': '0000000000000000000000000000000000000000000000000000000000000000',
   'script_sig': '47656e61726f3334333139',
   'vout': -1}],
 'outputs': [{'script': '1f4e24ae96324bb8c765fffb34708247036cff86',
   'value': 5035000448}],
 'size': 113}

hash_obtenido = TransactionManager._hash_transaction(transaction)

print(hash_esperado)
print(hash_obtenido)
print(hash_esperado == hash_obtenido)